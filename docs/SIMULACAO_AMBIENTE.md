# Diagnóstico do ambiente de simulação

Data: 2026-09-30

## Questa Intel FPGA Lite 21.1

Executáveis encontrados em `C:\intelFPGA_lite\21.1\questa_fse\win64`, incluindo `vsim.exe`, `vlog.exe`, `vcom.exe` e `lmutil.exe`.

Foi feita uma execução real em modo batch, a partir de `tmp\simulacao_ambiente`:

```powershell
& 'C:\intelFPGA_lite\21.1\questa_fse\win64\vsim.exe' -c -do 'quit -f'
```

Resultado: o processo informou que não conseguiu obter uma licença, encerrou o simulador e retornou código `4` (`Invalid license`). Portanto, o binário está instalado, mas a execução do Questa está bloqueada por licença neste ambiente. A saída registrada foi limitada ao erro de checkout; nenhum conteúdo de arquivo ou variável de licença foi lido ou divulgado.

## Icarus Verilog e WSL

`iverilog` e `vvp` não estão no `PATH`. Também não foi encontrado `iverilog.exe` nos locais comuns verificados: `C:\iverilog`, `C:\tools`, `C:\msys64`, diretórios padrão de `Program Files`, diretório de bibliotecas do Chocolatey e diretório de apps do Scoop. A busca foi local; nenhuma instalação ou download foi feito.

`wsl.exe` está presente, mas `wsl --list --quiet` retornou `Wsl/EnumerateDistros/Service/E_ACCESSDENIED`. Não foi possível confirmar por CLI se há uma distribuição Linux configurada nem verificar simuladores dentro dela.

## Conclusão

No estado verificado, não há um simulador utilizável confirmado: o Questa falha no checkout da licença e o Icarus não foi localizado. A presença do `winget.exe` foi observada, mas nenhum pacote foi instalado. Para prosseguir sem alterar o ambiente, é necessário resolver a licença do Questa ou obter acesso a uma instalação existente de Icarus/WSL.
