# Roadmap — Agente de Inteligência Assistencial

> Criado em 01/10/2026. Deriva de `backlog.md` (o quê) e de `estado-atual-e-erros.md` (ponto de partida).
> Este documento define **a ordem** e o **critério de pronto** de cada fase. Não tem datas: o ritmo depende do tempo disponível, e cada fase só começa quando a anterior cumpre seu critério.
> Mudanças de ordem devem ser registradas no `CHANGELOG.md`.
> **Reescrito em 08/10/2026** (Fase 1 reorganizada por componente; implantação em nuvem). **Última atualização do status:** 08/10/2026.

---

## 1. Princípios de ordenação

1. **Evitar retrabalho** pesa mais que seguir o fluxo natural do ciclo de dados.
2. **Medir antes de melhorar**: testes e avaliação existem antes das mudanças que eles protegem.
3. **Corrigir a lógica antes de mudar a fonte**: a lógica de cálculo sobrevive à troca de planilha por banco, o código de leitura não.
4. **Decidir antes de construir** quando a decisão limita o desenho (onde o texto é processado, onde o app roda, qual é o identificador da notificação).
5. **Custo zero** em toda ferramenta escolhida.
6. **Cada fase entrega algo utilizável**, não só preparação.
7. **Um arquivo de código é revisado em um único bloco.** Um item que atravessa componentes fecha no último bloco que ele toca. Assim nenhum arquivo é aberto duas vezes para o mesmo assunto. A única exceção é o Bloco 1, que toca os dois pontos únicos de entrada e saída de dados (a leitura e a função `chamar_gemini`) porque a privacidade precisa existir antes de tudo.
8. **Cada correção nasce com o teste do valor correto, no mesmo commit.** Não há teste que registre o comportamento errado para depois trocá-lo.
9. **O que sai do hospital é decidido antes de tudo.** A privacidade vem antes das correções de cálculo, porque define como são os dados que entram em todos os componentes.
10. **Documentos são atualizados uma vez, ao fim de cada bloco**, e não a cada commit.

## 2. Por que a ordem não é estritamente "ingestão → implantação"

O ciclo de dados é um bom mapa do **que** existe, mas a ordem de **fazer** muda por quatro razões:

- **Qualidade, segurança e documentação são transversais.** Se ficassem para o fim, tudo o que fosse construído antes teria que ser revisto. Elas viram trilhas que começam na Fase 0.
- **O sistema atual tem erros nos cálculos** (E-xx). Se a ingestão e o banco forem refeitos primeiro, os erros são carregados para o banco e para os modelos.
- **O relatório do 3º trimestre é uma entrega real** e não pode esperar a reconstrução.
- **A implantação depende de conta, faturamento e decisão de LGPD**, que ficam fora do código. Esperar o fim para começar significaria descobrir tarde um bloqueio que pode ser tratado em paralelo.

A lógica do fluxo de dados continua valendo **dentro** das fases 2 a 5: dados, depois cálculos, depois modelos, depois IA. Dentro da Fase 1, a ordem segue o caminho do dado pelos arquivos: privacidade, depois `processador.py`, depois `visualizador.py`, depois `agente_ia.py`, depois `app.py` e `resultados.py`.

## 3. Retrabalho evitado por decisão de ordem

