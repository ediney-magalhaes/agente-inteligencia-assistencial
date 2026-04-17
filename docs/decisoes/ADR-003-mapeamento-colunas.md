# ADR-003: Mapeamento e Validação de Colunas

**Data:** 17/04/2026  
**Status:** Aprovado  
**Autor:** Ediney Magalhães

## Contexto
O sistema EPIMED reorganiza nomes de colunas entre exportações sem aviso prévio — problema conhecido como schema drift. Isso causou falhas nos Blocos 5 e 6 na execução do 1º Trimestre de 2026, exigindo correção manual no código para cada coluna divergente encontrada.

## Decisão
Criar um dicionário central de mapeamento de colunas no `utils.py`. Ele define o nome interno esperado pelo sistema e lista todos os nomes alternativos já observados nas exportações do EPIMED.

Uma função de validação executará esse mapeamento automaticamente logo após o carregamento de qualquer planilha — antes de qualquer análise.

## Colunas mapeadas

| Nome interno (esperado) | Alternativas conhecidas |
|---|---|
| `Data da notificação` | — |
| `Classificação da Notificação` | — |
| `Taxonomia da OMS` | `Taxonomia` |
| `Setor Responsável` | `Responsável` |
| `Grau do dano` | — |
| `Incidente` | — |
| `Turno` | — |
| `Descrição do incidente` | — |
| `Assistencial/ Administrativo/ Apoio` | — |

## Colunas removidas
| Coluna | Motivo |
|---|---|
| `Servico Proprio / Servico tercerizado` | Não contemplada no novo Modelo Relatório |

## Consequências
- Mudanças no EPIMED exigem atualização apenas do dicionário no `utils.py`
- O restante do sistema permanece sem alteração
- Erros de coluna passam a ser detectados na entrada com mensagem clara
- O arquivo `inspecionar.py` criado durante o diagnóstico deve ser removido