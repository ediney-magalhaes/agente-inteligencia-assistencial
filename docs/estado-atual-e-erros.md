# Estado Atual e Erros a Corrigir

**Projeto:** Agente de Inteligência Assistencial
**Data:** 01/10/2026
**Base do levantamento:** `app.py`, `resultados.py`, `processador.py`, `agente_ia.py`, `visualizador.py` e `utils.py` (versões enviadas em 01/10/2026) e histórico de sessões até 27/07/2026.

**Legenda de situação**
- **Confirmado:** o comportamento decorre do código lido.
- **A verificar:** depende de dado real ou de decisão; a coluna "Como verificar" indica o passo.

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
| `utils.py` | Constantes de colunas, mapeamento de nomes alternativos, validação de schema, 4 funções auxiliares | Em uso. As 4 auxiliares não são chamadas nos arquivos enviados |

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
| Gráficos 5 e 6 — Setores | Coberto com ressalva | Coluna do Gráfico 5 a verificar (V-02) |
| Gráfico 7 — Índices de qualidade | Parcial | Sem alvo ou tolerância (E-11). Sem número absoluto por indicador, que o Modelo pede |
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

Documentação existente: README, `arquitetura.md` e ADRs. Não existem roadmap, changelog nem testes automatizados.

### 1.6 Evolução planejada (conforme `arquitetura.md`)

| Fase | Situação |
|---|---|
| 1. Fundação | Concluída na prática. Pendências de robustez na seção 2 |
| 2. Persistência (SQLite) | Não iniciada. O schema não foi desenhado |
| 3. Painel Epidemiológico | Aba marcador |
| 5. Agente conversacional | Aba marcador |

A Fase 4 não foi identificada no material consultado.

### 1.7 Operação

Execução local com acesso pela rede interna (`Ligar_Painel.bat`). Ramos `main` e `desenvolvimento`, último merge em `main` em 27/07/2026. Registro de erros apenas por `print` no terminal.

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
| E-03 | `resultados.py`, `analisar_bloco7_queda` | O parâmetro descrito como dataset de notificações recebe a tabela mensal do indicador, e a função de queda não produz descrições. As três tabelas de queda usam `to_string(index=False)` sobre séries, o que remove os rótulos (grau, local, tipo). É a mesma causa do bug de 27/07 | Confirmado |
| E-04 | `preparar_bloco1`/`app.py`, `grafico_classificacoes`, `preparar_bloco7` | "Trimestre anterior" tem dois sentidos. No Gráfico 3 a legenda diz mesmo trimestre do ano anterior, mas os dados são do trimestre imediatamente anterior (o Modelo pede o do ano anterior; o recorte existe no bloco 1 e é descartado). No bloco 7 os dados são do mesmo trimestre do ano anterior, mas legenda e prompts dizem "trimestre anterior" | Confirmado |
| E-06 | `agente_ia.chamar_gemini` | Qualquer exceção é tratada igual, sem nova tentativa com espera. Se todos os modelos falham, a frase de erro é exibida e guardada como se fosse a análise. A troca de modelo não é informada | Confirmado |
| E-07 | `carregar_validar`, `preparar_bloco1` | Datas inválidas viram vazias e somem dos totais sem aviso. O período do relatório é o trimestre da data máxima do arquivo, então uma única notificação de outro trimestre (por exemplo, exportação com data de outubro) desloca o relatório inteiro | Confirmado |

### 2.3 Médio

| ID | Onde | Problema | Situação |
|---|---|---|---|
| E-05 | `grafico_volume_notificacoes` | Meses sem dado no ano corrente aparecem como barra 0 com rótulo. Mais de 2 anos na planilha quebra o gráfico (só há 2 cores). Os parâmetros de trimestre e ano são ignorados | Confirmado. A quebra com 3 anos decorre da leitura do código |
| E-09 | `preparar_bloco1`, `preparar_bloco2`, `preparar_bloco3` | Variação com base zero resulta em 0%, enquanto o bloco 4 usa "-". Critérios diferentes, e 0% pode ser lido como estabilidade | Confirmado |
| E-10 | `preparar_bloco_setores` | O top 3 do trimestre anterior é calculado de forma independente do atual. Setores líderes hoje podem não aparecer no anterior. O rótulo "(%)" é participação, não variação | Confirmado |
| E-11 | `gerar_grafico_bloco7_geral`, `resultados.py` | O parâmetro de metas é ignorado e o app passa `{}`, então o alvo exigido pelo Modelo nunca aparece. Eixo X rotulado "Classificações". O título "Gráfico 7" é impresso depois do gráfico geral | Confirmado |
| E-12 | `gerar_grafico_bloco8` | Pela indentação, os trimestres são desenhados dentro do laço das barras mensais e redesenhados cerca de 12 vezes por ano. O eixo vem só das tabelas do ano anterior | Confirmado. Efeito visual leve |
| E-13 | `visualizador.py` (todas as funções) | Figuras criadas com `pyplot` global e nunca fechadas, acumulando a cada reexecução. O Streamlit avisa que o Matplotlib não funciona bem com threads, e o acesso é pela rede (ADR-013) | Confirmado |
| E-14 | `utils.MAPEAMENTO_COLUNAS`, `atualizacao_schema` | As 18 colunas são obrigatórias, inclusive "Nota do Classificador (Opcional)" e colunas sem uso nos arquivos enviados (`COL_TIPO_SETOR`, `COL_EFETIVO`, `COL_SETOR_NOTIFICANTE`). A falta de uma recusa a planilha. Renomeios por nome alternativo não deixam registro, e a função altera o DataFrame de entrada | Confirmado |
| E-15 | `app.py` (leitura de indicadores), `preparar_bloco7` | `indicadores.xlsx` é lido direto no `app.py`, sem validação e sem escolha de aba, contornando o processador. `'Ano'`, `'Mês'` e os nomes de mês (`'Março'`) são texto fixo, e uma variação de grafia gera filtro vazio sem erro | Confirmado |

