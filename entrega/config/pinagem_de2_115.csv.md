# pinagem_de2_115.csv

Tabela de 96 sinais físicos: 13 SW, 18 LEDR, 9 LEDG e 56 segmentos HEX. Cada linha registra sinal, pino, padrão de I/O e página do manual, com conferência visual pela página 3 do enunciado.

Perfil de referência: JP6 em 3,3 V e JP7 em 2,5 V, padrões de fábrica documentados. Pinos fixos em 2,5 V usam `2.5 V`; pinos JP6 ou fixos 3,3 V usam `3.3-V LVTTL`. HEX7[6] é fixo em 3,3 V. O Fitter deve confirmar as atribuições finais, inclusive saídas constantes.

Exemplos: SW0=AB28, LEDG0=E21, HEX0[0]=G18. `gerar_pinagem.py` exige cobertura completa e ausência de duplicação de sinal ou pino; o compilador valida a legalidade elétrica. Conferência dos jumpers reais permanece a cargo do usuário antes da programação.
