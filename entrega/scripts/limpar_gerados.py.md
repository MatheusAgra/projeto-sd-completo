# limpar_gerados.py

Remove apenas comentários não legais de arquivos gerados, mantendo strings e avisos de Copyright/License Agreement. Antes de gravar exige igualdade dos tokens funcionais entre original e versão limpa. Exemplo: python scripts/limpar_gerados.py simulation/netlist/ula_de2_115.vo. A netlist foi compilada/simulada novamente depois da limpeza e o ZIP será recompilado com os símbolos limpos. Cabeçalhos legais preservados são a exceção documentada à ausência literal de comentários.
