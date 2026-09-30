# tb_bin_bcd.sv

## Objetivo

Testbench exaustivo para o conversor binário→BCD.

## Entradas e saídas

Aplica os 32 padrões em `MAG[4:0]` e observa `DEZ[3:0]` e `UNI[3:0]`.

## Funcionamento

O esperado usa divisão inteira por dez e resto, independente do grafo. Cada vetor recebe um passo de simulação; uma divergência chama `$fatal`. A execução grava `waveforms/bin_bcd.vcd`.

## Exemplo

Para MAG=31, espera DEZ=3 e UNI=1.

## Verificação

Executado em Icarus Verilog 13.0 contra `simulation/generated/bin_bcd.v`; passou nos 32 vetores. O log está em `docs/logs/sim_bin_bcd.log`, e o teste escreveu `simulation/waveforms/bin_bcd.vcd`.
