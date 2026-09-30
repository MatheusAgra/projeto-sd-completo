# bin_bcd.bdf

## Objetivo

Converte a magnitude binária sem sinal `MAG[4:0]` para dezenas `DEZ[3:0]` e unidades `UNI[3:0]` em BCD.

## Entradas e saídas

`MAG` cobre 0 a 31. `DEZ` e `UNI` são vetores BCD de quatro bits. O bloco `somador_subtrator_5bit` fornece a subtração da correção decimal.

## Funcionamento

O circuito detecta `T10=(MAG>=10)`, `T20=(MAG>=20)` e `T30=(MAG>=30)`. As equações são `T10=MAG[4] OR (MAG[3] AND (MAG[2] OR MAG[1]))`, `T20=MAG[4] AND (MAG[3] OR MAG[2])` e `T30=MAG[4] AND MAG[3] AND MAG[2] AND MAG[1]`. As dezenas válidas são codificadas por `DEZ[0]=(T10 AND NOT T20) OR T30`, `DEZ[1]=T20` e `DEZ[3:2]=0`. A correção `K` é 0, 10, 20 ou 30: `K[4]=T20`, `K[3]=DEZ[0]`, `K[2]=T20`, `K[1]=DEZ[0]` e `K[0]=0`. O subtrator calcula `UNI=MAG-K` com `SUB=1`.

As fronteiras produzem 9→09, 10→10, 19→19, 20→20, 29→29, 30→30 e 31→31. Em 10, `K=01010`; em 30, `K=11110`. Para MAG=0..31, `MAG-K` é 0..9, então o quinto bit `R[4]` do subtrator é sempre zero e não é uma saída do contrato; `UNI` recebe `R[3:0]`. O valor 31 permanece determinístico embora não seja uma magnitude aritmética de F.

## Exemplo

Para `MAG=23`, `T20=1`, `DEZ=0010`, `K=20` e `UNI=3` (`0011`).

## Verificação

`bin_bcd.bdf` passou pela análise do Quartus 21.1 sem erros nem avisos e foi convertido para HDL. `tb_bin_bcd.sv`, executado com Icarus Verilog 13.0 sobre o HDL convertido, passou nos 32 valores usando divisão inteira independente. O log está em `docs/logs/sim_bin_bcd.log`; o VCD está em `simulation/waveforms/bin_bcd.vcd`.
