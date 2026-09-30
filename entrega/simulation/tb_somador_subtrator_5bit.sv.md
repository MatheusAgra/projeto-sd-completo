# tb_somador_subtrator_5bit.sv

Testbench SystemVerilog do módulo `somador_subtrator_5bit`. A comparação esperada vem de um modelo independente baseado em inteiros, não das equações do grafo. O modelo calcula A+(B XOR {5{SUB}})+SUB como inteiro e compara os cinco bits baixos de R e Cout.

## Resultado executado

Icarus executou este testbench contra o Verilog exportado nativamente pelo Quartus a partir do BDF `somador_subtrator_5bit`: **PASS, 2048 casos**. Consulte [`sim_somador_subtrator_5bit.log`](../docs/logs/sim_somador_subtrator_5bit.log). O log registra que o VCD abriu e foi salvo em [`waveforms/somador_subtrator_5bit.vcd`](waveforms/somador_subtrator_5bit.vcd). A análise, conversão BDF→Verilog e geração de símbolo da revisão estão em [`somador_subtrator_5bit_analyze.log`](../docs/logs/somador_subtrator_5bit_analyze.log), [`somador_subtrator_5bit_convert.log`](../docs/logs/somador_subtrator_5bit_convert.log) e [`somador_subtrator_5bit_symbol.log`](../docs/logs/somador_subtrator_5bit_symbol.log).
