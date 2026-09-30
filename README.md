# ULA para DE2-115

Projeto Quartus para EP4CE115F29C7, implementado exclusivamente com os 16 BDF de [entrega/modulos](entrega/modulos). Abra [ULA_DE2_115.qpf](entrega/ULA_DE2_115.qpf).

A refatoração dos 16 BDF/BSF foi implementada em 30/09/2026: conexões contínuas por contato físico, barramentos, fan-out, constantes, carry e níveis internos até as portas do somador de um bit. Auditoria offline: 1020/1020 destinos por bit, 26 testes de mutação e regeneração idêntica dos 32 BDF/BSF. Interfaces, grafos, pinagem, QSF/QPF e testbenches foram preservados. Esses checks seguem o modelo geométrico documentado; a interpretação nativa dos taps/cruzamentos ainda exige Quartus.

**Validação nativa e conferência visual pendentes.** Quartus/Icarus não estão disponíveis nesta sessão, e o usuário está instalando ambos. Não foram executadas novas exportações, testes HDL, compilação ou simulação de netlist. O [relatório técnico atual](entrega/docs/REFATORACAO_VISUAL_TECNICA.md) registra cobertura, evidências, bloqueios e retomada. O [guia visual](docs/GUIA_CONFERENCIA_VISUAL_QUARTUS.md) permanece sem aprovação; nenhuma imagem ou screenshot foi inspecionado nesta etapa.

Para reproduzir os checks disponíveis, execute `python entrega/scripts/preparar.py --generate-only` e `python entrega/scripts/validar_refatoracao.py`. Depois de instalar as ferramentas, use `python entrega/scripts/validar_nativo.py --quartus caminho/quartus --icarus-root caminho/iverilog`.

O ZIP, SOF, HDL/netlist, relatório DOCX, figuras e resultados anteriores são históricos e não representam o novo roteamento. Os documentos/logs anteriores foram preservados em [historico_pre_refatoracao](entrega/docs/historico_pre_refatoracao). Nenhum novo pacote ou SOF validado foi emitido nesta etapa.

Decisões funcionais preservadas: AND/XOR incluem os cinco bits e o alinhamento `{L4,0,L3,L2,L1,L0}`; operação 010 mantém provisoriamente −B em C2 de seis bits. Semântica do professor e teste físico na placa continuam pendentes.
