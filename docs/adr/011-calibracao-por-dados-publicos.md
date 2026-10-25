# ADR-011 — Calibração por dados públicos ("dados antes de julgamento")

**Status:** Aceita (12 a 25/10/2026 — revisão da Etapa 1)

## Contexto
Na primeira versão, multiplicadores de setor, frequências base e parte das magnitudes eram estimativas da autora.
A frequência estava calibrada pelo Hiscox (59% das PMEs atacadas por ano), que mede ataques, não perdas, e
superestimava a chance de prejuízo em cerca de 3,5 vezes.

## Decisão
1. **Princípio P1:** todo parâmetro numérico vem de fonte pública com cálculo explícito; sem dado, valor neutro
   (1,0); julgamento só quando inevitável, marcado `fonte: julgamento`, listado nas Limitações e coberto pela análise
   de sensibilidade. O validador imprime a lista de parâmetros `julgamento` e `pendente`.
2. **Setores** (`{valor, fonte, calculo}`): ransomware pela Sophos 2024 (saúde 1,24; indústria 1,18; tecnologia
   0,90; varejo 0,67; serviços neutro e pendente); demais cenários neutros; custo por registro pelas razões IBM 2025.
3. **Frequência base** pelo UK CSBS 2025/26: 12,9% das empresas com evento de perda no ano (43% × 30%),
   ransomware 1%, fraude 3%; tef = λ × 1,096 / V(0,5). Resultado na EPP: 25% / 14% / 1,6% de chance de prejuízo no
   ano sem controles / maturidade média / máxima.
4. **Ransomware** pela Sophos 2025: horas de parada 8 / 40 / 176; probabilidade de vazamento junto 22%.
5. **Tipo de dado** deixa de multiplicar o prejuízo (sem dado) e vira selo nas recomendações de privacidade.
6. **Apetite e tolerância "não sei dizer"**: 1% da receita (materialidade, ISA 320) e margem antes do IR por setor
   (IBGE PAC, PAS e PIA 2023; saúde sem dado → menor valor, 4,5%).
7. **Custos**: vida útil de 5 anos (IN RFB 1.700/2017); link reserva dedicado de fibra R$ 1.044,63/mês (média de
   contratações públicas), só para a média empresa; seguro cibernético sem custo calculado.

## Consequências
- Continuam como julgamento declarado: horas de esforço por controle, GB por usuário em backup, repartição da
  frequência entre VAZ, IND, TER e IA, demais magnitudes, faixa de vulnerabilidade e pesos das perguntas.
- Fontes em `audit/fontes.yaml` e `docs/referencias.bib` com as mesmas chaves.
