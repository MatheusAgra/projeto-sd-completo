# relatar_caminhos.tcl

Abre o projeto compilado e usa o TimeQuest nativo para relatar os vinte caminhos combinacionais de entrada a saída de maior atraso no modelo de timing carregado. Execute `quartus_sta -t scripts/relatar_caminhos.tcl` na pasta da entrega após compilar. Não cria clock nem restrição temporal; o relatório é uma estimativa do modelo do dispositivo, sem requisito de aprovação ou medição física. A execução e o corner efetivamente utilizado constam em `docs/logs/caminhos_sta.log` e `output_files/caminhos_entrada_saida.rpt`.
