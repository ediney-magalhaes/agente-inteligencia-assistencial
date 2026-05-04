# ADR-012: Módulo de Exibição de Resultados

**Data:** 04/05/2026
**Status:** Aprovado
**Autor:** Ediney Magalhães

## Contexto

A aba "Resultados" do app.py precisava exibir gráficos, tabelas e análises
de IA organizados por seção. A solução inicial colocava toda essa lógica
diretamente no app.py, repetindo o problema do motor_analise.py — um único
arquivo acumulando responsabilidades de orquestração e exibição.

## Decisão

Criar o módulo resultados.py com uma única função pública: exibir(session_state).
O app.py chama apenas essa função. Toda a lógica de renderização de seções
fica encapsulada no resultados.py.

## Justificativa

Mantém o app.py como orquestrador puro. Mudanças na exibição de qualquer
seção não tocam o app.py. Segue o mesmo princípio de responsabilidade única
aplicado aos módulos processador.py, visualizador.py e agente_ia.py.

## Consequências

- app.py permanece enxuto e estável
- resultados.py é o único ponto de manutenção para exibição
- Novos blocos são adicionados apenas no resultados.py