## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# ula_de2_115.bsf

Símbolo do topo `ula_de2_115`: entrada SW de treze bits; LEDR de dezoito, LEDG de nove e oito HEX de sete bits como saídas. Gerado para completude, embora o topo não seja instanciado por outro módulo.

Este arquivo só descreve a interface gráfica. A implementação existe em `ula_de2_115.bdf`, e as atribuições físicas estão no QSF/CSV. As portas são conferidas automaticamente com o contrato e a exportação nativa. Exemplo: SW[12..0] é o conjunto A/B/S aprovado; não há clock no símbolo.

Resultados da geração e da hierarquia efetiva em `docs/VALIDACAO.md`.
