## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# ula_core.bsf

Símbolo de `ula_core`, correspondente ao BDF do mesmo nome. A e B são entradas de cinco bits SM; S tem três bits. F tem seis bits; STATUS e EXIBE_F são saídas escalares. O símbolo é instanciado como `ula` no topo físico.

O BSF descreve as portas e o desenho do bloco; a função é implementada no BDF. A correspondência é conferida contra o contrato e o Verilog exportado nativamente; o BSF final é gerado pelo Quartus a partir dessa exportação e não inclui entidade duplicada no QSF.

Exemplo: conectar A a SW[4..0], B a SW[9..5] e S a SW[12..10] no topo. A negação 010 provisória não muda as portas deste símbolo. Resultado da conferência e compilação da hierarquia em `docs/VALIDACAO.md`.
