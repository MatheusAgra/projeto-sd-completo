# Layout de logica_5bit

Contrato: `version=1`; células `[coluna, faixa]` únicas; instâncias correspondem integralmente ao grafo original.

Cada faixa `i` reúne `and_bit_i` e `xor_bit_i` para o mesmo bit de A_SM/B_SM. A faixa 4 corresponde ao bit de sinal e escreve em AND6[5]/XOR6[5]; AND6[4] e XOR6[4] permanecem ligados às instâncias GND de alinhamento. A e B têm fan-out para as duas primitivas de cada bit.

Validação do metadado: 12 nomes originais presentes, sem nomes extras e sem células duplicadas. A coordenada é uma sugestão de agrupamento ao emissor; não representa por si só prova de continuidade elétrica.

Conferência visual no Quartus: pendente, conforme instrução da refatoração. Este documento registra somente a organização lógica proposta.
