# ADR-001: Arquitetura em Camadas

**Data:** 17/04/2026  
**Status:** Aprovado  
**Autor:** Ediney Magalhães

## Contexto
O projeto nasceu como scripts soltos no Google Colab e evoluiu para uma aplicação Streamlit com dois arquivos principais: `app.py` e `motor_analise.py`.
O `motor_analise.py` acumulou responsabilidades de leitura, limpeza, cálculo, geração de gráficos e chamadas de IA — tornando a manutenção difícil e o sistema frágil a mudanças na fonte de dados.

## Decisão
Adotar a filosofia de arquitetura em camadas, inspirada no padrão Medalhão, mas com ferramentas proporcionais ao tamanho e contexto do projeto:

- **Camada 1 — Fundação:** Separação de responsabilidades e governança
- **Camada 2 — Dados:** Persistência e histórico com SQLite
- **Camada 3 — Inteligência:** Novos blocos, modelos estatísticos e agente de IA

## Por que não a Medalhão completa?
Ferramentas como Databricks, Delta Lake e Spark são projetadas para escala empresarial e custo elevado. Aplicá-las aqui seria over-engineering — tecnologia maior que o problema. A filosofia foi preservada, as ferramentas 
foram adaptadas ao contexto de custo zero.

## Consequências
- O projeto passa a ter estrutura compreensível por qualquer pessoa que assuma
- Mudanças em uma camada não afetam as outras
- A evolução futura para escala maior fica documentada e justificada