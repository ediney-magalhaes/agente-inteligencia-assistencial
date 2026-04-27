# ADR-007: Estratégia de Visualização do Bloco 7 — Indicadores de Qualidade

**Data:** 27/04/2026  
**Status:** Aprovado  
**Autor:** Ediney Magalhães

## Contexto
O bloco 7 do relatório exige visualização de 4 indicadores clínicos (Queda, 
Lesão de Pele, Erro de Medicação e Flebite). O modelo do relatório pede um 
gráfico comparativo geral entre trimestres e seções individuais por indicador.
As metas de cada indicador mudam anualmente, tornando inviável fixá-las no código.

## Decisão
Adotar dois tipos de gráfico complementares no bloco 7:

**1. Gráfico Geral (barras agrupadas)**
- Exibe os 4 indicadores lado a lado
- Compara trimestre anterior vs trimestre atual
- Meta de cada indicador representada por um ponto (marcador) sobre as barras
- Valores de meta inseridos pelo analista via Streamlit — sem manutenção no código

**2. Gráfico Individual por Indicador (linhas)**
- Um gráfico por indicador
- Série temporal mês a mês: ano atual vs ano anterior
- Meta representada por linha horizontal tracejada de janeiro a dezembro
- Função `gerar_grafico_bloco7` já implementada cobre esse caso

## Consequências
- Metas desacopladas do código — manutenção zero a cada virada de ano
- O gráfico geral exige uma nova função no `visualizador.py`
- O Streamlit precisará de campos de entrada para as 4 metas no bloco 7
- As duas funções são independentes e podem evoluir separadamente