### 2.4 Baixo

| ID | Onde | Problema | Situação |
|---|---|---|---|
| E-16 | `agente_ia.py` (prompts) | Concatenação sem espaço ("quantitativase", "Nessemomento", "ondeos"). Nome do hospital fixo no texto, enquanto o campo "hospital" da Configuração não é usado | Confirmado |
| E-17 | `resultados.py`, `app.py` | O código lê `img_*` da sessão (Gráficos 2, 4.2, 5, 6), mas nenhum campo de upload existe no app. Caminho morto | Confirmado |
| E-18 | `agente_ia.py`, `resultados.py`, `utils.py` | `analisar_top3_bloco3` e `analisar_bloco7_geral` sem chamador. O bloco 1 não recebe total e variação do ano anterior, que o processador já calcula. Funções auxiliares e importações sem uso | Confirmado |
| E-19 | `carregar_validar` | O erro esperado de coluna ausente aparece como "Erro inesperado" no terminal, e o traceback completo é mostrado ao usuário final | Confirmado |

### 2.5 A verificar com dado real

| ID | Onde | Dúvida | Como verificar |
|---|---|---|---|
| V-01 | `preparar_bloco8` e `utils` (`tem_investigacao`, `foi_tratada`) | Duas definições de "elegível" e "tratada". Se os trimestres antigos foram calculados pela regra legada, há quebra na série histórica | Aplicar as duas regras ao 2º trimestre de 2026 e comparar as contagens |
| V-02 | `app.py` (Gráfico 5) | O Gráfico 5 (notificantes) usa `'Setor Responsável'`. A ADR-004 e o histórico apontavam outra coluna, e `COL_SETOR_NOTIFICANTE` existe sem uso | Conferir no EPIMED o que cada coluna representa |
| V-03 | `preparar_bloco7` | A média simples de taxas mensais difere da razão das somas quando o denominador varia | Ver se `indicadores.xlsx` traz numerador e denominador |
| V-04 | `preparar_detalhe_queda` | O filtro por trecho "queda" em Incidente pode incluir incidentes que não são queda de paciente | Listar os valores distintos que casam com o filtro |
| V-05 | `grafico_volume_notificacoes` | Quantos anos tem a exportação usual | Gerar o Gráfico 1 com o arquivo real |
| V-06 | `preparar_bloco8` | Trimestre com elegíveis e nenhuma tratada fica ausente em vez de 0% (comportamento esperado do pandas) | Testar com um caso real |
| V-07 | `gerar_grafico_bloco7` | O eixo Y diz "Nº notificações" para valores que parecem ser índices | Conferir a unidade em `indicadores.xlsx` |

---

## 3. Cuidados para o relatório do 3º trimestre

Enquanto os erros não são corrigidos:

1. Exportar do EPIMED com data final em 30/09 (E-07).
2. Ajustar manualmente trimestre e ano na aba Configuração (E-02).
3. Reiniciar o app entre processamentos (E-01).
4. Ler a legenda do Gráfico 3 sabendo que a série "anterior" é o trimestre imediatamente anterior (E-04).
5. Conferir os números das tabelas de queda antes de usar a análise (E-03).
6. Verificar a chave do Gemini antes de enviar dados (E-08).
7. Conferir a coluna usada no Gráfico 5 (V-02).

---

## 4. Melhorias ainda não discutidas

Seção reservada. Será preenchida a partir da discussão pelo ciclo de vida do dado: ingestão, armazenamento, tratamento, cálculos, modelos estatísticos e epidemiológicos, agente de IA, e qualidade e observabilidade.