# Roadmap — Agente de Inteligência Assistencial

> Criado em 01/10/2026. Deriva de `backlog.md` (o quê) e de `estado-atual-e-erros.md` (ponto de partida).
> Este documento define **a ordem** e o **critério de pronto** de cada fase. Não tem datas: o ritmo depende do tempo disponível, e cada fase só começa quando a anterior cumpre seu critério.
> Mudanças de ordem devem ser registradas no `CHANGELOG.md`.
> **Última atualização do status:** 05/10/2026.

---

## 1. Princípios de ordenação

1. **Evitar retrabalho** pesa mais que seguir o fluxo natural do ciclo de dados.
2. **Medir antes de melhorar**: testes e avaliação existem antes das mudanças que eles protegem.
3. **Corrigir a lógica antes de mudar a fonte**: a lógica de cálculo sobrevive à troca de planilha por banco, o código de leitura não.
4. **Decidir antes de construir** quando a decisão limita o desenho (onde o texto é processado, qual é o identificador da notificação).
5. **Custo zero** em toda ferramenta escolhida.
6. **Cada fase entrega algo utilizável**, não só preparação.

## 2. Por que a ordem não é estritamente "ingestão → implantação"

O ciclo de dados é um bom mapa do **que** existe, mas a ordem de **fazer** muda por quatro razões:

- **Qualidade, segurança e documentação são transversais.** Se ficassem para o fim, tudo o que fosse construído antes teria que ser revisto. Elas viram trilhas que começam na Fase 0.
- **O sistema atual tem erros nos cálculos** (E-xx). Se a ingestão e o banco forem refeitos primeiro, os erros são carregados para o banco e para os modelos.
- **O relatório do 3º trimestre é uma entrega real** e não pode esperar a reconstrução.
- **A implantação depende de uma pessoa fora do projeto** (infraestrutura do hospital). Esperar o fim para começar significaria descobrir tarde um bloqueio que pode ser tratado em paralelo.

A lógica do seu fluxo continua valendo **dentro** das fases 2 a 5: dados, depois cálculos, depois modelos, depois IA.

## 3. Retrabalho evitado por decisão de ordem

| Decisão de ordem | Retrabalho que evita |
|---|---|
| Testes (QUA-01) **antes** das correções e antes do SQLite | Sem eles, não dá para saber se a refatoração mudou algum resultado |
| Corrigir cálculos e período (COR-02, COR-03, COR-04) na Fase 1 | Carregar seis anos de histórico com a lógica errada obrigaria recarregar tudo |
| Deixar E-14 e E-15 (leitura de planilha) para a ingestão da Fase 2 | Esse código será substituído; corrigi-lo agora é trabalho jogado fora |
| Fechar V-01 (definições de "elegível" e "tratada") antes do histórico | A definição entra no esquema do banco; mudar depois obriga a recalcular |
| Confirmar o identificador da notificação (ING-02) antes de desenhar o banco | É a chave do histórico de mudanças de status; sem ela o desenho precisa ser refeito |
| Denominador oficial (ING-01) antes dos modelos | Todas as taxas e modelos dependem dele |
| Decidir onde o texto é processado (SEG-01) antes de qualquer IA com texto livre | Determina se embeddings, RAG e classificação rodam local ou via API |
| Régua de avaliação (QUA-05, QUA-06) antes de evoluir a IA | Sem ela, não há como saber se o RAG ou o agente melhorou ou piorou |
| Caminhos e configurações fora do código (arquivo de configuração) já na Fase 2 | A implantação em outro computador não exigirá mexer no código |

## 4. Visão geral

| Horizonte | Fases |
|---|---|
| **Agora** | Fase 0 (Fundação) e Fase 1 (Relatório confiável) |
| **Próximo** | Fase 2 (Dados) e Fase 3 (Painel epidemiológico); Implantação mínima em paralelo |
| **Depois** | Fase 4 (Modelos) e Fase 5 (Agente de IA), em qualquer ordem entre si; reforço da implantação |

Trilhas transversais (começam cedo e continuam): **Qualidade**, **Segurança e LGPD**, **Documentação**, **Implantação**.

---

## 5. AGORA

### Fase 0 — Fundação (decisões, linha de base e documentação)

**Objetivo:** ter o terreno definido antes de mexer no código.

Os itens abaixo não formam uma sequência: a coluna **Status** diz onde estamos. Legenda: Pendente, Em andamento, Concluído (com data).

