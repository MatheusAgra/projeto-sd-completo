# display_decimal_2digitos.json

## Objetivo

Descreve a hierarquia de conversão, decodificação e máscara dos dois displays decimais.

## Entradas e saídas

`MAG[4:0]` e `ENABLE` entram; `DEZ_SEG[6:0]` e `UNI_SEG[6:0]` saem.

## Funcionamento

Instancia `bin_bcd`, dois `bcd_7seg` e uma inversão de ENABLE. Quatorze portas OR aplicam `SEG[i] OR NOT(ENABLE)`, apagando os vetores com nível alto.

## Exemplo

MAG=27 com ENABLE=1 mostra 2 e 7; ENABLE=0 força ambas as saídas a 1111111.

## Verificação

`tb_display_decimal_2digitos.sv` contém 64 combinações com referência independente. O BDF passou pela análise Quartus 21.1 e foi convertido; Icarus Verilog 13.0 executou o HDL convertido e passou as 64 combinações, conforme `docs/logs/sim_display_decimal_2digitos.log`.
