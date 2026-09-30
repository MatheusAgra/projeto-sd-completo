## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# decodificador_operacao.bdf

O circuito combina `S[2..0]` para gerar `D[7..0]` one-hot e `EXIBE_F`. Para cada valor i de 0 a 7, somente D[i] fica em 1 quando S=i. `EXIBE_F = NOT(S2) AND NOT(S1)`, portanto fica ativo apenas para 000 e 001.

Exemplo: `S=101` gera `D=00100000` e `EXIBE_F=0`; `S=001` ativa D1 e `EXIBE_F`.

Dependências: três NOT, oito AND3 e um AND2. O grafo estrutural está em `config/grafos/decodificador_operacao.json`.

Verificação: Quartus analisou o BDF, converteu o HDL e gerou o símbolo, cada etapa com zero erros e zero avisos. No Icarus, os oito seletores passaram; log em `docs/logs/sim_decodificador_operacao.log` e waveform real em `simulation/waveforms/decodificador_operacao.vcd`.
