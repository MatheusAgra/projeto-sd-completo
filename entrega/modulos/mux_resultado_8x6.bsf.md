## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# mux_resultado_8x6.bsf

O BSF expõe a interface gráfica do multiplexador `mux_resultado_8x6`; não contém lógica de seleção. As entradas C0–C7 têm seis bits cada, D tem oito bits e F tem seis bits.

Exemplo: se D3 for o único bit ativo, o BDF encaminha C3 a F.

Verificação: símbolo gerado pelo Quartus sem erros ou avisos. Os dez nomes, direções e larguras coincidem com `config/interfaces.json`; a seleção foi verificada no HDL convertido do BDF.
