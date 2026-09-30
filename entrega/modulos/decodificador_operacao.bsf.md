## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# decodificador_operacao.bsf

O BSF é o símbolo de interface da entidade `decodificador_operacao`; não implementa suas equações. Ele expõe `S[2..0]` como entrada de três bits, `D[7..0]` como saída de oito bits e `EXIBE_F` como saída escalar.

Exemplo: S=`101` seleciona D5 no BDF e mantém `EXIBE_F=0`.

Verificação: geração pelo Quartus concluída sem erros ou avisos. As três portas, direções e larguras coincidem com `config/interfaces.json`; o BDF foi testado nos oito valores de S.
