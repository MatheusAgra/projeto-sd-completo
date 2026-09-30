# decodificador_operacao.json

Grafo de doze instâncias: três NOT, oito AND3 para os mintermos `D[7..0]` e um AND2 para `EXIBE_F`. Cada combinação do seletor afirma somente a linha D correspondente. A habilitação vale para S=000 e S=001.

Exemplo: S=`101` gera D5 ativo.

Verificação: análise e exportação nativas Quartus passaram sem erros nem avisos. O testbench independente passou os oito seletores no Icarus e gravou VCD real.
