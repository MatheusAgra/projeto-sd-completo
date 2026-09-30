# Layout de `somador_subtrator_6bit`

As seis faixas pares representam os bits 0 a 5. Cada XOR de SUB precede o somador completo da mesma faixa; as faixas ímpares deixam espaço para desvios e para a cadeia de carry.

Cada derivação de B alimenta `xor_sub_i`, cujo resultado vai somente ao B de `fa_i`. A deriva ao A da etapa correspondente. SUB alimenta as seis XOR e o Cin de `fa_0`; carries subsequentes devem seguir estritamente entre etapas vizinhas. `fa_i.S` dirige R[i], e `fa_5.Cout` termina na porta Cout.

Não alterar a interpretação de carry, índices ou ordem dos bits. O emissor ainda precisa calcular posições de pinos e confirmar as derivações dos barramentos; o JSON sozinho não demonstra conexão elétrica.
