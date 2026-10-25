"""Modelos do catálogo de auditoria (espelham os arquivos de `audit/`).

A validação cruzada (referências entre arquivos) fica em `Catalogo`, de modo que um erro de digitação no YAML
— um cenário, controle ou fonte inexistente — é detectado ao carregar, e não durante uma simulação.
"""

from __future__ import annotations

import itertools
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .custos import CustoDetalhado, ModeloCusto, custo_controle

FUNCOES_CSF = ("GV", "ID", "PR", "DE", "RS", "RC")
NIVEIS_PORTE = (1, 2, 3, 4)

NaoNegativo = Annotated[float, Field(ge=0)]


class _Base(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


def _lista(v: str | list[str]) -> list[str]:
    return [v] if isinstance(v, str) else v


# --------------------------------------------------------------------------- fontes
class Fonte(_Base):
    id: str
    titulo: str
    url: str | None = None
    dados: list[str] = []
    limitacao: str | None = None


# --------------------------------------------------------------------------- perfil
class Porte(_Base):
    """Nível de porte, classificado pela Receita Operacional Bruta anual (ADR-010)."""

    nivel: int
    nome: str
    pessoas: tuple[int, int | None]      # só referência (Sebrae); a classificação é pela ROB
    rob_min: float = Field(ge=0)         # exclusivo (o nível 1 começa em 0, inclusivo)
    rob_max: float = Field(gt=0)         # inclusivo
    multiplicador_tef: float = Field(gt=0)
    calculo: str | None = None
    fonte: list[str]

    _fonte = field_validator("fonte", mode="before")(_lista)

    @field_validator("nivel")
    @classmethod
    def _nivel(cls, v: int) -> int:
        if v not in NIVEIS_PORTE:
            raise ValueError(f"nível de porte deve ser 1 a 4, recebido {v}")
        return v


class Multiplicador(_Base):
    """Parâmetro rastreável (revisão S5): valor + fonte + cálculo; `pendente` marca neutro à espera de dado."""

    valor: float = Field(gt=0)
    fonte: str
    calculo: str | None = None
    pendente: bool = False


class Setor(_Base):
    id: str
    nome: str
    exemplos: str
    multiplicador_tef: dict[str, Multiplicador] = {}
    multiplicador_custo_registro: Multiplicador

    def mult_tef(self, cenario_id: str) -> float:
        m = self.multiplicador_tef.get(cenario_id)
        return m.valor if m else 1.0

    @property
    def custo_registro(self) -> float:
        return self.multiplicador_custo_registro.valor


# --------------------------------------------------------------------------- cenários (FAIR)
Tri = tuple[NaoNegativo, NaoNegativo, NaoNegativo]
COMPONENTES_PRIMARIA = ("horas_parada", "pct_faturamento", "fixo")
COMPONENTES_SECUNDARIA = ("por_registro", "pct_faturamento", "fixo")


class PerdaPrimaria(_Base):
    """Custos diretos da empresa. Três pontos (mín, mais provável, máx) de cada componente → Beta-PERT."""

    horas_parada: Tri = (0, 0, 0)
    pct_faturamento: Tri = (0, 0, 0)
    fixo: Tri = (0, 0, 0)

    @model_validator(mode="after")
    def _ordenados(self) -> PerdaPrimaria:
        for nome in COMPONENTES_PRIMARIA:
            a, b, c = getattr(self, nome)
            if not (a <= b <= c):
                raise ValueError(f"perda_primaria.{nome} precisa ser mín ≤ mais provável ≤ máx, recebido {(a, b, c)}")
        if all(getattr(self, n)[2] == 0 for n in COMPONENTES_PRIMARIA):
            raise ValueError("perda_primaria sem nenhum componente")
        return self


class PontoSecundaria(_Base):
    por_registro: NaoNegativo = 0
    pct_faturamento: NaoNegativo = 0
    fixo: NaoNegativo = 0


class PerdaSecundaria(_Base):
    """Reação de terceiros. Ocorre com `probabilidade` (SLEF); valor ~ Lognormal(mediana, p95), com teto."""

    probabilidade: float = Field(ge=0, le=1)
    mediana: PontoSecundaria
    p95: PontoSecundaria
    teto_pct_faturamento: float = Field(gt=0)

    @model_validator(mode="after")
    def _p95_maior(self) -> PerdaSecundaria:
        maior = False
        for nome in COMPONENTES_SECUNDARIA:
            m, p = getattr(self.mediana, nome), getattr(self.p95, nome)
            if p < m:
                raise ValueError(f"perda_secundaria: p95.{nome} ({p}) menor que mediana.{nome} ({m})")
            maior |= p > m
        if not maior:
            raise ValueError("perda_secundaria: p95 precisa ser maior que a mediana em ao menos um componente")
        if all(getattr(self.mediana, n) == 0 for n in COMPONENTES_SECUNDARIA):
            raise ValueError("perda_secundaria: mediana precisa ter ao menos um componente > 0 (lognormal exige valor positivo)")
        return self


class ReducaoMagnitude(_Base):
    """Quanto as perguntas de Detecção e Resposta reduzem o prejuízo do cenário (FAIR-CAM, revisão MAG).

    componente: "primaria" (toda a perda primária), "horas_parada" (só horas × custo da hora: receita perdida)
    ou "secundaria". Fator aplicado = 1 − maxima × maturidade de resposta do cenário.
    """

    componente: Literal["primaria", "horas_parada", "secundaria"]
    maxima: float = Field(ge=0, le=1)
    fonte: str
    calculo: str
    sensibilidade: float = Field(ge=0, le=1)        # valor alternativo para a análise de sensibilidade
    fonte_sensibilidade: str


class Cenario(_Base):
    id: str
    nome: str
    descricao: str
    ameaca: str
    efeito: list[Literal["confidencialidade", "integridade", "disponibilidade"]]
    tef_base: float = Field(gt=0)
    perda_primaria: PerdaPrimaria
    perda_secundaria: PerdaSecundaria
    reducao_magnitude: ReducaoMagnitude
    fonte: list[str]

    _fonte = field_validator("fonte", mode="before")(_lista)


class EfeitoMagnitude(_Base):
    """Perguntas cuja subcategoria do NIST CSF começa com um destes prefixos reduzem o prejuízo, não a chance."""

    subcategorias: list[str] = Field(min_length=1)
    fonte: str


class ParametrosModelo(_Base):
    vulnerabilidade_min: float = Field(gt=0, lt=1)
    vulnerabilidade_max: float = Field(gt=0, lt=1)
    pert_lambda: float = Field(gt=0)
    iteracoes: int = Field(ge=1000)
    resposta_nao_sei: int = Field(ge=0, le=4)
    percentil_mapa_calor: float = Field(gt=50, lt=100)
    z_p95: float = Field(gt=1.6, lt=1.7)
    efeito_magnitude: EfeitoMagnitude

    def reduz_magnitude(self, subcategoria: str) -> bool:
        return subcategoria.startswith(tuple(self.efeito_magnitude.subcategorias))

    @model_validator(mode="after")
    def _faixa(self) -> ParametrosModelo:
        if self.vulnerabilidade_min >= self.vulnerabilidade_max:
            raise ValueError("vulnerabilidade_min deve ser menor que vulnerabilidade_max")
        return self


# --------------------------------------------------------------------------- controles e perguntas
class Controle(_Base):
    id: str
    nome: str
    tipo: Literal["preventivo", "detectivo", "corretivo"]
    esforco: Literal["baixo", "medio", "alto"]


class TermoGlossario(_Base):
    id: str
    termo: str
    aliases: list[str] = Field(min_length=1)
    explicacao: str = Field(min_length=20)
    exemplo: str | None = None


class ConceitoResultado(_Base):
    id: str
    termo: str
    explicacao: str = Field(min_length=20)


class Glossario(_Base):
    evitar_no_texto: list[str]
    termos: list[TermoGlossario]
    conceitos_resultado: list[ConceitoResultado]


class Instrucoes(_Base):
    titulo: str
    texto: str
    tempo_estimado_min: dict[int, int]


class FuncaoCSF(_Base):
    nome: str
    descricao: str


class OpcaoEscala(_Base):
    valor: int | None
    rotulo: str


class CondicaoVariante(_Base):
    portes: list[int] | None = None          # níveis em que a variante vale (None = todos)
    usuarios_max: int | None = None          # vale só se usuarios_ti <= este número (ex.: 1 = quem trabalha sozinho)


class Variante(_Base):
    """Texto alternativo da pergunta para um perfil (revisão Q-SOLO, Q-RSMEI, Q-GV04)."""

    quando: CondicaoVariante
    texto: str | None = None
    ajuda: str | None = None
    recomendacao: str | None = None
    cenarios: dict[str, int] | None = None

    def vale_para(self, porte: int, usuarios: int | None) -> bool:
        q = self.quando
        if q.portes is not None and porte not in q.portes:
            return False
        return not (q.usuarios_max is not None and (usuarios is None or usuarios > q.usuarios_max))


class Pergunta(_Base):
    id: str
    funcao: Literal["GV", "ID", "PR", "DE", "RS", "RC"]
    subcategoria: str
    texto: str = Field(min_length=10)
    ajuda: str = Field(min_length=40)   # RNF04: toda pergunta explica o que é e por que importa
    porte_min: int = Field(ge=1, le=4)
    setores: list[str] | None = None
    cenarios: dict[str, int]
    controle: str
    recomendacao: str
    variantes: list[Variante] = []

    @field_validator("cenarios")
    @classmethod
    def _pesos(cls, v: dict[str, int]) -> dict[str, int]:
        if not v:
            raise ValueError("a pergunta precisa alimentar ao menos um cenário")
        for c, p in v.items():
            if p not in (1, 2, 3):
                raise ValueError(f"peso de {c} deve ser 1, 2 ou 3 (recebido {p})")
        return v

    @model_validator(mode="after")
    def _subcategoria(self) -> Pergunta:
        if not self.subcategoria.startswith(self.funcao + "."):
            raise ValueError(f"{self.id}: subcategoria {self.subcategoria} não pertence à função {self.funcao}")
        return self

    def aplica_a(self, porte: int, setor: str) -> bool:
        return porte >= self.porte_min and (self.setores is None or setor in self.setores)

    def para_perfil(self, porte: int, usuarios: int | None = None) -> Pergunta:
        """A pergunta como o gestor deste perfil a vê: a primeira variante que vale substitui os campos dela."""
        for v in self.variantes:
            if v.vale_para(porte, usuarios):
                troca = {k: getattr(v, k) for k in ("texto", "ajuda", "recomendacao", "cenarios")
                         if getattr(v, k) is not None}
                return self.model_copy(update=troca | {"variantes": []})
        return self


# --------------------------------------------------------------------------- catálogo completo
class Catalogo(_Base):
    fontes: list[Fonte]
    portes: list[Porte]
    setores: list[Setor]
    parametros_modelo: ParametrosModelo
    cenarios: list[Cenario]
    controles: list[Controle]
    instrucoes: Instrucoes
    funcoes: dict[Literal["GV", "ID", "PR", "DE", "RS", "RC"], FuncaoCSF]
    escala: list[OpcaoEscala]
    aviso_legal: str = Field(min_length=40)    # revisão Q-AVISO: tela inicial e relatório
    perguntas: list[Pergunta]
    glossario: Glossario
    custos: ModeloCusto
    contexto: dict  # perguntas de contexto (RF02, RF03, RF05) — validadas em `validate.py`

    # ---- consultas -----------------------------------------------------------------------------------------
    def porte(self, nivel: int) -> Porte:
        return _unico(self.portes, lambda p: p.nivel == nivel, f"porte {nivel}")

    def setor(self, setor_id: str) -> Setor:
        return _unico(self.setores, lambda s: s.id == setor_id, f"setor '{setor_id}'")

    def cenario(self, cenario_id: str) -> Cenario:
        return _unico(self.cenarios, lambda c: c.id == cenario_id, f"cenário '{cenario_id}'")

    def controle(self, controle_id: str) -> Controle:
        return _unico(self.controles, lambda c: c.id == controle_id, f"controle '{controle_id}'")

    def classificar_porte(self, rob: float) -> int:
        """Nível de porte pela Receita Operacional Bruta anual (ADR-010). Acima do teto: fora do escopo."""
        if rob < 0:
            raise ValueError("receita operacional bruta não pode ser negativa")
        for p in sorted(self.portes, key=lambda x: x.nivel):
            if rob <= p.rob_max:
                return p.nivel
        raise ValueError(f"receita de R$ {rob:,.0f} acima do limite da média empresa: fora do escopo da ferramenta")

    def custo_controle(self, controle_id: str, porte: int, usuarios: int) -> CustoDetalhado:
        """Custo anual (R$) de implantar e manter um controle numa empresa do porte dado, com `usuarios`
        pessoas usando TI (resposta à pergunta `usuarios_ti`)."""
        self.controle(controle_id)
        return custo_controle(self.custos, controle_id, porte, usuarios)

    def questionario(self, porte: int, setor: str, usuarios: int | None = None) -> list[Pergunta]:
        """Perguntas aplicáveis a um perfil (RF01 + RF04), na ordem do catálogo, já com as variantes do perfil."""
        self.porte(porte)
        self.setor(setor)
        return [p.para_perfil(porte, usuarios) for p in self.perguntas if p.aplica_a(porte, setor)]

    def tef(self, cenario_id: str, porte: int, setor: str) -> float:
        """TEF do perfil = tef_base × multiplicador do setor × multiplicador do porte (RF07, ADR-006)."""
        c = self.cenario(cenario_id)
        return c.tef_base * self.setor(setor).mult_tef(cenario_id) * self.porte(porte).multiplicador_tef

    # ---- integridade referencial ---------------------------------------------------------------------------
    @model_validator(mode="after")
    def _referencias(self) -> Catalogo:
        erros: list[str] = []
        for nome, itens, chave in (
            ("fontes", self.fontes, "id"),
            ("portes", self.portes, "nivel"),
            ("setores", self.setores, "id"),
            ("cenarios", self.cenarios, "id"),
            ("controles", self.controles, "id"),
            ("perguntas", self.perguntas, "id"),
        ):
            vistos: set = set()
            for it in itens:
                k = getattr(it, chave)
                if k in vistos:
                    erros.append(f"{nome}: id duplicado '{k}'")
                vistos.add(k)

        if sorted(p.nivel for p in self.portes) != list(NIVEIS_PORTE):
            erros.append("portes: devem existir exatamente os níveis 1, 2, 3 e 4")

        fontes = {f.id for f in self.fontes}
        cenarios = {c.id for c in self.cenarios}
        setores = {s.id for s in self.setores}
        controles = {c.id for c in self.controles}

        for grupo in (self.portes, self.cenarios):
            for it in grupo:
                for f in it.fonte:
                    if f not in fontes:
                        erros.append(f"{type(it).__name__} {getattr(it, 'id', getattr(it, 'nivel', '?'))}: fonte '{f}' inexistente")
        for c in self.cenarios:
            for f in (c.reducao_magnitude.fonte, c.reducao_magnitude.fonte_sensibilidade):
                if f not in fontes:
                    erros.append(f"cenário {c.id}: fonte '{f}' da redução de magnitude inexistente")
        if self.parametros_modelo.efeito_magnitude.fonte not in fontes:
            erros.append(f"parametros_modelo.efeito_magnitude: fonte '{self.parametros_modelo.efeito_magnitude.fonte}' "
                         "inexistente")
        for s in self.setores:
            for c, m in s.multiplicador_tef.items():
                if c not in cenarios:
                    erros.append(f"setor {s.id}: multiplicador para cenário inexistente '{c}'")
                if m.fonte not in fontes:
                    erros.append(f"setor {s.id}.{c}: fonte '{m.fonte}' inexistente")
            if s.multiplicador_custo_registro.fonte not in fontes:
                erros.append(f"setor {s.id}: fonte '{s.multiplicador_custo_registro.fonte}' do custo por registro inexistente")

        niveis = sorted(self.portes, key=lambda x: x.nivel)
        if niveis and niveis[0].rob_min != 0:
            erros.append("portes: o nível 1 deve começar em ROB 0")
        for a, b in itertools.pairwise(niveis):
            if a.rob_max != b.rob_min:
                erros.append(f"portes: faixas de ROB descontínuas entre os níveis {a.nivel} e {b.nivel}")
        for p in self.perguntas:
            for c in list(p.cenarios) + [c for v in p.variantes for c in (v.cenarios or {})]:
                if c not in cenarios:
                    erros.append(f"pergunta {p.id}: cenário inexistente '{c}'")
            if p.controle not in controles:
                erros.append(f"pergunta {p.id}: controle inexistente '{p.controle}'")
            for s in p.setores or []:
                if s not in setores:
                    erros.append(f"pergunta {p.id}: setor inexistente '{s}'")

        valores = [o.valor for o in self.escala]
        if valores[:5] != [0, 1, 2, 3, 4]:
            erros.append("escala: os cinco primeiros valores devem ser 0, 1, 2, 3, 4")

        for c in controles:
            if c not in self.custos.controles:
                erros.append(f"controle {c}: sem composição de custo em custos.yaml")
        for c in self.custos.controles:
            if c not in controles:
                erros.append(f"custos.yaml: composição para controle inexistente '{c}'")
        fontes_custo = list(self.custos.parametros.fonte) + [p.fonte for p in self.custos.precos]
        fontes_custo += [f for m in self.custos.mao_de_obra for f in m.fonte]
        for f in fontes_custo:
            if f not in fontes:
                erros.append(f"custos.yaml: fonte '{f}' inexistente em fontes.yaml")

        if set(self.funcoes) != set(FUNCOES_CSF):
            erros.append(f"funcoes: devem ser exatamente as 6 do NIST CSF 2.0 {FUNCOES_CSF}")

        ids_glossario = [t.id for t in self.glossario.termos] + [c.id for c in self.glossario.conceitos_resultado]
        if len(ids_glossario) != len(set(ids_glossario)):
            erros.append("glossario: ids duplicados")

        if erros:
            raise ValueError("Catálogo inconsistente:\n  - " + "\n  - ".join(erros))
        return self


def _unico(itens, pred, descricao):
    for it in itens:
        if pred(it):
            return it
    raise KeyError(f"{descricao} não existe no catálogo")
