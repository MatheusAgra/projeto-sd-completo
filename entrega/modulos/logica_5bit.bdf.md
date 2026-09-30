## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# logica_5bit.bdf

O circuito aplica AND e XOR bit a bit aos vetores brutos de sinal e magnitude `A_SM[4..0]` e `B_SM[4..0]`. As saídas `AND6[5..0]` e `XOR6[5..0]` usam o alinhamento aprovado `{L4,0,L3,L2,L1,L0}`: o bit mais significativo permanece na posição de sinal, o bit 4 da saída é zero e os quatro bits inferiores são preservados. O módulo não normaliza sinal e magnitude zero.

Exemplo: `10000 AND 10000` produz `AND6=100000`, preservando o resultado bit a bit.

Dependências: cinco AND2, cinco XOR e GND para os bits de alinhamento. A topologia está em `config/grafos/logica_5bit.json`.

Verificação: análise Quartus, conversão BDF→Verilog e geração de símbolo passaram sem erros nem avisos. No Icarus, o HDL exportado passou os 1024 pares; confira `docs/logs/sim_logica_5bit.log` e `simulation/waveforms/logica_5bit.vcd`.
