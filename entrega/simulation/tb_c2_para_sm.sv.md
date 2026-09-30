# tb_c2_para_sm.sv

Testbench SystemVerilog do módulo `c2_para_sm`. A comparação esperada vem de um modelo independente baseado em inteiros, não das equações do grafo. O modelo decodifica cada R como inteiro signed e compara sinal/magnitude. Para −32, fora do domínio, verifica a saída efetiva 000000.

## Resultado executado

Icarus executou este testbench contra o Verilog exportado nativamente pelo Quartus a partir do BDF `c2_para_sm`: **PASS, 64 casos**. Consulte [`sim_c2_para_sm.log`](../docs/logs/sim_c2_para_sm.log). O log registra que o VCD abriu e foi salvo em [`waveforms/c2_para_sm.vcd`](waveforms/c2_para_sm.vcd). A análise, conversão BDF→Verilog e geração de símbolo da revisão estão em [`c2_para_sm_analyze.log`](../docs/logs/c2_para_sm_analyze.log), [`c2_para_sm_convert.log`](../docs/logs/c2_para_sm_convert.log) e [`c2_para_sm_symbol.log`](../docs/logs/c2_para_sm_symbol.log).
