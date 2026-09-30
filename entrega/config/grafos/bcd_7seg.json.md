# bcd_7seg.json

## Objetivo

Representa em portas a minimização das sete saídas ativas em zero do decodificador BCD.

## Entradas e saídas

`BCD[3:0]` entra e `SEG[6:0]` sai na ordem `{g,f,e,d,c,b,a}`.

## Funcionamento

Inversores compartilhados formam as literais negativas. Produtos compartilhados implementam os implicantes primos e portas OR combinam os termos por segmento. Os mintermos 10..15 são incluídos explicitamente nas funções que precisam gerar nível alto de apagamento.

## Exemplo

BCD=2 deve gerar SEG=0100100.

## Verificação

`docs/tabelas/reducoes_bcd_displays.md` registra as expressões QMC e `tb_bcd_7seg.sv` compara os 16 códigos com uma tabela literal. O BDF passou pela análise Quartus 21.1 e foi convertido; Icarus Verilog 13.0 executou o HDL convertido e passou os 16 padrões, conforme `docs/logs/sim_bcd_7seg.log`.
