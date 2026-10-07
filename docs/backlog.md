# Backlog — Agente de Inteligência Assistencial

> Criado em 01/10/2026 a partir da discussão de melhorias por etapa do ciclo de vida dos dados.
> Este documento **lista** o que pode ser feito. Ele **não define prioridade nem ordem**: isso é papel do `roadmap.md` (Agora / Próximo / Depois).
> Os detalhes de cada item serão discutidos na fase em que ele entrar.
> Correções de erros estão em `estado-atual-e-erros.md` (IDs E-xx e V-xx) e aqui aparecem agrupadas em pacotes.

## Como ler

- **ID**: etapa + número (ex.: ARM-02). Não muda ao longo do tempo.
- **Origem**: `D` = discussão de 01/10/2026; `E-xx` / `V-xx` = documento de estado e erros; `Fase n` = roadmap original de 5 fases.
- **Depende de**: itens que precisam existir antes.

---

## 1. Correções (pacotes de erros conhecidos)

Detalhes e evidências em `estado-atual-e-erros.md`.

| ID | Pacote | Erros incluídos | Observação |
|---|---|---|---|
| COR-01 | Estado da sessão e reprocessamento | E-01, E-13 | Resultados antigos persistem ao reprocessar; figuras nunca fechadas |
| COR-02 | Período único e comparações | E-02, E-04, E-07 | Trimestre e ano vêm de fontes diferentes; ambiguidade de "trimestre anterior"; datas inválidas somem |
| COR-03 | Cálculos e gráficos | E-05, E-09, E-10, E-11, E-12, E-23, E-24 | Gráfico 1, base zero, top-3 independentes, metas ignoradas, gráfico do bloco 8 desenhado dentro do laço mensal, rótulo do eixo Y do bloco 7, trimestre sem tratadas no bloco 8 |
| COR-04 | Análise de queda | E-03 | Entrada errada para a análise de queda (tabela mensal no lugar do conjunto de dados) |
| COR-05 | Robustez e erros | E-06, E-14, E-15, E-19 | Falha da API vira "análise"; colunas opcionais obrigatórias; leitura direta da planilha; traceback exposto |
| COR-06 | Higiene de código | E-16, E-17, E-18 | Prompts, caminho morto, funções sem uso |
| COR-07 | Privacidade do envio à API | E-08 | Revisão pendente. Detalhes mantidos fora do repositório. Exige ADR |
| COR-08 | Verificações com dados reais | V-01 a V-07 | **Concluídas em 05/10/2026.** Resultados em `estado-atual-e-erros.md` |
| COR-09 | Colunas dos Gráficos 5 e 6 | E-20, E-21 | Gráfico 5 deve agrupar por Setor notificante e o 6 por Setor Responsável. Correção pequena |
| COR-10 | Valor trimestral dos indicadores | E-22 | Soma dos eventos sobre soma dos pacientes-dia. Só é possível com ING-01 e CAL-01 |

---

## 2. Ingestão

