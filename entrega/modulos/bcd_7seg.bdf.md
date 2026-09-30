# bcd_7seg.bdf

## Objetivo

Decodifica um nibble BCD em sete linhas de display ativas em zero.

## Entradas e saídas

`BCD[3:0]` é o dígito de entrada. `SEG[6:0]={g,f,e,d,c,b,a}` é a saída; `SEG[0]` controla o segmento a.

## Funcionamento

As dez entradas válidas usam a tabela convencional para display de cátodo comum com polaridade ativa em zero. Códigos 10 a 15 produzem `1111111`, apagando todos os segmentos. As funções foram reduzidas por Quine–McCluskey sobre a tabela completa de 16 linhas. Os mintermos 10 a 15 são especificados como 1 em todas as saídas e não são tratados como don't-cares.

## Exemplo

`BCD=4'b0010` (dígito 2) produz `SEG=7'b0100100`.

## Verificação

`bcd_7seg.bdf` passou pela análise do Quartus 21.1 sem erros nem avisos e foi convertido para HDL. `tb_bcd_7seg.sv`, executado com Icarus Verilog 13.0 sobre o HDL convertido, passou nos 16 códigos contra tabela literal independente. O log está em `docs/logs/sim_bcd_7seg.log`; o VCD está em `simulation/waveforms/bcd_7seg.vcd`.
