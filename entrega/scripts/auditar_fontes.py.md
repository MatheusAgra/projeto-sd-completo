# auditar_fontes.py

Audita comentários e docstrings nas fontes autorais, reconhece strings e comentários de Verilog/BDF/BSF e aceita somente os cabeçalhos legais Intel/Altera obrigatórios. Confere documentação individual para fontes, scripts, configurações, tabelas, figuras, waveforms, pinagem, SOF e DOCX. Caches, logs internos e relatórios nativos têm índices gerais. Grava o relatório com LF explícito, inclusive no Windows.

Execute com Python 3: `python scripts/auditar_fontes.py`. `--compare pasta/entrega` compara SHA-256 das fontes BDF/BSF/QPF/QSF e dos HDL/testbenches com o pacote extraído. O resultado é gravado em `docs/auditoria_fontes.json`; qualquer ausência ou divergência aborta. A auditoria não substitui a análise Quartus nem a simulação.
