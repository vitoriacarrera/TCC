"""API da ferramenta RiscoPME (FastAPI, ADR-001 e ADR-005).

Sem estado: nada do que entra em /questionario e /simulacoes é gravado nem registrado em log (o log de acesso do
servidor não inclui o corpo das requisições). Só /contribuicoes grava, e apenas com consentimento explícito.

    uvicorn riskpme.api.app:app --reload          # desenvolvimento
    RISKPME_CORS="https://meu-front.app"          # origens permitidas, separadas por vírgula
    RISKPME_CONTRIBUICOES_DB=/data/contrib.sqlite # ativa a coleta anonimizada (sem a variável: desativada)
"""

from __future__ import annotations

import hashlib
import os
from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ..catalog import carregar_catalogo
from ..catalog.loader import diretorio_padrao
from ..catalog.models import Catalogo
from ..engine.maturidade import NOTA_MAXIMA
from ..engine.perfil import Perfil, resolver
from ..engine.plano import plano_de_acao
from ..engine.simulacao import simular
from . import contribuicoes
from .esquemas import Contribuicao, PedidoQuestionario, PedidoSimulacao

FORA_DO_ESCOPO = ("A ferramenta foi feita para micro, pequenas e médias empresas, com receita de até R$ 300 milhões "
                  "por ano. Para empresas maiores, a análise precisa de dados mais detalhados do que os pedidos aqui.")


@lru_cache(maxsize=1)
def catalogo() -> Catalogo:
    return carregar_catalogo()


@lru_cache(maxsize=1)
def versao_catalogo() -> str:
    """Impressão digital dos YAML de `audit/`: identifica com qual catálogo cada contribuição foi respondida."""
    h = hashlib.sha256()
    for arq in sorted(diretorio_padrao().glob("*.yaml")):
        h.update(arq.name.encode())
        h.update(arq.read_bytes())
    return h.hexdigest()[:12]


@asynccontextmanager
async def _ciclo(_: FastAPI):
    catalogo()          # carrega e valida o catálogo na subida: erro de YAML derruba o deploy, não o usuário
    versao_catalogo()
    yield


app = FastAPI(title="RiscoPME API", version="0.2.0", lifespan=_ciclo,
              description="Apoio à decisão em risco cibernético para PMEs (ISO/IEC 27005 + FAIR + Monte Carlo).")
_origens = [o.strip() for o in os.environ.get("RISKPME_CORS", "http://localhost:5173").split(",") if o.strip()]
app.add_middleware(CORSMiddleware, allow_origins=_origens, allow_methods=["GET", "POST"], allow_headers=["*"])


# ------------------------------------------------------------------ utilitários
def _erro(msg: str, status: int = 422) -> HTTPException:
    return HTTPException(status_code=status, detail=msg)


def _porte(cat: Catalogo, receita: float) -> int:
    try:
        return cat.classificar_porte(receita)
    except ValueError:
        raise _erro(FORA_DO_ESCOPO) from None


def _setor(cat: Catalogo, setor: str) -> None:
    if setor not in {s.id for s in cat.setores}:
        raise _erro(f"setor '{setor}' não existe; use um destes: {', '.join(s.id for s in cat.setores)}")


def _checar_respostas(cat: Catalogo, ids_validos: set[str], respostas: dict[str, int | None]) -> None:
    fora = sorted(set(respostas) - ids_validos)
    if fora:
        raise _erro(f"respostas para perguntas que não fazem parte do questionário deste perfil: {', '.join(fora)}")
    ruins = sorted(k for k, v in respostas.items() if v is not None and not 0 <= v <= NOTA_MAXIMA)
    if ruins:
        raise _erro(f"respostas fora da escala de 0 a 4: {', '.join(ruins)}")


def _contexto_pergunta(cat: Catalogo, pid: str) -> dict:
    return next(q for b in ("financeiro", "ativos", "calibracao_risco") for q in cat.contexto[b] if q["id"] == pid)


# ------------------------------------------------------------------ rotas
@app.get("/saude")
def saude() -> dict:
    return {"status": "ok", "versao_catalogo": versao_catalogo(),
            "coleta_anonimizada": contribuicoes.caminho_banco() is not None}


