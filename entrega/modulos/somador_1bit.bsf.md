## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# somador_1bit.bsf — documentação do símbolo

## Função do arquivo

O BSF é o símbolo de interface para instâncias hierárquicas da entidade `somador_1bit`. Ele não contém a lógica; o circuito está no BDF correspondente, definido pelo grafo de portas da entrega. A conversão e conferência de correspondência entre os arquivos são responsabilidade da integração Quartus.

## Portas

Entradas escalares A, B e Cin; saídas escalares S e Cout.

## Relação com o circuito

Implementa um somador completo combinacional de um bit. P=A XOR B; S=P XOR Cin; Cout=(A AND B) OR (P AND Cin). O grafo de portas usa dois XOR, dois AND2 e um OR2, sem constante ou estado.

## Exemplo e limites

A=1, B=1 e Cin=0 produzem S=0 e Cout=1. Com A=B=Cin=1, a saída é 11. Todos os oito padrões de entrada são definidos.

## Dependências e verificação

O BSF expõe a interface gráfica da entidade, sem implementar lógica. O Quartus Prime Lite 21.1.0 gerou o símbolo correspondente após a análise e conversão do BDF, com zero erros e zero avisos; consulte o [log de geração do símbolo](../docs/logs/somador_1bit_symbol.log). A execução do testbench valida o HDL exportado do BDF, não o desenho do BSF em isolamento: PASS — 8 casos. O resultado está em [sim_somador_1bit.log](../docs/logs/sim_somador_1bit.log), e o VCD correspondente em [somador_1bit.vcd](../simulation/waveforms/somador_1bit.vcd). As portas do símbolo continuam sujeitas à conferência da interface declarada no contrato.
