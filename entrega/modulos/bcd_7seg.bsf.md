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
