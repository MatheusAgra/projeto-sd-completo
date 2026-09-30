# somador_1bit.bdf — documentação do circuito

## Objetivo e interface

Implementa um somador completo combinacional de um bit. Entradas escalares A, B e Cin; saídas escalares S e Cout.

## Funcionamento

P=A XOR B; S=P XOR Cin; Cout=(A AND B) OR (P AND Cin). O grafo de portas usa dois XOR, dois AND2 e um OR2, sem constante ou estado.

## Exemplo e limites

A=1, B=1 e Cin=0 produzem S=0 e Cout=1. Com A=B=Cin=1, a saída é 11. Todos os oito padrões de entrada são definidos.

## Dependências

Somente primitivas XOR, AND2 e OR2.

## Verificação

Quartus Prime Lite 21.1.0 concluiu análise do BDF, conversão BDF→Verilog e geração do símbolo: [análise](../docs/logs/somador_1bit_analyze.log), [conversão](../docs/logs/somador_1bit_convert.log) e [símbolo](../docs/logs/somador_1bit_symbol.log), cada etapa com zero erros e zero avisos. O HDL exportado nativamente foi executado no Icarus pelo testbench independente: PASS — 8 casos. A referência soma os inteiros A+B+Cin e compara S e Cout. Resultado registrado em [sim_somador_1bit.log](../docs/logs/sim_somador_1bit.log); o VCD foi aberto e salvo em [somador_1bit.vcd](../simulation/waveforms/somador_1bit.vcd).

Esses registros validam o BDF analisado e o HDL que o Quartus exportou nesta revisão; não afirmam teste físico na placa.