| Item | Descrição | Status |
|---|---|---|
| Operação do 3º trimestre | Gerar o relatório com o sistema atual seguindo os cuidados da seção 3 de `estado-atual-e-erros.md`. **Sem alterar o código antes de entregar** | Em andamento (prazo 10/10) |
| Linha de base | Marcar o estado atual no git (tag) antes de qualquer correção | Concluído (05/10): tag `baseline-pre-fase1` no commit `299ab61` |
| DOC-01 | Publicar este roadmap e o backlog | Concluído (05/10): commit `c339cfb` |
| DOC-03 | Escrever ADR-015 (estrutura documental) | Concluído (05/10): commit `4db5a82` |
| DOC-02 | Definir o versionamento (ADR própria) e iniciar o `CHANGELOG.md` | Concluído (05/10): ADR-017 e `CHANGELOG.md` |
| DOC-04 | Ligar `arquitetura.md` ao roadmap | Pendente |
| DOC-05 | Preencher a seção 4 do estado atual | Concluído (05/10): commit `132fb73` |
| COR-08 (V-01 a V-07) | Conferir com dados reais; resultado alimenta TRA-01 | Concluído (05/10): resultados em `estado-atual-e-erros.md`. Geraram os erros E-20 a E-24 |
| Confirmar no export | Identificador da notificação (ING-02) e fonte das ações definidas nas tratativas (ARM-05) | Concluído (05/10): ID confirmado (único e estável) e fonte das ações identificada: o relatório consolidado da investigação do EPIMED, que entra como segunda fonte (ING-10) |
| SEG-01 / COR-07 / DOC-06 | Decidir onde o texto é processado e registrar em ADR (conteúdo sensível fora do repositório público) | Pendente |
| IMP-02 | Investigar por que o app "desconfigura" quando acessado por outro computador. Pode ser causa simples e resolver a dor imediata | Pendente: aguarda print da tela desconfigurada, navegador e endereço usado por quem acessa |

**Critério de pronto:** relatório do 3º trimestre entregue; tag de linha de base criada; V-01 a V-07 respondidas; identificador e datas confirmados no export; ADR-015 e ADR de SEG-01 escritos; roadmap e backlog publicados.

### Fase 1 — Relatório confiável

**Objetivo:** o sistema atual passa a produzir resultados corretos, testados e reprodutíveis.

Ordem interna (sprints):

1. **Rede de segurança**: QUA-03 (logs e tratamento de erros) e QUA-01 (testes que registram o comportamento atual e depois o comportamento correto).
2. **Período e estado**: COR-02, COR-01. Período único como parâmetro (TRA-02) e definições de V-01 (TRA-01).
3. **Cálculos e gráficos**: COR-03, COR-04, COR-09 (colunas dos Gráficos 5 e 6), CAL-04 (cobertura do Modelo Relatório, tópico a tópico).
4. **Erros de execução**: E-06 e E-19 (de COR-05), COR-06. E-14 e E-15 ficam para a Fase 2.
5. **Automação da conferência**: QUA-02 e QUA-04 (integração contínua).
6. **IA atual mensurável**: IA-09 (saída estruturada), QUA-05 (verificação dos números citados), QUA-06 (casos de referência), IA-12 (revisão humana antes de aprovar).

**Critério de pronto:** testes passando na integração contínua; reprocessar não deixa resultado antigo (E-01); as análises de IA têm verificação numérica e um conjunto de referência; relatório do 4º trimestre geraria sem os cuidados manuais da seção 3.

---

## 6. PRÓXIMO

### Fase 2 — Dados: ingestão, armazenamento e histórico

**Objetivo:** os dados deixam de ser planilhas soltas e viram uma base histórica confiável.

| Bloco | Itens |
|---|---|
| Contrato e leitura | ING-05, ING-06, ING-07, ING-08, ING-09 (minimização de dados), TRA-03 (inclui E-14 e E-15), contrato de dados com severidade erro × aviso |
| Banco | ARM-01 (SQLite em camadas, ADR-001), caminhos e configuração em arquivo externo |
| Fontes | ING-01 (planilha de indicadores como denominador oficial), ING-02 (identificador), ING-10 (consolidado da investigação) |
| Histórico | ING-03 (carga desde 04/2020), ING-04 (rotina de exportação mensal e trimestral), ARM-02 (histórico de mudanças de status) |
| Derivados | ARM-03 (taxa no fechamento × atual), ARM-04 (tempo até a conclusão), ARM-05 (planos de ação ligados às notificações) |
| Operação | IMP-05 (backup do banco) |

**Pontos de decisão (ADR):** modelo de histórico (como guardar a mudança de status), estrutura dos esquemas por camada, política de recarga.

**Critério de pronto:** o relatório trimestral é gerado a partir do banco com resultado idêntico ao da Fase 1 (os testes provam); uma notificação que mudou de status mostra a história; rotina mensal de carga documentada e repetível.

### Fase 3 — Painel epidemiológico e modelos descritivos

**Objetivo:** a aba 2 do app passa a existir, com taxa correta e sinal separado de ruído.

| Bloco | Itens |
|---|---|
| Cálculos | CAL-01 (taxa por pacientes-dia), CAL-02 (razão das somas, já decidida como valor oficial) com COR-10, CAL-03 (variação com incerteza) |
| Descrever | MOD-01 (tendência, sazonalidade, correlação) |
| Sinal × ruído | MOD-02 (cartas de controle, funnel plot, aumento anormal) |
| Produto | MOD-07 (painel) |

