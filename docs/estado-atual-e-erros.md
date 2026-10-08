# Estado Atual e Erros a Corrigir

**Projeto:** Agente de Inteligência Assistencial
**Data do levantamento:** 01/10/2026
**Última atualização:** 08/10/2026 (situação dos erros E-06 e E-19 após o QUA-03; destino de cada erro no roadmap)
**Base do levantamento:** `app.py`, `resultados.py`, `processador.py`, `agente_ia.py`, `visualizador.py` e `utils.py` (versões enviadas em 01/10/2026) e histórico de sessões até 27/07/2026.

**Legenda de situação**
- **Confirmado:** o comportamento decorre do código lido ou foi confirmado com dado real.
- **A verificar:** depende de dado real ou de decisão.

---

## 1. Estado atual

### 1.1 Visão geral

Sistema local em Streamlit que recebe a exportação de notificações do EPIMED e a planilha de indicadores, calcula os blocos do Relatório Trimestral de Segurança do Paciente, exibe gráficos e tabelas e gera análises narrativas com a API Gemini, uma por bloco e sob demanda (ADR-011). O profissional usa o resultado na tela para finalizar o relatório no Word (ADR-014). A execução é local, na rede do hospital (ADR-013). O sistema foi usado para o relatório do 2º trimestre de 2026.

### 1.2 Módulos

| Arquivo | Responsabilidade | Situação |
|---|---|---|
| `app.py` | Interface em abas, upload, orquestração do processamento | Em uso. As abas Painel Epidemiológico e Agente IA são marcadores |
| `resultados.py` | Exibição por bloco e botões de análise de IA | Em uso. 12 das 14 funções de análise estão ligadas |
| `processador.py` | Validação de entrada e preparação dos blocos 1 a 10 | Em uso |
| `visualizador.py` | 7 funções de gráfico | Em uso |
| `agente_ia.py` | Chamada ao Gemini (3 modelos em sequência) e 14 funções de análise | Em uso |
| `utils.py` | Constantes de colunas, mapeamento de nomes alternativos, validação de schema, 4 funções auxiliares | Em uso. As funções `tem_investigacao` e `foi_tratada` não são chamadas (ver V-01) |

Arquivados em `arquivo/`: `motor_analise.py`, `gerador.py`, `teste.py`.

### 1.3 Fluxo de dados

Planilha de notificações (aba 1) e planilha de indicadores → `carregar_validar` → `preparar_bloco1` (define o período a partir da data máxima) → blocos 2 a 10 → `session_state` → `resultados.exibir` → botão de IA por bloco → Gemini → texto na tela.

### 1.4 Cobertura do Modelo Relatório

Numeração conforme o documento Modelo Relatório (o modelo não tem tópico 8).

| Seção do modelo | Situação | Observação |
|---|---|---|
| Objetivo e Definições | Não coberto | Texto fixo, preenchido no Word |
| Gráfico 1 — Quantidade de notificações | Coberto | Ver E-05 |
| Gráfico 2 — Turno | Parcial | Tabela e análise de IA. O gráfico vem do EPIMED e não há entrada de imagem (E-17) |
| Gráfico 3 — Classificação e top 3 | Parcial | Análise de IA só para o gráfico geral (E-18). Período de comparação errado (E-04) |
| Gráfico 4 — Eventos adversos | Coberto | O gráfico 4.2 depende de imagem do EPIMED (E-17) |
| Gráficos 5 e 6 — Setores | **Colunas erradas** | Gráfico 5 usa o setor responsável e o 6 usa o local de ocorrência (E-20, E-21) |
| Gráfico 7 — Índices de qualidade | Parcial | Sem alvo ou tolerância (E-11). Valor trimestral calculado como média das taxas mensais (E-22). Rótulo do eixo errado (E-23). Sem número absoluto por indicador, que o Modelo pede |
| Gráfico 8 — Cumprimento de análises | Coberto | Ver E-12 |
| 4. Auditoria de ROPs | Não coberto | Dados em dashboard |
| 5. Protocolos gerenciados | Parcial | Feito por IA lendo descrições. O Modelo pede apenas informar se houve evento adverso relacionado ao protocolo |
| 6. Comissão de óbitos | Não coberto | |
| 7. Comissão de prontuários | Não coberto | |
| 9. Plano de Segurança do Paciente | Não coberto | |
| 10. Interrelação e mapeamento de risco | Parcial | A saída não segue o formato do Modelo: faltam controles existentes, classificação O x D x G = NPR e proposta NQSP. O prompt não manda suprimir o que já foi analisado nas seções anteriores |
| 11. Ações táticas e estratégicas | Não coberto | |
| 12. Referências | Não coberto | Texto fixo |

### 1.5 Decisões vigentes

