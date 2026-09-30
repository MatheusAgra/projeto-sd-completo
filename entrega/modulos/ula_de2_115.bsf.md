# ula_de2_115.bsf

Símbolo do topo `ula_de2_115`: entrada SW de treze bits; LEDR de dezoito, LEDG de nove e oito HEX de sete bits como saídas. Gerado para completude, embora o topo não seja instanciado por outro módulo.

Este arquivo só descreve a interface gráfica. A implementação existe em `ula_de2_115.bdf`, e as atribuições físicas estão no QSF/CSV. As portas são conferidas automaticamente com o contrato e a exportação nativa. Exemplo: SW[12..0] é o conjunto A/B/S aprovado; não há clock no símbolo.

Resultados da geração e da hierarquia efetiva em `docs/VALIDACAO.md`.
