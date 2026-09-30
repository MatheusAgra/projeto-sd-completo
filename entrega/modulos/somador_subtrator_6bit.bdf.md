# somador_subtrator_6bit.bdf — documentação do circuito

## Objetivo e interface

Soma ou subtrai dois vetores de seis bits usando complemento de dois e ripple carry. A[5:0], B[5:0] e SUB escalares de controle entram; R[5:0] e Cout saem.

## Funcionamento

Para cada i, BX[i]=B[i] XOR SUB. Se SUB=0, a cadeia calcula A+B; se SUB=1, calcula A+~B+1. O primeiro carry é SUB. Seis instâncias de somador_1bit produzem cada R[i] e propagam Cout. Cout é o carry aritmético sem sinal do cálculo transformado, não é sinal nem overflow signed.

## Exemplo e limites

A=000101, B=000011 e SUB=1 calculam 5−3=2, logo R=000010. A=111111, B=000001 e SUB=0 resulta em 000000 com Cout=1. As 8192 combinações de entradas são definidas módulo 64. Para valores C2 válidos da ULA (−15..+15), a soma/subtração varia de −30 a +30 e cabe em seis bits.

## Dependências

Seis XOR e seis instâncias de somador_1bit.

## Verificação

Quartus Prime Lite 21.1.0 concluiu análise do BDF, conversão BDF→Verilog e geração do símbolo: [análise](../docs/logs/somador_subtrator_6bit_analyze.log), [conversão](../docs/logs/somador_subtrator_6bit_convert.log) e [símbolo](../docs/logs/somador_subtrator_6bit_symbol.log), cada etapa com zero erros e zero avisos. O HDL exportado nativamente foi executado no Icarus pelo testbench independente: PASS — 8192 casos. A referência independente calcula A+(B XOR {6{SUB}})+SUB como inteiro e compara os seis bits de R e Cout. Resultado registrado em [sim_somador_subtrator_6bit.log](../docs/logs/sim_somador_subtrator_6bit.log); o VCD foi aberto e salvo em [somador_subtrator_6bit.vcd](../simulation/waveforms/somador_subtrator_6bit.vcd).

Esses registros validam o BDF analisado e o HDL que o Quartus exportou nesta revisão; não afirmam teste físico na placa.
