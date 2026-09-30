# run.do

Script Tcl do Questa que compila os dezesseis HDL convertidos do BDF e os dezesseis testbenches numa biblioteca temporária. Depois executa cada `tb_<modulo>`, gravando logs em `docs/logs` e VCDs em `simulation/waveforms`.

Execute `do run.do` a partir do Questa, ou chame `simular.ps1 -QuestaPath <pasta-ou-vsim.exe>`. Os caminhos de fontes e de logs são resolvidos a partir do script.

A análise e a compilação Quartus das fontes BDF finais passaram. As baterias funcionais foram executadas pelo Icarus e passaram. Questa permanece como alternativa preparada: a execução local anterior falhou ao obter licença e não há uma execução Questa aprovada registrada.
