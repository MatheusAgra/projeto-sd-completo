# tabelas_controle.py

Gera dois arquivos Markdown em `entrega/docs/tabelas`: `mapa_logica_5bit.md`, com tabela de verdade e mapas de Karnaugh de duas variáveis para AND/XOR e o alinhamento de cinco para seis bits; e `tabela_decodificador_operacao.md`, com as oito combinações do seletor, o vetor D one-hot e a habilitação de exibição, além dos mintermos.

Exemplo: execute `python entrega/scripts/tabelas_controle.py` na raiz. Para direcionar a saída, use `python entrega/scripts/tabelas_controle.py --output <pasta>`. O programa gera somente documentação, sem editar o contrato ou os grafos.

Verificação: a execução foi feita e produziu os dois arquivos. A tabela de controle cobre oito seletores; as tabelas por bit de lógica enumeram as quatro combinações de A e B.
