# Memória de cálculo — custo anual dos controles

Gerado por `riskpme-catalogo custos` a partir de `audit/custos.yaml`. Não edite este arquivo.

custo_anual = Σ licenças + (horas_implantação ÷ vida útil + horas_anuais + horas_por_usuário × usuários) × custo_hora

## Parâmetros

- Câmbio: US$ 1 = R$ 5.1408 (PTAX venda, [@bcb2026ptax])
- Vida útil da implantação: 3 anos
- Usuários por porte: 2, 10, 50, 150 ([@tcc1], Tabela 3.1)
- Dados em backup (TB): 0.2, 1, 5, 20 (estimativa)

| Portes | Perfil | Salário P50 | Encargos | Custo/hora | Fonte |
|---|---|---|---|---|---|
| 1, 2 | Analista de Suporte Pleno (P50) | R$ 6.500 | 39.37% | R$ 41.18 | [@roberthalf2026suporte] [@fernandes2023encargos] |
| 3, 4 | Analista de Segurança Pleno (P50) | R$ 11.150 | 68.18% | R$ 85.24 | [@roberthalf2026seguranca] [@fernandes2023encargos] |

## Preços de licença

| Item | Preço | Unidade | Fonte |
|---|---|---|---|
| Bitwarden Teams (gerenciador de senhas corporativo) | USD 4.00 | usuario_mes | [@bitwarden2026] |
| Microsoft Defender for Business (antivírus com detecção e resposta) | USD 3.00 | usuario_mes | [@microsoft2026smb] |
| Microsoft Defender for Office 365 Plano 1 (filtro avançado de e-mail) | USD 2.00 | usuario_mes | [@microsoft2026smb] |
| Microsoft Intune Plano 1 (gestão e criptografia de dispositivos) | USD 8.00 | usuario_mes | [@microsoft2026smb] |
| Diferença Microsoft 365 Business Premium (US$ 22) − Business Standard (US$ 14): inclui prevenção de vazamento de dados (Purview DLP) | USD 8.00 | usuario_mes | [@microsoft2026smb] |
| Backblaze B2 (armazenamento em nuvem para backup) | USD 6.95 | tb_mes | [@backblaze2026] |
| Cloudflare Pro (proteção do site contra ataques e sobrecarga) | USD 20.00 | mes | [@cloudflare2026] |
| Cloudflare Business | USD 200.00 | mes | [@cloudflare2026] |
| Link de internet reserva (4G/5G ou fibra de 2ª operadora) | BRL 150.00 | mes | [@julgamento] |

## Custo anual por controle (R$)

