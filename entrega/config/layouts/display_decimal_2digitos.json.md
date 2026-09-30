# Layout de display_decimal_2digitos

Metadados de posicionamento versão 1 para o emissor BDF. As células são únicas; coordenadas são `[coluna, faixa]` e não alteram grafo, interface ou hierarquia.

## Organização

- O fluxo vai de convert_mag para dois decodificadores independentes, um para dezenas e outro para unidades, e termina em máscaras por segmento.
- ENABLE é invertido uma vez em DISABLED e distribuído às 14 portas OR; tornar o fan-out comum contínuo.
- DEZ_SEG e UNI_SEG são canais separados de sete bits; manter cada máscara alinhada ao mesmo índice de segmento e as interfaces externas intactas.

## Verificação

O mapeamento contém 18 instâncias: os nomes coincidem integralmente com `../grafos/display_decimal_2digitos.json`, as células são únicas e todas as coordenadas são inteiros não negativos.

A continuidade elétrica será determinada pelo roteador do gerador e auditada nos BDF finais; este arquivo define somente agrupamento e posição relativa. Nenhuma conferência visual foi realizada.
