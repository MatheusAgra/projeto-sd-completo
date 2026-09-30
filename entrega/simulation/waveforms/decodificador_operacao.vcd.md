> Evidência histórica anterior à refatoração dos BDF: não foi reexportada, ressimulada nem regenerada para esta geometria. Consulte docs/REFATORACAO_VISUAL_TECNICA.md.

# decodificador_operacao.vcd

Waveform VCD real da execução Icarus 13.0 do testbench do decodificador contra o HDL exportado pelo Quartus a partir do BDF final. Registra os oito valores S, o vetor one-hot D e `EXIBE_F`.

Os oito seletores passaram; o log é `docs/logs/sim_decodificador_operacao.log`. A expectativa está documentada em `simulation/tb_decodificador_operacao.sv.md`.
