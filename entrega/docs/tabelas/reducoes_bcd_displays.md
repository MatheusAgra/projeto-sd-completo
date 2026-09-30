# Reduções Booleanas

## `bin_bcd`

As comparações são simplificadas para:

- `T10 = MAG[4] OR (MAG[3] AND (MAG[2] OR MAG[1]))`
- `T20 = MAG[4] AND (MAG[3] OR MAG[2])`
- `T30 = MAG[4] AND MAG[3] AND MAG[2] AND MAG[1]`
- `DEZ[0] = (T10 AND NOT T20) OR T30`; `DEZ[1]=T20`; `DEZ[3:2]=0`.
- O seletor de correção produz `K[4]=T20`, `K[3]=DEZ[0]`, `K[2]=T20`, `K[1]=DEZ[0]`, `K[0]=0`; `UNI=MAG-K` via `somador_subtrator_5bit` com `SUB=1`.

A tabela e os mapas cobrem os 32 valores. Em 31, DEZ=3, K=30 e UNI=1.

## `bcd_7seg`

Variáveis: `x=BCD[3]`, `y=BCD[2]`, `z=BCD[1]`, `w=BCD[0]`. Os conjuntos de mintermos em que cada saída ativa em zero assume 1 são:
- `SEG[6] (g)`: mintermos 1 `[0, 1, 7, 10, 11, 12, 13, 14, 15]`; SOP simplificada: (y AND z AND w) OR (!x AND !y AND !z) OR (x AND z) OR (x AND y).
- `SEG[5] (f)`: mintermos 1 `[1, 2, 3, 7, 10, 11, 12, 13, 14, 15]`; SOP simplificada: (z AND w) OR (!y AND z) OR (!x AND !y AND w) OR (x AND y).
- `SEG[4] (e)`: mintermos 1 `[1, 3, 4, 5, 7, 9, 10, 11, 12, 13, 14, 15]`; SOP simplificada: (w) OR (y AND !z) OR (x AND z).
- `SEG[3] (d)`: mintermos 1 `[1, 4, 7, 10, 11, 12, 13, 14, 15]`; SOP simplificada: (y AND !z AND !w) OR (y AND z AND w) OR (!x AND !y AND !z AND w) OR (x AND z) OR (x AND y).
- `SEG[2] (c)`: mintermos 1 `[2, 10, 11, 12, 13, 14, 15]`; SOP simplificada: (!y AND z AND !w) OR (x AND z) OR (x AND y).
- `SEG[1] (b)`: mintermos 1 `[5, 6, 10, 11, 12, 13, 14, 15]`; SOP simplificada: (y AND !z AND w) OR (y AND z AND !w) OR (x AND z) OR (x AND y).
- `SEG[0] (a)`: mintermos 1 `[1, 4, 10, 11, 12, 13, 14, 15]`; SOP simplificada: (y AND !z AND !w) OR (!x AND !y AND !z AND w) OR (x AND z) OR (x AND y).

Os mintermos 10..15 aparecem nas saídas iguais a 1, o que implementa explicitamente display apagado para códigos BCD inválidos. Não há dont-cares. A implementação no grafo usa a forma soma de produtos com inversores compartilhados para as quatro entradas.
