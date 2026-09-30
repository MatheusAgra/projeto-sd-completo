# limpar_gerados.py

Remove apenas comentÃ¡rios nÃ£o legais de arquivos gerados, mantendo strings e avisos de Copyright/License Agreement. Antes de gravar exige igualdade dos tokens funcionais entre original e versÃ£o limpa. Exemplo: python scripts/limpar_gerados.py simulation/netlist/ula_de2_115.vo. A netlist foi compilada/simulada novamente depois da limpeza e o ZIP serÃ¡ recompilado com os sÃ­mbolos limpos. CabeÃ§alhos legais preservados sÃ£o a exceÃ§Ã£o documentada Ã  ausÃªncia literal de comentÃ¡rios.
