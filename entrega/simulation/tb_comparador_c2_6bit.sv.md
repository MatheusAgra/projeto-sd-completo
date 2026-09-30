# tb_comparador_c2_6bit.sv

Testbench SystemVerilog do comparador C2 de seis bits. O modelo de referência converte A e B para inteiros signed e compara os valores, sem repetir a lógica de portas.

A bateria percorre os 64×64=4096 pares, inclusive −32 e +31. A execução real no Icarus 13.0 passou em todos os casos e gravou `waveforms/comparador_c2_6bit.vcd`. O log registra `PASS comparador_c2_6bit: 4096 pares signed C2`.

A entrada da simulação é o Verilog convertido pelo Quartus a partir de `modulos/comparador_c2_6bit.bdf`.
