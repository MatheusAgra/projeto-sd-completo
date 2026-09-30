# tb_logica_5bit.sv

Testbench de `logica_5bit`. Calcula AND/XOR de forma independente sobre os cinco bits de entrada e aplica explicitamente `{L4,0,L3,L2,L1,L0}` às saídas esperadas.

A execução percorreu os 32×32=1024 pares e passou. O Icarus gravou a waveform real `waveforms/logica_5bit.vcd`; o log contém `PASS logica_5bit: 1024 pares`.

A simulação usou `simulation/generated/logica_5bit.v`, convertido pelo Quartus a partir do BDF.
