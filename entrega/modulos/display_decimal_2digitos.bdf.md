## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# display_decimal_2digitos.bdf

## Objetivo

Converte uma magnitude binária de cinco bits e dirige os displays de dezena e unidade, com habilitação de apagamento.

## Entradas e saídas

`MAG[4:0]` e `ENABLE` são entradas. `DEZ_SEG[6:0]` e `UNI_SEG[6:0]` são saídas ativas em zero na ordem `{g,f,e,d,c,b,a}`.

## Funcionamento

A instância `bin_bcd` produz os dois nibbles BCD. Duas instâncias de `bcd_7seg` os decodificam. Um inversor calcula `DISABLED=NOT ENABLE`, compartilhado pelas 14 portas OR de máscara: cada saída é `SEG[i] OR DISABLED`. Logo, quando ENABLE=0, ambos os vetores são 1111111.

## Exemplo

Para `MAG=27` e `ENABLE=1`, as saídas mostram 2 e 7. Com os mesmos dados e `ENABLE=0`, as duas saídas são 1111111.

## Verificação

`display_decimal_2digitos.bdf` passou pela análise do Quartus 21.1 sem erros nem avisos e foi convertido para HDL. `tb_display_decimal_2digitos.sv`, executado com Icarus Verilog 13.0 sobre o HDL convertido, passou em 64 combinações de magnitude e ENABLE. O modelo usa divisão inteira e tabela literal independente. O log está em `docs/logs/sim_display_decimal_2digitos.log`; o VCD está em `simulation/waveforms/display_decimal_2digitos.vcd`.