| Decisão de ordem | Retrabalho que evita |
|---|---|
| Anonimização e minimização (Bloco 1) **antes** de qualquer correção | Todo teste, prompt e log escrito depois já nasce com a forma final dos dados que chegam à IA |
| Teste do valor correto no mesmo commit da correção | Evita escrever um teste que registra o erro e depois reescrevê-lo |
| Integração contínua (QUA-04) como primeiro item da Fase 1 | Todo teste novo já roda a cada push desde o primeiro |
| Pacientes-dia lidos da planilha de indicadores na Fase 1 (E-22) | A lógica da taxa oficial (razão das somas) fica pronta e testada; na Fase 2 só muda a origem do dado |
| Arquivo de configuração (IMP-06) já na Fase 1 | Nome do hospital, metas e nomes de aba não ficam fixos no código para serem trocados depois; a nuvem lê a mesma configuração |
| Corrigir cálculos e período (COR-02, COR-03, COR-04) na Fase 1 | Carregar seis anos de histórico com a lógica errada obrigaria recarregar tudo |
| Deixar E-14 (colunas opcionais) para a ingestão da Fase 2 | Esse código será substituído; corrigi-lo agora é trabalho jogado fora |
| Fechar V-01 (definições de "elegível" e "tratada") antes do histórico | A definição entra no esquema do banco; mudar depois obriga a recalcular |
| Confirmar o identificador da notificação (ING-02) antes de desenhar o banco | É a chave do histórico de mudanças de status |
| Decidir o armazenamento persistente na nuvem antes do SQLite (Fase 2) | O disco do Cloud Run é temporário; um banco em arquivo local se perderia a cada reinício |
| Régua de avaliação (QUA-05, QUA-06) antes de evoluir a IA | Sem ela, não há como saber se o RAG ou o agente melhorou ou piorou |
| Nada vai para a nuvem antes do Bloco 1 e do IMP-06 | A planilha bruta e a chamada ao Gemini passariam a existir fora do hospital sem a proteção |

## 4. Visão geral

| Horizonte | Fases |
|---|---|
| **Agora** | Fase 0 (Fundação) e Fase 1 (Relatório confiável) |
| **Próximo** | Fase 2 (Dados) e Fase 3 (Painel epidemiológico); Implantação em nuvem em paralelo |
| **Depois** | Fase 4 (Modelos) e Fase 5 (Agente de IA), em qualquer ordem entre si; reforço da implantação |

Trilhas transversais (começam cedo e continuam): **Qualidade**, **Segurança e LGPD**, **Documentação**, **Implantação**.

---

## 5. AGORA

### Fase 0 — Fundação (decisões, linha de base e documentação)

**Objetivo:** ter o terreno definido antes de mexer no código.

Os itens abaixo não formam uma sequência: a coluna **Status** diz onde estamos. Legenda: Pendente, Em andamento, Concluído (com data).

| Item | Descrição | Status |
|---|---|---|
| Operação do 3º trimestre | Gerar o relatório com o sistema atual seguindo os cuidados da seção 3 de `estado-atual-e-erros.md`. **Sem alterar o código antes de entregar** | Em andamento (prazo 10/10). Roda em paralelo à Fase 1, executado no computador local como hoje, e **deve usar o código da tag `baseline-pre-fase1`**, nunca o da branch `desenvolvimento` |
| Linha de base | Marcar o estado atual no git (tag) antes de qualquer correção | Concluído (05/10): tag `baseline-pre-fase1` no commit `299ab61` |
| DOC-01 | Publicar este roadmap e o backlog | Concluído (05/10): commit `c339cfb`. Reescrito em 08/10 |
| DOC-03 | Escrever ADR-015 (estrutura documental) | Concluído (05/10): commit `4db5a82` |
| DOC-02 | Definir o versionamento (ADR própria) e iniciar o `CHANGELOG.md` | Concluído (05/10): ADR-017 e `CHANGELOG.md` |
| DOC-04 | Ligar `arquitetura.md` ao roadmap | Concluído (07/10) |
| DOC-05 | Preencher a seção 4 do estado atual | Concluído (05/10): commit `132fb73` |
| COR-08 (V-01 a V-07) | Conferir com dados reais; resultado alimenta TRA-01 | Concluído (05/10): resultados em `estado-atual-e-erros.md`. Geraram os erros E-20 a E-24 |
| Confirmar no export | Identificador da notificação (ING-02) e fonte das ações definidas nas tratativas (ARM-05) | Concluído (05/10): ID confirmado (único e estável) e fonte das ações identificada: o relatório consolidado da investigação do EPIMED, que entra como segunda fonte (ING-10) |
| SEG-01 / COR-07 / DOC-06 | Decidir onde o texto é processado e registrar em ADR (conteúdo sensível fora do repositório público) | Concluído (07/10): ADR-016 aprovada (ponto de partida: API externa com anonimização e registro; alvo: híbrido) |
| IMP-02 | Investigar por que o app "desconfigura" quando acessado por outro computador | Substituído (08/10) pela implantação em nuvem (IMP-01). O acesso via `localhost` de outro computador deixa de existir |

