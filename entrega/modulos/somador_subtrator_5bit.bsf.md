## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# somador_subtrator_5bit.bsf — documentação do símbolo

## Função do arquivo

O BSF é o símbolo de interface para instâncias hierárquicas da entidade `somador_subtrator_5bit`. Ele não contém a lógica; o circuito está no BDF correspondente, definido pelo grafo de portas da entrega. A conversão e conferência de correspondência entre os arquivos são responsabilidade da integração Quartus.

## Portas

A[4:0], B[4:0], SUB entram; R[4:0] e Cout saem.

## Relação com o circuito

Bloco estrutural de soma/subtração de cinco bits, útil em caminhos que precisam de carry de largura cinco. BX[i]=B[i] XOR SUB em cada bit; o carry inicial é SUB. Cinco instâncias de somador_1bit implementam A+BX+SUB. O resultado R é módulo 32 e Cout registra o sexto bit do cálculo transformado.

## Exemplo e limites

A=00101, B=00011, SUB=1 produz R=00010 e Cout=1. O carry é esperado porque 5+~3+1=34. Todos os padrões são definidos: 32×32×2. A interpretação de carry é unsigned da operação transformada; não equivale a overflow signed.

## Dependências e verificação

O BSF expõe a interface gráfica da entidade, sem implementar lógica. O Quartus Prime Lite 21.1.0 gerou o símbolo correspondente após a análise e conversão do BDF, com zero erros e zero avisos; consulte o [log de geração do símbolo](../docs/logs/somador_subtrator_5bit_symbol.log). A execução do testbench valida o HDL exportado do BDF, não o desenho do BSF em isolamento: PASS — 2048 casos. O resultado está em [sim_somador_subtrator_5bit.log](../docs/logs/sim_somador_subtrator_5bit.log), e o VCD correspondente em [somador_subtrator_5bit.vcd](../simulation/waveforms/somador_subtrator_5bit.vcd). As portas do símbolo continuam sujeitas à conferência da interface declarada no contrato.
