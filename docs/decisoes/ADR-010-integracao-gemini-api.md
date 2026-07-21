# ADR-010: Integração com Gemini API para Geração de Análises Textuais

**Data:** 30/04/2026

**Status:** Aprovado

**Autor:** Ediney Magalhães

## Contexto

O gerador.py precisa inserir textos de análise clínica em cada seção do 
relatório trimestral. Esses textos não podem ser gerados por lógica 
determinística — exigem linguagem natural com raciocínio clínico, 
interpretação de variações e recomendações contextualizadas.

A arquitetura do projeto prevê um módulo dedicado (agente_ia.py) 
responsável por toda comunicação com um modelo de linguagem externo.

## Decisão

Usar a Gemini API (Google AI Studio) via biblioteca google-generativeai.

| Decisão | Escolha | Justificativa |
|---|---|---|
| Provedor | Google Gemini | Free tier generoso, sem cartão de crédito |
| Modelo | gemini-2.5-flash | Equilíbrio entre capacidade e limites do free tier |
| Autenticação | Chave API via .env | Padrão da indústria, nunca exposta no repositório |
| Leitura da chave | os.getenv() via python-dotenv | Universal, independente de framework |

## Gerenciamento de Segredos

- Chave armazenada exclusivamente no arquivo `.env` na raiz do projeto
- `.env` listado no `.gitignore` — nunca vai ao repositório
- Leitura via `os.getenv('GEMINI_API_KEY')` no início do agente_ia.py
- A interface Streamlit não solicita mais a chave ao usuário — carregada 
  automaticamente na inicialização do sistema

## Limites do Free Tier (referência para manutenção futura)

| Modelo | RPM | RPD | TPM |
|---|---|---|---|
| gemini-2.5-pro | 5 | 100 | 250.000 |
| gemini-2.5-flash | 10 | 500 | 250.000 |
| gemini-2.5-flash-lite | 15 | 1.000 | 250.000 |

O relatório trimestral realiza aproximadamente 10 chamadas por execução.
Com 500 RPD, o sistema suporta até 50 execuções completas por dia —
suficiente para uso interno hospitalar.

Atenção: o RPD reseta à meia-noite no horário do Pacífico (04h de Brasília).

## Consequências

- O agente_ia.py é o único módulo que se comunica com a API — nenhum 
  outro módulo faz chamadas diretas
- Mudanças de modelo ou provedor exigem alteração apenas no agente_ia.py
- O sistema falha graciosamente se a chave não estiver no .env — 
  o gerador.py deve tratar esse cenário com mensagem clara ao usuário
- Limitação documentada: se o RPD for atingido, o sistema não consegue 
  gerar análises textuais até o reset às 04h de Brasília