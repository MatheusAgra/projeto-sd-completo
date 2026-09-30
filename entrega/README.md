# ULA para DE2-115

Abra `ULA_DE2_115.qpf` no Quartus Prime Lite 21.1. O QSF cadastra exclusivamente os 16 BDF reais de `modulos`, para EP4CE115F29C7. Interfaces, grafos, testbenches e os 96 pinos/padrões I/O foram preservados.

Os 16 BDF/BSF foram refatorados com fios/barramentos contínuos no modelo geométrico auditado. Checks offline atuais: 1020/1020 destinos por bit, 26 testes de mutação, 32/32 arquivos BDF/BSF reproduzidos byte a byte. Detalhes em [REFATORACAO_VISUAL_TECNICA.md](docs/REFATORACAO_VISUAL_TECNICA.md).

**Exportação Quartus, testes do HDL novo, compilação completa, simulação de netlist e conferência visual estão pendentes.** O usuário está instalando Quartus/Icarus; nenhuma nova etapa nativa foi executada. O SOF, HDL/netlist, ZIP, manifesto, DOCX e imagens anteriores são históricos. Não usar esses artefatos como aprovação dos BDF refatorados.

Na raiz do workspace: `python entrega/scripts/preparar.py --generate-only`; `python entrega/scripts/validar_refatoracao.py`. Na entrega extraída, os mesmos scripts aceitam `--root`; depois de instalar ferramentas, execute `python scripts/validar_nativo.py --quartus caminho/quartus --icarus-root caminho/iverilog`. Os guardas de proveniência impedem a aprovação com HDL/logs antigos.

A=SW4..0, B=SW9..5, S=SW12..10; LEDG5..0=F, LEDG6=STATUS. HEX5/4 mostra A, HEX3/2 B e HEX1/0 F segundo as habilitações preservadas. AND/XOR mantêm o sinal e o alinhamento `{L4,0,L3,L2,L1,L0}`. Operação 010 mantém provisoriamente −B em C2. Nenhuma decisão funcional foi alterada para facilitar o layout.

O [guia visual](docs/GUIA_CONFERENCIA_VISUAL_QUARTUS.md) está pronto para a revisão futura dos 16 módulos e permanece pendente. Não houve screenshots, inspeção visual, confirmação de jumpers ou teste físico.
