# somador_subtrator_6bit.bsf — documentação do símbolo

## Função do arquivo

O BSF é o símbolo de interface para instâncias hierárquicas da entidade `somador_subtrator_6bit`. Ele não contém a lógica; o circuito está no BDF correspondente, definido pelo grafo de portas da entrega. A conversão e conferência de correspondência entre os arquivos são responsabilidade da integração Quartus.

## Portas

A[5:0], B[5:0] e SUB escalares de controle entram; R[5:0] e Cout saem.

## Relação com o circuito

Soma ou subtrai dois vetores de seis bits usando complemento de dois e ripple carry. Para cada i, BX[i]=B[i] XOR SUB. Se SUB=0, a cadeia calcula A+B; se SUB=1, calcula A+~B+1. O primeiro carry é SUB. Seis instâncias de somador_1bit produzem cada R[i] e propagam Cout. Cout é o carry aritmético sem sinal do cálculo transformado, não é sinal nem overflow signed.

## Exemplo e limites

A=000101, B=000011 e SUB=1 calculam 5−3=2, logo R=000010. A=111111, B=000001 e SUB=0 resulta em 000000 com Cout=1. As 8192 combinações de entradas são definidas módulo 64. Para valores C2 válidos da ULA (−15..+15), a soma/subtração varia de −30 a +30 e cabe em seis bits.

## Dependências e verificação

O BSF expõe a interface gráfica da entidade, sem implementar lógica. O Quartus Prime Lite 21.1.0 gerou o símbolo correspondente após a análise e conversão do BDF, com zero erros e zero avisos; consulte o [log de geração do símbolo](../docs/logs/somador_subtrator_6bit_symbol.log). A execução do testbench valida o HDL exportado do BDF, não o desenho do BSF em isolamento: PASS — 8192 casos. O resultado está em [sim_somador_subtrator_6bit.log](../docs/logs/sim_somador_subtrator_6bit.log), e o VCD correspondente em [somador_subtrator_6bit.vcd](../simulation/waveforms/somador_subtrator_6bit.vcd). As portas do símbolo continuam sujeitas à conferência da interface declarada no contrato.
