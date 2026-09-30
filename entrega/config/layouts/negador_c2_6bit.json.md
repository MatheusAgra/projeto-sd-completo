# Layout de `negador_c2_6bit`

Seis faixas alinham cada `invert_i` à instância `fa_i` do mesmo bit. A cadeia calcula `~B_C2 + 1`: cada saída NOT alimenta o pino A correspondente, GND alimenta os pinos B, e VCC inicia o carry em `fa_0`.

Os carries devem conectar cada par de etapas adjacentes em ordem 0 a 5. As somas ligam a `NEG[i]` preservando a ordem original. A instância GND tem fan-out para as seis etapas e precisa de derivações físicas contínuas.

O carry de `fa_5` liga à rede interna `COUT`, sem porta de mesmo nome na interface e sem consumidor. A documentação funcional define descarte do carry final; o layout não adiciona interface nem altera a operação módulo 64. Os offsets das portas e a continuidade só podem ser avaliados depois de o emissor gerar o BDF.
