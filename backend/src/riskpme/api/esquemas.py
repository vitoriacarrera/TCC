"""Esquemas de entrada da API (RF01 a RF05). A saída reaproveita os dataclasses do motor (`to_dict`)."""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StrictInt

# Limites de entrada (OWASP API4/API8): números finitos e plausíveis, textos curtos, no máximo 100 respostas.
Id = Annotated[str, Field(min_length=1, max_length=40, pattern=r"^[A-Za-z0-9_-]+$")]
Receita = Annotated[float, Field(gt=0, le=1e12, allow_inf_nan=False)]
Usuarios = Annotated[int, Field(ge=1, le=100_000)]
Nota = Annotated[StrictInt, Field(ge=0, le=4)] | None
Respostas = Annotated[dict[Id, Nota], Field(max_length=100)]


class _Entrada(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=False)   # campo desconhecido é erro (minimização, ADR-005)


class PerfilEntrada(_Entrada):
    """Respostas de contexto do gestor (ids das opções de `audit/contexto.yaml`)."""

    setor: Id
    receita_operacional_bruta: Receita
    usuarios_ti: Usuarios
    registros_pessoais: Id
    tipo_dado: Id
    ativo_critico: Id
    apetite: Id
    tolerancia: Id
    custo_hora_parada: Annotated[float, Field(gt=0, le=1e9, allow_inf_nan=False)] | None = None   # None = "não sei"


class PedidoQuestionario(_Entrada):
    setor: Id
    receita_operacional_bruta: Receita
    usuarios_ti: Usuarios


class PedidoSimulacao(_Entrada):
    perfil: PerfilEntrada
    respostas: Respostas = Field(
        description='Resposta 0 a 4 por id de pergunta; null = "Não sei". Pergunta ausente também conta como "Não sei".')
    semente: int | None = Field(default=None, ge=0, le=2**32 - 1,
                                description="Fixa o sorteio (reprodutibilidade, testes)")


class Contribuicao(_Entrada):
    """Contribuição anonimizada (ADR-005): só setor, porte e respostas. Nada financeiro, nada que identifique."""

    consentimento: bool = Field(description="Precisa ser true: o gestor marcou a autorização (desmarcada por padrão)")
    setor: Id
    porte: int = Field(ge=1, le=4)
    respostas: Respostas
    comprovante: str = Field(max_length=200, description="`comprovante_contribuicao` devolvido por POST /simulacoes")