| ID | Item | Origem | Depende de |
|---|---|---|---|
| ING-01 | Planilha de indicadores (pacientes-dia e internações) como **fonte oficial do denominador** | D | — |
| ING-02 | Identificador estável da notificação na exportação do EPIMED. **Confirmado em 05/10/2026:** coluna `ID`, única em cada exportação e a mesma em todas as exportações. Serve de chave do histórico | D | — |
| ING-03 | Carga inicial do histórico (desde 04/2020) | D, Fase 2 | ING-02, ARM-01 |
| ING-04 | Rotina de exportação mensal e trimestral recorrente | D | ING-02 |
| ING-05 | Contrato de dados e validação em níveis (estrutura, tipo/nulos, domínio), com severidade (erro × aviso) | D, E-07, E-14 | — |
| ING-06 | Leitura de planilha por nome da aba e colunas configuráveis | E-14, E-15 | ING-05 |
| ING-07 | Glossário dos status do EPIMED, validação de consistência (status "Concluído sem necessidade de investigação" ou "Concluída – Outra natureza" com unidade responsável preenchida gera aviso) e alerta de status novo ou com grafia diferente | V-01 | ING-05 |
| ING-08 | Janela de 2 anos (atual e anterior) como parâmetro explícito, com aviso quando o export tiver outro número de anos | V-05 | ING-05 |
| ING-09 | Minimização de dados: descartar na ingestão as colunas com identificadores diretos do paciente e as que o sistema não usa, antes de qualquer armazenamento | D (conferência do export) | ING-05, SEG-01 |
| ING-10 | **Segunda fonte:** relatório consolidado da investigação do EPIMED (plano de ação, fatores contribuintes, Protocolo de Londres, força da intervenção RCA², efetividade). **Granularidade verificada em 05/10/2026:** o ID se repete, com uma linha por fator contribuinte (exemplo com 4 linhas para o mesmo ID, repetindo os campos da investigação). Repetição também por ação do plano: a confirmar. Contar linhas não conta notificações, e a Fase 2 precisa separar a investigação, os fatores e as ações. O texto livre de fatores e comentários traz informação sensível (condição do paciente e conduta de profissionais) e exige anonimização antes de qualquer envio externo (SEG-02). Pode alimentar também a seção 11 do Modelo, hoje não coberta | D | ING-02, ING-09 |

## 3. Armazenamento

| ID | Item | Origem | Depende de |
|---|---|---|---|
| ARM-01 | SQLite com camadas raw / tratada / consolidada (ADR-001) | Fase 2 | ING-02 |
| ARM-02 | Histórico de mudanças por notificação (o status muda meses depois) | D | ARM-01, ING-02 |
| ARM-03 | Taxa "no fechamento do trimestre" × taxa "atual" | D | ARM-02 |
| ARM-04 | Indicador de tempo até a conclusão da notificação e de cada etapa da tratativa (as colunas Encaminhada, Em andamento, Elaborada, Aprovada e Finalizada de cada ferramenta são datas). Ressalva: fechamento em lote (várias etapas na mesma data) pode distorcer o tempo | D | ARM-02 |
| ARM-05 | **Resolvido em 05/10/2026:** as intervenções para a inferência causal são as **ações definidas pelos gestores nas tratativas** de qualquer notificação. A fonte existe: o relatório **consolidado da investigação** do EPIMED traz, ligados ao ID, o plano de ação (descrição, responsável, data inicial, prazo, novo prazo, data de conclusão, progresso), a força da intervenção (RCA²) e a Escala de Efetividade. Falta carregá-lo (ING-10) e relacioná-lo às notificações. O acompanhamento ao fim do relatório (fechamento da reunião de análise, sem datas nem identificador) é um registro separado, útil como insumo do RAG (IA-02) | D | ING-10 |

## 4. Tratamento

| ID | Item | Origem | Depende de |
|---|---|---|---|
| TRA-01 | Definições únicas de "elegível" e "tratada" | V-01 | COR-08 |
| TRA-02 | Período do relatório como parâmetro único, nunca inferido | E-02, E-07 | COR-02 |
| TRA-03 | Tratamento de colunas opcionais e valores ausentes | E-14 | ING-05 |

## 5. Cálculos

| ID | Item | Origem | Depende de |
|---|---|---|---|
| CAL-01 | Taxa de incidência com pacientes-dia (por 1.000) | D | ING-01 |
| CAL-02 | Razão das somas × média das taxas mensais. **Decidido em 05/10/2026:** o valor oficial é a razão das somas. Implementar e documentar (junto com COR-10) | V-03 | CAL-01 |
| CAL-03 | Variação com incerteza (não só diferença percentual) | D | CAL-01 |
| CAL-04 | Cobertura do "Modelo Relatório": conferir tópico a tópico | Projeto | — |

## 6. Modelos estatísticos e epidemiológicos

