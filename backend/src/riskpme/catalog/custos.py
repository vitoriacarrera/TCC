"""Modelo de custo dos controles (audit/custos.yaml) — base do ROI do plano de ação.

custo_anual = Σ licenças + (horas_implantacao / vida_util + horas_anuais + horas_por_usuario × usuarios) × custo_hora

`usuarios` é informado pelo gestor (pergunta `usuarios_ti` de audit/contexto.yaml); não há mais valor por porte.
Preços de licença, câmbio e custo da hora têm fonte pública; as horas de esforço e o volume de dados por usuário
são estimativas declaradas.
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
    gb_por_usuario: Positivo
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
    referencia_cis_ig1_empregados: tuple[int, int, int, int]

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
    usuarios: int
    licencas: float
    mao_de_obra: float
    horas_ano: float
    itens: tuple[tuple[str, float], ...]

    @property
    def total(self) -> float:
        return self.licencas + self.mao_de_obra


def volume_backup_tb(modelo: ModeloCusto, usuarios: int) -> float:
    """Volume a proteger em backup (TB) = usuários × GB por usuário ÷ 1024."""
    return usuarios * modelo.parametros.gb_por_usuario / 1024


def custo_licenca_anual(modelo: ModeloCusto, preco: Preco, usuarios: int) -> float:
    par = modelo.parametros
    fator_moeda = par.cambio_usd_brl if preco.moeda == "USD" else 1.0
    quantidade = {
        "usuario_mes": usuarios,
        "tb_mes": volume_backup_tb(modelo, usuarios),
        "mes": 1,
    }[preco.unidade]
    return preco.valor * fator_moeda * quantidade * 12


def custo_controle(modelo: ModeloCusto, controle_id: str, porte: int, usuarios: int) -> CustoDetalhado:
    """Custo anual (R$) de um controle para uma empresa do `porte` com `usuarios` pessoas usando TI."""
    if porte not in (1, 2, 3, 4):
        raise ValueError(f"porte deve ser 1 a 4, recebido {porte}")
    if usuarios < 1:
        raise ValueError(f"usuarios deve ser ≥ 1, recebido {usuarios}")
    if controle_id not in modelo.controles:
        raise KeyError(f"controle {controle_id} sem composição de custo em custos.yaml")
    comp = modelo.controles[controle_id]
    par = modelo.parametros
    i = porte - 1

    itens = []
    for lic in comp.licencas:
        if porte in lic.portes:
            preco = modelo.preco(lic.preco)
            itens.append((preco.descricao, custo_licenca_anual(modelo, preco, usuarios)))
    horas = (comp.horas_implantacao[i] / par.vida_util_anos + comp.horas_anuais[i]
             + comp.horas_por_usuario_ano * usuarios)
    return CustoDetalhado(
        controle=controle_id,
        porte=porte,
        usuarios=usuarios,
        licencas=sum(v for _, v in itens),
        mao_de_obra=horas * par.custo_hora[i],
        horas_ano=horas,
        itens=tuple(itens),
    )


def custo_fixo_e_por_usuario(modelo: ModeloCusto, controle_id: str, porte: int) -> tuple[float, float]:
    """Decompõe o custo (linear em usuários) em parte fixa + parte por usuário — usado na memória de cálculo.

    custo(u) = fixo + por_usuario × u  ⇒  por_usuario = custo(2) − custo(1);  fixo = custo(1) − por_usuario.
    """
    c1 = custo_controle(modelo, controle_id, porte, 1).total
    c2 = custo_controle(modelo, controle_id, porte, 2).total
    por_usuario = c2 - c1
    return c1 - por_usuario, por_usuario
