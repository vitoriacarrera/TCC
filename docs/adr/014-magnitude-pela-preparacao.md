# ADR-014 — Preparação reduz o prejuízo (FAIR-CAM): perguntas de detecção e resposta na magnitude

**Status:** Aceita (25/10/2026 — revisão MAG1 a MAG5)

## Contexto
Até aqui todas as respostas alteravam só a vulnerabilidade (frequência). Backup, plano de incidentes e continuidade,
que na prática reduzem o estrago, eram avaliados por um efeito que não têm (evitar o incidente). O FAIR Controls
Analytics Model (faircam2025) separa os controles em Prevenção (afeta a frequência) e Detecção e Resposta (contenção,
resiliência, redução de perda), que "reduzem a magnitude da perda quando um evento ocorre".

## Decisão
1. **Mesmas perguntas, dois efeitos, sem contagem dupla.** As perguntas cuja subcategoria NIST começa com DE., RS.,
   RC., PR.DS-11 ou PR.IR-03 (15 de 52: DE-01 a 05, RS-01 a 04, RC-01/02, PR-10/11/12, PR-21) entram só na
   **maturidade de resposta**; as demais, só na **maturidade de prevenção** (vulnerabilidade). Lista em
   `cenarios.yaml`, `parametros_modelo.efeito_magnitude`. O validador garante que nenhum cenário fica sem pergunta
   de prevenção em nenhum perfil.
2. **Fator por cenário:** componente × (1 − máxima × maturidade de resposta), com `reducao_magnitude` em cada
   cenário:

| Cenário | Componente | Máxima | Fonte e cálculo | Sensibilidade |
|---|---|---|---|---|
| RAN | perda primária | 50% | sophos2023: recuperação US$ 375 mil com backup × US$ 750 mil pagando resgate | 87,5% (sophos2024backups: US$ 375 mil × US$ 3 mi) |
| VAZ, TER, IA | perda secundária | 17,7% | ibm2024: identificada pela própria equipe US$ 4,55 mi × revelada pelo atacante US$ 5,53 mi | 34,2% (ibm2025, ciclo < 200 × > 200 dias; conferir) |
| FRA | perda primária | 9,2% | bcbmed2025: MED do Pix devolveu 9,2% do contestado (jan.–ago. 2025) | 66% (ic3_2024, Recovery Asset Team) |
| IND | só horas paradas × custo da hora (receita perdida) | 50% | julgamento: analogia ao RAN; o conserto custa o mesmo com ou sem plano | 92,6% (1 − mínimo/média PERT das horas) |

3. **RS-02 (comunicação à ANPD):** sem fator próprio, entra no fator do vazamento; a dosimetria da ANPD
   (anpd2023dosimetria: atenuantes de 20% por governança, 20% por mecanismos para minimizar o dano, 20%/10% por
   mitigação, 5% por cooperação) é citada no texto como apoio qualitativo.
4. **Implementação multiplicativa:** os fatores multiplicam a perda primária e a secundária de cada evento. Para
   "horas_parada", o fator é 1 − redução × (média PERT das horas em R$ / média PERT total), o que preserva
   exatamente a perda média (a média da Beta-PERT é linear nos pontos). A secundária é multiplicada depois do teto.
5. **Riscos de ruptura:** as ações de preparação mostram quanto baixam o impacto do cenário (P90 no ano em que
   acontece) e o plano informa o impacto com todas elas e se o cenário sairia da faixa acima da tolerância
   (substitui a lista `matriz.selo_ruptura.preparacao` do ADR-013 pela lista única de `efeito_magnitude`).

## Consequências
- Clínica de exemplo: maturidade de resposta de 25% a 62% por cenário; prejuízo do ransomware 27% menor. Com toda a
  preparação, o impacto do ransomware cai de R$ 128 mil para R$ 99 mil, ainda acima da tolerância de R$ 54 mil: por
  isso a transferência (seguro) continua recomendada.
- **Achado para os Resultados:** com efeitos medidos (no máximo 50%) frente à faixa de vulnerabilidade de 0,02 a
  0,35 (até 94% de redução da chance, julgamento declarado CJ5), as ações de preparação têm ROSI pela média ainda
  menor que antes (backup de −91% para −97% na clínica; plano de incidentes de +2% para −69%). O valor delas
  aparece no impacto dos riscos de ruptura, não na média. Isso reforça a discussão do ADR-013.
- Limitações: fatores de comparações entre grupos de empresas maiores (IBM, Sophos), não de experimentos; o menor
  valor é a base e o maior vai para a sensibilidade. IA só tem perguntas de detecção no porte 4. MAG4 é julgamento.
  `custo_hora_parada` = receita ÷ 2.080 supõe que toda venda da parada é perdida (premissa conservadora).
