# ADR-005: Triagem por IA para Indicadores sem Filtro Determinístico

**Data:** 24/04/2026  
**Status:** Aprovado  
**Autor:** Ediney Magalhães

## Contexto

Alguns indicadores de qualidade — erro de medicação, flebite e lesão por 
pressão — não podem ser identificados com precisão por filtros fixos de 
palavra-chave ou valores de coluna. Os motivos são:

- Erro de medicação abrange toda a cadeia de suprimentos — compra, 
  armazenamento, dispensação e administração — sem um campo único que 
  capture todos os casos
- Flebite pode aparecer apenas na descrição do incidente, sem nenhuma 
  referência nas colunas de classificação
- Lesão por pressão tem variações de nomenclatura e a distinção entre 
  adquirida e admitida fica na nota do classificador em texto livre

## Decisão

Não usar filtros determinísticos por palavra-chave para esses indicadores. 
Em vez disso, preparar um dataset estruturado com as colunas relevantes e 
passar para a IA identificar os candidatos e montar a tabela filtrada para 
validação do analista.

Funções criadas:
- `preparar_dataset_ia(df_atual)` — dataset genérico para medicação e flebite
- `preparar_dataset_ia_LPP(df_atual)` — dataset filtrado por categoria de 
  pele para lesão por pressão

## Justificativa

Filtros fixos em registros clínicos têm alta taxa de falsos negativos — 
casos reais que escapam por variação de linguagem, erro de digitação ou 
classificação incorreta do notificante. A IA lida com variação de linguagem 
naturalmente e produz triagem mais abrangente.

O analista mantém a decisão final — a IA apresenta os candidatos, o 
humano valida o que entra na contagem.

## Consequências

- Maior cobertura de casos — reduz falsos negativos
- Decisão humana preservada — o sistema não classifica automaticamente
- Dependência da qualidade do modelo de IA — prompts precisam ser bem 
  construídos no agente_ia.py
- Limitação documentada — casos sem nenhuma referência em nenhuma coluna 
  ou descrição continuam não identificáveis