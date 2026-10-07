# ADR-016: Onde o Texto das Notificações é Processado

**Data:** 07/10/2026

**Status:** Aprovado

**Autor:** Ediney Magalhães

## Contexto

As análises narrativas do relatório são geradas por um modelo de
linguagem acessado por API externa (Gemini). Usar uma API externa
significa que parte do conteúdo das notificações sai da rede do
hospital, enquanto a ADR-013 parte da premissa de execução local. Esse
envio é uma exceção que ainda não estava registrada em ADR.

As notificações têm campos de texto livre (descrições do incidente,
fatores contribuintes, planos de ação) que podem conter informações
sobre pacientes e sobre profissionais. O roadmap prevê ampliar o uso
desse texto nas fases seguintes (busca semântica, RAG, classificação
por LLM e agente), o que torna a decisão necessária antes dessa
ampliação.

## Decisão

O processamento do texto das notificações evolui em duas etapas:

1. **Ponto de partida:** manter o uso de API externa, com anonimização
   do texto livre antes de qualquer envio (SEG-02), registro do que é
   enviado (SEG-04) e coleta apenas dos dados necessários (ING-09).
2. **Alvo:** arquitetura híbrida. Apenas dados agregados vão à API
   externa. O processamento do texto livre (embeddings, classificação,
   RAG sobre descrições e planos de ação) fica em modelo executado
   localmente (IA-10).

Detalhes de conformidade que não devam ser públicos ficam fora do
repositório, conforme a regra 7 da ADR-015.

## Justificativa

Foram consideradas três direções:

- **API externa com anonimização.** Mantém o que já funciona e tem custo
  baixo, mas ainda envia dados para fora da rede e depende da qualidade
  da anonimização. Por isso é o ponto de partida, e não o destino.
- **Somente modelo local.** Nenhum dado sai da rede. Exige hardware
  adequado, e a qualidade dos textos tende a ser menor.
- **Híbrido.** Reduz a exposição, porque o texto livre fica em ambiente
  controlado, e mantém a qualidade da API nas análises sobre dados
  agregados. Exige operar um modelo local.

A prática comum em organizações com dados sensíveis combina
classificação do dado, anonimização antes do envio, contrato
corporativo com o provedor, registro de auditoria e revisão humana. A
decisão segue essa linha e permite avançar por etapas, sem esperar pelo
hardware do modelo local.

## Consequências

- Os itens SEG-02, SEG-03 (injeção de prompt), SEG-04 e ING-09 passam a
  ser pré-requisito para ampliar o uso de texto livre em IA
- A subetapa de modelo local e roteamento (IA-10 e IA-11) só é
  confirmada depois do teste de viabilidade no hardware disponível
- Se uma mudança de contexto exigir outra direção (por exemplo, outra
  regra do provedor ou nova orientação da instituição), esta ADR é
  substituída por uma nova, e o status desta é atualizado
- O erro E-08 do estado atual permanece aberto até a conclusão dessas
  etapas