ADR-001 a ADR-014 em `docs/decisoes/`. As mais relevantes para este levantamento: ADR-005 (triagem de indicadores por IA), ADR-011 (IA sob demanda), ADR-013 (execução na rede local) e ADR-014 (simplificação da interface). A ADR-008 descreve o gerador de Word, descartado em 04/05; a decisão do bloco 9 registrada nela segue vigente e o status da ADR merece revisão.

Documentação: README, `arquitetura.md`, ADRs, este documento, `backlog.md` e `roadmap.md` (criados em 01/10/2026). Existem `CHANGELOG.md` (ADR-017) e `tests/` (poucos testes, sem integração contínua ainda). A ADR-013 (rede local) será substituída pela ADR-018 (nuvem), conforme o roadmap.

### 1.6 Evolução planejada

Substituída pelo `roadmap.md`. O texto de "Evolução Planejada" em `arquitetura.md` deve ser trocado por um link para ele (item DOC-04).

### 1.7 Operação

Execução local com acesso pela rede interna (`Ligar_Painel.bat`). Ramos `main` e `desenvolvimento`, último merge em `main` em 27/07/2026. Linha de base registrada em 05/10/2026: tag `baseline-pre-fase1`, commit `299ab61`. Registro de execução em arquivo e no terminal desde 08/10 (QUA-03). A implantação em nuvem (Cloud Run, login por conta Google corporativa) está planejada na trilha de implantação do roadmap.

---

## 2. Erros a corrigir

### 2.1 Crítico

| ID | Onde | Problema | Situação |
|---|---|---|---|
| E-08 | `agente_ia.py` | Revisão de privacidade e conformidade do envio de dados à API pendente. Detalhes mantidos fora do repositório. Exige ADR | A verificar |

### 2.2 Alto

| ID | Onde | Problema | Situação |
|---|---|---|---|
| E-01 | `app.py` (bloco de processamento) | Ao reprocessar, as chaves `ia_*` e `dados_processados` não são limpas. Textos de IA antigos aparecem sobre dados novos. Uma falha no meio do processamento deixa blocos novos misturados com antigos na tela | Confirmado |
| E-02 | `app.py`, `resultados.py`, `preparar_bloco7` | Trimestre e ano têm duas origens. O bloco 1 infere da data máxima da planilha. O bloco 7, os títulos de gráficos e o prompt da interrelação usam os seletores da aba Configuração (padrão: 1º trimestre e ano 2020, o valor mínimo do campo). Seletores esquecidos geram bloco 7 vazio e texto "1º trimestre de 2020", sem erro | Confirmado |
| E-03 | `resultados.py`, `analisar_bloco7_queda` | O parâmetro descrito como dataset de notificações recebe a tabela mensal do indicador, e a função de queda não produz descrições. As três tabelas de queda usam `to_string(index=False)` sobre séries, o que remove os rótulos (grau, local, tipo). É a mesma causa do bug de 27/07 | Confirmado. Parcialmente tratado em 05/10 (commit `299ab61`): só a formatação das médias. As tabelas e o dataset seguem como descrito |
| E-04 | `preparar_bloco1`/`app.py`, `grafico_classificacoes`, `preparar_bloco7` | "Trimestre anterior" tem dois sentidos. No Gráfico 3 a legenda diz mesmo trimestre do ano anterior, mas os dados são do trimestre imediatamente anterior (o Modelo pede o do ano anterior; o recorte existe no bloco 1 e é descartado). No bloco 7 os dados são do mesmo trimestre do ano anterior, mas legenda e prompts dizem "trimestre anterior" | Confirmado |
| E-06 | `agente_ia.chamar_gemini` | Qualquer exceção é tratada igual, sem nova tentativa com espera. Se todos os modelos falham, a frase de erro é exibida e guardada como se fosse a análise. A troca de modelo não é informada | Parcialmente tratado em 08/10 (QUA-03): a frase de erro não entra mais no relatório e a resposta vazia conta como falha do modelo. Falta nova tentativa com espera e informar a troca de modelo (Bloco 4) |
| E-07 | `carregar_validar`, `preparar_bloco1` | Datas inválidas viram vazias e somem dos totais sem aviso. O período do relatório é o trimestre da data máxima do arquivo, então uma única notificação de outro trimestre (por exemplo, exportação com data de outubro) desloca o relatório inteiro | Confirmado |
| E-20 | `app.py` (Gráfico 5) | O Gráfico 5 (Setores Notificantes) agrupa por **Setor Responsável**, que é o setor que realiza a tratativa. O setor de quem notifica é **Setor notificante**. A tabela e a análise de IA descrevem setores trocados | Confirmado em 05/10 (V-02) |
| E-21 | `app.py` (Gráfico 6) | O Gráfico 6 (Setores Notificados) agrupa por **Local de ocorrência**. O setor notificado é o **Setor Responsável** | Confirmado em 05/10 (V-02). A correção dos dois gráficos é trocar a coluna passada a cada chamada da mesma função |
| E-22 | `preparar_bloco7` | O valor trimestral de cada indicador é a média simples das três taxas mensais. O valor oficial do hospital é a soma dos eventos dividida pela soma dos pacientes-dia do trimestre. A planilha de indicadores traz só as taxas, sem numerador nem denominador, então a correção exige trazer os pacientes-dia para o sistema (ING-01) | Confirmado em 05/10 (V-03) |

