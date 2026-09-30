# ULA para DE2-115

Abra `ULA_DE2_115.qpf` no Quartus Prime Lite 21.1. O projeto usa o EP4CE115F29C7 e exclusivamente os dezesseis BDF reais de `modulos`. A compilação final produziu `output_files/ULA_DE2_115.sof`; a pinagem completa está no QSF e em `config/pinagem_de2_115.csv`.

O circuito passou a compilação nativa, os dezesseis testes dos módulos sobre HDL exportado e a simulação adicional da netlist funcional mapeada. Consulte `docs/VALIDACAO.md` para contagens, logs, avisos e limites. `docs/PACOTE_VALIDADO.md` registra a validação do ZIP fechado.

As interfaces e o mapeamento físico foram aprovados. A=SW4..0, B=SW9..5, S=SW12..10; LEDG5..0 mostra F e LEDG6 mostra STATUS. HEX5/4 mostra magnitude de A, HEX3/2 de B e HEX1/0 de F em soma/subtração. AND/XOR incluem o sinal e usam `{L4,0,L3,L2,L1,L0}`. A operação 010 adota provisoriamente −B em C2, com +3→111101; a semântica permanece pendente do professor. A alternativa e o procedimento exato de alteração estão em `docs/OPERACAO_010_ALTERNATIVAS.md`.

Para recompilar, execute `./scripts/compilar.ps1`. Para regenerar/exportar BDF e símbolos, use Python 3 em `scripts/preparar.py`; os caminhos Quartus podem ser parametrizados. Para os testes, execute `./scripts/simular.ps1 -IcarusRoot caminho/iverilog` ou `-QuestaPath caminho/ModelSim`. `scripts/obter_icarus.ps1` obtém a alternativa portátil com hashes verificados. A licença Questa local falhou, por isso os resultados executados são de Icarus autorizado pelo usuário. `simulation/run.do` permanece preparado para ModelSim/Questa.

Cada implementação, símbolo, script e evidência possui seu próprio `.md`. O relatório imprimível está em `relatorio/RELATORIO.docx`, com identificação a preencher. `docs/COMO_ABRIR_E_PROGRAMAR.md` descreve os passos manuais na placa. Conferência visual no Quartus, confirmação dos jumpers e teste físico cabem ao usuário e não foram declarados executados.
