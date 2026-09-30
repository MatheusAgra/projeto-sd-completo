## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# sm_para_c2.bdf — documentação do circuito

## Objetivo e interface

Converte sinal e magnitude de cinco bits para complemento de dois de seis bits. SM[4:0] entrada, com SM[4] como sinal; C2[5:0] saída.

## Funcionamento

Forma Z={00,SM[3:0]}, calcula X=Z XOR {6{SM[4]}} e soma SM[4] em uma cadeia de seis instâncias de somador_1bit. A primeira entrada Cin é o sinal e as demais propagam o carry. Isso implementa (Z XOR sinal)+sinal sem converter o bit de sinal como magnitude.

## Exemplo e limites

SM=00111 representa +7 e resulta em 000111. SM=10111 representa −7 e resulta em 111001. Os padrões 00000 e 10000 resultam ambos em 000000. Os 32 padrões SM estão cobertos. A faixa numérica de entrada é −15..+15; ambos os códigos de zero são normalizados.

## Dependências

Seis instâncias do módulo somador_1bit; XOR e GND.

## Verificação

Quartus Prime Lite 21.1.0 concluiu análise do BDF, conversão BDF→Verilog e geração do símbolo: [análise](../docs/logs/sm_para_c2_analyze.log), [conversão](../docs/logs/sm_para_c2_convert.log) e [símbolo](../docs/logs/sm_para_c2_symbol.log), cada etapa com zero erros e zero avisos. O HDL exportado nativamente foi executado no Icarus pelo testbench independente: PASS — 32 casos. A referência decodifica sinal e magnitude como inteiro e compara o padrão C2 de seis bits; inclui os dois zeros SM. Resultado registrado em [sim_sm_para_c2.log](../docs/logs/sim_sm_para_c2.log); o VCD foi aberto e salvo em [sm_para_c2.vcd](../simulation/waveforms/sm_para_c2.vcd).

Esses registros validam o BDF analisado e o HDL que o Quartus exportou nesta revisão; não afirmam teste físico na placa.
