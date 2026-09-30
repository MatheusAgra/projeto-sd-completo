# tb_ula_de2_115.sv

Testa a integração física exportada do BDF principal. Percorre todas as 8192 combinações A/B/S com S variando primeiro e repete em ordem inversa com S constante por bloco, totalizando 16384 verificações e 8192 entradas únicas.

O modelo usa inteiros para SM e tabela literal independente de segmentos. Compara todos os 18 LEDR, 9 LEDG e 56 segmentos: espelhamento das chaves, F, STATUS, constantes, A/B sempre visíveis, F somente nas operações 000/001 e HEX6/7 sempre apagados.

Inclui ambos os zeros, negativos, ±15/±30, comparações, limites de dezenas e todas as operações. Para 010 lê o padrão C2, mantendo a interpretação provisória. O VCD sai da execução real, sem geração por expectativas. Os 10 ns são acomodação funcional de delta cycles, sem representar atraso medido da placa.

Executado por `scripts/simular.ps1` contra `simulation/generated`. Resultados reais estão em `docs/VALIDACAO.md`.
