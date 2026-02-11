# 🏥 Agente de Inteligência Assistencial  
### Automação de Relatórios de Segurança Hospitalar

## 📌 Contexto

Este projeto foi desenvolvido para automatizar a elaboração de relatórios trimestrais de incidentes assistenciais em ambiente hospitalar.

Tradicionalmente, a consolidação do relatório envolvia:

- Coleta manual de múltiplas planilhas  
- Cruzamento estatístico de indicadores  
- Construção de gráficos históricos  
- Redação técnica explicando variações  

O processo demandava esforço operacional significativo e apresentava risco de inconsistências manuais.

---

## 🎯 Objetivo

Reduzir o tempo de consolidação e padronizar a análise, automatizando:

- ETL e consolidação de bases  
- Geração de indicadores estatísticos  
- Séries históricas e gráficos  
- Análise textual assistida por IA para interpretação de variações  

---

## 🧠 Arquitetura da Solução

O sistema foi desenvolvido em arquitetura modular:

- `app.py` → Interface Streamlit  
- `motor_analise.py` → Motor de processamento e cálculos  
- Engine analítica baseada em Pandas  
- Integração com API Gemini para análise semântica  

O deploy ocorre localmente via compilação com PyInstaller, garantindo que dados sensíveis permaneçam na rede interna.

---

## ⚙️ Stack Tecnológica

- Python 3.x  
- Streamlit  
- Pandas  
- Matplotlib  
- Google Gemini API  
- PyInstaller  

---

## 📊 Funcionalidades Principais

- Consolidação automatizada de notificações  
- Análise de séries temporais (5 anos)  
- Cruzamento por turno, setor e gravidade  
- Indicadores assistenciais (queda, LPP, flebite, etc.)  
- Geração assistida de análise textual executiva  
- Geração automática de matriz de risco (Ishikawa)  

---

## 🔐 Considerações de Segurança

- Dados processados localmente  
- Nenhum armazenamento externo de informações sensíveis  
- Chave de API inserida manualmente pelo usuário  
- Projeto demonstrado com dados fictícios  

---

## 🚀 Resultado

Redução significativa do tempo de elaboração do relatório e maior padronização analítica para suporte à tomada de decisão.

---

📌 Desenvolvido por **Ediney Magalhães**  
Analytics Engineer | Estatística Aplicada