**Critério de pronto:** o painel mostra taxas de incidência com limites de controle por indicador; cada alerta tem explicação do critério usado.

### Implantação mínima (trilha paralela)

**Objetivo:** o app deixa de depender do computador do desenvolvedor.

| Item | Descrição |
|---|---|
| IMP-01, IMP-03 | Servidor sempre ligado na rede do hospital (ADR-013) e empacotamento (Docker) |
| IMP-04 | Controle de acesso básico |

**Dependência externa:** infraestrutura e autorização do hospital. É um risco do projeto: se a resposta demorar, a trilha espera e o restante segue.

---

## 7. DEPOIS

As Fases 4 e 5 dependem da Fase 3 e são independentes entre si, exceto por IA-01 (precisa de MOD-02). A ordem entre elas pode seguir o seu interesse de aprendizado.

### Fase 4 — Modelos explicativos, preditivos e causais

| Bloco | Itens |
|---|---|
| Explicar | MOD-03 (regressão logística, modelos de contagem, risco por setor, NPR) |
| Prever | MOD-04 (média móvel, suavização exponencial, Prophet) |
| Causal | MOD-05 (série temporal interrompida, diferenças em diferenças) |
| Revisão | MOD-06 (outros métodos que os dados reais permitirem) |

**Critério de pronto:** cada modelo tem pressupostos verificados, validação (no caso da previsão, contra o histórico) e uma frase clara sobre o que **não** se pode concluir com ele.

### Fase 5 — Agente de IA

Subetapas (cada uma entregável sozinha):

| Subetapa | Itens |
|---|---|
| 5.1 Segurança do texto | SEG-02 (anonimização), SEG-03 (injeção de prompt), SEG-04 (log de auditoria). **Antes de qualquer item com texto livre** |
| 5.2 Contexto histórico | IA-01 |
| 5.3 Embeddings e busca semântica | IA-05, IA-08 (duplicatas), IA-06 (temas) |
| 5.4 RAG local | IA-02; IA-13 (montar na mão, depois comparar com framework); QUA-11 |
| 5.5 Classificação estruturada | IA-07, com contagem feita pelo código |
| 5.6 Modelo local e roteamento | IA-10, IA-11 (se o modelo local já foi decidido em SEG-01, esta subetapa sobe para antes de 5.3) |
| 5.7 Observabilidade de LLM | QUA-09, QUA-07 (drift), QUA-08 (sinais de uso), QUA-10 (LLM como juiz) |
| 5.8 Agente | IA-03 (ferramentas), IA-04 (conversacional, aba 3) |

**Critério de pronto:** toda técnica nova tem sua métrica de avaliação rodando contra o conjunto de referência da Fase 1; o agente só chama ferramentas controladas e não executa consulta livre.

### Horizonte futuro (fora do roadmap atual)

Registrado para não se perder: depois da subetapa 5.8 existe espaço para evoluir.

| Item | Descrição | Pré-requisitos |
|---|---|---|
| IA-14 | Agente proativo (nível 4): disparado por evento (nova carga mensal, alerta de carta de controle), investiga sozinho com as ferramentas já existentes e deixa um rascunho de alerta para revisão humana. Começa só com ações de leitura | IA-03, ING-04, QUA-09, QUA-06 (avaliação do percurso, não só da resposta final), SEG-03 |

Só entra em planejamento quando a subetapa 5.8 estiver medida e confiável.

### Reforço da implantação

IMP-05 completo (rotina de backup testada), monitoramento do servidor e atualização controlada de versões.

---

## 8. Pontos de decisão (ADRs a escrever)

| ADR | Tema | Quando |
|---|---|---|
| 015 | Estrutura da documentação (roadmap, backlog, changelog, ADRs) | Fase 0 |
| 016 | Onde o texto das notificações é processado (API × local). Conteúdo sensível fora do repositório público | Fase 0 |
| a numerar | Versionamento e CHANGELOG | Fase 0 |
| a numerar | Modelo de histórico e esquemas do banco | Fase 2 |
| a numerar | Banco de vetores (ChromaDB, FAISS ou extensão do SQLite) | Fase 5 |

## 9. Riscos e premissas

- **Prazo do próximo relatório** não está definido neste documento. Se houver urgência, a Fase 1 pode ser fatiada e entregue por sprints.
- **Infraestrutura do hospital**: a implantação depende de aprovação e de uma máquina disponível.
- **Hardware para modelo local**: o item IA-10 só se confirma depois de testar o que a máquina disponível suporta.
- **Tempo do desenvolvedor**: o roadmap assume um único desenvolvedor, que também está estudando. As fases foram desenhadas para entregar valor mesmo se pausadas no meio.
- **Dados reais**: as premissas sobre o export (identificador, datas) ainda estão por confirmar na Fase 0 e podem alterar a Fase 2.