# Layout de bcd_7seg

Metadados de posicionamento versão 1 para o emissor BDF. As células são únicas; coordenadas são `[coluna, faixa]` e não alteram grafo, interface ou hierarquia.

## Organização

- As quatro inversões de BCD ficam agrupadas antes dos termos produto compartilhados; os OR de cada segmento ocupam a etapa de saída.
- NBCD0..3 e os produtos P_* têm fan-out entre vários segmentos; roteá-los por corredores compartilhados com derivações físicas para cada consumidor.
- OR_D_FIRST liga a or_segment_d_final antes de formar SEG[3]; preservar esta etapa em dois ORs e a ordem dos bits SEG[0..6].

## Verificação

O mapeamento contém 25 instâncias: os nomes coincidem integralmente com `../grafos/bcd_7seg.json`, as células são únicas e todas as coordenadas são inteiros não negativos.

A continuidade elétrica será determinada pelo roteador do gerador e auditada nos BDF finais; este arquivo define somente agrupamento e posição relativa. Nenhuma conferência visual foi realizada.
