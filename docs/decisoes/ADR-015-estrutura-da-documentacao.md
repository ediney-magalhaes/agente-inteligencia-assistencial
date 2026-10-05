# ADR-015: Estrutura da Documentação

**Data:** 05/10/2026

**Status:** Aprovado

**Autor:** Ediney Magalhães

## Contexto

Ao retomar o projeto em 01/10/2026, depois de quase dois meses sem
sessão, não havia um documento que dissesse onde o trabalho tinha
parado. O repositório tinha README, arquitetura.md e as ADRs 001 a 014.
Não existiam roadmap, backlog nem changelog, e a seção "Evolução
Planejada" do arquitetura.md era o único registro do que vinha a seguir.

Recuperar o estado do projeto exigiu reler o código e o histórico de
sessões. Os erros conhecidos e as melhorias discutidas só existiam na
memória do desenvolvedor e em conversas, sem um lugar fixo no
repositório. O repositório também é público, o que limita o que pode
ser registrado nele.

## Decisão

Adotar um conjunto fixo de documentos, cada um com uma única
responsabilidade:

| Documento | Responde a |
|---|---|
| README.md | O que é o projeto e como executá-lo |
| arquitetura.md | Como o sistema é construído hoje |
| docs/decisoes/ (ADRs) | Por que cada decisão foi tomada |
| docs/estado-atual-e-erros.md | Retrato datado do estado do sistema e dos erros conhecidos |
| docs/backlog.md | Tudo o que pode ser feito, por etapa do ciclo de vida do dado, sem prioridade |
| docs/roadmap.md | Em que ordem fazer, critério de pronto de cada fase e situação de cada item |
| CHANGELOG.md | O que mudou entre uma versão e outra |

Regras de manutenção:

1. Cada informação mora em um só documento. Os demais apontam para ele
   em vez de repeti-la. O arquitetura.md deixa de descrever o futuro e
   passa a apontar para o roadmap.
2. Todo item do backlog tem um identificador fixo (por exemplo ING-02 ou
   MOD-05). Roadmap, estado atual e ADRs usam esse identificador para
   se referir ao item.
3. A situação de cada item é mantida no roadmap e atualizada ao fim de
   cada sessão de trabalho.
4. O estado atual é um retrato datado. Um novo levantamento é feito ao
   fim de cada fase.
5. Mudanças na ordem do roadmap são registradas no CHANGELOG.
6. Uma ADR aprovada não é reescrita. Se a decisão mudar, uma nova ADR a
   substitui e o status da anterior é atualizado.
7. Nenhum documento do repositório contém dados de paciente,
   credenciais ou detalhes de conformidade que não devam ser públicos.
   Quando uma decisão tiver esse tipo de detalhe, a ADR registra apenas
   que a decisão existe, e o conteúdo fica fora do repositório.
8. Commits de documentação usam o prefixo `docs:`, como já ocorre nas
   Conventional Commits do projeto.

O formato do CHANGELOG e o esquema de versionamento serão definidos em
ADR própria.

## Justificativa

Um documento por pergunta evita a duplicação e a contradição entre
documentos, como acontecia entre a "Evolução Planejada" do
arquitetura.md e o que realmente estava em andamento. Os identificadores
fixos dão rastreabilidade: dá para seguir um mesmo item do backlog até o
roadmap, a um erro conhecido e a uma ADR sem depender de busca por
texto.

Como o projeto tem um único desenvolvedor, que o retoma em intervalos
longos, o roadmap com a situação de cada item é o que permite recuperar o
contexto em minutos. A regra de manter detalhes sensíveis fora do
repositório decorre de ele ser público.

## Consequências

- Retomar o projeto depois de uma pausa passa a exigir a leitura do
  roadmap, e não do código e do histórico de conversas
- Todo item discutido tem um lugar e um identificador
- Há um custo de manutenção: a situação dos itens precisa ser atualizada
  ao fim de cada sessão, e documentos desatualizados voltam a gerar o
  problema que esta ADR resolve
- A seção "Evolução Planejada" do arquitetura.md precisa ser trocada por
  um link para o roadmap (item DOC-04 do backlog)
- Ficam pendentes a ADR do CHANGELOG e do versionamento (DOC-02) e a ADR
  sobre onde o texto das notificações é processado (SEG-01 e DOC-06)