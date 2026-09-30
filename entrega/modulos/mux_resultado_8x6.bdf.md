## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# mux_resultado_8x6.bdf

O módulo seleciona entre `C0[5..0]` a `C7[5..0]`, cada um com seis bits, por meio de `D[7..0]` one-hot e produz `F[5..0]`. Para cada bit j, oito AND2 formam `P_i_j = C_i[j] AND D[i]`; um OR8 combina os oito termos. A estrutura contém 48 AND2 e seis OR8. Se mais de um bit D estiver ativo, os candidatos se combinam por OR, sem prioridade.

Exemplo: com apenas D3 ativo, F copia C3.

Dependências: primitivas AND2 e OR8. A topologia está em `config/grafos/mux_resultado_8x6.json`.

Verificação: Quartus analisou o BDF, converteu-o para Verilog e gerou o BSF sem erros nem avisos. O Icarus testou os oito seletores e todos os 64 valores no caminho escolhido: 512/512 passaram. Log em `docs/logs/sim_mux_resultado_8x6.log`; waveform real em `simulation/waveforms/mux_resultado_8x6.vcd`.
