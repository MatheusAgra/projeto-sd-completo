# Layout de `c2_para_sm`

O layout separa três grupos: inversão e cadeia de valor absoluto à esquerda; redução de magnitude e controle de sinal no centro; seleção por bit à direita. `invert_i` e `fa_abs_i` alinham-se pelo índice. Cada carry do somador de valor absoluto deve seguir à etapa seguinte; GND alimenta os seis pinos B e VCC inicia o carry.

A redução de não zero conserva a árvore original: `or_mag_01` reúne R[0:1], `or_mag_23` reúne R[2:3], `or_mag_0123` combina os dois resultados e `or_mag_01234` incorpora R[4] para formar `MAG_NONZERO`. R[5] também alimenta a inversão de sinal, cinco ramos negativos e a porta `sign_nonzero`. `NOT_SIGN` alimenta cinco ramos positivos. Cada bit de POS/NEG vai ao mux de mesmo índice e daí a F_SM[i]; `sign_nonzero` dirige F_SM[5].

R[0..4] é compartilhado entre a árvore de redução, inversores e seleção positiva, enquanto ABS[0..4] alimenta seleção negativa. O roteador deve conservar esses fan-outs e o índice de cada tap. O Cout do caminho ABS sai da etapa final, mas não está na interface e não tem consumidor; preserve-o conforme o grafo sem criar conexão funcional.

As posições relativas não especificam rotas ou offsets reais dos símbolos. O Quartus ainda precisa confirmar a sintaxe/semântica dos taps e a análise do BDF gerado. Nenhuma análise Quartus ou inspeção visual foi realizada para este metadado.
