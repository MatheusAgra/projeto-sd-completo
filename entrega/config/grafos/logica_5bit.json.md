# logica_5bit.json

Grafo estrutural de `logica_5bit` com cinco AND2, cinco XOR e dois GND. O mapeamento implementa `{L4,0,L3,L2,L1,L0}` para AND e XOR e preserva o sinal bruto das entradas.

Exemplo: `A_SM=B_SM=10000` dá `AND6=100000`.

Verificação: Quartus analisou o BDF e converteu a entidade sem erros nem avisos. A simulação independente passou 1024/1024 vetores no Icarus.
