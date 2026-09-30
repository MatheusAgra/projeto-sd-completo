# Layout de ula_de2_115

Metadados de posicionamento versão 1 para o emissor BDF. As células são únicas; coordenadas são `[coluna, faixa]` e não alteram grafo, interface ou hierarquia.

## Organização

- SW alimenta ula pelos slices externos originais A=SW[4..0], B=SW[9..5], S=SW[12..10]; manter os índices e a ordem exata dos bits.
- Buffers mag_a_* e mag_b_* formam MAGA/MAGB de quatro bits e os GND fixam o bit 4 de cada magnitude; distribuir MAGA/MAGB aos displays correspondentes.
- Os 13 espelhos mirror_* levam SW[0..12] a LEDR[0..12]; LEDR[13..17] têm GND individuais.
- display_a, display_b e display_f ficam como canais independentes; ONE habilita os displays de operandos e EXIBE_F habilita o resultado.
- LEDG[0..5] espelha F[0..5], LEDG[6] recebe STATUS e LEDG[7..8] são fixados em GND; HEX6/HEX7 ficam desativados pelos VCC existentes.

## Verificação

O mapeamento contém 56 instâncias: os nomes coincidem integralmente com `../grafos/ula_de2_115.json`, as células são únicas e todas as coordenadas são inteiros não negativos.

A continuidade elétrica será determinada pelo roteador do gerador e auditada nos BDF finais; este arquivo define somente agrupamento e posição relativa. Nenhuma conferência visual foi realizada.
