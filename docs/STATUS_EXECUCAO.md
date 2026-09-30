# Status da execução

Checkpoint em 30/09/2026. Implementação integrada, compilação e simulação concluídas; fechamento documental em andamento.

O plano foi lido integralmente. As quatro páginas do enunciado foram inspecionadas como imagens e seu texto foi extraído. As cópias do Drive permanecem em `tmp/drive/PROJETO_ULA`, fora da entrega. A tabela completa de pinagem e os perfis JP6/JP7 foram consultados no manual local.

Decisões preservadas: AND/XOR incluem todos os cinco bits brutos; operação 010 adota provisoriamente a negação numérica em C2 de seis bits, +3→111101. Não há confirmação semântica do professor.

O usuário aprovou os 16 módulos, distribuição SW/LED/HEX, F zerado nas comparações e alinhamento lógico `{L4,0,L3,L2,L1,L0}`. As interfaces estão congeladas em `entrega/config/interfaces.json`. Existem 16 BDF reais conectados por primitivas e hierarquia e 16 BSF gerados nativamente, com documentos individuais; QPF/QSF cadastram somente BDF e pinagem completa. O grafo possui 342 instâncias. Os subagentes Luna/high trabalharam em arquivos delimitados; contrato, gerador e integração ficaram sob responsabilidade do principal.

Questa falhou por checkout de licença, saída 4, sem teste aprovado. O usuário autorizou Icarus temporário e solicitou manter ModelSim preparado. Icarus 13.0 portátil executou os 16 testbenches independentes sobre Verilog efetivamente exportado dos BDF. Core: 8192 combinações; topo: 16384 verificações sobre 8192 entradas únicas. Todos os módulos isolados passaram. Zeros, negativos, ±15, ±30, polaridade e apagamento foram verificados. VCDs completos reais e PNGs derivados estão na entrega. Detalhes em `entrega/docs/FERRAMENTAS_SIMULACAO.md`.

Os 16 BDF passaram análise, conversão nativa e geração de símbolos com zero erros/avisos. A revisão final compilou no Quartus Lite 21.1 para EP4CE115F29C7: zero erros, 36 avisos preservados e classificados. Recursos: 100 LE, 96 pinos, zero registradores, memória, DSP e PLL. As 96 localizações e padrões de I/O do Fitter coincidiram com o CSV. O SOF final tem SHA-256 `42e9b19a48a38a36f0bc3bc9fcd2d7a49ac828c207be5762bab68065b5e14069`.

A netlist funcional mapeada pelo Quartus, com a biblioteca oficial Cyclone IV E, também passou 16384 verificações/8192 entradas únicas. Os avisos de coerção de portas do Icarus foram preservados. A tentativa legada de simulador interno incompatível foi registrada e substituída por `quartus_eda`. O TimeQuest relatou 20 caminhos combinacionais; maior estimativa 23,788 ns SW[5]→HEX0[1], Slow 1200mV 85C. Não existe orçamento temporal definido nem aprovação temporal/SDF alegada.

O ZIP candidato foi extraído em `tmp/recompilacao_candidato/entrega` e recompilado: zero erros, 36 avisos. A auditoria repetida conferiu os 96 pinos e ausência de estado. Os hashes de 66 fontes BDF/BSF/QPF/QSF/Verilog/testbench coincidiram com a entrega. SOFs recompilados podem ter metadados de compilação distintos; o SOF entregue permanece o da revisão original final validada.

A auditoria de comentários/docstrings e cobertura de documentos passou. Cabeçalhos legais Intel/Altera obrigatórios foram preservados e enumerados; não se declara ausência literal de comentários nesses arquivos gerados. Documentação profunda, tabelas, mapas e imagens dos circuitos estão presentes.

Relatório DOCX gerado, com identificação em branco conforme escolha do usuário. A integridade OOXML, referências de imagens, 74 inserções de imagens, 40 tabelas e 96 pinos foram conferidos. O runtime não fornece LibreOffice, e o renderer canônico da skill documents falhou por ausência de soffice.exe. Foi solicitada ao usuário autorização para LibreOffice temporário ou conferência visual pelo próprio usuário; a resposta ainda está pendente. A aprovação visual não pode ser declarada e impede o fechamento do relatório como entrega visualmente validada.

O ZIP fechado `ULA_DE2_115.zip` foi criado e extraído em `tmp/recompilacao_pacote_fechado/entrega`, seguido de nova compilação nativa: zero erros/36 avisos, 100 LE/96 pinos/zero estado. Os dezesseis testes foram repetidos nessa extração e passaram. A comparação de 66 fontes manteve os hashes e a verificação do ZIP conferiu CRC, lista exata e os hashes SHA-256 dos 456 arquivos do manifesto. SHA-256 do ZIP: `1a0f402b5d84c78bcde45c3a4476dc1580bbc17570906a540675626a5ae48a6f`. A prova externa está em `PACOTE_VALIDADO_FINAL.json`; os logs são `RECOMPILACAO_PACOTE_FINAL.log` e `SIMULACAO_PACOTE_FINAL.log`. O pacote contém DOCX com inspeção visual explicitamente pendente e aguarda essa decisão antes da entrega final do relatório.

Conferência visual no Quartus e teste físico permanecem posteriores, a cargo do usuário. Jumpers reais JP6=3,3 V/JP7=2,5 V não foram conferidos fisicamente.

Última leitura de limites: janela semanal com 90% usados, 10% restantes; dois resets existentes disponíveis. Nenhum reset consumido e nenhuma compra. Ao chegar a 2% restantes, registrar novo checkpoint e solicitar confirmação explícita para um consumo específico, com chave de idempotência persistida antes da chamada e reutilizada em resultado incerto. A ferramenta de reset não foi chamada.

Única pendência para fechar a entrega documental: decisão do usuário sobre renderizador temporário ou conferência visual própria do DOCX. Se a renderização provocar alterações no documento, atualizar manifesto, pacote e evidência externa. As etapas autorizadas de implementação, exportação, compilação, simulação, documentação estrutural e portabilidade estão concluídas.

Publicação autorizada em 30/09/2026: o usuário solicitou enviar todo o projeto para `https://github.com/MatheusAgra/projeto-sd-completo.git`. O repositório estava vazio, com branch padrão main, e a autenticação estava ativa. As fontes e evidências validadas, relatório com revisão visual pendente, SOF, ZIP, plano e enunciado estão preparados para commit. Referências e ferramentas temporárias, caches e bancos regeneráveis são excluídos pelo `.gitignore`. A publicação não altera as evidências nem declara resolvidas as pendências técnicas/documentais.
