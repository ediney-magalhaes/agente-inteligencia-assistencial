# Arquitetura do Sistema

**Projeto:** Agente de Análise - Segurança do Paciente  
**Autor:** Ediney Magalhães  
**Última atualização:** 29/04/2026

---

## Visão Geral

Sistema de automação analítica para geração do Relatório Trimestral de 
Segurança do Paciente. Transforma planilhas brutas exportadas do EPIMED 
em análises, gráficos e textos prontos para composição do relatório oficial.

---

## Fluxo de Dados
```
CAMADA DE INTERFACE
    app.py (Streamlit) — uploads e configuração
        ↓
CAMADA DE ORQUESTRAÇÃO
    resultados.py — conecta processamento e exibição
        ↓
CAMADA DE PROCESSAMENTO
    processador.py → cálculos e transformações
    visualizador.py → geração de gráficos
    agente_ia.py → narrativas e triagem via LLM
        ↓
CAMADA DE DADOS
    Planilhas EPIMED (entrada atual)
    SQLite → histórico acumulado por trimestre (Fase 2)
        ↓
CAMADA DE SAÍDA
    Interface Streamlit — resultados por seção
    Painel Epidemiológico (Fase 3)
    Agente de Análise — chat com os dados (Fase 5)
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
| `resultados.py` | Exibição dos resultados por seção na interface Streamlit |

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
| 2 | Turno de Notificações | Manual | ⚠️ Manual |
| 3 | Classificação das Notificações com Top 3 | Automação | ✅ Pronto |
| 4.1 | Eventos Adversos — Top 3 | Automação | ✅ Pronto |
| 4.2 | Eventos Adversos por Grau do Dano | Manual | ⚠️ Manual |
| 5 | Setores Notificantes — Top 3 | Manual | ⚠️ Manual |
| 6 | Setores Notificados — Top 3 | Manual | ⚠️ Manual |
| 7 | Índices de Qualidade — Comparativo trimestral | Automação | ✅ Pronto |
| 7.1 | Queda | Automação | ✅ Pronto |
| 7.2 | Erro de Medicação | Automação + IA | ✅ Pronto |
| 7.3 | Flebite | Automação + IA | ✅ Pronto |
| 7.4 | Lesão por Pressão | Automação + IA | ✅ Pronto |
| 8 | Cumprimento de Análises | Automação | ✅ Pronto |
| 9 | Protocolos Gerenciados — AVC, Dor Torácica, Sepse, TEV | Automação + IA | ✅ Pronto |
| 10 | Auditoria de ROPS | Manual | ⚠️ Manual |
| 11 | Comissão de Óbitos | Manual | ⚠️ Manual |
| 12 | Comissão de Prontuários | Manual | ⚠️ Manual |
| 13 | Plano de Segurança do Paciente | Manual | ⚠️ Manual |
| 14 | Interrelação e Mapeamento de Risco | Automação + IA | ✅ Pronto |
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
- [ADR-004](decisoes/ADR-004-funcao-generica-setores.md) — Função Genérica para Análise por Setor
- [ADR-005](decisoes/ADR-005-triagem-ia-indicadores.md) — Triagem por IA para Indicadores sem Filtro Determinístico
- [ADR-006](decisoes/ADR-006-grafico-top3-generico.md) — Função Genérica para Gráficos Top 3 por Classificação
- [ADR-007](decisoes/ADR-007-grafico-bloco7-duplo.md) — Estratégia de Visualização do Bloco 7 — Indicadores de Qualidade
- [ADR-008](decisoes/ADR-008-gerador-relatorio.md) — Gerador de Relatório 
- [ADR-009](decisoes/ADR-009-interface-streamlit.md) — Interface Streamlit e ordem de desenvolvimento
- [ADR-010](decisoes/ADR-010-integracao-gemini-api.md) — Integração com Gemini API e Gerenciamento de Segredos
- [ADR-011](decisoes/ADR-011-execucao-sob-demanda-ia.md) — Execução sob Demanda das Análises de IA
- [ADR-012](decisoes/ADR-012-modulo-resultados.md) — Módulo de Exibição de Resultados
- [ADR-013](decisoes/ADR-013-deploy-rede-local.md) — Deploy em Rede Local
- [ADR-014](decisoes/ADR-014-simplificacao-interface.md) — Simplificação da Interface
---

## Evolução Planejada

| Fase | Descrição | Status |
|---|---|---|
| 1 — Relatório automatizado | Interface Streamlit + gerador.py + documento Word final | 🔄 Em andamento — app.py completo, gerador.py com fluxo validado, estrutura do Word pendente |
| 2 — Banco de dados | SQLite para histórico acumulado por trimestre | ⏳ Pendente |
| 3 — Painel epidemiológico | Tendência temporal, sazonalidade, correlações, CEP | ⏳ Pendente |
| 4 — Modelos preditivos | Previsão de volume, risco por setor | ⏳ Pendente |
| 5 — Agente de IA | Chat com os dados, narrativas automáticas, alertas | ⏳ Pendente |