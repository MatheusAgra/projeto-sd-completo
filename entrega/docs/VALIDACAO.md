# Validação da revisão refatorada

**Estado atual: PASS_OFFLINE_PENDING_NATIVE; conferência visual pendente.**

Veja [REFATORACAO_VISUAL_TECNICA.md](REFATORACAO_VISUAL_TECNICA.md), [refatoracao_tecnica.json](refatoracao_tecnica.json), [preparacao_atual.json](preparacao_atual.json) e [validacao_nativa_atual.json](validacao_nativa_atual.json).

Executado: auditoria geométrica dos 16 BDF finais, 1020/1020 destinos por bit; 26 testes de mutação; grafos/contratos/pinagem/QSF/QPF/testbenches preservados; regeneração idêntica dos 32 BDF/BSF e integração isolada. Não executado no novo estado: análise/exportação Quartus, 16 testbenches do HDL novo, compilação completa, netlist funcional, conferência visual ou placa.

A validação funcional anterior está preservada em [historico_pre_refatoracao/VALIDACAO.md](historico_pre_refatoracao/VALIDACAO.md). Os resultados anteriores não aprovam os novos BDF. As figuras e artefatos nativos existentes permanecem históricos até a retomada com Quartus/Icarus.
