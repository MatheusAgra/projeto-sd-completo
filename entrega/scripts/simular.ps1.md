# simular.ps1

Automação PowerShell dos dezesseis testbenches. Para cada módulo, compila todos os dezesseis arquivos `simulation/generated/*.v` com o testbench correspondente, executa o resultado no Icarus e grava `compile_<modulo>.log` e `sim_<modulo>.log` em `docs/logs`. Os testbenches gravam VCDs reais em `simulation/waveforms`.

Por padrão, procura Icarus em `tmp/tools/iverilog`. Em uma cópia extraída em outra pasta, `-IcarusRoot` aponta para a raiz que contém `ucrt64/bin` e `ucrt64/lib/ivl`. Para Questa, `-QuestaPath` recebe a pasta com `vsim.exe` ou o caminho do executável e delega a `simulation/run.do`; use só um dos parâmetros.

Exemplo: `powershell -ExecutionPolicy Bypass -File entrega/scripts/simular.ps1 -IcarusRoot D:/tools/iverilog`.

Verificação: as dezesseis baterias executaram contra as exportações finais do Quartus e passaram no Icarus. Os logs e waveforms registram a execução observada. ModelSim/Questa não foi executado com checkout de licença bem-sucedido.

