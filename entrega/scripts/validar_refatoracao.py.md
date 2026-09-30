# validar_refatoracao.py

Executa verificações disponíveis sem Quartus/Icarus: hashes das interfaces,
grafos, testbenches, pinagem e QSF/QPF contra o baseline; validador lógico;
auditoria geométrica dos BDF finais; cadastro exclusivo de 16 BDF e 96 pinos/I/O;
ordem hierárquica; contratos BSF; regeneração em pasta temporária com igualdade
byte a byte dos 32 BDF/BSF. Emite `docs/refatoracao_tecnica.json` somente após
todos esses checks passarem. Não apresenta esses resultados como simulação.

Comando: `python entrega/scripts/validar_refatoracao.py`. `--root` seleciona
outra entrega extraída, cujo baseline e metadados devem estar presentes.
`PASS_OFFLINE_PENDING_NATIVE` exige ainda exportação Quartus, 16 testbenches,
compilação completa, netlist funcional e a revisão visual posterior.
