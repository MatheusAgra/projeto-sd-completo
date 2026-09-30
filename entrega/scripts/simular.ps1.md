> Fluxo atual: logs/HDL anteriores são históricos. A simulação modular exige docs/preparacao_atual.json com hashes atuais e exportação PASS. A netlist exige compilação atual registrada por validar_nativo.py. Use `python entrega/scripts/validar_nativo.py --quartus caminho/quartus --icarus-root caminho/iverilog` após instalar as ferramentas. Não foram executadas novas simulações nesta etapa.

# simular.ps1

AutomaÃ§Ã£o PowerShell dos dezesseis testbenches. Para cada mÃ³dulo, compila todos os dezesseis arquivos `simulation/generated/*.v` com o testbench correspondente, executa o resultado no Icarus e grava `compile_<modulo>.log` e `sim_<modulo>.log` em `docs/logs`. Os testbenches gravam VCDs reais em `simulation/waveforms`.

Por padrÃ£o, procura Icarus em `tmp/tools/iverilog`. Em uma cÃ³pia extraÃ­da em outra pasta, `-IcarusRoot` aponta para a raiz que contÃ©m `ucrt64/bin` e `ucrt64/lib/ivl`. Para Questa, `-QuestaPath` recebe a pasta com `vsim.exe` ou o caminho do executÃ¡vel e delega a `simulation/run.do`; use sÃ³ um dos parÃ¢metros.

Exemplo: `powershell -ExecutionPolicy Bypass -File entrega/scripts/simular.ps1 -IcarusRoot D:/tools/iverilog`.

VerificaÃ§Ã£o: as dezesseis baterias executaram contra as exportaÃ§Ãµes finais do Quartus e passaram no Icarus. Os logs e waveforms registram a execuÃ§Ã£o observada. ModelSim/Questa nÃ£o foi executado com checkout de licenÃ§a bem-sucedido.

