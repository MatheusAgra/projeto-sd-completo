param(
    [string]$IcarusRoot,
    [string]$Quartus = 'C:/intelFPGA_lite/21.1/quartus'
)
$ErrorActionPreference = 'Stop'
$DeliveryRoot = Split-Path -Parent $PSScriptRoot
$WorkspaceRoot = Split-Path -Parent $DeliveryRoot
$CurrentPath = Join-Path $DeliveryRoot 'docs/validacao_nativa_atual.json'
if (-not (Test-Path -LiteralPath $CurrentPath)) { throw 'Compilação atual não registrada; execute scripts/validar_nativo.py.' }
$Current = Get-Content -LiteralPath $CurrentPath -Raw | ConvertFrom-Json
if ($Current.stages.compilation.status -ne 'PASS') { throw 'Compilação dos BDF refatorados ainda pendente; a netlist histórica não valida esta revisão.' }
foreach ($Property in $Current.sources.PSObject.Properties) {
    $SourcePath = Join-Path $DeliveryRoot $Property.Name
    if ((Get-FileHash -LiteralPath $SourcePath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Property.Value) { throw ('Fonte alterada após compilação: ' + $Property.Name) }
}
if (-not $IcarusRoot) { $IcarusRoot = Join-Path $WorkspaceRoot 'tmp/tools/iverilog' }
$BinRoot = if (Test-Path -LiteralPath (Join-Path $IcarusRoot 'ucrt64/bin/iverilog.exe')) { Join-Path $IcarusRoot 'ucrt64/bin' } else { $IcarusRoot }
$env:PATH = $BinRoot + ';' + $env:PATH
$env:IVL_ROOT = if (Test-Path -LiteralPath (Join-Path $IcarusRoot 'ucrt64/lib/ivl')) { Join-Path $IcarusRoot 'ucrt64/lib/ivl' } else { Join-Path (Split-Path -Parent $BinRoot) 'lib/ivl' }
$LogsRoot = Join-Path $DeliveryRoot 'docs/logs'
$NetlistRoot = Join-Path $DeliveryRoot 'simulation/netlist'
$RunRoot = Join-Path $WorkspaceRoot 'tmp/netlist_run'
New-Item -ItemType Directory -Force -Path $NetlistRoot,$RunRoot,(Join-Path $RunRoot 'waveforms') | Out-Null
Push-Location $DeliveryRoot
try {
    & (Join-Path $Quartus 'bin64/quartus_eda.exe') ULA_DE2_115 --simulation --tool=questa_oem --format=verilog --functional *> (Join-Path $LogsRoot 'netlist_eda.log')
    if ($LASTEXITCODE -ne 0) { throw 'Falha no EDA Netlist Writer' }
    Copy-Item -LiteralPath (Join-Path $DeliveryRoot 'simulation/modelsim/ULA_DE2_115.vo') -Destination (Join-Path $NetlistRoot 'ula_de2_115.vo')
    & python (Join-Path $PSScriptRoot 'limpar_gerados.py') (Join-Path $NetlistRoot 'ula_de2_115.vo') *> (Join-Path $LogsRoot 'netlist_cleanup.log')
    if ($LASTEXITCODE -ne 0) { throw 'Falha na verificacao de tokens da netlist' }
} finally {
    Pop-Location
}
Push-Location $RunRoot
try {
    & (Join-Path $BinRoot 'iverilog.exe') -g2012 -s tb_ula_de2_115 -o netlist.vvp (Join-Path $Quartus 'eda/sim_lib/cycloneive_atoms.v') (Join-Path $NetlistRoot 'ula_de2_115.vo') (Join-Path $DeliveryRoot 'simulation/tb_ula_de2_115.sv') *> (Join-Path $LogsRoot 'netlist_compile.log')
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao compilar modelo Cyclone IV e netlist' }
    & (Join-Path $BinRoot 'vvp.exe') netlist.vvp *> (Join-Path $LogsRoot 'netlist_sim.log')
    if ($LASTEXITCODE -ne 0) { throw 'Falha na simulacao da netlist nativa' }
    Copy-Item -LiteralPath (Join-Path $RunRoot 'waveforms/ula_de2_115.vcd') -Destination (Join-Path $DeliveryRoot 'simulation/waveforms/ula_de2_115_netlist.vcd')
} finally {
    Pop-Location
}
