# ADR-008: Gerador de Relatório

**Data:** 27/04/2026  
**Status:** Aprovado  
**Autor:** Ediney Magalhães

## Contexto
Com o `processador.py` e `visualizador.py` completos, o projeto precisa de um 
orquestrador que conecte todas as camadas e produza o documento Word final 
seguindo a estrutura do Modelo Relatório.

## Decisão
Criar o `gerador.py` como camada de orquestração responsável por:

1. Chamar o `processador.py` para preparar os dados de cada bloco
2. Chamar o `visualizador.py` para gerar os gráficos
3. Inserir gráficos, tabelas e textos no documento Word seguindo o Modelo Relatório
4. Salvar o arquivo final com nomenclatura padronizada

## Responsabilidades do gerador.py
- Não realiza cálculos — delega ao processador
- Não gera gráficos — delega ao visualizador
- Não gera textos de análise — delega ao agente_ia.py
- Apenas orquestra e monta o documento final

## Consequências
- O `app.py` passa a chamar apenas o `gerador.py` — ponto único de entrada
- Mudanças no modelo do relatório exigem alteração apenas no `gerador.py`
- O sistema fica preparado para gerar relatórios de diferentes trimestres 
  sem alteração no código