# Tabela de controle de decodificador_operacao

Para cada seletor `S[2..0]`, exatamente `D[S]` fica ativo. `EXIBE_F = NOT(S2) AND NOT(S1)`, habilitando F somente para as operacoes 000 e 001.

| S2 S1 S0 | D[7..0] | EXIBE_F |
|---|---|---:|
| 000 | 00000001 | 1 |
| 001 | 00000010 | 1 |
| 010 | 00000100 | 0 |
| 011 | 00001000 | 0 |
| 100 | 00010000 | 0 |
| 101 | 00100000 | 0 |
| 110 | 01000000 | 0 |
| 111 | 10000000 | 0 |

## Mintermos

- `D0 = NOT S2 AND NOT S1 AND NOT S0`.
- `D1 = NOT S2 AND NOT S1 AND S0`.
- `D2 = NOT S2 AND S1 AND NOT S0`.
- `D3 = NOT S2 AND S1 AND S0`.
- `D4 = S2 AND NOT S1 AND NOT S0`.
- `D5 = S2 AND NOT S1 AND S0`.
- `D6 = S2 AND S1 AND NOT S0`.
- `D7 = S2 AND S1 AND S0`.
- `EXIBE_F = NOT S2 AND NOT S1`.
