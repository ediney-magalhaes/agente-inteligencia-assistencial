# ADR-013: Deploy em Rede Local

**Data:** 04/05/2026

**Status:** Aprovado

**Autor:** Ediney Magalhães

## Contexto

O sistema processa dados de notificações hospitalares — classificados como
dados sensíveis pela LGPD. Avaliar deploy externo via Streamlit Community
Cloud levantou riscos de compliance: dados trafegando e sendo processados
fora da infraestrutura do hospital.

## Decisão

Manter o sistema em execução local na rede interna do hospital. O arquivo
Ligar_Painel.bat já está configurado com --server.address 0.0.0.0,
permitindo acesso de outros dispositivos na rede sem instalação adicional.

## Justificativa

Dados de saúde exigem controles específicos de tratamento pela LGPD.
O modelo local garante que os dados nunca saiam da rede hospitalar,
elimina custos de infraestrutura externa e mantém custo zero ao projeto.

## Consequências

- Acesso restrito à rede interna do hospital
- Sistema depende da máquina do operador estar ligada
- Sem necessidade de configuração adicional para outros usuários