### 2.3 Médio

| ID | Onde | Problema | Situação |
|---|---|---|---|
| E-05 | `grafico_volume_notificacoes` | Meses sem dado no ano corrente aparecem como barra 0 com rótulo. Mais de 2 anos na planilha quebra o gráfico (só há 2 cores). Os parâmetros de trimestre e ano são ignorados | Confirmado. A quebra com 3 anos não ocorre na prática: o relatório trabalha sempre com 2 anos (V-05) |
| E-09 | `preparar_bloco1`, `preparar_bloco2`, `preparar_bloco3` | Variação com base zero resulta em 0%, enquanto o bloco 4 usa "-". Critérios diferentes, e 0% pode ser lido como estabilidade | Confirmado |
| E-10 | `preparar_bloco_setores` | O top 3 do trimestre anterior é calculado de forma independente do atual. Setores líderes hoje podem não aparecer no anterior. O rótulo "(%)" é participação, não variação | Confirmado |
| E-11 | `gerar_grafico_bloco7_geral`, `resultados.py` | O parâmetro de metas é ignorado e o app passa `{}`, então o alvo exigido pelo Modelo nunca aparece. Eixo X rotulado "Classificações". O título "Gráfico 7" é impresso depois do gráfico geral | Confirmado |
| E-12 | `gerar_grafico_bloco8` | Pela indentação, os trimestres são desenhados dentro do laço das barras mensais e redesenhados cerca de 12 vezes por ano. O eixo vem só das tabelas do ano anterior | Confirmado. Efeito visual leve |
| E-13 | `visualizador.py` (todas as funções) | Figuras criadas com `pyplot` global e nunca fechadas, acumulando a cada reexecução. O Streamlit avisa que o Matplotlib não funciona bem com threads, e o acesso é pela rede (ADR-013) | Confirmado |
| E-14 | `utils.MAPEAMENTO_COLUNAS`, `atualizacao_schema` | As 18 colunas são obrigatórias, inclusive "Nota do Classificador (Opcional)" e colunas sem uso nos arquivos enviados (`COL_TIPO_SETOR`, `COL_EFETIVO`, `COL_SETOR_NOTIFICANTE`). A falta de uma recusa a planilha. Renomeios por nome alternativo não deixam registro, e a função altera o DataFrame de entrada. Com o E-20, `COL_SETOR_NOTIFICANTE` passa a ser necessária | Confirmado |
| E-15 | `app.py` (leitura de indicadores), `preparar_bloco7` | `indicadores.xlsx` é lido direto no `app.py`, sem validação e sem escolha de aba, contornando o processador. `'Ano'`, `'Mês'` e os nomes de mês (`'Março'`) são texto fixo, e uma variação de grafia gera filtro vazio sem erro | Confirmado |

### 2.4 Baixo

| ID | Onde | Problema | Situação |
|---|---|---|---|
| E-16 | `agente_ia.py` (prompts) | Concatenação sem espaço ("quantitativase", "Nessemomento", "ondeos"). Nome do hospital fixo no texto, enquanto o campo "hospital" da Configuração não é usado | Confirmado |
| E-17 | `resultados.py`, `app.py` | O código lê `img_*` da sessão (Gráficos 2, 4.2, 5, 6), mas nenhum campo de upload existe no app. Caminho morto | Confirmado |
| E-18 | `agente_ia.py`, `resultados.py`, `utils.py` | `analisar_top3_bloco3` e `analisar_bloco7_geral` sem chamador. O bloco 1 não recebe total e variação do ano anterior, que o processador já calcula. `tem_investigacao`, `foi_tratada` e importações sem uso | Confirmado |
| E-19 | `carregar_validar` | O erro esperado de coluna ausente aparece como "Erro inesperado" no terminal, e o traceback completo é mostrado ao usuário final | **Corrigido em 08/10** (QUA-03): coluna ausente mostra quais colunas faltam, os demais erros mostram mensagem genérica e o detalhe fica no log |
| E-23 | `gerar_grafico_bloco7` | O eixo Y diz "Nº notificações", mas os quatro indicadores são incidência por 1.000 pacientes-dia | Confirmado em 05/10 (V-07) |
| E-24 | `preparar_bloco8`, `gerar_grafico_bloco8` | Trimestre com elegíveis e nenhuma tratada fica ausente em vez de 0%, e o gráfico não distingue "taxa zero" de "trimestre futuro". Não ocorreu até o 2º trimestre de 2026 | Confirmado (comportamento do pandas). Baixa prioridade |

