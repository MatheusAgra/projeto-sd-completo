# Layout de ula_core

Metadados de posicionamento versão 1 para o emissor BDF. As células são únicas; coordenadas são `[coluna, faixa]` e não alteram grafo, interface ou hierarquia.

## Organização

- conv_a e conv_b convertem operandos antes dos blocos aritmético e comparador; logica usa diretamente A/B em sinal-magnitude.
- Aritmética, negação, comparação e lógica entregam candidatos ao mux selecionado por controle; agrupar os blocos de processamento antes da seleção.
- AC2 e BC2 têm fan-out para aritmética, negação/comparação; D alimenta mux e três portas de STATUS, mantendo cada barramento contínuo.
- ZERO[5..0] é formado por seis constantes GND para os candidatos C3..C5; STATUS reúne EQS/GTS/LTS conforme os enables D[3..5].

## Verificação

O mapeamento contém 18 instâncias: os nomes coincidem integralmente com `../grafos/ula_core.json`, as células são únicas e todas as coordenadas são inteiros não negativos.

A continuidade elétrica será determinada pelo roteador do gerador e auditada nos BDF finais; este arquivo define somente agrupamento e posição relativa. Nenhuma conferência visual foi realizada.