**Situação em 08/10/2026:** a Fase 0 foi encerrada por ora. Fica em aberto apenas a operação do 3º trimestre (prazo 10/10, em paralelo). A Fase 1 começa sem esperar por ela, desde que o relatório use a tag de linha de base.

**Critério de pronto:** relatório do 3º trimestre entregue; tag de linha de base criada; V-01 a V-07 respondidas; identificador e datas confirmados no export; ADR-015 e ADR de SEG-01 escritos; roadmap e backlog publicados.

### Fase 1 — Relatório confiável

**Objetivo:** o sistema atual passa a produzir resultados corretos, testados, reprodutíveis e sem enviar dado identificável para fora.

**Regras de trabalho:** a ordem segue o caminho do dado pelos arquivos (princípio 7); cada correção entra com o teste do valor correto no mesmo commit (princípio 8); os documentos são atualizados uma vez ao fim de cada bloco (princípio 10).

#### Etapa A — Definições (sem código)

Status: **Concluído (08/10)**. Decisões que valem para todos os blocos:

| Decisão | Efeito |
|---|---|
| O Modelo Relatório (17/04/2026) é a única versão e a referência | A cobertura está na seção 1.4 de `estado-atual-e-erros.md` |
| Os tópicos do Modelo sem entrada de dados deste projeto (Objetivo, Definições, 4, 6, 7, 9 e 12) vêm de fontes externas ou são texto fixo | Ficam fora do escopo. A seção 11 será alimentada na Fase 2 (ING-10). As seções 5 e 10 seguem o formato do Modelo (CAL-06) |
| Gráfico 3 compara o trimestre atual com o **mesmo trimestre do ano anterior** | Muda o dado no `processador.py` (E-04); no `visualizador.py` muda só a coluna lida |
| O gráfico mostra os dois comparativos (trimestre anterior e ano anterior) e a análise de IA **não é ancorada em um só** | A IA recebe todos os dados relevantes, rotulados. O código calcula apenas os números exatos (contagens e taxas) |
| Gráficos e tabelas seguem o Modelo e já existem | Ajustes são só de formato e legenda. Exceção: os dados do Gráfico 3 |
| Pacientes-dia ficam na coluna `Paciente-dia` da planilha de indicadores (01/2021 a 06/2026), consultada no sistema e acrescentada mês a mês por quem opera | Permite corrigir o E-22 na Fase 1 |
| Números absolutos de eventos vêm da planilha de notificações, contados pelo código | Necessários ao Gráfico 7 (CAL-05) |
| A anonimização abre a Fase 1 | Bloco 1 |
| O app vai para a nuvem (Cloud Run), com login por conta Google corporativa como única barreira | Trilha de implantação (seção 6). ADR-013 será substituída |

#### Bloco 1 — Privacidade e integração contínua

Arquivos: módulo novo de anonimização, `agente_ia.py` (somente a função `chamar_gemini`, ponto único de saída), leitura em `processador.py` (só a lista de colunas descartadas), `.github/workflows`.

