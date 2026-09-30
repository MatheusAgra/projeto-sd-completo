# tb_somador_1bit.sv

Testbench SystemVerilog do módulo `somador_1bit`. A comparação esperada vem de um modelo independente baseado em inteiros, não das equações do grafo. O modelo soma os inteiros A+B+Cin e compara S e Cout.

## Resultado executado

Icarus executou este testbench contra o Verilog exportado nativamente pelo Quartus a partir do BDF `somador_1bit`: **PASS, 8 casos**. Consulte [`sim_somador_1bit.log`](../docs/logs/sim_somador_1bit.log). O log registra que o VCD abriu e foi salvo em [`waveforms/somador_1bit.vcd`](waveforms/somador_1bit.vcd). A análise, conversão BDF→Verilog e geração de símbolo da revisão estão em [`somador_1bit_analyze.log`](../docs/logs/somador_1bit_analyze.log), [`somador_1bit_convert.log`](../docs/logs/somador_1bit_convert.log) e [`somador_1bit_symbol.log`](../docs/logs/somador_1bit_symbol.log).
