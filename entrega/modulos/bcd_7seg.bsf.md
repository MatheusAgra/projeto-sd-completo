## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# bcd_7seg.bsf

## Objetivo

Símbolo gráfico da entidade `bcd_7seg`.

## Entradas e saídas

Uma entrada de quatro bits, `BCD[3:0]`, e uma saída de sete bits, `SEG[6:0]`.

## Funcionamento

O BSF apenas apresenta as portas da entidade. A tabela, a polaridade ativa em zero e a implementação por portas estão no BDF correspondente; o símbolo não substitui a lógica.

## Exemplo

A entrada BCD para o dígito 8 deve expor `SEG=0000000`, com os sete segmentos acesos.

## Verificação

O Quartus gerou o símbolo a partir do HDL convertido do BDF. Nomes, direções e larguras foram comparados com `interfaces.json`. A verificação funcional executada é a do HDL convertido do BDF; o BSF apenas representa as portas e não contém lógica.
