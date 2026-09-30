# Layout de `sm_para_c2`

As seis linhas agrupam `xor_sinal_i` e `fa_i` pelo mesmo índice, avançando do bit 0 ao bit 5. Essa disposição mantém cada operando transformado próximo da etapa que o consome e deixa espaço para a propagação de carry entre as etapas.

`SM[4]` tem fan-out para seis XOR e para o carry inicial. `GND` alimenta as duas entradas de XOR superiores de magnitude, as entradas B dos seis somadores e os outros consumidores explicitados no grafo. O roteador precisa criar derivações contínuas sem trocar os índices. Cada saída S vai a `C2[i]`; carries internos ligam etapas consecutivas.

O `Cout` final está conectado à rede `Cout` do grafo, mas a interface de `sm_para_c2` só expõe `C2[5:0]`; essa rede não possui consumidor contratual. Não se deve criar porta nem consumidor novo para ela. O layout não fixa coordenadas físicas, apenas células relativas, e não comprova a semântica Quartus dos taps.

Não foi executada análise/exportação Quartus nem conferência visual nesta entrega de metadados.