| ISO 27002 | Controle | MEI | ME | EPP | Média |
|---|---|---|---|---|---|
| 5.1 | Políticas de segurança da informação | R$ 96 | R$ 191 | R$ 1.360 | R$ 2.493 |
| 5.2 | Papéis e responsabilidades pela segurança da informação | R$ 0 | R$ 1.011 | R$ 8.273 | R$ 16.547 |
| 5.9 | Inventário de informações e outros ativos associados | R$ 68 | R$ 219 | R$ 1.813 | R$ 4.533 |
| 5.10 | Uso aceitável de informações e outros ativos associados | R$ 68 | R$ 137 | R$ 567 | R$ 1.133 |
| 5.14 | Transferência de informações | R$ 55 | R$ 191 | R$ 1.133 | R$ 2.267 |
| 5.15 | Controle de acesso | R$ 55 | R$ 219 | R$ 2.040 | R$ 5.100 |
| 5.16 | Gestão de identidade | R$ 0 | R$ 137 | R$ 1.133 | R$ 3.173 |
| 5.17 | Informações de autenticação | R$ 507 | R$ 2.604 | R$ 13.018 | R$ 38.374 |
| 5.18 | Direitos de acesso | R$ 0 | R$ 109 | R$ 793 | R$ 2.267 |
| 5.19 | Segurança da informação nas relações com fornecedores | R$ 0 | R$ 137 | R$ 1.133 | R$ 3.173 |
| 5.23 | Segurança da informação para uso de serviços em nuvem | R$ 0 | R$ 137 | R$ 1.133 | R$ 2.493 |
| 5.24 | Planejamento e preparação da gestão de incidentes de segurança da informação | R$ 68 | R$ 273 | R$ 1.360 | R$ 3.173 |
| 5.30 | Prontidão de TIC para continuidade de negócios | R$ 68 | R$ 273 | R$ 2.267 | R$ 5.667 |
| 5.31 | Requisitos legais, estatutários, regulamentares e contratuais | R$ 14 | R$ 68 | R$ 283 | R$ 567 |
| 5.34 | Privacidade e proteção de dados pessoais | R$ 137 | R$ 547 | R$ 3.740 | R$ 8.500 |
| 6.3 | Conscientização, educação e treinamento em segurança da informação | R$ 150 | R$ 547 | R$ 4.817 | R$ 13.883 |
| 8.1 | Dispositivos endpoint do usuário | R$ 14 | R$ 68 | R$ 25.243 | R$ 75.388 |
| 8.2 | Direitos de acessos privilegiados | R$ 14 | R$ 137 | R$ 1.133 | R$ 2.493 |
| 8.5 | Autenticação segura | R$ 14 | R$ 68 | R$ 567 | R$ 1.133 |
| 8.7 | Proteção contra malware | R$ 14 | R$ 1.960 | R$ 10.160 | R$ 30.254 |
| 8.8 | Gestão de vulnerabilidades técnicas | R$ 96 | R$ 547 | R$ 4.533 | R$ 11.333 |
| 8.9 | Gestão de configuração | R$ 0 | R$ 68 | R$ 1.133 | R$ 2.493 |
| 8.10 | Exclusão de informações | R$ 55 | R$ 109 | R$ 567 | R$ 1.360 |
| 8.12 | Prevenção de vazamento de dados | R$ 0 | R$ 0 | R$ 1.133 | R$ 77.201 |
| 8.13 | Backup das informações | R$ 195 | R$ 729 | R$ 4.637 | R$ 13.562 |
| 8.14 | Redundância dos recursos de tratamento de informações | R$ 0 | R$ 1.937 | R$ 2.933 | R$ 4.293 |
| 8.15 | Registros (logs) | R$ 0 | R$ 0 | R$ 907 | R$ 2.720 |
| 8.16 | Atividades de monitoramento | R$ 0 | R$ 519 | R$ 9.293 | R$ 36.493 |
| 8.20 | Segurança de redes | R$ 14 | R$ 137 | R$ 2.367 | R$ 14.831 |
| 8.22 | Segregação de redes | R$ 0 | R$ 191 | R$ 1.360 | R$ 3.060 |
| 8.23 | Filtragem da web | R$ 0 | R$ 1.288 | R$ 6.622 | R$ 19.414 |
| 8.24 | Uso de criptografia | R$ 14 | R$ 68 | R$ 397 | R$ 793 |
| 8.28 | Codificação segura | R$ 0 | R$ 1.203 | R$ 9.293 | R$ 22.667 |
| | **Total (todos os controles)** | **R$ 1.714** | **R$ 15.830** | **R$ 127.144** | **R$ 432.832** |
| | Teto CIS IG1 – ferramentas [@cis2025cost] | R$ 195.988 | R$ 195.988 | R$ 909.721 | R$ 7.434.558 |

## Detalhamento

**5.1 Políticas de segurança da informação** — horas de implantação [4.0, 8.0, 24.0, 40.0], horas/ano [1.0, 2.0, 8.0, 16.0]

**5.2 Papéis e responsabilidades pela segurança da informação** — horas de implantação [0.0, 2.0, 4.0, 8.0], horas/ano [0.0, 24.0, 96.0, 192.0]

**5.9 Inventário de informações e outros ativos associados** — horas de implantação [2.0, 4.0, 16.0, 40.0], horas/ano [1.0, 4.0, 16.0, 40.0]

**5.10 Uso aceitável de informações e outros ativos associados** — horas de implantação [2.0, 4.0, 8.0, 16.0], horas/ano [1.0, 2.0, 4.0, 8.0]

**5.14 Transferência de informações** — horas de implantação [1.0, 2.0, 4.0, 8.0], horas/ano [1.0, 4.0, 12.0, 24.0]

**5.15 Controle de acesso** — horas de implantação [1.0, 4.0, 24.0, 60.0], horas/ano [1.0, 4.0, 16.0, 40.0]

**5.16 Gestão de identidade** — horas de implantação [0.0, 4.0, 16.0, 40.0], horas/ano [0.0, 2.0, 8.0, 24.0]

**5.17 Informações de autenticação** — horas de implantação [1.0, 4.0, 12.0, 24.0], horas/ano [0.0, 2.0, 4.0, 8.0]
- licença: Bitwarden Teams (gerenciador de senhas corporativo), portes [1, 2, 3, 4]

**5.18 Direitos de acesso** — horas de implantação [0.0, 2.0, 4.0, 8.0], horas/ano [0.0, 2.0, 8.0, 24.0]

**5.19 Segurança da informação nas relações com fornecedores** — horas de implantação [0.0, 4.0, 16.0, 40.0], horas/ano [0.0, 2.0, 8.0, 24.0]

**5.23 Segurança da informação para uso de serviços em nuvem** — horas de implantação [0.0, 4.0, 16.0, 40.0], horas/ano [0.0, 2.0, 8.0, 16.0]

