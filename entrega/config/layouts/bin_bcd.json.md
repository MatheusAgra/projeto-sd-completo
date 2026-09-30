# Layout de bin_bcd

Metadados de posicionamento versão 1 para o emissor BDF. As células são únicas; coordenadas são `[coluna, faixa]` e não alteram grafo, interface ou hierarquia.

## Organização

- Colunas organizam a classificação do valor MAG, a lógica de correção das dezenas, a subtração do valor corretivo e as saídas UNI.
- Os sinais T20 e DEZ0_INTERNAL alimentam tanto a formação de DEZ quanto derivações do barramento K; manter seus fan-outs como redes contínuas.
- K[0] é fixado em GND e SUB_ONE em VCC; K[1..4] são derivados conforme o grafo, sem reordenar bits.
- COUT_UNUSED é uma saída intencionalmente sem consumidor; preservar seu terminal e registrá-lo como tal.

## Verificação

O mapeamento contém 24 instâncias: os nomes coincidem integralmente com `../grafos/bin_bcd.json`, as células são únicas e todas as coordenadas são inteiros não negativos.

A continuidade elétrica será determinada pelo roteador do gerador e auditada nos BDF finais; este arquivo define somente agrupamento e posição relativa. Nenhuma conferência visual foi realizada.
