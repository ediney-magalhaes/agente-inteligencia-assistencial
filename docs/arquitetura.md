# Arquitetura do Sistema

**Projeto:** Agente de Análise - Segurança do Paciente  
**Autor:** Ediney Magalhães  
**Última atualização:** 17/04/2026

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
| `agente_ia.py` | Análises textuais via API Gemini |
| `relatorio.py` | Montagem do documento Word final |

---

## Fontes de Dados

| Planilha | Conteúdo | Blocos que alimenta |
|---|---|---|
| Notificações (principal) | Base completa de incidentes | 1 a 5, 9, 10, 11, 15 |
| tabela_setores.xlsx | Classificação dos setores | 6, 7, 8 |
| indicadores.xlsx | Índices históricos de qualidade | 8 |

---

## Mapeamento: Blocos x Modelo Relatório

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
| 10 | Auditoria de ROPS | ⚠️ MANUAL |
| 11 | Protocolos Gerenciados | Automação |
| 12 | Comissão de Óbitos | ⚠️ MANUAL |
| 13 | Comissão de Prontuários | ⚠️ MANUAL |
| 14 | Plano de Segurança do Paciente | ⚠️ MANUAL |
| 15 | Interrelação e Mapeamento de Risco | Automação |
| 16 | Ações Táticas e Estratégicas | ⚠️ MANUAL |

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