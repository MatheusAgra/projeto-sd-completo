# modulo2_soma_sub.json — descrição do grafo

## Interface congelada

Entradas: A_C2[5:0], B_C2[5:0], SUB. Saídas: F_SM[5:0]. As direções e larguras são as de `../interfaces.json`; este arquivo não altera o contrato.

## Representação do grafo

`name` identifica a entidade hierárquica e cada item de `instances` é um símbolo a converter para BDF. `type` seleciona uma primitiva de biblioteca ou submódulo; `name` é o identificador local; `connections` mapeia cada pino para uma rede. Redes internas de propagação de carry usam o prefixo `CARRY`, evitando colisão de nomes achatados com barramentos de saída como `C2`. `X[0]` representa um bit individual; vetores conectados a portas hierárquicas usam intervalos explícitos, como `A_C2[5..0]` e `F_SM[5..0]`. `GND` e `VCC` usam o pino `1` para dirigir a constante.

## Conteúdo e ligações

Instâncias por tipo: c2_para_sm: 1; somador_subtrator_6bit: 1. É hierárquico: somador_subtrator_6bit alimenta c2_para_sm. A saída é sinal e magnitude; o carry intermediário não muda essa representação.

## Dependências e exemplo

As dependências são os tipos listados acima. As equações, exemplos e limites estão em [`modulo2_soma_sub.bdf.md`](../../modulos/modulo2_soma_sub.bdf.md).

## Verificação e estado

Quartus Prime Lite 21.1.0: **PASS** para análise BDF, conversão para Verilog e geração de símbolo, com zero erros e zero avisos em cada etapa ([análise](../../docs/logs/modulo2_soma_sub_analyze.log), [conversão](../../docs/logs/modulo2_soma_sub_convert.log), [símbolo](../../docs/logs/modulo2_soma_sub_symbol.log)). Icarus: **PASS, 1922 casos**, executando o HDL exportado; consulte [sim_modulo2_soma_sub.log](../../docs/logs/sim_modulo2_soma_sub.log). O VCD produzido está em [`modulo2_soma_sub.vcd`](../../simulation/waveforms/modulo2_soma_sub.vcd). A avaliação aritmética direta dos grafos, feita anteriormente como checagem auxiliar, é distinta e não foi usada como substituto da simulação HDL.
