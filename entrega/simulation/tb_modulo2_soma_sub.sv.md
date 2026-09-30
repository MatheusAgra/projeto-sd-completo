# tb_modulo2_soma_sub.sv

Testbench SystemVerilog do módulo `modulo2_soma_sub`. A comparação esperada vem de um modelo independente baseado em inteiros, não das equações do grafo. O modelo decodifica A_C2 e B_C2 como inteiros de −15 a +15, calcula soma ou subtração e codifica sinal/magnitude normalizados.

## Resultado executado

Icarus executou este testbench contra o Verilog exportado nativamente pelo Quartus a partir do BDF `modulo2_soma_sub`: **PASS, 1922 casos**. Consulte [`sim_modulo2_soma_sub.log`](../docs/logs/sim_modulo2_soma_sub.log). O log registra que o VCD abriu e foi salvo em [`waveforms/modulo2_soma_sub.vcd`](waveforms/modulo2_soma_sub.vcd). A análise, conversão BDF→Verilog e geração de símbolo da revisão estão em [`modulo2_soma_sub_analyze.log`](../docs/logs/modulo2_soma_sub_analyze.log), [`modulo2_soma_sub_convert.log`](../docs/logs/modulo2_soma_sub_convert.log) e [`modulo2_soma_sub_symbol.log`](../docs/logs/modulo2_soma_sub_symbol.log).