@app.get("/catalogo")
def ler_catalogo() -> dict:
    """Tudo o que a interface precisa para montar as telas: textos, escala, contexto, glossário e matriz."""
    cat = catalogo()
    return {
        "versao": versao_catalogo(),
        "instrucoes": cat.instrucoes.model_dump(),
        "aviso_legal": cat.aviso_legal,
        "escala": [o.model_dump() for o in cat.escala],
        "funcoes": {k: v.model_dump() for k, v in cat.funcoes.items()},
        "setores": [{"id": s.id, "nome": s.nome, "exemplos": s.exemplos} for s in cat.setores],
        "portes": [{"nivel": p.nivel, "nome": p.nome, "rob_min": p.rob_min, "rob_max": p.rob_max}
                   for p in sorted(cat.portes, key=lambda x: x.nivel)],
        "contexto": {b: cat.contexto[b] for b in ("financeiro", "ativos", "calibracao_risco")},
        "matriz": cat.contexto["matriz"],
        "cenarios": [{"id": c.id, "nome": c.nome, "descricao": c.descricao} for c in cat.cenarios],
        "glossario": {"termos": [t.model_dump() for t in cat.glossario.termos],
                      "conceitos": [c.model_dump() for c in cat.glossario.conceitos_resultado]},
    }


@app.post("/questionario")
def montar_questionario(pedido: PedidoQuestionario) -> dict:
    """Classifica o porte pela receita e devolve as perguntas do perfil (com as variantes de quem trabalha sozinho)."""
    cat = catalogo()
    _setor(cat, pedido.setor)
    porte = _porte(cat, pedido.receita_operacional_bruta)
    nome = cat.porte(porte).nome
    msg = _contexto_pergunta(cat, "receita_operacional_bruta")["mensagem_porte"].format(porte=nome)
    perguntas = cat.questionario(porte, pedido.setor, pedido.usuarios_ti)
    return {
        "porte": {"nivel": porte, "nome": nome},
        "mensagem_porte": msg,
        "tempo_estimado_min": cat.instrucoes.tempo_estimado_min.get(porte),
        "perguntas": [{"id": p.id, "funcao": p.funcao, "texto": p.texto, "ajuda": p.ajuda} for p in perguntas],
    }


@app.post("/simulacoes")
def simular_perfil(pedido: PedidoSimulacao) -> dict:
    """Monte Carlo, matriz 3 × 3 e plano de ação. Nada é gravado."""
    cat = catalogo()
    p = pedido.perfil
    _setor(cat, p.setor)
    porte = _porte(cat, p.receita_operacional_bruta)
    _checar_respostas(cat, {q.id for q in cat.questionario(porte, p.setor, p.usuarios_ti)}, pedido.respostas)
    perfil = Perfil(**p.model_dump())
    try:
        resolver(cat, perfil)
    except ValueError as e:
        raise _erro(str(e)) from None

    r = simular(cat, perfil, pedido.respostas, semente=pedido.semente)
    plano = plano_de_acao(cat, perfil, pedido.respostas, [c.id for c in r.cenarios if c.ruptura])
    celulas = {f"{i},{j}": [] for i in (1, 2, 3) for j in (1, 2, 3)}
    for c in r.cenarios:
        celulas[f"{c.nivel_impacto},{c.nivel_probabilidade}"].append(c.id)
    return {
        "porte": {"nivel": porte, "nome": cat.porte(porte).nome},
        "resultado": r.to_dict(),
        "matriz": {"celulas": celulas, "chave": "impacto,probabilidade"},
        "plano": plano.to_dict(),
        "versao_catalogo": versao_catalogo(),
    }


@app.post("/contribuicoes", status_code=201)
def contribuir(c: Contribuicao) -> dict:
    """Grava a contribuição anonimizada (ADR-005). Exige consentimento explícito."""
    if not c.consentimento:
        raise _erro("a contribuição só é gravada com a autorização marcada")
    caminho = contribuicoes.caminho_banco()
    if caminho is None:
        raise _erro("a coleta anonimizada não está ativa neste servidor", status=503)
    cat = catalogo()
    _setor(cat, c.setor)
    validas = {q.id for u in (None, 1) for q in cat.questionario(c.porte, c.setor, u)}
    _checar_respostas(cat, validas, c.respostas)
    contribuicoes.gravar(caminho, versao_catalogo(), c.setor, c.porte, c.respostas)
    return {"gravado": True}
