# c2_para_sm.bdf — documentação do circuito

## Objetivo e interface

Converte um resultado C2 de seis bits em sinal e magnitude de seis bits, normalizando zero. R[5:0] é a entrada C2; F_SM[5] é o sinal e F_SM[4:0] é a magnitude.

## Funcionamento

Um caminho calcula ABS=~R+1 por seis inversores e seis somadores completos com carry inicial 1. Um mux por portas AND/OR escolhe R[4:0] quando R5=0 e ABS[4:0] quando R5=1. O sinal é R5 AND OR(R4..R0). Assim, zero sempre sai 000000.

## Exemplo e limites

R=111110 representa −2 e sai F_SM=100010. R=000000 sai 000000. R=100000 (−32) produz 000000 pela truncagem da magnitude aos cinco bits e supressão do sinal quando os cinco bits baixos de R são zero. O domínio contratual é −31..+31. −32 não pode ser representado em sinal e magnitude de seis bits, permanece explicitamente fora do domínio e o comportamento de porta efetivo para esse padrão é 000000. Todos os 64 padrões são testados para caracterizar esse limite, sem alegar que −32 foi convertido corretamente.

## Dependências

NOT, AND2, OR2, GND, VCC e seis instâncias de somador_1bit para o caminho absoluto.

## Verificação

Quartus Prime Lite 21.1.0 concluiu análise do BDF, conversão BDF→Verilog e geração do símbolo: [análise](../docs/logs/c2_para_sm_analyze.log), [conversão](../docs/logs/c2_para_sm_convert.log) e [símbolo](../docs/logs/c2_para_sm_symbol.log), cada etapa com zero erros e zero avisos. O HDL exportado nativamente foi executado no Icarus pelo testbench independente: PASS — 64 casos. A referência decodifica cada R como inteiro signed. Para −32, fora do domínio, compara a saída efetiva 000000 definida pela regra de magnitude e sinal do circuito. Resultado registrado em [sim_c2_para_sm.log](../docs/logs/sim_c2_para_sm.log); o VCD foi aberto e salvo em [c2_para_sm.vcd](../simulation/waveforms/c2_para_sm.vcd).

Esses registros validam o BDF analisado e o HDL que o Quartus exportou nesta revisão; não afirmam teste físico na placa.
