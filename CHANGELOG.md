# Changelog

Registro das mudanças do projeto Agente de Inteligência Assistencial.

O formato segue o Keep a Changelog e o versionamento segue o SemVer, em
fase 0.y.z (ADR-017). Datas no formato DD/MM/AAAA. Mudanças apenas de
documentação entram aqui somente quando alteram a ordem do roadmap ou a
estrutura documental (ADR-015).

## [Não lançado]

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