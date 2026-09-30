## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# modulo2_soma_sub.bsf — documentação do símbolo

## Função do arquivo

O BSF é o símbolo de interface para instâncias hierárquicas da entidade `modulo2_soma_sub`. Ele não contém a lógica; o circuito está no BDF correspondente, definido pelo grafo de portas da entrega. A conversão e conferência de correspondência entre os arquivos são responsabilidade da integração Quartus.

## Portas

A_C2[5:0], B_C2[5:0], SUB entram; F_SM[5:0] sai em sinal e magnitude normalizada.

## Relação com o circuito

Conecta o somador/subtrator C2 de seis bits ao conversor C2 para sinal e magnitude. A instância somador_subtrator_6bit calcula A_C2+(B_C2 XOR {6{SUB}})+SUB. Seu R segue à instância c2_para_sm; Cout interno não altera sinal/magnitude. Não há BCD neste módulo.

## Exemplo e limites

A_C2=+15, B_C2=−15 e SUB=0 resultam em F_SM=000000. Com A_C2=−15, B_C2=+15 e SUB=1, o resultado numérico é −30 e F_SM=111110. A saída SM representa resultados −30..+30 para entradas válidas da ULA, −15..+15. O vetor C2 interno cobre seis bits. O conversor filho tem −32 fora de domínio; esse padrão é inalcançável com os operandos válidos.

## Dependências e verificação

O BSF expõe a interface gráfica da entidade, sem implementar lógica. O Quartus Prime Lite 21.1.0 gerou o símbolo correspondente após a análise e conversão do BDF, com zero erros e zero avisos; consulte o [log de geração do símbolo](../docs/logs/modulo2_soma_sub_symbol.log). A execução do testbench valida o HDL exportado do BDF, não o desenho do BSF em isolamento: PASS — 1922 casos. O resultado está em [sim_modulo2_soma_sub.log](../docs/logs/sim_modulo2_soma_sub.log), e o VCD correspondente em [modulo2_soma_sub.vcd](../simulation/waveforms/modulo2_soma_sub.vcd). As portas do símbolo continuam sujeitas à conferência da interface declarada no contrato.
