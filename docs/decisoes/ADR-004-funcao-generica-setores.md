# ADR-004: Função Genérica para Análise por Setor

**Data:** 24/04/2026  
**Status:** Aprovado  
**Autor:** Ediney Magalhães

## Contexto

Os blocos 5 e 6 do relatório analisam respectivamente os setores 
notificantes e os setores notificados. A estrutura de cálculo dos dois 
blocos é idêntica — top 3 com frequência e percentual por trimestre atual 
e anterior, mais dataset de descrições para a IA.

## Decisão

Criar uma única função genérica `preparar_bloco_setores` que recebe a 
coluna como parâmetro em vez de duplicar o código em duas funções separadas.

```python
preparar_bloco_setores(df_atual, df_anterior, coluna)
```

Para o bloco 5 passa-se `COL_SETOR` (setor notificante).  
Para o bloco 6 passa-se `COL_SETOR_RESPONSAVEL` (setor notificado).

## Justificativa

Aplicação do princípio DRY — Don't Repeat Yourself. Código duplicado 
é dívida técnica: quando a lógica muda, exige correção em múltiplos 
lugares com risco de inconsistência.

## Consequências

- Manutenção centralizada — mudanças na lógica afetam os dois blocos 
  automaticamente
- Padrão extensível — novos blocos de análise por setor podem reutilizar 
  a mesma função
- Assinatura explícita — quem chama a função define qual dimensão analisar