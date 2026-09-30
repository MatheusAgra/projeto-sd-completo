# interfaces.json

Contrato congelado após aprovação do usuário em 30/09/2026. Define os 16 módulos, nomes de portas, direção e largura em bits. O principal é o único responsável por mudanças neste arquivo e no gerador.

A/B de cinco bits são sinal e magnitude, com sinal no bit 4. Os vetores A_C2/B_C2 de seis bits são C2 signed. F_SM de seis bits tem sinal no bit 5 e magnitude nos cinco inferiores. R nos somadores é um padrão modular; Cout é carry, não sinal. O conversor C2→SM não representa −32.

A saída F do core é SM para soma/subtração; padrão C2 da negação de B em 010, provisoriamente; zero nas comparações; `{L4,0,L3,L2,L1,L0}` para AND/XOR. STATUS só responde nas comparações e EXIBE_F só habilita 000/001.

BCD e os vetores DEZ/UNI têm quatro bits; segmentos ativos em zero possuem sete bits, `{g,f,e,d,c,b,a}`. O topo tem treze chaves, dezoito LEDs vermelhos, nove verdes e oito displays de sete segmentos, sem clock.

Exemplo: `sm_para_c2.SM=10011` produz `C2=111101`. A correspondência final será verificada nos BDF, BSF e Verilog exportado, além da compilação hierárquica.
