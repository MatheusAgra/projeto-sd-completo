# mux_resultado_8x6.json

Grafo de 54 instâncias: oito AND2 por bit da saída e seis OR8, ligando oito candidatos de seis bits ao vetor F sob seleção one-hot.

Exemplo: D3 sozinho selecionado encaminha C3 a F.

Verificação: análise e conversão BDF→Verilog passaram no Quartus sem erros nem avisos. Os caminhos dos oito candidatos passaram 512/512 verificações independentes no Icarus.
