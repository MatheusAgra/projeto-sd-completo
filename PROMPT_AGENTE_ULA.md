# Instrução para o agente executor

Leia integralmente `PLANO_EXECUCAO_ULA.md` e o enunciado `Projeto_Primeira_Unidade_2026_2.pdf`, incluindo as imagens. O estudo e as cópias de referência do Drive estão em `tmp/drive/PROJETO_ULA`. O objetivo desta execução é produzir a ULA completa e integrada no Quartus, para a DE2-115 com EP4CE115F29C7, e não somente gerar exemplos ou explicar como construir.

Antes de fixar decisões ainda propostas, apresente ao usuário a arquitetura, o mapeamento de chaves/LEDs/displays e o alinhamento de cinco para seis bits das operações lógicas. Preserve as decisões já dadas: AND/XOR incluem todos os cinco bits, inclusive o sinal; 010 mostra o padrão C2, adotando provisoriamente +3→111101, com a indecisão documentada. Não pedir de novo essas definições. Resolva a licença de simulação ou combine alternativa antes de declarar testes concluídos.

Implemente todos os módulos em BDF reais, com primitivas lógicas e hierarquia estrutural. Gere BSF coerentes e o circuito principal efetivamente conectado. A implementação sintetizada não deve ser substituída por HDL comportamental, IP aritmético ou BDF decorativo. HDL exportado pelo Quartus pode servir para geração de símbolos e simulação; não o cadastre como entidade duplicada no projeto BDF.

Entregue QPF/QSF com fontes e pinos completos, circuitos de conversão, aritmética, comparação, lógica, seleção, BCD e sete segmentos, integração física, testes executáveis, waveforms reais, documentação, relatório e `.sof` final. Use o inventário e os critérios do plano; só adapte a decomposição após validar a mudança relevante.

Não use Computer Use para validar a interface do Quartus. O usuário fará essa conferência depois. Execute análise, conversão, síntese, fitting, assembly e simulação por ferramentas nativas. Os caminhos locais e o fluxo BDF→Verilog→BSF verificado estão no plano. A ausência de licença no Questa não equivale a teste aprovado.

Não inclua comentários didáticos, TODO, docstrings ou notas explicativas nos arquivos de implementação/automação. Explique cada arquivo em seu próprio `<arquivo.ext>.md`, incluindo documentos separados para BDF e BSF. Dê mais atenção aos conversores, BCD, caminho aritmético, ULA/core e circuito principal. Confira também cabeçalhos gerados automaticamente, sem remover avisos cuja preservação seja obrigatória nem ocultar incompatibilidades.

Crie `docs/OPERACAO_010_ALTERNATIVAS.md` com a leitura provisória, a diferença entre negar B e representar B em C2, e o procedimento exato para mudar a saída da negação para sinal e magnitude. Indique circuitos, conexões, símbolos, testes e documentos afetados. Não trate essa operação como semanticamente resolvida pelo professor.

Teste a implementação efetiva exportada dos BDF contra modelo independente: 8192 combinações de A/B/S, todos os módulos isolados, zero positivo/negativo, negativos, ±15, ±30, polaridade e apagamento de displays. Confira pinagem produzida pelo Fitter, ausência de estado, correspondência entre símbolos e entidades e recompilação do ZIP extraído em outra pasta. Não invente resultados ou waveforms.

Pode usar subagentes `gpt-6-luna` com esforço `high` para frentes independentes, conforme autorização do usuário. Congele interfaces, delimite arquivos de cada subagente e mantenha integração/verificação sob responsabilidade do principal. Não permita edições concorrentes no contrato e no gerador compartilhado.

Salve progresso em `docs/STATUS_EXECUCAO.md`. Quando uma janela principal de uso chegar a 2% ou menos restantes, registre checkpoint. O usuário deseja usar um reset existente, mas a ferramenta atual exige confirmação explícita por consumo: cumpra essa exigência e a política de idempotência do plano. Não contorne por Computer Use nem prometa consumo automático irrestrito. Não comprar créditos.

Persista até concluir as etapas autorizadas e necessárias. Registre objetivamente qualquer bloqueio, mantenha as fontes prontas para retomada e diferencie circuito compilado, circuito simulado, conferência visual e teste físico. Ao final, informe os arquivos entregues, validações efetivamente executadas e pendências reais.
