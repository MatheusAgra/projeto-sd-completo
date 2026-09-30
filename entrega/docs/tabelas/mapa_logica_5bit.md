# Mapas e tabela de logica_5bit

A operacao bit a bit recebe os cinco bits brutos de sinal e magnitude. Para cada posicao i, `A_AND_B[i] = A_SM[i] AND B_SM[i]` e `A_XOR_B[i] = A_SM[i] XOR B_SM[i]`.

## Tabela de verdade por bit

| A | B | AND | XOR |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 0 |

## Mapas de Karnaugh de duas variaveis

Colunas em ordem Gray B=0,1; linhas A=0,1.

| AND\ A/B | B=0 | B=1 |
|---|---:|---:|
| A=0 | 0 | 0 |
| A=1 | 0 | 1 |

| XOR\ A/B | B=0 | B=1 |
|---|---:|---:|
| A=0 | 0 | 1 |
| A=1 | 1 | 0 |

## Alinhamento da saida

Para `L[4..0]`, ambas as saidas usam `{L4,0,L3,L2,L1,L0}`. O bit de sinal original e preservado; o novo bit de magnitude e zero. A operacao nao normaliza `10000`: `10000 AND 10000 = 100000`.
