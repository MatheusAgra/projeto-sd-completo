> Histórico anterior à refatoração visual. O ZIP, manifesto, SOF, relatório, figuras e logs anteriores não representam os BDF atuais. Os novos checks e pendências estão em docs/REFATORACAO_VISUAL_TECNICA.md.

# Validação das fontes do pacote

As fontes finais foram compactadas no candidato `ULA_DE2_115_candidato.zip`, extraídas em pasta nova `tmp/recompilacao_candidato/entrega` e recompiladas nativamente: zero erros e 36 avisos. O verificador repetiu a auditoria das 96 atribuições de pinos e confirmou zero registradores, memória, DSP e PLL. As 66 fontes BDF/BSF/QPF/QSF/Verilog/testbench coincidiram por SHA-256 com a entrega. Consulte `logs/recompile_zip.log` e `auditoria_fontes.json`.

Após essa aprovação das fontes, foram acrescentados relatório, documentação, auditoria de comentários e scripts de empacotamento; os BDF, BSF, QPF/QSF e modelos exportados não foram modificados. `manifest.json` lista por SHA-256 todos os arquivos incluídos, exceto o próprio manifesto. Não inclui bancos `db`/`incremental_db`, caches Python, bibliotecas compiladas de simulação ou binários Icarus. Os relatórios relevantes do Quartus e o SOF original final foram preservados.

O relatório DOCX foi gerado e sua integridade OOXML foi conferida. A inspeção visual das páginas permanece pendente do renderizador ou da conferência pelo usuário. Conferência gráfica no Quartus, teste físico e confirmação semântica do professor sobre 010 permanecem posteriores. Não se declara execução dessas etapas.

O fechamento do ZIP com esses documentos exige uma nova extração e compilação. O resultado dessa última verificação, o SHA-256 do ZIP efetivamente verificado e a pasta de extração são registrados fora do arquivo compactado em `docs/PACOTE_VALIDADO_FINAL.json` e em `docs/STATUS_EXECUCAO.md` do workspace. Essa evidência externa evita uma referência circular do ZIP ao seu próprio hash.
