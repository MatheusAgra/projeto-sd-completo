> Evidência histórica anterior à refatoração dos BDF: não foi reexportada, ressimulada nem regenerada para esta geometria. Consulte docs/REFATORACAO_VISUAL_TECNICA.md.

# mux_resultado_8x6.vcd

Waveform VCD real da execução Icarus 13.0 do testbench de mux contra o HDL exportado pelo Quartus a partir do BDF final. Registra cada seleção one-hot e os 64 padrões aplicados ao candidato selecionado.

Os 512 estímulos passaram. O log é `docs/logs/sim_mux_resultado_8x6.log`; método e cobertura estão em `simulation/tb_mux_resultado_8x6.sv.md`.
