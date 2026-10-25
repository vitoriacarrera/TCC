"""Esquemas de entrada da API (RF01 a RF05). A saída reaproveita os dataclasses do motor (`to_dict`)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class _Entrada(BaseModel):
    model_config = ConfigDict(extra="forbid")   # campo desconhecido é erro (minimização, ADR-005)


class PerfilEntrada(_Entrada):
    """Respostas de contexto do gestor (ids das opções de `audit/contexto.yaml`)."""

    setor: str
    receita_operacional_bruta: float = Field(gt=0)
    usuarios_ti: int = Field(ge=1)
    registros_pessoais: str
    tipo_dado: str
    ativo_critico: str
    apetite: str
    tolerancia: str
    custo_hora_parada: float | None = Field(default=None, gt=0)   # None = "não sei" (receita ÷ 2.080)


class PedidoQuestionario(_Entrada):
    setor: str
    receita_operacional_bruta: float = Field(gt=0)
    usuarios_ti: int = Field(ge=1)


class PedidoSimulacao(_Entrada):
    perfil: PerfilEntrada
    respostas: dict[str, int | None] = Field(
        description='Resposta 0 a 4 por id de pergunta; null = "Não sei". Pergunta ausente também conta como "Não sei".')
    semente: int | None = Field(default=None, description="Fixa o sorteio (reprodutibilidade, testes)")


class Contribuicao(_Entrada):
    """Contribuição anonimizada (ADR-005): só setor, porte e respostas. Nada financeiro, nada que identifique."""

    consentimento: bool = Field(description="Precisa ser true: o gestor marcou a autorização (desmarcada por padrão)")
    setor: str
    porte: int = Field(ge=1, le=4)
    respostas: dict[str, int | None]
