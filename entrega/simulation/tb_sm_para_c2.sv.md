# tb_sm_para_c2.sv

Testbench SystemVerilog do módulo `sm_para_c2`. A comparação esperada vem de um modelo independente baseado em inteiros, não das equações do grafo. O modelo decodifica sinal e magnitude como inteiro e compara o padrão C2 de seis bits; percorre ambos os padrões de zero SM.

## Resultado executado

Icarus executou este testbench contra o Verilog exportado nativamente pelo Quartus a partir do BDF `sm_para_c2`: **PASS, 32 casos**. Consulte [`sim_sm_para_c2.log`](../docs/logs/sim_sm_para_c2.log). O log registra que o VCD abriu e foi salvo em [`waveforms/sm_para_c2.vcd`](waveforms/sm_para_c2.vcd). A análise, conversão BDF→Verilog e geração de símbolo da revisão estão em [`sm_para_c2_analyze.log`](../docs/logs/sm_para_c2_analyze.log), [`sm_para_c2_convert.log`](../docs/logs/sm_para_c2_convert.log) e [`sm_para_c2_symbol.log`](../docs/logs/sm_para_c2_symbol.log).