| Ordem | Item | Descrição | Status |
|---|---|---|---|
| 1 | QUA-04 | Integração contínua gratuita (GitHub Actions) rodando `pytest` a cada push, com `requirements-dev.txt` | Pendente |
| 2 | ING-09 | Descartar, na leitura, as colunas com identificadores diretos do paciente e as que o sistema não usa | Pendente |
| 3 | SEG-02 | Anonimização do texto livre antes de qualquer envio (Presidio ou spaCy em português), aplicada em `chamar_gemini` sobre o prompt completo. Se a anonimização falhar, **nada é enviado**. Testes com texto fictício (o repositório é público) | Pendente |
| 4 | SEG-04 | Log de auditoria do que sai para a API: horário, bloco, tamanho e quantidade de itens removidos, sem gravar o texto | Pendente. Depende de QUA-03 (concluído) |
| 5 | COR-07 (E-08) | Fechar a revisão de privacidade do envio com base nos itens acima. Detalhes fora do repositório | Pendente |

#### Bloco 2 — `processador.py`, `utils.py` e configuração

Arquivos: `processador.py`, `utils.py`, arquivo de configuração novo, `tests/`.

| Ordem | Item | Descrição | Status |
|---|---|---|---|
| 1 | IMP-06 | Arquivo de configuração: nome do hospital, metas dos indicadores, nomes de aba, caminhos. Chave da API por variável de ambiente. Os valores das metas são fornecidos por quem opera | Pendente |
| 2 | COR-02 / TRA-02 (E-02, E-07) | Período do relatório como **parâmetro único**, nunca inferido da data máxima; datas inválidas geram aviso e são contadas | Pendente |
| 3 | COR-02 (E-04, dados) | "Trimestre anterior" e "mesmo trimestre do ano anterior" como dois recortes explícitos e nomeados. Gráfico 3 passa a receber o do ano anterior | Pendente |
| 4 | TRA-01 | Definições únicas de "elegível" e "tratada"; remover as duas funções sem uso (parte do E-18) | Pendente |
| 5 | COR-03 (E-09, E-10, E-24) | Variação com base zero tratada igual em todos os blocos (reescreve `test_variacao_com_base_zero` com o valor correto); top 3 do trimestre anterior consistente com o atual; trimestre sem tratadas aparece como 0% | Pendente |
| 6 | E-15 | Leitura da planilha de indicadores feita no `processador.py`, com escolha da aba por nome e validação de colunas e meses | Pendente |
| 7 | ING-01, CAL-01, CAL-02, COR-10 (E-22) | Pacientes-dia lidos da coluna `Paciente-dia`; incidência por 1.000 pacientes-dia; valor trimestral oficial = soma dos eventos sobre a soma dos pacientes-dia | Pendente |
| 8 | CAL-05 | Número absoluto de eventos por indicador no Gráfico 7, contado pelo código | Pendente |
| 9 | E-18 (bloco 1) | O cálculo do volume de notificações (bloco 1 do relatório) passa a devolver também total e variação do ano anterior, que já são calculados | Pendente |

#### Bloco 3 — `visualizador.py`

| Ordem | Item | Descrição | Status |
|---|---|---|---|
| 1 | COR-03 (E-12, E-24) | Gráfico 8: desenhar os trimestres fora do laço mensal; distinguir taxa 0% de trimestre futuro | Pendente |
| 2 | COR-03 (E-05) | Gráfico 1: mês sem dado em branco (`np.nan`, como no Gráfico 8); cores não quebram com mais de 2 anos; parâmetros usados | Pendente |
| 3 | COR-03 (E-11, E-23) | Gráfico 7: metas lidas da configuração e exibidas; eixo X e Y corretos (incidência por 1.000 pacientes-dia); número absoluto por indicador; título impresso uma vez | Pendente |
| 4 | COR-02 (E-04, legendas) | Gráfico 3 lê a coluna do ano anterior; legendas do Gráfico 7 coerentes com o recorte usado | Pendente |
| 5 | COR-01 (E-13) | Fechar cada figura depois de exibida (`plt.close`) | Pendente |

#### Bloco 4 — `agente_ia.py`

