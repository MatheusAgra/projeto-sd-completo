# somador_1bit.json — descrição do grafo

## Interface congelada

Entradas: A, B, Cin. Saídas: S, Cout. As direções e larguras são as de `../interfaces.json`; este arquivo não altera o contrato.

## Representação do grafo

`name` identifica a entidade hierárquica e cada item de `instances` é um símbolo a converter para BDF. `type` seleciona uma primitiva de biblioteca ou submódulo; `name` é o identificador local; `connections` mapeia cada pino para uma rede. Redes internas de propagação de carry usam o prefixo `CARRY`, evitando colisão de nomes achatados com barramentos de saída como `C2`. `X[0]` representa um bit individual; vetores conectados a portas hierárquicas usam intervalos explícitos, como `A_C2[5..0]` e `F_SM[5..0]`. `GND` e `VCC` usam o pino `1` para dirigir a constante.

## Conteúdo e ligações

Instâncias por tipo: AND2: 2; OR2: 1; XOR: 2. P=A XOR B; S=P XOR Cin; Cout=(A AND B) OR (P AND Cin).

## Dependências e exemplo

As dependências são os tipos listados acima. As equações, exemplos e limites estão em [`somador_1bit.bdf.md`](../../modulos/somador_1bit.bdf.md).

## Verificação e estado

Quartus Prime Lite 21.1.0: **PASS** para análise BDF, conversão para Verilog e geração de símbolo, com zero erros e zero avisos em cada etapa ([análise](../../docs/logs/somador_1bit_analyze.log), [conversão](../../docs/logs/somador_1bit_convert.log), [símbolo](../../docs/logs/somador_1bit_symbol.log)). Icarus: **PASS, 8 casos**, executando o HDL exportado; consulte [sim_somador_1bit.log](../../docs/logs/sim_somador_1bit.log). O VCD produzido está em [`somador_1bit.vcd`](../../simulation/waveforms/somador_1bit.vcd). A avaliação aritmética direta dos grafos, feita anteriormente como checagem auxiliar, é distinta e não foi usada como substituto da simulação HDL.
