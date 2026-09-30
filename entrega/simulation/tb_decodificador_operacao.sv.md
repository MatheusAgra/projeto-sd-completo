# tb_decodificador_operacao.sv

Testbench do decodificador de três bits. A expectativa D one-hot é calculada por deslocamento do bit 1; `EXIBE_F` deve valer 1 somente para seletores 0 e 1.

A simulação real no Icarus percorreu os oito seletores e passou. O log registra `PASS decodificador_operacao: 8 seletores`; a waveform é `waveforms/decodificador_operacao.vcd`.

Foi testado o Verilog exportado pelo Quartus do BDF final.
