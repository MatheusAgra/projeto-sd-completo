# Como abrir e programar

Abra `ULA_DE2_115.qpf` no Quartus Prime Lite 21.1. O topo é `ula_de2_115`, e todos os circuitos estão em `modulos`. Os documentos de cada BDF e BSF ficam ao lado dos arquivos. A conferência visual dos esquemas será feita pelo usuário.

Para recompilar por CLI, execute `scripts/compilar.ps1`; use o parâmetro Quartus se o diretório de instalação diferir. Os pinos estão no QSF e em `config/pinagem_de2_115.csv`. Nenhum banco do projeto histórico é necessário.

Antes de programar a DE2-115, confira fisicamente JP6 em 3,3 V e JP7 em 2,5 V, perfil usado nas atribuições de I/O. Abra o Programmer, selecione o hardware USB-Blaster e o arquivo `output_files/ULA_DE2_115.sof`, marque Program/Configure e inicie a programação. Essa ação não foi executada pelo agente.

Use SW4/SW9 como sinais, SW3..0/SW8..5 como magnitudes e SW12..10 como seletor. Por exemplo, +15−(−15) deve acender o padrão F=011110 em LEDG5..0 e exibir 30 em HEX1/0. Confira também o apagamento de F em 010..111 e a polaridade dos segmentos.

O teste físico deve registrar revisão, resultado e jumpers reais. O `.sof` configura memória volátil; esta entrega não grava imagem persistente em flash.