| ID | Item | Origem | Depende de |
|---|---|---|---|
| MOD-01 | **Descrever**: tendência, sazonalidade (decomposição), correlação entre indicadores, taxas | D | ARM-01, CAL-01 |
| MOD-02 | **Separar sinal de ruído**: cartas de controle (CEP, gráficos c/u), funnel plot por setor, detecção de aumento anormal | D | MOD-01 |
| MOD-03 | **Explicar fatores**: regressão logística (dano grave), modelos de contagem (Poisson / binomial negativa), risco por setor, NPR | D | MOD-01 |
| MOD-04 | **Prever**: média móvel, suavização exponencial, Prophet | D, Fase 4 | MOD-01 |
| MOD-05 | **Inferência causal**: série temporal interrompida, diferenças em diferenças, para avaliar as ações definidas nas tratativas | D | ARM-05, ING-10, MOD-01 |
| MOD-06 | Revisar com os dados reais se cabem outros métodos. Candidatos vistos no export em 05/10/2026: análise de tempo até o evento (prazo e conclusão das tratativas), análise do fluxo das etapas da investigação, uso da matriz de prioridade do EPIMED (probabilidade, gravidade, grau de prioridade) e da Escala de Efetividade, idade e sexo como covariáveis nos modelos de fatores. Do consolidado da investigação: força da intervenção (RCA²) como intensidade da ação, fatores contribuintes, completude do Protocolo de Londres e atraso ou reprogramação de prazos (prazo × novo prazo) | D | Fase de construção |
| MOD-07 | Painel epidemiológico (aba 2 do app) | Fase 3 | MOD-01, MOD-02 |

## 7. Agente de IA

| ID | Item | Origem | Depende de |
|---|---|---|---|
| IA-01 | **Contexto histórico**: Gemini recebe trimestres anteriores e resultados dos modelos | D | ARM-01, MOD-02 |
| IA-02 | **RAG local** sobre análises e relatórios anteriores e, depois, sobre planos de ação e fatores contribuintes (permite perguntar que ações já foram tomadas para eventos parecidos e como foram avaliadas) | D | ARM-01, IA-05, ING-10 |
| IA-03 | **Agente com ferramentas** (funções controladas, sem SQL livre) | D | IA-01, SEG-03 |
| IA-04 | **Agente conversacional** (aba 3 do app) | D, Fase 5 | IA-02, IA-03 |
| IA-05 | Embeddings e busca semântica (sentence-transformers; ChromaDB, FAISS ou extensão do SQLite) | D | ARM-01 |
| IA-06 | Agrupamento de temas nos textos (BERTopic) | D | IA-05 |
| IA-07 | Classificação estruturada pelo LLM, com **contagem feita pelo código** | D | QUA-06 |
| IA-08 | Detecção de duplicatas e eventos repetidos | D | IA-05 |
| IA-09 | Saída estruturada (Pydantic) | D | — |
| IA-10 | Modelo local (Ollama com Gemma, Llama ou Qwen) | D | SEG-01 |
| IA-11 | Roteamento de modelos (leve × forte) | D | QUA-09 |
| IA-12 | Revisão humana antes de entrar no relatório, registrando o que foi editado | D | — |
| IA-13 | Trilha de aprendizado: montar o RAG na mão, depois refazer com framework e comparar (LangChain, LangGraph, LlamaIndex) | D | IA-02 |
| IA-14 | **Agente proativo (nível 4)**: disparado por evento (nova carga, alerta de CEP), investiga e deixa rascunho para revisão humana. **Horizonte futuro, fora do roadmap atual** | D | IA-03, ING-04, QUA-09, QUA-06 (avaliação do percurso), SEG-03 |

## 8. Qualidade, monitoramento e observabilidade

