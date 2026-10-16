# ADR-019: Anonimização do Texto Antes do Envio à API Externa

**Data:** 16/10/2026

**Status:** Aprovado

**Autor:** Ediney Magalhães

## Contexto

A ADR-016 decidiu manter a API externa (Gemini) como ponto de partida,
com anonimização do texto livre antes de qualquer envio, registro do que
é enviado e coleta apenas dos dados necessários. Ela não registrou o
método de anonimização nem seus limites.

O texto livre das notificações pode conter nomes de pacientes e de
profissionais, CPF, telefone e e-mail. Esta ADR registra como a
anonimização foi implementada (SEG-02), como o envio é auditado
(SEG-04) e quais riscos permanecem. Ela recebe o número 019 porque a 018
está reservada para a implantação em nuvem (IMP-07).

## Decisão

1. **Ponto único de saída.** Todo envio à API passa por `chamar_gemini`,
   que anonimiza o prompt completo antes de qualquer tentativa de envio.
2. **Anonimização em camadas**, aplicadas em ordem:
   - Expressões regulares para CPF, telefone, e-mail e números longos.
   - Palavras-gatilho (parentesco, tratamento e função) seguidas de até
     duas palavras, tratadas como nome. Uma lista de palavras comuns
     impede que verbos, preposições e conjunções sejam confundidos com
     nome.
   - Modelo de linguagem em português (spaCy, `pt_core_news_sm`) para
     entidades de pessoa. O texto é normalizado em capitalização para o
     reconhecimento, e só são removidos os trechos classificados como
     nome próprio na versão em minúsculas.
3. **Falha fechada.** Se a anonimização gerar erro, nada é enviado. O
   envio nunca recorre ao texto original.
4. **Registro de auditoria.** Cada envio gera uma linha de log com a
   origem (bloco), a quantidade de itens removidos por camada e o
   tamanho do texto. O texto nunca é gravado no log. Um teste
   automatizado garante essa regra.
5. **Testes com texto fictício.** O repositório é público, então os
   testes usam apenas texto inventado. Cada falso positivo encontrado
   em instruções de prompt ganha um teste de regressão.

Detalhes de conformidade que não devam ser públicos ficam fora do
repositório, conforme a regra 7 da ADR-015.

## Justificativa

- **Somente reconhecimento de entidades (spaCy).** Foi medido e
  descartado como solução única: em texto em letras maiúsculas, que é
  comum nas notificações, o modelo marcou palavras comuns como nome e
  incluiu verbos na entidade. Por isso entra como última camada, com
  filtro por classe gramatical.
- **Somente expressões regulares.** Cobrem bem dados com formato fixo
  (CPF, telefone, e-mail), mas não nomes sem palavra-gatilho.
- **Presidio.** Não foi adotado nesta etapa, pelo peso das dependências
  e porque as camadas atuais cobrem o escopo da Fase 1. Pode ser
  reavaliado.

A combinação em camadas usa o que cada técnica faz melhor, roda
localmente e não tem custo, o que respeita a premissa de custo zero.

## Consequências

- O envio à API depende do carregamento do modelo spaCy (versão fixada em
  `requirements.txt`) e de uma etapa extra de instalação no CI.
- **Riscos que permanecem.** A anonimização reduz o risco, mas não o
  elimina:
  - Nomes sem palavra-gatilho que o modelo não reconheça (nomes raros,
    grafias incomuns, texto em letras maiúsculas) podem passar.
  - Combinações de informações indiretas (data, setor e circunstâncias
    do evento) podem permitir a identificação de uma pessoa mesmo sem
    nome.
  - A lista de palavras comuns exige manutenção. Um falso positivo pode
    alterar uma instrução do prompt. A medição sobre os prompts atuais
    encontrou uma ocorrência, já corrigida e coberta por teste.
- **Monitoramento.** A contagem de nomes encontrados pelo spaCy é
  revisada na regeneração do relatório. Em prompts de dados agregados,
  valor acima de zero é investigado.
- Evoluções previstas: lista de primeiros nomes como camada adicional e
  o alvo híbrido da ADR-016, com o texto livre processado em modelo
  local (IA-10).