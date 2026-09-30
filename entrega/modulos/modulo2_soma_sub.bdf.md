# modulo2_soma_sub.bdf — documentação do circuito

## Objetivo e interface

Conecta o somador/subtrator C2 de seis bits ao conversor C2 para sinal e magnitude. A_C2[5:0], B_C2[5:0], SUB entram; F_SM[5:0] sai em sinal e magnitude normalizada.

## Funcionamento

A instância somador_subtrator_6bit calcula A_C2+(B_C2 XOR {6{SUB}})+SUB. Seu R segue à instância c2_para_sm; Cout interno não altera sinal/magnitude. Não há BCD neste módulo.

## Exemplo e limites

A_C2=+15, B_C2=−15 e SUB=0 resultam em F_SM=000000. Com A_C2=−15, B_C2=+15 e SUB=1, o resultado numérico é −30 e F_SM=111110. A saída SM representa resultados −30..+30 para entradas válidas da ULA, −15..+15. O vetor C2 interno cobre seis bits. O conversor filho tem −32 fora de domínio; esse padrão é inalcançável com os operandos válidos.

## Dependências

somador_subtrator_6bit e c2_para_sm.

## Verificação

Quartus Prime Lite 21.1.0 concluiu análise do BDF, conversão BDF→Verilog e geração do símbolo: [análise](../docs/logs/modulo2_soma_sub_analyze.log), [conversão](../docs/logs/modulo2_soma_sub_convert.log) e [símbolo](../docs/logs/modulo2_soma_sub_symbol.log), cada etapa com zero erros e zero avisos. O HDL exportado nativamente foi executado no Icarus pelo testbench independente: PASS — 1922 casos. A referência decodifica A_C2 e B_C2 como inteiros de −15 a +15, calcula soma ou subtração e codifica sinal/magnitude normalizados. Resultado registrado em [sim_modulo2_soma_sub.log](../docs/logs/sim_modulo2_soma_sub.log); o VCD foi aberto e salvo em [modulo2_soma_sub.vcd](../simulation/waveforms/modulo2_soma_sub.vcd).

Esses registros validam o BDF analisado e o HDL que o Quartus exportou nesta revisão; não afirmam teste físico na placa.
