# ULA para DE2-115

Projeto Quartus Prime Lite 21.1 para EP4CE115F29C7, implementado com dezesseis BDF reais e hierarquia de portas lógicas. Abra [ULA_DE2_115.qpf](entrega/ULA_DE2_115.qpf). O [ZIP](ULA_DE2_115.zip) contém a entrega portátil; o [SOF final](entrega/output_files/ULA_DE2_115.sof) foi gerado pela compilação validada.

Compilação nativa: zero erros, 36 avisos classificados, 100 elementos lógicos e 96 pinos conferidos. Não há registradores, memória, DSP ou PLL. Os dezesseis testbenches independentes passaram sobre HDL efetivamente exportado dos BDF. Core: 8192 combinações; topo e netlist funcional mapeada: 16384 verificações cada, cobrindo 8192 entradas únicas. O pacote fechado foi extraído em outra pasta, recompilado e novamente simulado; seus 456 arquivos foram conferidos pelo manifesto.

Consulte [validação](entrega/docs/VALIDACAO.md), [prova do pacote fechado](docs/PACOTE_VALIDADO_FINAL.json), [status atual](docs/STATUS_EXECUCAO.md) e [instruções de operação](entrega/docs/COMO_ABRIR_E_PROGRAMAR.md). Fontes, símbolos, scripts e evidências têm documentos individuais. [O relatório DOCX](entrega/relatorio/RELATORIO.docx) contém circuitos, tabelas, mapas e waveforms; a capa tem campos a preencher. A integridade OOXML foi conferida, mas sua revisão visual permanece pendente por ausência de renderizador no runtime.

AND/XOR incluem todos os cinco bits, inclusive sinal, e usam alinhamento `{L4,0,L3,L2,L1,L0}`. A operação 010 adota provisoriamente −B em C2 de seis bits, +3→111101. Sua semântica não foi confirmada pelo professor; as alternativas e o procedimento exato de alteração estão [documentados](entrega/docs/OPERACAO_010_ALTERNATIVAS.md).

A licença Questa local falhou no checkout. As simulações executadas usam Icarus autorizado pelo usuário; ModelSim/Questa permanece preparado. [Ferramentas e comandos](entrega/docs/FERRAMENTAS_SIMULACAO.md) explicam como reproduzir os testes. A implementação sintetizada continua exclusivamente em BDF.

Conferência visual no Quartus, confirmação física de JP6/JP7 e teste na placa são etapas posteriores a cargo do usuário. Não são apresentados como executados. Referências do Drive, ferramentas portáteis e caches locais ficam fora do Git; plano, enunciado e registros do projeto estão preservados.
