# c2_para_sm.json — descrição do grafo

## Interface congelada

Entradas: R[5:0]. Saídas: F_SM[5:0]. As direções e larguras são as de `../interfaces.json`; este arquivo não altera o contrato.

## Representação do grafo

`name` identifica a entidade hierárquica e cada item de `instances` é um símbolo a converter para BDF. `type` seleciona uma primitiva de biblioteca ou submódulo; `name` é o identificador local; `connections` mapeia cada pino para uma rede. Redes internas de propagação de carry usam o prefixo `CARRY`, evitando colisão de nomes achatados com barramentos de saída como `C2`. `X[0]` representa um bit individual; vetores conectados a portas hierárquicas usam intervalos explícitos, como `A_C2[5..0]` e `F_SM[5..0]`. `GND` e `VCC` usam o pino `1` para dirigir a constante.

## Conteúdo e ligações

Instâncias por tipo: AND2: 11; GND: 1; NOT: 7; OR2: 9; VCC: 1; somador_1bit: 6. O caminho de valor absoluto forma ABS=~R+1. A rede de seleção usa R5 para escolher R ou ABS e o sinal R5 AND OR(R[4:0]); −32 produz efetivamente 000000 fora do domínio.

## Dependências e exemplo

As dependências são os tipos listados acima. As equações, exemplos e limites estão em [`c2_para_sm.bdf.md`](../../modulos/c2_para_sm.bdf.md).

## Verificação e estado

Quartus Prime Lite 21.1.0: **PASS** para análise BDF, conversão para Verilog e geração de símbolo, com zero erros e zero avisos em cada etapa ([análise](../../docs/logs/c2_para_sm_analyze.log), [conversão](../../docs/logs/c2_para_sm_convert.log), [símbolo](../../docs/logs/c2_para_sm_symbol.log)). Icarus: **PASS, 64 casos**, executando o HDL exportado; consulte [sim_c2_para_sm.log](../../docs/logs/sim_c2_para_sm.log). O VCD produzido está em [`c2_para_sm.vcd`](../../simulation/waveforms/c2_para_sm.vcd). A avaliação aritmética direta dos grafos, feita anteriormente como checagem auxiliar, é distinta e não foi usada como substituto da simulação HDL.
