# Agente de Inteligência Assistencial

Sistema de automação para elaboração do Relatório Trimestral de Segurança do 
Paciente em ambiente hospitalar, desenvolvido com Python e IA generativa.

---

## Contexto

A elaboração do relatório trimestral envolvia consolidação manual de múltiplas 
planilhas, cruzamentos estatísticos, construção de gráficos e redação técnica 
interpretativa. O ciclo completo consumia aproximadamente 30 dias de trabalho.

---

## Solução

O sistema automatiza o pipeline completo de dados — da ingestão ao relatório — 
estruturado em módulos especializados e alinhado ao modelo institucional de 
relatório de segurança do paciente.

O fluxo de trabalho é:

1. Usuário exporta as planilhas do sistema MV e carrega na interface
2. O sistema valida, padroniza e processa os dados por bloco analítico
3. Gráficos, tabelas e análises textuais são gerados automaticamente
4. O profissional utiliza os outputs para consolidar o relatório final

O sistema não substitui a análise humana. Ele automatiza a etapa operacional 
e entrega diagnóstico técnico estruturado para validação e decisão.

---

## Impacto

- Geração dos outputs em aproximadamente 5 minutos
- Consolidação e conclusão do relatório em 2 a 3 horas
- Redução de aproximadamente 30 dias para menos de um dia de trabalho
- Análise padronizada e replicável a cada trimestre

---

## Arquitetura
```
├── app.py              # Interface Streamlit — entrada de dados e exibição
├── processador.py      # Preparação e cálculo dos dados por bloco analítico
├── utils.py            # Padronização e mapeamento de colunas entre versões
├── motor_analise.py    # Regras de negócio e geração de análise via IA
├── gerador_graficos.py # Geração dos gráficos por bloco (em desenvolvimento)
├── Ligar_Painel.bat    # Script de inicialização do servidor local
└── docs/               # Documentação técnica e decisões de arquitetura (ADRs)
```
## Fluxo de Dados
```
Planilha Excel (EPIMED / MV)
↓
utils.py — validação e padronização de colunas
↓
processador.py — cálculo dos blocos analíticos
↓
gerador_graficos.py — visualizações por bloco
↓
motor_analise.py — análise textual via Gemini API
↓
app.py — interface Streamlit para o usuário final
```
## Blocos Analíticos

Cada bloco corresponde a uma seção do modelo institucional de relatório:

| Bloco | Conteúdo |
|-------|----------|
| 1 | Volume de notificações — comparativo trimestral e anual |
| 2 | Distribuição por turno |
| 3 | Classificação das notificações com top 3 por categoria |
| 4 | Eventos adversos — top 3, grau do dano e status de investigação |
| 5 | Setores notificantes |
| 6 | Setores notificados — local de ocorrência |
| 7 | Índices de qualidade — flebite, lesão por pressão, queda, erro de medicação |
| 8 | Cumprimento de análise de notificações |

---

## Segurança e Governança

- Execução centralizada na rede interna hospitalar
- Nenhum dado de paciente é armazenado externamente
- Chave de API inserida em tempo de execução
- Acesso por IP interno — sem exposição à internet

---

## Execução

```bash
Ligar_Painel.bat
```

O servidor Streamlit é iniciado localmente. Usuários da rede interna acessam 
via IP + porta configurada.

---

## Tecnologias

- Python 3
- Streamlit
- Pandas
- Matplotlib
- Google Gemini API

---

## Documentação Técnica

Decisões de arquitetura, justificativas e histórico de mudanças estão 
registrados em `docs/`.

---

Desenvolvido por Ediney Magalhães
Analytics Engineer | Estatístico| Data Engineer