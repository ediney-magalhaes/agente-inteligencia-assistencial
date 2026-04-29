# ADR-009 — Interface Streamlit e Ordem de Desenvolvimento

**Data:** 29/04/2026
**Status:** Aprovado
**Autor:** Ediney Magalhães

## Contexto
O sistema precisa coletar dados de duas naturezas distintas antes de gerar
o documento Word final:

1. Dados automáticos — processados a partir das planilhas EPIMED
2. Dados manuais — imagens de gráficos externos, textos de comissões,
   planos de ação e auditorias que não existem no EPIMED

Sem uma interface, esses dados manuais precisariam ser inseridos diretamente
no Word após a geração — eliminando o benefício da automação e introduzindo
risco de inconsistência no documento final.

## Decisão
Adotar o Streamlit como interface do sistema, organizada em três abas:

- Relatório — coleta de dados e geração do Word
- Painel Epidemiológico — análises estatísticas avançadas (Fase 3)
- Agente IA — chat com os dados (Fase 5)

O `app.py` passa a ser o ponto de entrada único do sistema.
O `gerador.py` é escrito DEPOIS do `app.py` porque depende de conhecer
a estrutura dos dados que a interface vai entregar.

## Consequências
- O `gerador.py` recebe dados via parâmetros vindos do `app.py`
- Seções manuais são coletadas na interface e inseridas automaticamente
- Imagens externas (EPIMED, ROPs, Óbitos) são recebidas via upload
- O sistema elimina a necessidade de edição manual do Word após geração
- Streamlit adicionado ao requirements.txt