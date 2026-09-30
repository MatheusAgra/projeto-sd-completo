## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# ula_core.bdf

Integra A[4:0] e B[4:0] em sinal e magnitude e S[2:0]. Entrega F[5:0], STATUS e EXIBE_F, sem clock nem memória. Os conversores `conv_a` e `conv_b` produzem AC2/BC2 de seis bits; ambos os códigos de zero SM passam a C2=0.

`aritmetica` recebe AC2/BC2 e S0, calcula soma ou subtração em C2 e converte o resultado para SM. O carry interno não é enviado como sinal; o sinal é derivado do resultado signed. A faixa ±30 cabe em C2 de seis bits e em SM com cinco bits de magnitude.

`negacao_b` calcula −B_C2 módulo 64. A rede NEG alimenta C2 de `selecao`, o candidato 010. Essa saída é mostrada diretamente como padrão C2, provisoriamente conforme decisão do usuário. +3 gera 111101. A divergência com o requisito geral de F em SM não foi resolvida pelo professor; consulte `OPERACAO_010_ALTERNATIVAS.md` para mudar o circuito efetivo.

`comparacao` calcula EQ, GT e LT assinados sobre AC2/BC2. Comparar o SM bruto daria resultados incorretos para negativos e zeros. STATUS é `(D3·EQ)+(D4·GT)+(D5·LT)`; fica zero nas demais operações. As três comparações selecionam o vetor ZERO em F.

`logica` recebe A/B brutos, incluindo sinal. Seus candidatos LAND/LXOR preservam todos os cinco bits com o sinal em F5, zero em F4 e os quatro bits inferiores inalterados. `10000 AND 10000` produz `100000`, sem normalização do sinal lógico.

`controle` produz exatamente um D ativo e EXIBE_F em 000/001. O mux recebe ARIT nos candidatos C0 e C1, NEG em C2, ZERO em C3/C4/C5, LAND em C6 e LXOR em C7. Reutilizar ARIT permite compartilhar o caminho ripple enquanto S0 escolhe soma/subtração. Cada bit de F é combinação AND/OR dos oito candidatos.

Exemplos: +15−(−15)=+30 em 001; −15−(+15)=−30; −7<−3 acende STATUS em 101; zero positivo e negativo comparam iguais. Todas essas saídas são combinacionais, sem estado anterior.

Dependências: dois sm_para_c2, modulo2_soma_sub, negador_c2_6bit, comparador_c2_6bit, logica_5bit, decodificador_operacao, mux_resultado_8x6 e portas para STATUS/zeros. O corpo BDF possui as instâncias e conectores nomeados, não apenas símbolos decorativos. Geração, análise/conversão nativas e 8192 casos do HDL exportado são registrados em `docs/VALIDACAO.md`.
