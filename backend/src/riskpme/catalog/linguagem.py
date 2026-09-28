"""Regras de linguagem acessível (RNF04) e detecção de termos do glossário.

A interface usa `termos_no_texto` para sublinhar palavras técnicas e mostrar a explicação ao toque.
O validador usa `verificar_linguagem` para impedir que siglas e jargões cheguem ao usuário sem explicação.
"""

from __future__ import annotations

import re
from functools import lru_cache

from .models import Catalogo, Glossario

LIMITE_TEXTO = 260      # caracteres — pergunta curta, legível no celular
LIMITE_AJUDA = 520


@lru_cache(maxsize=512)
def _regex(alias: str) -> re.Pattern[str]:
    # Siglas (ex.: "IA", "MFA", "LGPD") casam só em maiúsculas, para não confundir com palavras comuns.
    sigla = alias.isupper() or any(ch.isdigit() for ch in alias)
    flags = 0 if sigla else re.IGNORECASE
    return re.compile(rf"(?<!\w){re.escape(alias)}(?!\w)", flags)


def contem(texto: str, alias: str) -> bool:
    return bool(_regex(alias).search(texto))


def termos_no_texto(glossario: Glossario, texto: str) -> list[str]:
    """Ids dos termos do glossário mencionados no texto, na ordem do glossário."""
    return [t.id for t in glossario.termos if any(contem(texto, a) for a in t.aliases)]


def _textos_exibidos(cat: Catalogo):
    """(origem, campo, texto) de tudo o que o usuário lê durante o questionário."""
    for p in cat.perguntas:
        yield p.id, "texto", p.texto
        yield p.id, "ajuda", p.ajuda
    for bloco in ("financeiro", "ativos", "calibracao_risco"):
        for q in cat.contexto.get(bloco, []):
            yield q["id"], "texto", q["texto"]
            if q.get("ajuda"):
                yield q["id"], "ajuda", q["ajuda"]
            for op in q.get("opcoes", []):
                yield f"{q['id']}.{op['id']}", "rotulo", op["rotulo"]
    for c in cat.cenarios:
        yield c.id, "descricao", c.descricao
        yield c.id, "nome", c.nome


def verificar_linguagem(cat: Catalogo) -> tuple[list[str], list[str]]:
    erros: list[str] = []
    avisos: list[str] = []
    g = cat.glossario
    todos_aliases = [a for t in g.termos for a in t.aliases]

    # 1. Toda sigla "a evitar" precisa ter explicação no glossário (para quando aparecer nas recomendações).
    for termo in g.evitar_no_texto:
        if not any(contem(a, termo) or a == termo for a in todos_aliases):
            erros.append(f"glossário: '{termo}' está em evitar_no_texto mas não é explicado por nenhum termo")

    # 2. Nada da lista "a evitar" no que o usuário lê durante o questionário.
    for origem, campo, texto in _textos_exibidos(cat):
        for termo in g.evitar_no_texto:
            if contem(texto, termo):
                erros.append(f"{origem}.{campo}: usa '{termo}' — troque por linguagem simples (RNF04)")

    # 3. Tamanho: perguntas e ajudas curtas, legíveis no celular.
    for p in cat.perguntas:
        if len(p.texto) > LIMITE_TEXTO:
            avisos.append(f"{p.id}: pergunta com {len(p.texto)} caracteres (sugestão: até {LIMITE_TEXTO})")
        if len(p.ajuda) > LIMITE_AJUDA:
            avisos.append(f"{p.id}: ajuda com {len(p.ajuda)} caracteres (sugestão: até {LIMITE_AJUDA})")

    # 4. Glossário sem uso é sinal de termo órfão (não é erro: pode ser usado no relatório).
    corpus = " ".join(t for _, _, t in _textos_exibidos(cat)) + " " + " ".join(p.recomendacao for p in cat.perguntas)
    for t in g.termos:
        if not any(contem(corpus, a) for a in t.aliases):
            avisos.append(f"glossário: termo '{t.id}' não aparece em nenhum texto")

    return erros, avisos
