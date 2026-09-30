# bin_bcd.json

## Objetivo

Descreve o grafo estrutural usado para gerar o conversor `bin_bcd`.

## Entradas e saídas

A interface vem de `interfaces.json`: `MAG[4:0]` entra; `DEZ[3:0]` e `UNI[3:0]` saem.

## Funcionamento

O grafo deriva os limiares T10/T20/T30, codifica as dezenas, seleciona K em {0,10,20,30} e conecta o subtrator hierárquico de cinco bits com SUB=1. A unidade usa os quatro bits baixos do resultado. R4 é descartado intencionalmente: para MAG=0..31, a diferença MAG−K está entre 0 e 9, então R4 é sempre zero. K[1] acompanha DEZ[0], que é necessário para as correções 10 e 30.

## Exemplo

MAG=30 produz DEZ=3, K=30, R=00000 e UNI=0.

## Verificação

O grafo foi convertido para HDL e o BDF passou na análise Quartus 21.1 sem erros nem avisos. Icarus Verilog 13.0 executou o HDL convertido e `tb_bin_bcd.sv` passou nos 32 valores, conforme `docs/logs/sim_bin_bcd.log`. Isso valida a função HDL exportada do BDF, sem transformar o JSON em fonte simulada diretamente.
