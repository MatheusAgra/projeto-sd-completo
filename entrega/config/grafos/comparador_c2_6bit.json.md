# comparador_c2_6bit.json

Grafo estrutural de 32 instâncias para `comparador_c2_6bit`: seis XNOR, oito NOT, AND2/3/4/6 e OR2/3. Os cinco bits inferiores são comparados lexicograficamente por prefixos de XNOR. Para sinais iguais, a ordem unsigned desses bits é válida também quando ambos são negativos em complemento de dois. Com sinais diferentes, A negativo implica `LT`; `GT` deriva de `NOT(EQ OR LT)`.

Exemplo: A=`100000` e B=`100001` ativa `LT` e não ativa `EQ` nem `GT`.

Verificação: Quartus analisou e converteu o BDF gerado a partir deste grafo sem erros ou avisos. A bateria independente de 4096 pares no Icarus passou. Esta é a revisão final corrigida; o cone unsigned-GT foi removido.
