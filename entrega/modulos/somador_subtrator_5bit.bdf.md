# somador_subtrator_5bit.bdf — documentação do circuito

## Objetivo e interface

Bloco estrutural de soma/subtração de cinco bits, útil em caminhos que precisam de carry de largura cinco. A[4:0], B[4:0], SUB entram; R[4:0] e Cout saem.

## Funcionamento

BX[i]=B[i] XOR SUB em cada bit; o carry inicial é SUB. Cinco instâncias de somador_1bit implementam A+BX+SUB. O resultado R é módulo 32 e Cout registra o sexto bit do cálculo transformado.

## Exemplo e limites

A=00101, B=00011, SUB=1 produz R=00010 e Cout=1. O carry é esperado porque 5+~3+1=34. Todos os padrões são definidos: 32×32×2. A interpretação de carry é unsigned da operação transformada; não equivale a overflow signed.

## Dependências

Cinco XOR e cinco instâncias de somador_1bit.

## Verificação

Quartus Prime Lite 21.1.0 concluiu análise do BDF, conversão BDF→Verilog e geração do símbolo: [análise](../docs/logs/somador_subtrator_5bit_analyze.log), [conversão](../docs/logs/somador_subtrator_5bit_convert.log) e [símbolo](../docs/logs/somador_subtrator_5bit_symbol.log), cada etapa com zero erros e zero avisos. O HDL exportado nativamente foi executado no Icarus pelo testbench independente: PASS — 2048 casos. A referência calcula A+(B XOR {5{SUB}})+SUB como inteiro e compara os cinco bits baixos de R e Cout. Resultado registrado em [sim_somador_subtrator_5bit.log](../docs/logs/sim_somador_subtrator_5bit.log); o VCD foi aberto e salvo em [somador_subtrator_5bit.vcd](../simulation/waveforms/somador_subtrator_5bit.vcd).

Esses registros validam o BDF analisado e o HDL que o Quartus exportou nesta revisão; não afirmam teste físico na placa.
