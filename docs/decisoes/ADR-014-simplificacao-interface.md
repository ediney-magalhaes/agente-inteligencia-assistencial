# ADR-014: Simplificação da Interface

**Data:** 04/05/2026

**Status:** Aprovado

**Autor:** Ediney Magalhães

## Contexto

O app.py original tinha cinco subabas: Configuração, Dados EPIMED,
Imagens, Inserir Dados e Gerar Relatório. Com a mudança de arquitetura
— resultados exibidos na interface em vez de geração de Word — as abas
Imagens e Inserir Dados perderam sua função principal.

## Decisão

Remover as abas Imagens e Inserir Dados. Manter apenas Configuração,
Dados EPIMED e Resultados.

## Justificativa

As imagens do EPIMED são carregadas diretamente nos blocos relevantes
da aba Resultados. Os textos manuais são preenchidos diretamente no
documento Word pelo profissional responsável. Abas sem função geram
ruído na interface e confundem o usuário.

## Consequências

- Interface mais limpa e objetiva
- Uploads de imagens do EPIMED migram para a aba Resultados se necessário
- Textos manuais permanecem responsabilidade do profissional no Word