> Evidência histórica anterior à refatoração dos BDF: não foi reexportada, ressimulada nem regenerada para esta geometria. Consulte docs/REFATORACAO_VISUAL_TECNICA.md.

# comparador_c2_6bit.vcd

Waveform VCD real da execução Icarus 13.0 do testbench `tb_comparador_c2_6bit.sv` sobre o HDL exportado pelo Quartus do BDF final. Registra as entradas C2 e as saídas EQ/GT/LT durante os 4096 pares, incluindo o extremo −32 contra −31.

A simulação terminou com PASS em 4096 pares signed. O log correspondente é `docs/logs/sim_comparador_c2_6bit.log`; a cobertura e o modelo esperado são descritos em `simulation/tb_comparador_c2_6bit.sv.md`.
