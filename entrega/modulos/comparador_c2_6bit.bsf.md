## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# comparador_c2_6bit.bsf

O BSF é o símbolo gráfico da entidade `comparador_c2_6bit`; não contém a lógica do comparador. A interface tem entradas de seis bits `A_C2[5..0]` e `B_C2[5..0]`, e saídas escalares `EQ`, `GT` e `LT`.

Exemplo: para A=−32 e B=−31, o bloco implementado no BDF afirma apenas `LT`.

Verificação: Quartus gerou o BSF a partir da entidade convertida sem erros ou avisos. Seus cinco nomes, direções e larguras coincidem com `config/interfaces.json`. A lógica e os 4096 casos funcionais foram verificados pela simulação do HDL exportado do BDF.
