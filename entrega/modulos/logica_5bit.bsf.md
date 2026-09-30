# logica_5bit.bsf

O BSF representa somente a interface gráfica de `logica_5bit`. `A_SM[4..0]` e `B_SM[4..0]` são entradas de cinco bits; `AND6[5..0]` e `XOR6[5..0]` são saídas de seis bits. O alinhamento `{L4,0,L3,L2,L1,L0}` é implementado pelo BDF.

Exemplo: duas entradas `10000` produzem `AND6=100000`.

Verificação: Quartus gerou o símbolo sem erros ou avisos. As quatro portas, direções e larguras coincidem com `config/interfaces.json`; a lógica real foi verificada no HDL convertido do BDF.
