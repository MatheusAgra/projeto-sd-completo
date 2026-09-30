# render_evidencias.py

Lê diretamente a árvore BDF e renderiza símbolos, coordenadas, primitivas e conectores em PNG. Lê o VCD realmente executado para criar recortes de sinais observados; não calcula respostas esperadas. --circuits-only dispensa VCD. Usa Pillow e Arial local. Exemplo: python scripts/render_evidencias.py. As figuras são documentação programática do circuito e evidência de simulação, sem screenshot ou conferência da interface Quartus. O VCD completo preserva casos que não cabem no recorte.