| Ordem | Item | Descrição | Status |
|---|---|---|---|
| 1 | COR-05 (E-06, resto) | Nova tentativa com espera antes de trocar de modelo; informar ao usuário qual modelo respondeu | Em andamento. A frase de erro já não entra no relatório (08/10) |
| 2 | COR-06 (E-16) | Prompts sem palavras coladas; nome do hospital vindo da configuração | Pendente |
| 3 | COR-02 (E-04, prompts) | Prompts dizem o recorte que realmente recebem, e recebem os dois comparativos rotulados | Pendente |
| 4 | COR-04 (E-03, parte da função) | Análise de queda recebe o conjunto de dados e as tabelas com rótulos | Pendente |
| 5 | COR-06 (E-18) | Ligar ou remover as funções de análise sem chamador | Pendente |
| 6 | CAL-06 | Seções 5 e 10 no formato do Modelo: protocolos informam apenas se houve evento relacionado; seção 10 com controles existentes, classificação O × D × G = NPR e proposta do NQSP, sem repetir o que já foi analisado | Pendente |
| 7 | IA-09 | Saída estruturada (Pydantic) das análises | Pendente |

#### Bloco 5 — `app.py` e `resultados.py`

| Ordem | Item | Descrição | Status |
|---|---|---|---|
| 1 | COR-01 (E-01) | Limpar `ia_*` e `dados_processados` ao reprocessar; falha no meio não mistura blocos novos e antigos | Pendente |
| 2 | COR-02 (E-02) | Remover a segunda origem do período (seletores da Configuração); o período vem de um único lugar | Pendente |
| 3 | COR-09 (E-20, E-21) | Gráfico 5 por `Setor notificante`; Gráfico 6 por `Setor Responsável` | Pendente |
| 4 | COR-04 (E-03, chamada) | `resultados.py` passa os argumentos certos à análise de queda | Pendente |
| 5 | COR-06 (E-17, E-18) | Remover o caminho morto de imagens `img_*` e as importações sem uso | Pendente |
| 6 | IA-12 | Revisão humana antes de entrar no relatório, registrando o que foi editado | Pendente |
| 7 | COR-05 (E-19) | Traceback fora da tela do usuário | Concluído (08/10) |
| 8 | QUA-03 | Logs e tratamento de erros | Concluído (08/10): commits `cf39143` a `e7ad5fd` |

#### Bloco 6 — Qualidade e IA mensurável

| Ordem | Item | Descrição | Status |
|---|---|---|---|
| 1 | QUA-01 | Cobertura dos testes das funções de cálculo. Os testes já nascem nos blocos 1 a 5; aqui só se completam os que faltarem | Em andamento (`tests/test_processador.py`) |
| 2 | QUA-06 | Conjunto de casos de referência para avaliação | Pendente |
| 3 | QUA-05 | Verificação das afirmações do LLM contra as tabelas (números, setores, períodos) | Pendente. Depende de IA-09 |
| 4 | QUA-02 | Conferência automática entre os números do relatório e as planilhas de origem | Pendente |

**Critério de pronto da Fase 1:**

- Todos os itens dos blocos 1 a 6 concluídos e os testes passando na integração contínua.
- Nenhum envio à API sem passar pela anonimização, e o log de auditoria registra cada envio.
- **Prova com dado real:** o relatório do 2º trimestre de 2026 é regenerado com o sistema novo e comparado com o relatório já entregue. As diferenças aparecem somente onde havia erro corrigido (E-20, E-21, E-22, E-04 e os demais listados).
- Documentos atualizados (backlog, estado atual, `CHANGELOG.md`).

---

## 6. PRÓXIMO

### Implantação em nuvem (trilha paralela)

**Objetivo:** o app deixa de depender do computador do desenvolvedor e de qualquer instalação do usuário. Referência: o projeto de revisão que já roda no GCP, com acesso por conta Google corporativa como única barreira.

