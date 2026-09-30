# Visão geral da ULA

Projeto combinacional por portas e hierarquia BDF para a DE2-115 EP4CE115F29C7, com entradas SM de cinco bits (−15..+15), seletor de três bits e saída de seis bits. A arquitetura e o mapeamento foram aprovados pelo usuário em 30/09/2026.

Os operandos passam a C2 de seis bits para aritmética e comparação. Somadores completos em cadeia executam soma/subtração, seguida de conversão para SM; não são usados IP aritmético, ROM, DSP ou HDL comportamental no projeto sintetizado. O negador atende a leitura provisória de 010. AND/XOR operam nos cinco bits brutos, com alinhamento `{L4,0,L3,L2,L1,L0}`.

O decodificador de operações produz seleção one-hot; o mux estrutural AND/OR escolhe o vetor. STATUS só responde em comparação. A saída F fica zero em comparação; a lógica pode preservar zero negativo por ser bit a bit. O projeto não requer clock, reset ou memória.

| Código | F | STATUS | Display de F |
|---|---|---|---|
| 000 | A+B em SM | 0 | Magnitude |
| 001 | A−B em SM | 0 | Magnitude |
| 010 | −B em C2 de seis bits, provisório | 0 | Apagado |
| 011 | 0 | A=B | Apagado |
| 100 | 0 | A>B | Apagado |
| 101 | 0 | A<B | Apagado |
| 110 | AND dos cinco bits alinhado | 0 | Apagado |
| 111 | XOR dos cinco bits alinhado | 0 | Apagado |

O conversor decimal identifica limiares 10/20/30, seleciona K=0/10/20/30 e subtrai K com um ripple de cinco bits. O decoder de segmentos usa equações minimizadas por portas, inclui apagamento explícito de BCD inválido e polaridade ativa em zero.

| Recurso | Uso |
|---|---|
| SW4..0 / SW9..5 | A / B |
| SW12..10 | S2..0 |
| LEDR12..0 | Espelho das chaves |
| LEDG5..0 / LEDG6 | F / STATUS |
| HEX5/4 / HEX3/2 | Magnitudes de A / B |
| HEX1/0 | Magnitude de F em 000/001 |
| HEX7/6 e LEDs restantes | Apagados |

O manual e o enunciado foram lidos com as imagens. Inconsistências registradas: seis bits em F apesar da menção a sete LEDs; sete segmentos apesar da menção a vetores de seis bits; F4 é bit de magnitude, não carry final; 010 conflita com a regra geral de saída SM. Não se afirma confirmação do professor.

O QSF lista somente os 16 BDF, com caminhos relativos e pinagem completa. Verilog exportado pelo Quartus serve a símbolos e testes. Icarus temporário executa o circuito exportado; o fluxo de ModelSim/Questa é preparado, mas a instalação Questa atual tem licença inválida. Consulte `VALIDACAO.md` para o que foi realmente executado.
