param([string]$Quartus = 'C:/intelFPGA_lite/21.1/quartus/bin64')
$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $ProjectRoot
try {
    & (Join-Path $Quartus 'quartus_sh.exe') --flow compile ULA_DE2_115
    if ($LASTEXITCODE -ne 0) { throw "Quartus retornou $LASTEXITCODE" }
} finally {
    Pop-Location
}