**Quando começa:** a decisão (ADR) pode ser escrita agora. O Docker e a publicação **só começam depois do Bloco 1 e do IMP-06**, e não bloqueiam a Fase 1.

| Ordem | Item | Descrição |
|---|---|---|
| 1 | IMP-07 (ADR-018) | Substitui a ADR-013. Registra: nuvem como destino; região (a cota gratuita do Cloud Run é calculada sobre `us-central1`, e São Paulo é Tier 2, a confirmar; hospedar fora do Brasil implica transferência internacional pela LGPD); conta de faturamento com alerta de orçamento para manter custo zero; a planilha bruta fica só na memória, nunca em disco nem em log. Detalhes de conformidade fora do repositório |
| 2 | IMP-03 | Empacotamento em Docker (leitura de configuração e da chave por variável de ambiente; logs no terminal, que o Cloud Run encaminha ao Cloud Logging) |
| 3 | IMP-01 | Publicação no Cloud Run. Chave do Gemini no Secret Manager |
| 4 | IMP-04 | Controle de acesso por conta Google corporativa (IAP ou `st.login`), restrito ao domínio |
| 5 | IMP-02 | Encerrado: deixa de existir com a nuvem |

**Critério de pronto:** um usuário sem nada instalado abre o link, entra com a conta corporativa e gera o relatório; o computador do desenvolvedor pode estar desligado; custo mensal zero comprovado no painel de faturamento.

### Fase 2 — Dados: ingestão, armazenamento e histórico

**Objetivo:** os dados deixam de ser planilhas soltas e viram uma base histórica confiável.

| Bloco | Itens |
|---|---|
| Contrato e leitura | ING-05, ING-06 (planilha de notificações; a de indicadores já foi tratada no E-15), ING-07, ING-08, TRA-03 (E-14), contrato de dados com severidade erro × aviso |
| Banco | **Decisão antes de ARM-01:** onde o banco persiste, já que o disco do Cloud Run é temporário (candidatos: SQLite em bucket do Cloud Storage; BigQuery na cota gratuita; outro). ARM-01 (camadas, ADR-001, revisada conforme a decisão) |
| Fontes | ING-01 (a planilha de indicadores é carregada como qualquer outra fonte; a lógica já existe), ING-02 (identificador), ING-10 (consolidado da investigação, que alimenta a seção 11 do Modelo) |
| Histórico | ING-03 (carga desde 04/2020), ING-04 (rotina de exportação mensal e trimestral), ARM-02 (histórico de mudanças de status) |
| Derivados | ARM-03 (taxa no fechamento × atual), ARM-04 (tempo até a conclusão), ARM-05 (planos de ação ligados às notificações) |
| Operação | IMP-05 (backup do banco) |

**Pontos de decisão (ADR):** armazenamento persistente na nuvem, modelo de histórico (como guardar a mudança de status), estrutura dos esquemas por camada, política de recarga.

**Critério de pronto:** o relatório trimestral é gerado a partir do banco com resultado idêntico ao da Fase 1 (os testes provam); uma notificação que mudou de status mostra a história; rotina mensal de carga documentada e repetível.

### Fase 3 — Painel epidemiológico e modelos descritivos

**Objetivo:** a aba 2 do app passa a existir, com taxa correta e sinal separado de ruído.

| Bloco | Itens |
|---|---|
| Cálculos | CAL-03 (variação com incerteza). CAL-01 e CAL-02 já foram feitos na Fase 1 |
| Descrever | MOD-01 (tendência, sazonalidade, correlação) |
| Sinal × ruído | MOD-02 (cartas de controle, funnel plot, aumento anormal) |
| Produto | MOD-07 (painel) |

