# Layout de `modulo2_soma_sub`

As duas instâncias mantêm a hierarquia: `soma_sub` fica antes de `conversor` no sentido do fluxo do resultado. Entradas A_C2, B_C2 e SUB chegam à primeira; o barramento de saída R_C2[5..0] segue ao pino R da segunda; F_SM[5..0] sai da segunda para a porta do módulo.

Preserve integralmente larguras, direção e índices dos dois barramentos de seis bits. Cada bit de R_C2 deve chegar ao bit igual de R, e cada F_SM[i] ao correspondente pino de saída. `COUT` recebe somente o carry final da operação aritmética. Como o conversor não o consome e a interface não expõe COUT, essa rede não deve adquirir outro destino.

O posicionamento define somente a precedência dos blocos. O roteador precisa usar coordenadas reais dos pinos e produzir derivações/taps válidos. Não houve análise Quartus, exportação HDL ou conferência visual neste metadado.
