# Changelog

Registro das mudanças do projeto Agente de Inteligência Assistencial.

O formato segue o Keep a Changelog e o versionamento segue o SemVer, em
fase 0.y.z (ADR-017). Datas no formato DD/MM/AAAA. Mudanças apenas de
documentação entram aqui somente quando alteram a ordem do roadmap ou a
estrutura documental (ADR-015).

## [Não lançado]

### Adicionado

- Registro de execução em arquivo e no terminal, com data, hora, nível
  e origem de cada mensagem. A pasta de logs fica fora do git
- Erros na leitura da planilha, no processamento dos blocos e nos
  botões de análise passaram a ser registrados no log, com o nome do
  bloco que falhou
- Falha de cada modelo do Gemini passou a ser registrada como aviso, e
  a falha de todos os modelos como erro

### Alterado

- Os 13 botões de análise por IA passaram a usar uma função única de
  chamada e tratamento de erro, sem mudança visual para o usuário

### Corrigido

- Quando todos os modelos do Gemini falhavam, uma frase de erro entrava
  no relatório como se fosse a análise. Agora o usuário vê um aviso e
  nada é guardado
- Resposta vazia do Gemini aparecia na tela como análise. Agora é
  tratada como falha do modelo, e o sistema tenta o próximo

### Documentação

- Registrado o resultado das verificações V-01 a V-07 em
  `estado-atual-e-erros.md`. Identificados os erros E-20 a E-24 (colunas
  dos Gráficos 5 e 6, valor trimestral dos indicadores, rótulo do eixo do
  bloco 7 e trimestre sem tratadas no bloco 8)
- Backlog e roadmap atualizados com a conferência do export do EPIMED: ID
  confirmado como chave (ING-02), consolidado da investigação como segunda
  fonte (ING-10), minimização de dados (ING-09) e reformulação do ARM-05
- Roadmap passou a ter a coluna Status na Fase 0
- ADR-015: estrutura da documentação
- ADR-017: versionamento e CHANGELOG
- Roadmap: Fase 0 encerrada por ora (07/10). A Fase 1 começa em paralelo
  à entrega do relatório do 3º trimestre, que deve usar o código da tag
  `baseline-pre-fase1`. IMP-02 adiado
- `arquitetura.md` deixou de manter a tabela de evolução planejada e
  passou a apontar para o roadmap e o backlog (DOC-04). A lista de ADRs
  inclui agora as ADRs 015 a 017
- ADR-016: onde o texto das notificações é processado (API externa com
  anonimização como ponto de partida e arquitetura híbrida como alvo)

## [0.1.0] - 05/10/2026

Linha de base (tag `baseline-pre-fase1`). Estado do código usado no
relatório do 2º trimestre de 2026 e planejado para o do 3º trimestre,
antes das correções da Fase 1. O histórico anterior a esta versão está
nos commits e nas ADRs 001 a 014.

### Adicionado

- Documentação de estado e planejamento: `estado-atual-e-erros.md`
  (levantamento de 01/10/2026 com a lista de erros conhecidos),
  `backlog.md` e `roadmap.md`

### Corrigido

- Formatação das médias do trimestre no prompt da análise de queda:
  removida a chamada de `to_string`, alinhando a função às demais do
  bloco 7

### Estado do sistema

- Aplicação em Streamlit com processamento dos blocos 1 a 10, gráficos e
  análises por IA sob demanda (Gemini), execução local na rede do
  hospital
- Erros conhecidos e ainda não corrigidos: ver `estado-atual-e-erros.md`