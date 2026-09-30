# negador_c2_6bit.bdf — documentação do circuito

## Objetivo e interface

Calcula o inverso aditivo de qualquer padrão C2 de seis bits, módulo 64. B_C2[5:0] entrada; NEG[5:0] saída.

## Funcionamento

Inverte cada bit e soma 1 por seis somadores completos em ripple. A entrada de carry menos significativa é VCC; o resultado descarta o carry final e conserva os seis bits de NEG.

## Exemplo e limites

011101 (+29) resulta em 100011 (−29). O padrão 100000 (−32) resulta em 100000 devido à aritmética módulo 64. Os 64 padrões são definidos como NEG=(~B_C2+1) mod 64. No domínio numérico B=−15..+15, a saída representa −B. Zeros C2 permanecem zero.

## Dependências

Seis NOT, seis instâncias de somador_1bit, GND e VCC.

## Verificação

Quartus Prime Lite 21.1.0 concluiu análise do BDF, conversão BDF→Verilog e geração do símbolo: [análise](../docs/logs/negador_c2_6bit_analyze.log), [conversão](../docs/logs/negador_c2_6bit_convert.log) e [símbolo](../docs/logs/negador_c2_6bit_symbol.log), cada etapa com zero erros e zero avisos. O HDL exportado nativamente foi executado no Icarus pelo testbench independente: PASS — 64 casos. A referência nega o inteiro unsigned do padrão e compara os seis bits módulo 64; o ponto fixo −32 está incluído. Resultado registrado em [sim_negador_c2_6bit.log](../docs/logs/sim_negador_c2_6bit.log); o VCD foi aberto e salvo em [negador_c2_6bit.vcd](../simulation/waveforms/negador_c2_6bit.vcd).

Esses registros validam o BDF analisado e o HDL que o Quartus exportou nesta revisão; não afirmam teste físico na placa.
