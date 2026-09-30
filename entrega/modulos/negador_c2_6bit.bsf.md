# negador_c2_6bit.bsf — documentação do símbolo

## Função do arquivo

O BSF é o símbolo de interface para instâncias hierárquicas da entidade `negador_c2_6bit`. Ele não contém a lógica; o circuito está no BDF correspondente, definido pelo grafo de portas da entrega. A conversão e conferência de correspondência entre os arquivos são responsabilidade da integração Quartus.

## Portas

B_C2[5:0] entrada; NEG[5:0] saída.

## Relação com o circuito

Calcula o inverso aditivo de qualquer padrão C2 de seis bits, módulo 64. Inverte cada bit e soma 1 por seis somadores completos em ripple. A entrada de carry menos significativa é VCC; o resultado descarta o carry final e conserva os seis bits de NEG.

## Exemplo e limites

011101 (+29) resulta em 100011 (−29). O padrão 100000 (−32) resulta em 100000 devido à aritmética módulo 64. Os 64 padrões são definidos como NEG=(~B_C2+1) mod 64. No domínio numérico B=−15..+15, a saída representa −B. Zeros C2 permanecem zero.

## Dependências e verificação

O BSF expõe a interface gráfica da entidade, sem implementar lógica. O Quartus Prime Lite 21.1.0 gerou o símbolo correspondente após a análise e conversão do BDF, com zero erros e zero avisos; consulte o [log de geração do símbolo](../docs/logs/negador_c2_6bit_symbol.log). A execução do testbench valida o HDL exportado do BDF, não o desenho do BSF em isolamento: PASS — 64 casos. O resultado está em [sim_negador_c2_6bit.log](../docs/logs/sim_negador_c2_6bit.log), e o VCD correspondente em [negador_c2_6bit.vcd](../simulation/waveforms/negador_c2_6bit.vcd). As portas do símbolo continuam sujeitas à conferência da interface declarada no contrato.