**5.24 Planejamento e preparação da gestão de incidentes de segurança da informação** — horas de implantação [2.0, 8.0, 24.0, 40.0], horas/ano [1.0, 4.0, 8.0, 24.0]

**5.30 Prontidão de TIC para continuidade de negócios** — horas de implantação [2.0, 8.0, 32.0, 80.0], horas/ano [1.0, 4.0, 16.0, 40.0]

**5.31 Requisitos legais, estatutários, regulamentares e contratuais** — horas de implantação [1.0, 2.0, 4.0, 8.0], horas/ano [0.0, 1.0, 2.0, 4.0]

**5.34 Privacidade e proteção de dados pessoais** — horas de implantação [4.0, 16.0, 60.0, 120.0], horas/ano [2.0, 8.0, 24.0, 60.0]

**6.3 Conscientização, educação e treinamento em segurança da informação** — horas de implantação [2.0, 4.0, 8.0, 16.0], horas/ano [1.0, 2.0, 4.0, 8.0], 1 h por usuário/ano

**8.1 Dispositivos endpoint do usuário** — horas de implantação [1.0, 2.0, 8.0, 24.0], horas/ano [0.0, 1.0, 4.0, 8.0]
- licença: Microsoft Intune Plano 1 (gestão e criptografia de dispositivos), portes [3, 4]

**8.2 Direitos de acessos privilegiados** — horas de implantação [1.0, 4.0, 16.0, 40.0], horas/ano [0.0, 2.0, 8.0, 16.0]

**8.5 Autenticação segura** — horas de implantação [1.0, 2.0, 8.0, 16.0], horas/ano [0.0, 1.0, 4.0, 8.0]

**8.7 Proteção contra malware** — horas de implantação [1.0, 2.0, 8.0, 16.0], horas/ano [0.0, 2.0, 8.0, 24.0]
- licença: Microsoft Defender for Business (antivírus com detecção e resposta), portes [2, 3, 4]

**8.8 Gestão de vulnerabilidades técnicas** — horas de implantação [1.0, 4.0, 16.0, 40.0], horas/ano [2.0, 12.0, 48.0, 120.0]

**8.9 Gestão de configuração** — horas de implantação [0.0, 2.0, 16.0, 40.0], horas/ano [0.0, 1.0, 8.0, 16.0]

**8.10 Exclusão de informações** — horas de implantação [1.0, 2.0, 8.0, 24.0], horas/ano [1.0, 2.0, 4.0, 8.0]

**8.12 Prevenção de vazamento de dados** — horas de implantação [0.0, 0.0, 16.0, 40.0], horas/ano [0.0, 0.0, 8.0, 24.0]
- licença: Diferença Microsoft 365 Business Premium (US$ 22) − Business Standard (US$ 14): inclui prevenção de vazamento de dados (Purview DLP), portes [4]

**8.13 Backup das informações** — horas de implantação [2.0, 4.0, 16.0, 32.0], horas/ano [2.0, 6.0, 24.0, 48.0]
- licença: Backblaze B2 (armazenamento em nuvem para backup), portes [1, 2, 3, 4]

**8.14 Redundância dos recursos de tratamento de informações** — horas de implantação [0.0, 4.0, 16.0, 40.0], horas/ano [0.0, 2.0, 8.0, 16.0]
- licença: Link de internet reserva (4G/5G ou fibra de 2ª operadora), portes [2, 3, 4]

**8.15 Registros (logs)** — horas de implantação [0.0, 0.0, 8.0, 24.0], horas/ano [0.0, 0.0, 8.0, 24.0]

**8.16 Atividades de monitoramento** — horas de implantação [0.0, 2.0, 16.0, 40.0], horas/ano [0.0, 12.0, 104.0, 416.0]

**8.20 Segurança de redes** — horas de implantação [1.0, 4.0, 16.0, 40.0], horas/ano [0.0, 2.0, 8.0, 16.0]
- licença: Cloudflare Pro (proteção do site contra ataques e sobrecarga), portes [3]
- licença: Cloudflare Business, portes [4]

**8.22 Segregação de redes** — horas de implantação [0.0, 8.0, 24.0, 60.0], horas/ano [0.0, 2.0, 8.0, 16.0]

**8.23 Filtragem da web** — horas de implantação [0.0, 1.0, 4.0, 8.0], horas/ano [0.0, 1.0, 4.0, 8.0]
- licença: Microsoft Defender for Office 365 Plano 1 (filtro avançado de e-mail), portes [2, 3, 4]

**8.24 Uso de criptografia** — horas de implantação [1.0, 2.0, 8.0, 16.0], horas/ano [0.0, 1.0, 2.0, 4.0]

**8.28 Codificação segura** — horas de implantação [0.0, 16.0, 40.0, 80.0], horas/ano [0.0, 24.0, 96.0, 240.0]

