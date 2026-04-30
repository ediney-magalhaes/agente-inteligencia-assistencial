# ADR-011: Execução sob Demanda das Análises de IA

**Data:** 30/04/2026

**Status:** Aprovado

**Autor:** Ediney Magalhães

## Contexto

O agente_ia.py realiza chamadas à Gemini API para cada seção do relatório.
O relatório possui aproximadamente 13 chamadas de API por execução completa.

Disparar todas as chamadas simultaneamente representa dois riscos:

- Estouro do limite de RPM (10 requisições por minuto no free tier)
- Consumo excessivo de tokens em prompts com múltiplos DataFrames,
  podendo atingir o limite de 250.000 TPM em uma única execução

Além disso, gerar todas as análises de uma vez impede que o usuário
revise e valide cada texto antes de prosseguir para o próximo bloco.

## Decisão

As análises textuais geradas pela IA serão acionadas individualmente
pelo usuário através de botões na interface Streamlit — uma por seção.

O fluxo da interface será:

1. Usuário carrega os arquivos e clica em "Processar Dados"
2. O sistema roda o processador.py e exibe os gráficos de todos os blocos
3. Para cada bloco, um botão "Gerar Análise" aciona a função correspondente
   do agente_ia.py
4. O texto gerado aparece abaixo do gráfico e fica disponível para o
   gerador.py inserir no documento Word

## Impacto no app.py

- Cada seção do relatório terá um botão independente de geração de análise
- O texto gerado é armazenado no st.session_state para persistir entre
  interações sem nova chamada à API
- O usuário pode reprocessar uma análise específica sem afetar as demais
- O botão "Gerar Documento Word" só será habilitado após todas as análises
  obrigatórias estarem presentes no session_state

## Impacto no gerador.py

- O gerador.py receberá os textos já prontos como parâmetros — não fará
  chamadas à API diretamente
- Textos ausentes (seções não analisadas) serão sinalizados com
  [PREENCHER MANUALMENTE] no documento Word gerado

## Consequências

- Controle total do usuário sobre o ritmo de consumo da API
- Revisão incremental — cada análise é validada antes de prosseguir
- Reprocessamento seletivo — apenas a análise com problema é refeita
- Limitação documentada: o documento Word só estará completo após o
  usuário acionar todas as análises