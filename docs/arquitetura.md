# Arquitetura do Sistema

**Projeto:** Agente de Análise - Segurança do Paciente  
**Autor:** Ediney Magalhães  
**Última atualização:** 24/04/2026

---

## Visão Geral

Sistema de automação analítica para geração do Relatório Trimestral de 
Segurança do Paciente. Transforma planilhas brutas exportadas do EPIMED 
em análises, gráficos e textos prontos para composição do relatório oficial.

---

## Fluxo de Dados
```
Planilhas EPIMED → Validação → Processamento → Visualização → IA → Relatório Word
```
---

## Estrutura de Módulos

| Arquivo | Responsabilidade |
|---|---|
| `app.py` | Interface Streamlit — orquestra os módulos |
| `utils.py` | Constantes, mapeamento de colunas e funções auxiliares |
| `processador.py` | Preparação e transformação dos dados por bloco |
| `visualizador.py` | Geração de gráficos por bloco |
| `agente_ia.py` | Triagem por IA e análises textuais via API Gemini |
| `relatorio.py` | Montagem do documento Word final |

---

## Fontes de Dados

| Planilha | Conteúdo | Blocos que alimenta |
|---|---|---|
| Notificações (principal) | Base completa de incidentes — histórico disponível | 1, 2, 3, 4, 5, 6, 8, 9 |
| Indicadores.xlsx | Taxas mensais de qualidade calculadas | 7 |

---

## Mapeamento: Blocos x Modelo Relatório

| Bloco | Título | Fonte | Status |
|---|---|---|---|
| 1 | Quantidade de Notificações | Automação | ✅ Pronto |
| 2 | Turno de Notificações | Automação | ✅ Pronto |
| 3 | Classificação das Notificações com Top 3 | Automação | ✅ Pronto |
| 4 | Eventos Adversos — Top 3, Grau do Dano, Investigação | Automação | ✅ Pronto |
| 5 | Setores Notificantes — Top 3 | Automação | ✅ Pronto |
| 6 | Setores Notificados — Top 3 | Automação | ✅ Pronto |
| 7 | Índices de Qualidade — Taxas mensais e trimestrais | Automação | ✅ Pronto |
| 7.1 | Queda — Grau do dano, tipo e local | Automação | ✅ Pronto |
| 7.2 | Erro de Medicação — Dataset para triagem IA | Automação + IA | ✅ Pronto |
| 7.3 | Flebite — Dataset para triagem IA | Automação + IA | ✅ Pronto |
| 7.4 | Lesão por Pressão — Dataset com nota do classificador | Automação + IA | ✅ Pronto |
| 8 | Cumprimento de Análises — Taxa anual e mensal | Automação | ✅ Pronto |
| 9 | Protocolos Gerenciados — AVC, Dor Torácica, Sepse, TEV | Automação + IA | ⏳ Pendente |
| 10 | Auditoria de ROPS | Manual | ⚠️ Manual |
| 11 | Comissão de Óbitos | Manual | ⚠️ Manual |
| 12 | Comissão de Prontuários | Manual | ⚠️ Manual |
| 13 | Plano de Segurança do Paciente | Manual | ⚠️ Manual |
| 14 | Interrelação e Mapeamento de Risco | Automação | ⏳ Pendente |
| 15 | Ações Táticas e Estratégicas | Manual | ⚠️ Manual |

---

## Padrões de Função no processador.py

| Padrão | Quando usar | Exemplo |
|---|---|---|
| `preparar_blocoN(df_atual, df_anterior)` | Comparação trimestral | blocos 1 a 6 |
| `preparar_blocoN(df_completo)` | Requer histórico sem filtro de trimestre | bloco 8 |
| `preparar_bloco_setores(df, df_ant, coluna)` | Função genérica reutilizável | blocos 5 e 6 |
| `preparar_bloco7(df, df_ind, indicador, trim, ano)` | Múltiplas fontes | bloco 7 |
| `preparar_dataset_ia(df)` | Dataset para triagem por IA | medicação, flebite |
| `preparar_dataset_ia_LPP(df)` | Dataset filtrado para triagem por IA | lesão por pressão |

---

## Decisões de Arquitetura

As decisões técnicas estão documentadas individualmente em `docs/decisoes/`:

- [ADR-001](decisoes/ADR-001-arquitetura-camadas.md) — Arquitetura em Camadas
- [ADR-002](decisoes/ADR-002-modularizacao.md) — Modularização do Motor de Análise
- [ADR-003](decisoes/ADR-003-mapeamento-colunas.md) — Mapeamento e Validação de Colunas

---

## Evolução Planejada

| Camada | Descrição | Status |
|---|---|---|
| 1 — Fundação | Modularização e governança | 🔄 Em andamento |
| 2 — Dados | Persistência com SQLite | ⏳ Pendente |
| 3 — Inteligência | Modelos estatísticos e agente de IA | ⏳ Pendente |