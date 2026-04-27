# ADR-006: Função Genérica para Gráficos Top 3 por Classificação

**Data:** 27/04/2026  
**Status:** Aprovado  
**Autor:** Ediney Magalhães

## Contexto
O novo modelo de relatório exige subgráficos de Top 3 para cada classificação 
de notificação (Circunstância de Risco, Near Miss, Evento Adverso, etc.).
A abordagem inicial seria criar uma função específica para cada classificação,
o que geraria duplicação de código e dificuldade de manutenção a cada mudança
no modelo do relatório.

## Decisão
Criar uma única função genérica `gerar_grafico_top3(dicionario, classificacao)`
no `visualizador.py` que recebe o dicionário completo de Top 3 — já preparado 
pelo `processador.py` — e o nome de qualquer classificação como parâmetro.

O `gerador.py` (a ser criado) será responsável por iterar sobre todas as 
classificações e chamar essa função para cada uma.

## Consequências
- Adicionar ou remover uma classificação no futuro não exige alteração no visualizador
- A manutenção visual (cores, fonte, layout) é feita em um único lugar
- O `gerador.py` controla quais classificações entram no relatório e em qual ordem