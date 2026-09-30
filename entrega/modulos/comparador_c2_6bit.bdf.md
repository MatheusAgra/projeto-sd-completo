## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# comparador_c2_6bit.bdf

Este BDF compara dois valores signed de seis bits em complemento de dois. `A_C2[5..0]` e `B_C2[5..0]` são entradas; `EQ`, `GT` e `LT` são saídas escalares. O domínio completo é −32 a +31.

Seis XNOR combinadas por AND6 geram `EQ`. A comparação dos cinco bits inferiores examina os bits da posição mais significativa para a menos significativa, usando prefixos de igualdade. Com sinais distintos, o operando negativo é menor. Com o mesmo sinal, a ordem unsigned dos cinco bits inferiores preserva a ordem signed em C2, inclusive para dois negativos. `GT` é `NOT(EQ OR LT)`.

Exemplo: A=`100000` (−32) e B=`100001` (−31) produzem `LT=1`, `EQ=0` e `GT=0`.

Dependências: XNOR, NOT, AND2/3/4/6 e OR2/3, todas primitivas lógicas do Quartus. O grafo que gera este desenho está em `config/grafos/comparador_c2_6bit.json`.

Verificação: Quartus 21.1 analisou o BDF, converteu-o em Verilog e gerou o símbolo sem erros nem avisos em cada etapa. O HDL exportado passou 4096/4096 pares signed no Icarus; o resultado está em `docs/logs/sim_comparador_c2_6bit.log` e a waveform real em `simulation/waveforms/comparador_c2_6bit.vcd`.
