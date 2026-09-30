# negador_c2_6bit.json — descrição do grafo

## Interface congelada

Entradas: B_C2[5:0]. Saídas: NEG[5:0]. As direções e larguras são as de `../interfaces.json`; este arquivo não altera o contrato.

## Representação do grafo

`name` identifica a entidade hierárquica e cada item de `instances` é um símbolo a converter para BDF. `type` seleciona uma primitiva de biblioteca ou submódulo; `name` é o identificador local; `connections` mapeia cada pino para uma rede. Redes internas de propagação de carry usam o prefixo `CARRY`, evitando colisão de nomes achatados com barramentos de saída como `C2`. `X[0]` representa um bit individual; vetores conectados a portas hierárquicas usam intervalos explícitos, como `A_C2[5..0]` e `F_SM[5..0]`. `GND` e `VCC` usam o pino `1` para dirigir a constante.

## Conteúdo e ligações

Instâncias por tipo: GND: 1; NOT: 6; VCC: 1; somador_1bit: 6. O grafo calcula ~B_C2+1 com seis inversores e uma cadeia de incrementação; o carry final é descartado, logo a operação é módulo 64.

## Dependências e exemplo

As dependências são os tipos listados acima. As equações, exemplos e limites estão em [`negador_c2_6bit.bdf.md`](../../modulos/negador_c2_6bit.bdf.md).

## Verificação e estado

Quartus Prime Lite 21.1.0: **PASS** para análise BDF, conversão para Verilog e geração de símbolo, com zero erros e zero avisos em cada etapa ([análise](../../docs/logs/negador_c2_6bit_analyze.log), [conversão](../../docs/logs/negador_c2_6bit_convert.log), [símbolo](../../docs/logs/negador_c2_6bit_symbol.log)). Icarus: **PASS, 64 casos**, executando o HDL exportado; consulte [sim_negador_c2_6bit.log](../../docs/logs/sim_negador_c2_6bit.log). O VCD produzido está em [`negador_c2_6bit.vcd`](../../simulation/waveforms/negador_c2_6bit.vcd). A avaliação aritmética direta dos grafos, feita anteriormente como checagem auxiliar, é distinta e não foi usada como substituto da simulação HDL.