**Critério de pronto:** o painel mostra taxas de incidência com limites de controle por indicador; cada alerta tem explicação do critério usado.

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
| 5.1 Segurança do texto | SEG-03 (injeção de prompt). SEG-02 e SEG-04 já foram feitos no Bloco 1 e aqui apenas se estendem a novos usos de texto livre. **Antes de qualquer item com texto livre** |
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

IMP-05 completo (rotina de backup testada), monitoramento do serviço e atualização controlada de versões.

---

## 8. Pontos de decisão (ADRs a escrever)

| ADR | Tema | Quando |
|---|---|---|
| 015 | Estrutura da documentação (roadmap, backlog, changelog, ADRs) | Fase 0 (concluída) |
| 016 | Onde o texto das notificações é processado (API × local). Conteúdo sensível fora do repositório público | Fase 0 (concluída) |
| 017 | Versionamento e CHANGELOG | Fase 0 (concluída) |
| 018 | Implantação em nuvem (substitui a ADR-013) | Trilha de implantação, item 1 |
| a numerar | Armazenamento persistente na nuvem | Fase 2, antes de ARM-01 |
| a numerar | Modelo de histórico e esquemas do banco | Fase 2 |
| a numerar | Banco de vetores (ChromaDB, FAISS ou extensão do SQLite) | Fase 5 |

## 9. Riscos e premissas

- **Prazo do próximo relatório** não está definido neste documento. Se houver urgência, a Fase 1 pode ser fatiada e entregue por blocos.
- **Custo zero na nuvem** depende da conta de faturamento do GCP, do alerta de orçamento e de o uso ficar dentro da cota gratuita. A região escolhida pode mudar a cobertura da cota. Conferir na ADR-018.
- **LGPD na nuvem**: processar a planilha fora do hospital é uma mudança em relação à ADR-013. A decisão de aceitar esse risco é do hospital e fica registrada na ADR-018, com a anonimização, a planilha só em memória e o login corporativo como mitigações.
- **Persistência**: o disco do Cloud Run é temporário. Qualquer banco ou arquivo que precise sobreviver exige decisão própria (Fase 2).
- **Escopo do Modelo**: a lista de tópicos fora do escopo (etapa A) deve ser conferida por quem opera o relatório. Um tópico que passe a ser gerado pelo projeto entra como novo item.
- **Hardware para modelo local**: o item IA-10 só se confirma depois de testar o que a máquina disponível suporta. Com o app na nuvem, o modelo local deixa de poder rodar no servidor do app e precisa de outra solução ou fica restrito aos agregados.
- **Tempo do desenvolvedor**: o roadmap assume um único desenvolvedor, que também está estudando. As fases foram desenhadas para entregar valor mesmo se pausadas no meio.
- **Dados reais**: as premissas sobre o export (identificador, datas) já foram confirmadas na Fase 0.

## 10. Atualizações pendentes nos outros documentos

Aplicadas uma única vez, depois que este roadmap for aprovado.

| Documento | Mudança |
|---|---|
| `backlog.md` | QUA-01: remover a dependência de COR-01 a COR-06. ING-01 sem dependência e concluído na Fase 1. E-15 sai de COR-05 e vai para a Fase 1. Novos itens: CAL-05 (número absoluto no Gráfico 7), CAL-06 (seções 5 e 10 no formato do Modelo), IMP-06 (configuração), IMP-07 (ADR-018). IMP-01, IMP-03 e IMP-04 reescritos para nuvem. IMP-02 encerrado. SEG-02 e SEG-04 na Fase 1 |
| `estado-atual-e-erros.md` | Seções 1.5 e 1.7: ADR-013 será substituída; operação passa a ser em nuvem após a trilha. Situação dos erros conforme os blocos forem fechados |
| `CHANGELOG.md` | Registrar a mudança de ordem (anonimização primeiro, ordem por componente), a estratégia de testes (valor correto no mesmo commit) e a decisão pela nuvem |
| `arquitetura.md` | Trocar a execução em rede local por nuvem quando a ADR-018 for aprovada |