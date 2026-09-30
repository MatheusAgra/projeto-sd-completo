## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# ula_de2_115.bdf

Circuito principal efetivamente ligado aos recursos da DE2-115. Entrada SW[12:0]; saídas LEDR[17:0], LEDG[8:0] e HEX0..HEX7[6:0]. Não declara clock, KEY ou chaves não usadas. O dispositivo EP4CE115F29C7 e os 96 pinos são definidos no QSF.

SW4..0 entra em A do core, SW9..5 em B, SW12..10 em S. SW4 e SW9 são os sinais SM; SW10 é S0. Cada uma das treze chaves é replicada em LEDR do mesmo índice; LEDR17..13 ficam em zero.

O core fornece F nos seis LEDG inferiores, com F5 em LEDG5 e STATUS em LEDG6. LEDG8..7 ficam apagados. Soma/subtração usam F em SM; 010 usa padrão C2 de −B, provisoriamente; comparação zera F; AND/XOR preservam o sinal lógico alinhado em F5. Assim LEDG5 indica sinal SM somente nos modos em que a saída tem esse formato.

As magnitudes dos operandos são estendidas com zero para MAGA/MAGB de cinco bits e alimentam dois blocos de display sempre habilitados. A ocupa HEX5/4 (dezena/unidade); B ocupa HEX3/2. Os sinais negativos dos operandos aparecem no espelho de suas chaves, sem sinal nos displays decimais.

F[4..0] alimenta o terceiro display decimal. EXIBE_F habilita HEX1/0 somente em 000/001; nas demais operações seus sete segmentos ficam em 1 (apagados). HEX7/6 ficam em 1 em todos os modos. A unidade está no display à direita de cada par; os segmentos são ativos em zero, bit0=a e bit6=g.

Exemplo físico: SW4..0=01111, SW9..5=11111, SW12..10=001. A=+15, B=−15, F=+30; LEDG5..0=011110, STATUS=0, HEX1/0 mostram 30, A/B mostram 15. Os sinais dos operandos permanecem em LEDR4/9.

As ligações BUF do grafo são materializadas por dois inversores em série no BDF; não existe módulo HDL auxiliar. O Fitter pode otimizar esses pares. Conectores com o mesmo nome formam redes elétricas, e barramentos explícitos mantêm a ordem dos bits.

Dependências: ula_core e três display_decimal_2digitos, inversores de ligação e fontes GND/VCC. Perfil elétrico de referência JP6=3,3 V/JP7=2,5 V, com pinos fixos tratados individualmente. Atribuições do Fitter, todos os 8192 padrões físicos e a recompilação portátil são registrados em `docs/VALIDACAO.md`. A inspeção da interface Quartus e o teste real na placa ficam a cargo do usuário.
