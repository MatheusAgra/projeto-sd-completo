# sm_para_c2.json — descrição do grafo

## Interface congelada

Entradas: SM[4:0]. Saídas: C2[5:0]. As direções e larguras são as de `../interfaces.json`; este arquivo não altera o contrato.

## Representação do grafo

`name` identifica a entidade hierárquica e cada item de `instances` é um símbolo a converter para BDF. `type` seleciona uma primitiva de biblioteca ou submódulo; `name` é o identificador local; `connections` mapeia cada pino para uma rede. Redes internas de propagação de carry usam o prefixo `CARRY`, evitando colisão de nomes achatados com barramentos de saída como `C2`. `X[0]` representa um bit individual; vetores conectados a portas hierárquicas usam intervalos explícitos, como `A_C2[5..0]` e `F_SM[5..0]`. `GND` e `VCC` usam o pino `1` para dirigir a constante.

## Conteúdo e ligações

Instâncias por tipo: GND: 1; XOR: 6; somador_1bit: 6. Cada bit faz X[i]=Z[i] XOR SM[4], com Z={00,SM[3:0]}; seis somadores implementam C2=X+SM[4]. Isso normaliza os dois zeros.

## Dependências e exemplo

As dependências são os tipos listados acima. As equações, exemplos e limites estão em [`sm_para_c2.bdf.md`](../../modulos/sm_para_c2.bdf.md).

## Verificação e estado

Quartus Prime Lite 21.1.0: **PASS** para análise BDF, conversão para Verilog e geração de símbolo, com zero erros e zero avisos em cada etapa ([análise](../../docs/logs/sm_para_c2_analyze.log), [conversão](../../docs/logs/sm_para_c2_convert.log), [símbolo](../../docs/logs/sm_para_c2_symbol.log)). Icarus: **PASS, 32 casos**, executando o HDL exportado; consulte [sim_sm_para_c2.log](../../docs/logs/sim_sm_para_c2.log). O VCD produzido está em [`sm_para_c2.vcd`](../../simulation/waveforms/sm_para_c2.vcd). A avaliação aritmética direta dos grafos, feita anteriormente como checagem auxiliar, é distinta e não foi usada como substituto da simulação HDL.
