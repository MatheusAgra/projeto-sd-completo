# tb_display_decimal_2digitos.sv

## Objetivo

Testbench exaustivo do display decimal, incluindo apagamento.

## Entradas e saídas

Aplica todos os 32 valores de `MAG[4:0]` com `ENABLE` em zero e em um; observa `DEZ_SEG[6:0]` e `UNI_SEG[6:0]`.

## Funcionamento

O modelo de referência calcula dezena por divisão inteira e unidade pelo resto, e usa uma tabela literal independente para os sete segmentos. Com ENABLE baixo, ambas as saídas esperadas são 1111111. Qualquer diferença chama `$fatal`; a execução grava `waveforms/display_decimal_2digitos.vcd`.

## Exemplo

MAG=27 com ENABLE=1 mostra os dígitos 2 e 7. Com ENABLE=0, ambas as linhas são 1111111.

## Verificação

Executado em Icarus Verilog 13.0 contra `simulation/generated/display_decimal_2digitos.v`; passou em 64 vetores (32 magnitudes × 2 estados de ENABLE). O log está em `docs/logs/sim_display_decimal_2digitos.log`, e o teste escreveu `simulation/waveforms/display_decimal_2digitos.vcd`.
