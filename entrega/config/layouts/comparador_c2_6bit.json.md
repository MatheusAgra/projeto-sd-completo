# Layout de comparador_c2_6bit

Contrato: `version=1`; células `[coluna, faixa]` únicas; instâncias correspondem integralmente ao grafo original.

As seis células `eq_bit_i` formam uma faixa de comparações bit a bit. `equal_prefix_*` e `unsigned_lt_*` ficam em etapas separadas por prioridade; a redução `unsigned_lt_low/high/unsigned_lt` conduz ao tratamento de sinal e à formação final de LT/GT. As inversões de A e do sinal de B ficam à esquerda, perto das derivações de entrada. Redes de fan-out mais exigentes: A_C2[0..5], B_C2[5], EQBIT_4..EQBIT_1, ULT e EQ. As células indicam agrupamento lógico, não prescrevem trajetos de fio.

Validação do metadado: 32 nomes originais presentes, sem nomes extras e sem células duplicadas. A coordenada é uma sugestão de agrupamento ao emissor; não representa por si só prova de continuidade elétrica.

Conferência visual no Quartus: pendente, conforme instrução da refatoração. Este documento registra somente a organização lógica proposta.
