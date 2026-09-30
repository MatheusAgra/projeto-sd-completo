## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# sm_para_c2.bsf — documentação do símbolo

## Função do arquivo

O BSF é o símbolo de interface para instâncias hierárquicas da entidade `sm_para_c2`. Ele não contém a lógica; o circuito está no BDF correspondente, definido pelo grafo de portas da entrega. A conversão e conferência de correspondência entre os arquivos são responsabilidade da integração Quartus.

## Portas

SM[4:0] entrada, com SM[4] como sinal; C2[5:0] saída.

## Relação com o circuito

Converte sinal e magnitude de cinco bits para complemento de dois de seis bits. Forma Z={00,SM[3:0]}, calcula X=Z XOR {6{SM[4]}} e soma SM[4] em uma cadeia de seis instâncias de somador_1bit. A primeira entrada Cin é o sinal e as demais propagam o carry. Isso implementa (Z XOR sinal)+sinal sem converter o bit de sinal como magnitude.

## Exemplo e limites

SM=00111 representa +7 e resulta em 000111. SM=10111 representa −7 e resulta em 111001. Os padrões 00000 e 10000 resultam ambos em 000000. Os 32 padrões SM estão cobertos. A faixa numérica de entrada é −15..+15; ambos os códigos de zero são normalizados.

## Dependências e verificação

O BSF expõe a interface gráfica da entidade, sem implementar lógica. O Quartus Prime Lite 21.1.0 gerou o símbolo correspondente após a análise e conversão do BDF, com zero erros e zero avisos; consulte o [log de geração do símbolo](../docs/logs/sm_para_c2_symbol.log). A execução do testbench valida o HDL exportado do BDF, não o desenho do BSF em isolamento: PASS — 32 casos. O resultado está em [sim_sm_para_c2.log](../docs/logs/sim_sm_para_c2.log), e o VCD correspondente em [sm_para_c2.vcd](../simulation/waveforms/sm_para_c2.vcd). As portas do símbolo continuam sujeitas à conferência da interface declarada no contrato.