| ID | Item | Origem | Depende de |
|---|---|---|---|
| QUA-01 | Testes automatizados das funções de cálculo | D | COR-01 a COR-06 |
| QUA-02 | Conferência automática entre números do relatório e planilhas de origem | D | QUA-01 |
| QUA-03 | Logs estruturados e tratamento de erros (substitui print e traceback ao usuário) | D, E-19 | — |
| QUA-04 | Integração contínua gratuita (GitHub Actions) rodando os testes a cada push | D | QUA-01 |
| QUA-05 | Verificação das afirmações do LLM contra as tabelas (números, setores, períodos) | D | IA-09 |
| QUA-06 | Conjunto de casos de referência para avaliação | D | — |
| QUA-07 | Monitorar drift de entrada (distribuição das notificações) e de saída (medidas do texto), com distância de Wasserstein | D | ARM-01, QUA-06 |
| QUA-08 | Sinais de uso: taxa de edição humana, regerações, respostas fora do formato, tokens | D | IA-12 |
| QUA-09 | Observabilidade de LLM (Langfuse ou MLflow): prompts, custo, latência, versões | D | QUA-03 |
| QUA-10 | LLM como juiz, apenas como complemento | D | QUA-06 |
| QUA-11 | Métricas de avaliação de RAG (Ragas, promptfoo) | D | IA-02, QUA-06 |

## 9. Segurança e LGPD

| ID | Item | Origem | Depende de |
|---|---|---|---|
| SEG-01 | Decisão arquitetural sobre onde o texto das notificações é processado (API externa × local) → **ADR**. **Decidido em 07/10/2026 (ADR-016):** ponto de partida = API externa com anonimização e registro do que é enviado; alvo = híbrido (só dados agregados vão à API e o texto livre fica em modelo local) | D, COR-07 | — |
| SEG-02 | Anonimização antes de qualquer envio externo (Presidio ou spaCy pt) | D | SEG-01 |
| SEG-03 | Defesa contra injeção de prompt (texto livre das notificações no prompt) | D | — |
| SEG-04 | Log de auditoria do que sai para APIs externas | D | QUA-03 |

## 10. Implantação

Discutida em fase própria. Registrado agora apenas o que surgiu.

| ID | Item | Origem | Depende de |
|---|---|---|---|
| IMP-01 | Disponibilizar o app sem depender do computador do desenvolvedor (servidor sempre ligado na rede do hospital, ADR-013) | D | — |
| IMP-02 | Investigar por que o app "fica desconfigurado" quando acessado por outro computador via localhost | D | — |
| IMP-03 | Empacotamento (Docker) | D | IMP-01 |
| IMP-04 | Controle de acesso | D | IMP-01 |
| IMP-05 | Backup do banco | D | ARM-01 |

## 11. Documentação

| ID | Item | Origem | Depende de |
|---|---|---|---|
| DOC-01 | `docs/roadmap.md` | D | Este backlog |
| DOC-02 | `CHANGELOG.md` e definição de versionamento | D | — |
| DOC-03 | ADR-015: estrutura da documentação (roadmap, backlog, changelog, ADRs) | D | — |
| DOC-04 | Atualizar `arquitetura.md` (trocar "Evolução Planejada" por link ao roadmap) | D | DOC-01 |
| DOC-05 | Preencher a seção 4 de `estado-atual-e-erros.md` com este backlog | D | — |
| DOC-06 | ADR para SEG-01 (privado se necessário; o repositório é público) | D | SEG-01 |

---

## Dependências estruturais

1. **Fase 2 (armazenamento)** destrava quase tudo: ARM-01 e ING-02 antecedem histórico, modelos, RAG e agente.
2. **Correções (COR)** antecedem os testes (QUA-01) e qualquer análise nova, porque os cálculos precisam estar certos antes de modelar sobre eles.
3. **ING-01** (denominador) antecede as taxas e, portanto, todos os modelos.
4. **SEG-01** (onde processar o texto) antecede o uso de texto livre em IA-02, IA-06, IA-07 e IA-10.
5. **QUA-06** (casos de referência) antecede a avaliação de qualquer técnica de IA.

## Pendências do usuário (não são itens de desenvolvimento)

- Verificar V-01 a V-07 com dados reais.
- Confirmar no export: identificador da notificação (ING-02) e datas das intervenções (ARM-05).
- Cuidados do relatório do 3º trimestre, conforme a seção 3 de `estado-atual-e-erros.md`.