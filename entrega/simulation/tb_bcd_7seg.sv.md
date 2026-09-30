# tb_bcd_7seg.sv

## Objetivo

Testbench exaustivo da tabela BCD para sete segmentos.

## Entradas e saídas

Aplica os 16 códigos a `BCD[3:0]` e observa `SEG[6:0]`.

## Funcionamento

O valor esperado vem de uma tabela literal de segmentos ativos em zero, separada das expressões minimizadas. Os códigos inválidos 10..15 esperam 1111111. Divergências chamam `$fatal`; a simulação grava `waveforms/bcd_7seg.vcd`.

## Exemplo

BCD=2 deve resultar em 7'b0100100; BCD=15 deve resultar em 7'b1111111.

## Verificação

Executado em Icarus Verilog 13.0 contra `simulation/generated/bcd_7seg.v`; passou nos 16 códigos. O log está em `docs/logs/sim_bcd_7seg.log`, e o teste escreveu `simulation/waveforms/bcd_7seg.vcd`.
