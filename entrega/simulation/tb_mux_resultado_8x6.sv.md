# tb_mux_resultado_8x6.sv

Testbench para o mux de oito candidatos de seis bits. Ativa um seletor por vez, mantém os candidatos não selecionados em zero e percorre todos os 64 padrões no caminho escolhido.

Os 8×64=512 estímulos passaram no Icarus. O log registra `PASS mux_resultado_8x6: 512 estímulos um-hot`; a execução gravou `waveforms/mux_resultado_8x6.vcd`.

O DUT foi o Verilog exportado pelo Quartus a partir do BDF final.
