"""Modelo de custo dos controles (audit/custos.yaml) — base do ROI do plano de ação.

custo_anual = Σ licenças + (horas_implantacao / vida_util + horas_anuais + horas_por_usuario × usuarios) × custo_hora

Preços de licença, câmbio e custo da hora têm fonte pública; as horas de esforço são estimativas declaradas.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Positivo = Annotated[float, Field(gt=0)]
NaoNeg = Annotated[float, Field(ge=0)]
PorPorte = tuple[NaoNeg, NaoNeg, NaoNeg, NaoNeg]


class _Base(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ParametrosCusto(_Base):
    cambio_usd_brl: Positivo
    vida_util_anos: Positivo
    usuarios: tuple[int, int, int, int]
    dados_tb: PorPorte
    custo_hora: PorPorte
    fonte: list[str]


class MaoDeObra(_Base):
    portes: list[int]
    perfil: str
    salario_mensal: Positivo
    encargos: NaoNeg
    custo_hora_calculado: Positivo
    fonte: list[str]

    @model_validator(mode="after")
    def _conta(self) -> MaoDeObra:
        esperado = self.salario_mensal * (1 + self.encargos) / 220
        if abs(esperado - self.custo_hora_calculado) > 0.05:
            raise ValueError(f"{self.perfil}: custo_hora_calculado {self.custo_hora_calculado} ≠ {esperado:.2f}")
        return self


class Preco(_Base):
    id: str
    descricao: str
    valor: Positivo
    moeda: Literal["USD", "BRL"]
    unidade: Literal["usuario_mes", "tb_mes", "mes"]
    fonte: str


class Licenca(_Base):
    preco: str
    portes: list[int]


class ComposicaoControle(_Base):
    horas_implantacao: PorPorte
    horas_anuais: PorPorte
    horas_por_usuario_ano: NaoNeg = 0
    licencas: list[Licenca] = []


class ModeloCusto(_Base):
    parametros: ParametrosCusto
    mao_de_obra: list[MaoDeObra]
    precos: list[Preco]
    controles: dict[str, ComposicaoControle]
    referencia_cis_ig1_usd: PorPorte

    @model_validator(mode="after")
    def _consistencia(self) -> ModeloCusto:
        erros = []
        ids = {p.id for p in self.precos}
        for cid, comp in self.controles.items():
            for lic in comp.licencas:
                if lic.preco not in ids:
                    erros.append(f"custos: controle {cid} usa preço inexistente '{lic.preco}'")
                if any(p not in (1, 2, 3, 4) for p in lic.portes):
                    erros.append(f"custos: controle {cid} com porte inválido em licenças")
        for m in self.mao_de_obra:
            for p in m.portes:
                if round(m.custo_hora_calculado) != round(self.parametros.custo_hora[p - 1]):
                    erros.append(f"custos: custo_hora do porte {p} difere da mão de obra '{m.perfil}'")
        if erros:
            raise ValueError("\n  - ".join(erros))
        return self

    def preco(self, preco_id: str) -> Preco:
        return next(p for p in self.precos if p.id == preco_id)


@dataclass(frozen=True)
class CustoDetalhado:
    controle: str
    porte: int
    licencas: float
    mao_de_obra: float
    horas_ano: float
    itens: tuple[tuple[str, float], ...]

    @property
    def total(self) -> float:
        return self.licencas + self.mao_de_obra


def custo_licenca_anual(modelo: ModeloCusto, preco: Preco, porte: int) -> float:
    par = modelo.parametros
    fator_moeda = par.cambio_usd_brl if preco.moeda == "USD" else 1.0
    quantidade = {
        "usuario_mes": par.usuarios[porte - 1],
        "tb_mes": par.dados_tb[porte - 1],
        "mes": 1,
    }[preco.unidade]
    return preco.valor * fator_moeda * quantidade * 12


def custo_controle(modelo: ModeloCusto, controle_id: str, porte: int) -> CustoDetalhado:
    if controle_id not in modelo.controles:
        raise KeyError(f"controle {controle_id} sem composição de custo em custos.yaml")
    comp = modelo.controles[controle_id]
    par = modelo.parametros
    i = porte - 1

    itens = []
    for lic in comp.licencas:
        if porte in lic.portes:
            preco = modelo.preco(lic.preco)
            itens.append((preco.descricao, custo_licenca_anual(modelo, preco, porte)))
    horas = (comp.horas_implantacao[i] / par.vida_util_anos + comp.horas_anuais[i]
             + comp.horas_por_usuario_ano * par.usuarios[i])
    return CustoDetalhado(
        controle=controle_id,
        porte=porte,
        licencas=sum(v for _, v in itens),
        mao_de_obra=horas * par.custo_hora[i],
        horas_ano=horas,
        itens=tuple(itens),
    )
