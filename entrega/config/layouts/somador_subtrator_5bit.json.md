# Layout de `somador_subtrator_5bit`

As cinco faixas pares representam os bits 0 a 4. Em cada faixa, `xor_sub_i` precede `fa_i`, mantendo a transformação `B[i] XOR SUB` junto ao somador completo correspondente. As faixas ímpares ficam livres para corredores de roteamento.

O barramento B deve derivar cada bit para o XOR do mesmo índice; A deriva diretamente ao A de `fa_i`. SUB ramifica para os cinco XOR e para o Cin de `fa_0`. Cada carry de saída liga fisicamente ao Cin da etapa seguinte, e cada soma segue ao bit igual de R. O carry final permanece na porta Cout.

Os nomes e índices no grafo definem a correspondência lógica; o emissor deve conferir taps e pinos reais. O metadado não decide cruzamentos, dimensões dos símbolos ou coordenadas de terminais, e por si só não valida continuidade.
