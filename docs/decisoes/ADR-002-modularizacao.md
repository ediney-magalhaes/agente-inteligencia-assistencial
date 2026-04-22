# ADR-002: Modularização do Motor de Análise

**Data:** 17/04/2026  
**Status:** Aprovado  
**Autor:** Ediney Magalhães

## Contexto
O arquivo `motor_analise.py` acumulou ~1000 linhas com responsabilidades misturadas: preparação de dados, geração de gráficos, chamadas de IA e funções auxiliares. Isso tornava manutenção difícil e mudanças arriscadas.

Além disso, o novo Modelo Relatório introduziu tópicos que não existiam na automação anterior, exigindo realinhamento entre o sistema e o documento.

## Decisão
Separar o `motor_analise.py` em 5 módulos especializados, cada um com uma única responsabilidade:

| Módulo | Responsabilidade |
|---|---|
| `utils.py` | Funções auxiliares compartilhadas |
| `processador.py` | Preparação e transformação dos dados |
| `visualizador.py` | Geração de gráficos |
| `agente_ia.py` | Análises textuais via IA (Gemini) |
| `relatorio.py` | Montagem do documento Word final |

## Mapeamento: Módulos x Modelo Relatório

| Tópico | Título | Fonte |
|---|---|---|
| 1 | Objetivo e Definições | Automação |
| 2 | Quantidade de Notificações | Automação |
| 3 | Turno de Notificações | Análise: Automação / Gráfico: EPIMED |
| 4 | Classificação das Notificações | Automação |
| 5 | Eventos Adversos | Automação |
| 6 | Setores Notificantes | Automação |
| 7 | Setores Notificados | Automação |
| 8 | Índices de Qualidade | Automação |
| 9 | Cumprimento de Análises | Automação |
| 10 | Auditoria de ROPS | MANUAL |
| 11 | Protocolos Gerenciados | Automação |
| 12 | Comissão de Óbitos | MANUAL |
| 13 | Comissão de Prontuários | MANUAL |
| 14 | Plano de Segurança do Paciente | MANUAL |
| 15 | Interrelação e Mapeamento de Risco | Automação |
| 16 | Ações Táticas e Estratégicas | MANUAL |

## Convenção de marcadores no documento Word
Seções manuais serão sinalizadas com `[PREENCHER MANUALMENTE]` no documento gerado, eliminando risco de omissão na montagem do relatório.

## Consequências
- Cada módulo pode ser alterado sem risco para os demais
- Novos blocos são adicionados no módulo correto sem tocar nos outros
- O documento Word gerado já nasce alinhado com o Modelo Relatório
- Qualquer pessoa que assuma o projeto entende a estrutura imediatamente