### 2.5 Resultado das verificações (05/10/2026)

| ID | Resultado | Destino |
|---|---|---|
| V-01 | As duas regras de "elegível" e "tratada" coincidem neste export: células vazias são realmente vazias e nenhum status contém variação das expressões da regra. Os dois status "Concluído sem necessidade de investigação" e "Concluída – Outra natureza" não são encaminhados para tratativa e ficam fora das duas contagens, o que está correto | Sem quebra na série histórica. `tem_investigacao` e `foi_tratada` sem uso (E-18). Backlog: glossário dos status do EPIMED, validação de consistência dos status e validação por valor exato (um status novo ou com outra grafia deixaria de ser contado sem aviso) |
| V-02 | O setor notificante é o setor de quem notifica. O setor responsável realiza a tratativa | E-20 e E-21 |
| V-03 | A planilha de indicadores traz só as taxas (colunas Ano, Mês, Erro de Medicação, Flebite, Lesão de Pele, Queda). O valor trimestral oficial é soma dos eventos sobre soma dos pacientes-dia | E-22. Exige ING-01 e CAL-01 |
| V-04 | O filtro por "queda" em Incidente retorna um único valor: "Queda do paciente" | Sem erro |
| V-05 | O relatório trabalha sempre com 2 anos (o atual e o anterior), por escolha de legibilidade | Regra de negócio explícita no backlog (janela de 2 anos como parâmetro, com aviso) |
| V-06 | Nenhum trimestre dos gráficos anteriores ficou com elegíveis e nenhuma tratada | E-24, baixa prioridade |
| V-07 | Os indicadores são incidência por 1.000 pacientes-dia | E-23 |

### 2.6 Destino de cada erro no roadmap (08/10/2026)

| Bloco da Fase 1 | Erros |
|---|---|
| 1. Privacidade e integração contínua | E-08 |
| 2. `processador.py`, `utils.py` e configuração | E-02, E-04 (dados), E-07, E-09, E-10, E-15, E-18 (parte), E-22, E-24 (cálculo) |
| 3. `visualizador.py` | E-04 (legendas), E-05, E-11, E-12, E-13, E-23, E-24 (gráfico) |
| 4. `agente_ia.py` | E-03 (função), E-04 (prompts), E-06, E-16, E-18 (parte) |
| 5. `app.py` e `resultados.py` | E-01, E-02 (seletores), E-03 (chamada), E-17, E-18 (parte), E-20, E-21 |
| Já concluído | E-19 |
| Fase 2 | E-14 |

---

## 3. Cuidados para o relatório do 3º trimestre

Enquanto os erros não são corrigidos:

1. Exportar do EPIMED com data final em 30/09 (E-07).
2. Ajustar manualmente trimestre e ano na aba Configuração (E-02).
3. Reiniciar o app entre processamentos (E-01).
4. Ler a legenda do Gráfico 3 sabendo que a série "anterior" é o trimestre imediatamente anterior (E-04).
5. Conferir os números das tabelas de queda antes de usar a análise (E-03).
6. Rever a conformidade do envio de dados à API antes de gerar as análises (E-08).
7. **Gráficos 5 e 6:** as tabelas e as análises de IA do app estão agrupadas pela coluna errada. Montar à mão as contagens por **Setor notificante** (Gráfico 5) e por **Setor Responsável** (Gráfico 6) e escrever o texto a partir delas (E-20, E-21).
8. **Gráfico 7:** calcular o valor do trimestre de cada indicador pela soma dos eventos sobre a soma dos pacientes-dia e corrigir nos textos onde a média das taxas aparecer (E-22). Corrigir o título do eixo Y, que mostra "Nº notificações" (E-23).
9. **Comparação com o mesmo trimestre do ano anterior:** as notificações de julho a setembro de 2026 ainda estão em tratativa, enquanto as de 2025 tiveram um ano para serem concluídas. A taxa de cumprimento do 3º trimestre tende a parecer menor por esse motivo (ARM-03 no backlog).

---

## 4. Melhorias

As melhorias discutidas em 01/10/2026, organizadas por etapa do ciclo de vida do dado, estão em `backlog.md`. A ordem de execução, as fases e os critérios de pronto estão em `roadmap.md`. A situação de cada item da Fase 0 é mantida no próprio roadmap.