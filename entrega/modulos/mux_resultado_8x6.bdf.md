# mux_resultado_8x6.bdf

O módulo seleciona entre `C0[5..0]` a `C7[5..0]`, cada um com seis bits, por meio de `D[7..0]` one-hot e produz `F[5..0]`. Para cada bit j, oito AND2 formam `P_i_j = C_i[j] AND D[i]`; um OR8 combina os oito termos. A estrutura contém 48 AND2 e seis OR8. Se mais de um bit D estiver ativo, os candidatos se combinam por OR, sem prioridade.

Exemplo: com apenas D3 ativo, F copia C3.

Dependências: primitivas AND2 e OR8. A topologia está em `config/grafos/mux_resultado_8x6.json`.

Verificação: Quartus analisou o BDF, converteu-o para Verilog e gerou o BSF sem erros nem avisos. O Icarus testou os oito seletores e todos os 64 valores no caminho escolhido: 512/512 passaram. Log em `docs/logs/sim_mux_resultado_8x6.log`; waveform real em `simulation/waveforms/mux_resultado_8x6.vcd`.
