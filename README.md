# 🏥 Agente de Inteligência Assistencial  
### Automação de Relatórios de Segurança do Paciente com Python + NLP

---

## 📌 Contexto

Este projeto foi desenvolvido para otimizar a elaboração do **Relatório Trimestral de Segurança do Paciente** em uma unidade hospitalar.

Antes da implementação do sistema, o processo envolvia:

- Consolidação manual de múltiplas planilhas  
- Cruzamentos estatísticos  
- Construção manual de gráficos  
- Redação técnica interpretativa  
- Revisões sucessivas  

O ciclo completo levava, em média, **cerca de 30 dias de trabalho analítico distribuído para compilação do relatório**.

---

## 🎯 Objetivo

Reduzir drasticamente o tempo de geração do relatório e aumentar:

- 📊 Consistência estatística  
- 🔎 Padronização das análises  
- 📈 Confiabilidade dos indicadores  
- ⚡ Agilidade na tomada de decisão  

---

## 🚀 Resultado Obtido

Com o Agente de Inteligência Assistencial:

- O tempo de elaboração caiu para **poucas horas**
- A análise textual passou a ser **gerada automaticamente**
- A interpretação passou a considerar **variações estatísticas + contexto semântico**
- O processo tornou-se replicável, rastreável e menos dependente de esforço manual

Importante:  
O sistema **não substitui a análise humana**, mas automatiza a etapa operacional e gera um primeiro diagnóstico técnico estruturado.

---

## 🖥️ Interface do Sistema

### Tela Inicial
Upload das bases e configuração dos parâmetros:

![Tela Inicial](tela_inicial.png)

---

### Exemplo de Análise Gerada (DADOS FICTÍCIOS)
Gráficos comparativos + interpretação textual automática com IA:

![Exemplo de Análise](analise_gerada.png)

---

## 🧠 Como Funciona

O sistema executa:

1. **Ingestão de dados (Excel/CSV)**
2. Tratamento e padronização via **Pandas**
3. Cálculo de indicadores estatísticos
4. Geração de gráficos com **Matplotlib**
5. Processamento textual via **Google Gemini API**
6. Consolidação em relatório estruturado dentro da interface

---

## 🏗️ Arquitetura
```bash
├── app.py                # Interface Streamlit
├── motor_analise.py      # Regras de negócio e cálculos
├── utils/                # Funções auxiliares
├── tela_inicial.png      # Screenshot inicial
├── analise_gerada.png    # Screenshot com análise
└── requirements.txt
```



Principais decisões arquiteturais:

- Separação entre interface e motor analítico  
- Scanner dinâmico para modelos da API (resiliência a mudanças)  
- Execução local (compilação .exe) para preservar dados sensíveis  

---

## 🔐 Segurança e LGPD

- O sistema roda **localmente**
- Nenhum dado sensível é armazenado externamente
- A chave da API é inserida pelo usuário no momento da execução
- O executável foi gerado com **PyInstaller** para uso interno

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Streamlit**
- **Pandas**
- **Matplotlib**
- **Google Gemini API (NLP)**
- **PyInstaller**

---

## 📊 Estrutura Analítica do Relatório

O relatório é composto por 11 blocos:

1. Visão Geral
2. Histórico Temporal (5 anos)
3. Classificação de Incidentes
4. Análise por Turno
5. Gravidade e Taxonomia
6. Setores Assistenciais
7. Setores Administrativos
8. Setores de Apoio
9. Indicadores de Qualidade
10. Tratativas e Protocolos
11. Matriz de Risco (incluindo Ishikawa)

---

## 💡 Aprendizados Técnicos

Durante o desenvolvimento:

- Evolução de código monolítico para arquitetura modular
- Tratamento de inconsistências de base histórica
- Ajustes de prompt engineering para análise mais contextual
- Implementação de fallback dinâmico para modelos de IA
- Consolidação de boas práticas de automação analítica em ambiente hospitalar

---

## 📌 Considerações Finais

Este projeto representa a convergência entre:

- Engenharia de Dados  
- Estatística Aplicada  
- Business Analytics  
- IA Generativa  

Mais do que um dashboard, trata-se de um **sistema analítico automatizado aplicado a um problema real de negócio em ambiente de produção**.

---

Desenvolvido por **Ediney Magalhães**  
Analytics Engineer | Estatística Aplicada | Health Analytics

