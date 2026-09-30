# tb_negador_c2_6bit.sv

Testbench SystemVerilog do módulo `negador_c2_6bit`. A comparação esperada vem de um modelo independente baseado em inteiros, não das equações do grafo. O modelo nega o valor inteiro do padrão e compara os seis bits módulo 64, incluindo o ponto fixo −32.

## Resultado executado

Icarus executou este testbench contra o Verilog exportado nativamente pelo Quartus a partir do BDF `negador_c2_6bit`: **PASS, 64 casos**. Consulte [`sim_negador_c2_6bit.log`](../docs/logs/sim_negador_c2_6bit.log). O log registra que o VCD abriu e foi salvo em [`waveforms/negador_c2_6bit.vcd`](waveforms/negador_c2_6bit.vcd). A análise, conversão BDF→Verilog e geração de símbolo da revisão estão em [`negador_c2_6bit_analyze.log`](../docs/logs/negador_c2_6bit_analyze.log), [`negador_c2_6bit_convert.log`](../docs/logs/negador_c2_6bit_convert.log) e [`negador_c2_6bit_symbol.log`](../docs/logs/negador_c2_6bit_symbol.log).
