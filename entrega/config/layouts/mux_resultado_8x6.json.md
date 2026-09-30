# Layout de mux_resultado_8x6

Contrato: `version=1`; células `[coluna, faixa]` únicas; instâncias correspondem integralmente ao grafo original.

A matriz de AND está organizada em seis faixas de bit de saída e oito colunas de candidato: `gate_cN_bi` fica na coluna N, faixa i. A OR8 `sum_bit_i` fica depois da matriz na coluna 8, na mesma faixa i, e agrega os oito P_N_i para F[i]. D[N] distribui-se verticalmente às seis portas AND do candidato N; C[N][i] chega à célula da interseção candidato/bit. Esse fan-out de D e as oito entradas por OR8 exigem corredores e junções físicos claros no roteador.

Validação do metadado: 54 nomes originais presentes, sem nomes extras e sem células duplicadas. A coordenada é uma sugestão de agrupamento ao emissor; não representa por si só prova de continuidade elétrica.

Conferência visual no Quartus: pendente, conforme instrução da refatoração. Este documento registra somente a organização lógica proposta.
