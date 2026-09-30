param(
    [string]$IcarusRoot,
    [string]$QuestaPath
)
$ErrorActionPreference = 'Stop'
if ($IcarusRoot -and $QuestaPath) { throw 'Informe IcarusRoot ou QuestaPath, não ambos.' }
$entregaRoot = Split-Path -Parent $PSScriptRoot
$projectRoot = Split-Path -Parent $entregaRoot
$simulationRoot = Join-Path $entregaRoot 'simulation'
$generatedRoot = Join-Path $simulationRoot 'generated'
$logsRoot = Join-Path $entregaRoot 'docs\logs'
$modules = @('somador_1bit', 'sm_para_c2', 'somador_subtrator_6bit', 'c2_para_sm', 'negador_c2_6bit', 'modulo2_soma_sub', 'comparador_c2_6bit', 'logica_5bit', 'decodificador_operacao', 'mux_resultado_8x6', 'ula_core', 'somador_subtrator_5bit', 'bin_bcd', 'bcd_7seg', 'display_decimal_2digitos', 'ula_de2_115')
New-Item -ItemType Directory -Force -Path $logsRoot,(Join-Path $simulationRoot 'waveforms') | Out-Null
if ($QuestaPath) {
    $candidates = @()
    if ((Test-Path -LiteralPath $QuestaPath -PathType Leaf) -and ([IO.Path]::GetExtension($QuestaPath) -ieq '.exe')) { $candidates += $QuestaPath }
    $candidates += (Join-Path $QuestaPath 'vsim.exe'),(Join-Path $QuestaPath 'bin\vsim.exe'),(Join-Path $QuestaPath 'win64\vsim.exe')
    $vsim = $candidates | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1
    if (-not $vsim) { throw "vsim.exe não encontrado em QuestaPath: $QuestaPath" }
    Push-Location $simulationRoot
    try {
        $output = & $vsim -c -do 'do run.do' 2>&1
        $exitCode = $LASTEXITCODE
        $output | Set-Content -LiteralPath (Join-Path $logsRoot 'sim_questa_launch.log') -Encoding utf8
        $output | ForEach-Object { Write-Output $_ }
        if ($exitCode -ne 0) { throw "Questa terminou com código $exitCode; consulte docs/logs/sim_questa_launch.log" }
    }
    finally {
        Pop-Location
    }
    exit 0
}
if (-not $IcarusRoot) { $IcarusRoot = Join-Path $projectRoot 'tmp\tools\iverilog' }
$binRoot = if (Test-Path -LiteralPath (Join-Path $IcarusRoot 'ucrt64\bin\iverilog.exe')) { Join-Path $IcarusRoot 'ucrt64\bin' } else { $IcarusRoot }
$ivlRoot = if (Test-Path -LiteralPath (Join-Path $IcarusRoot 'ucrt64\lib\ivl')) { Join-Path $IcarusRoot 'ucrt64\lib\ivl' } else { Join-Path (Split-Path -Parent $binRoot) 'lib\ivl' }
$iverilog = Join-Path $binRoot 'iverilog.exe'
$vvp = Join-Path $binRoot 'vvp.exe'
$buildRoot = Join-Path $IcarusRoot 'build'
if (-not (Test-Path -LiteralPath $iverilog) -or -not (Test-Path -LiteralPath $vvp)) { throw "Icarus não encontrado em $binRoot" }
if (-not (Test-Path -LiteralPath $generatedRoot -PathType Container)) { throw "Pasta de HDL exportado ausente: $generatedRoot" }
$generatedFiles = @($modules | ForEach-Object { Join-Path $generatedRoot ($_ + '.v') })
$testbenchFiles = @($modules | ForEach-Object { Join-Path $simulationRoot ('tb_' + $_ + '.sv') })
foreach ($file in $generatedFiles + $testbenchFiles) { if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw "Arquivo requerido ausente: $file" } }
New-Item -ItemType Directory -Force -Path $buildRoot | Out-Null
$env:PATH = $binRoot + ';' + $env:PATH
$env:IVL_ROOT = $ivlRoot
Push-Location $simulationRoot
try {
    for ($i = 0; $i -lt $modules.Count; $i++) {
        $module = $modules[$i]
        $compileLog = Join-Path $logsRoot ('compile_' + $module + '.log')
        $simulationLog = Join-Path $logsRoot ('sim_' + $module + '.log')
        $output = Join-Path $buildRoot ('tb_' + $module + '.vvp')
        $compileOutput = & $iverilog -g2012 -s ('tb_' + $module) -o $output $generatedFiles $testbenchFiles[$i] 2>&1
        $compileExit = $LASTEXITCODE
        $compileOutput | Set-Content -LiteralPath $compileLog -Encoding utf8
        $compileOutput | ForEach-Object { Write-Output $_ }
        if ($compileExit -ne 0) { throw "Icarus compilation failed for $module (exit $compileExit); see $compileLog" }
        $simulationOutput = & $vvp $output 2>&1
        $simulationExit = $LASTEXITCODE
        $simulationOutput | Set-Content -LiteralPath $simulationLog -Encoding utf8
        $simulationOutput | ForEach-Object { Write-Output $_ }
        if ($simulationExit -ne 0) { throw "Icarus simulation failed for $module (exit $simulationExit); see $simulationLog" }
    }
}
finally {
    Pop-Location
}
