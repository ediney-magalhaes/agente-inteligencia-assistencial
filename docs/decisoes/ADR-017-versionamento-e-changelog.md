# ADR-017: Versionamento e CHANGELOG

**Data:** 05/10/2026

**Status:** Aprovado

**Autor:** Ediney Magalhães

## Contexto

A ADR-015 definiu o CHANGELOG como o documento que registra o que mudou
entre uma versão e outra, mas deixou o esquema de versionamento em
aberto. Até então o projeto não tinha versões. Existiam dois ramos
(`main` e `desenvolvimento`), mensagens de commit no padrão Conventional
Commits e, desde 05/10/2026, uma tag de linha de base
(`baseline-pre-fase1`), criada antes das correções planejadas para a
Fase 1.

O roadmap divide o trabalho em fases, cada uma com critério de pronto, e
o sistema é usado a cada trimestre para gerar o relatório. Sem um
número de versão, não há como dizer qual versão do código gerou um
relatório, nem como relacionar uma mudança de ordem do roadmap a um
ponto do histórico.

## Decisão

Adotar o versionamento semântico (SemVer) no formato MAJOR.MINOR.PATCH,
em fase 0.y.z enquanto o sistema estiver em desenvolvimento, e registrar
as mudanças em `CHANGELOG.md` no formato Keep a Changelog.

Regras de versão:

1. **PATCH** sobe a cada correção de erro que não altera o
   comportamento esperado.
2. **MINOR** sobe a cada funcionalidade nova ou fase do roadmap
   concluída.
3. **MAJOR** só sobe a partir da versão 1.0.0, quando uma mudança
   quebrar a compatibilidade (por exemplo, formato de entrada ou do
   banco de dados).
4. A versão **1.0.0** será declarada quando as Fases 1 e 2 e a
   implantação mínima do roadmap estiverem concluídas.
5. A linha de base (tag `baseline-pre-fase1`) corresponde à versão
   **0.1.0**. Essa tag não é duplicada.

Regras de publicação:

1. Cada versão recebe uma tag anotada no formato `vMAJOR.MINOR.PATCH`,
   criada no ramo `main` depois do merge a partir de `desenvolvimento`.
2. O CHANGELOG mantém uma seção "Não lançado" no topo, que recebe as
   mudanças à medida que acontecem. Ao criar uma versão, essa seção
   passa a ter o número e a data da versão.
3. As entradas são agrupadas por tipo: Adicionado, Alterado, Corrigido,
   Removido, Segurança e Documentação.
4. Mudanças apenas de documentação não geram versão. Entram em
   "Documentação" quando alteram a ordem do roadmap ou a estrutura
   documental (regra 5 da ADR-015).
5. As datas no CHANGELOG seguem o formato DD/MM/AAAA, como nas ADRs.
6. O relatório trimestral registra a versão do sistema que o gerou.

## Justificativa

O SemVer é a convenção mais usada e se encaixa no roadmap: uma fase
concluída corresponde a um MINOR, e uma correção, a um PATCH. O prefixo
0. comunica que o sistema ainda evolui e que mudanças grandes são
esperadas, sem criar a expectativa de estabilidade de uma versão 1.0.

A alternativa de versionar por trimestre do relatório liga a versão ao
ciclo de uso, mas não distingue uma correção pequena de uma mudança
grande. A alternativa de usar só datas não aproveita as tags do git e
dá pouca rastreabilidade.

Definir a versão 1.0.0 por critério do roadmap, e não por data, evita
declará-la antes de o sistema estar testado, com banco de dados e em uso
regular.

## Consequências

- Cada relatório pode ser associado à versão do código que o gerou
- As tags passam a ser criadas no ramo `main`, o que exige o merge de
  `desenvolvimento` a cada versão
- O CHANGELOG precisa ser atualizado junto com cada mudança relevante, e
  a seção "Não lançado" evita esquecer entradas
- O próximo MINOR (0.2.0) corresponde à conclusão da Fase 1
- A ADR-016 fica reservada para a decisão do SEG-01 (onde o texto das
  notificações é processado)