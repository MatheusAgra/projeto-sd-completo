param(
    [string]$IcarusRoot,
    [string]$TarPath
)
$ErrorActionPreference = 'Stop'
$entregaRoot = Split-Path -Parent $PSScriptRoot
$projectRoot = Split-Path -Parent $entregaRoot
if (-not $IcarusRoot) { $IcarusRoot = Join-Path $projectRoot 'tmp\tools\iverilog' }
if (-not $TarPath) {
    $tarCommand = Get-Command tar.exe -ErrorAction SilentlyContinue
    if (-not $tarCommand) { throw 'tar.exe não encontrado; indique -TarPath para bsdtar com suporte a zstd.' }
    $TarPath = $tarCommand.Source
}
if (-not (Test-Path -LiteralPath $TarPath -PathType Leaf)) { throw "Extrator não encontrado: $TarPath" }
$packagesRoot = Join-Path $IcarusRoot 'packages'
New-Item -ItemType Directory -Force -Path $packagesRoot,$IcarusRoot | Out-Null
$packages = @(
    @{ Name='mingw-w64-ucrt-x86_64-iverilog-1~13.0-2-any.pkg.tar.zst'; Hash='fd4d7d7cb60cda1eb437f5476673503d92964cf47ce6c11b460eb3bd05c43582' },
    @{ Name='mingw-w64-ucrt-x86_64-bzip2-1.0.8-4-any.pkg.tar.zst'; Hash='f03a2174034ddd2d96cecd34f617c5f8e2ef86c812b8d2bb3b8875257f2c8bfa' },
    @{ Name='mingw-w64-ucrt-x86_64-readline-8.3.003-1-any.pkg.tar.zst'; Hash='de2423c2e10fcd88272a0ab2f833f6a082cfe613d4c17c2f548cc50a5d2190c4' },
    @{ Name='mingw-w64-ucrt-x86_64-termcap-1.3.1-7-any.pkg.tar.zst'; Hash='17b78eb63e89458a6ae4d56aa1dc357e1decb2f845b29fded79bccdd628d9d41' },
    @{ Name='mingw-w64-ucrt-x86_64-zlib-1.3.2-2-any.pkg.tar.zst'; Hash='841401182976d2f9e17e5c0ebaac51f2a8014140ea53d67625e91c8fb3c85ea0' },
    @{ Name='mingw-w64-ucrt-x86_64-libatomic-16.2.0-4-any.pkg.tar.zst'; Hash='81d960422f47c9cff742aa5a6dd6c587ba39e5da64738d903730e79577479582' },
    @{ Name='mingw-w64-ucrt-x86_64-libgcc-16.2.0-4-any.pkg.tar.zst'; Hash='de65b4adae899d9278427402e29d03860bacba481794460f3a1d078610cbb783' },
    @{ Name='mingw-w64-ucrt-x86_64-libquadmath-16.2.0-4-any.pkg.tar.zst'; Hash='75960aa837a7fc6dc8313afb11014bf7f42548ab6067498d0b561cc3c490b5b2' },
    @{ Name='mingw-w64-ucrt-x86_64-libstdc++-16.2.0-4-any.pkg.tar.zst'; Hash='2211dbbf1220287e49f5d66bb6cb09ee5a157901a485197553c9a940cc902d5b' },
    @{ Name='mingw-w64-ucrt-x86_64-libwinpthread-14.0.0.r426.g4564ee4b5-1-any.pkg.tar.zst'; Hash='f8de8153bbc0e47ba244a423c12c426fa1d9f56395117ecaa34c6ad6ebed6ca3' }
)
foreach ($package in $packages) {
    $archive = Join-Path $packagesRoot $package.Name
    $actualHash = if (Test-Path -LiteralPath $archive -PathType Leaf) { (Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() } else { '' }
    if ($actualHash -ne $package.Hash) {
        if (Test-Path -LiteralPath $archive -PathType Leaf) { Remove-Item -LiteralPath $archive -Force }
        $encodedName = [uri]::EscapeDataString($package.Name).Replace('%2D','-').Replace('%2E','.').Replace('%7E','~')
        $url = 'https://repo.msys2.org/mingw/ucrt64/' + $encodedName
        & curl.exe -L --fail --silent --show-error -o $archive $url
        if ($LASTEXITCODE -ne 0) { throw "Download falhou: $($package.Name)" }
        $actualHash = (Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    if ($actualHash -ne $package.Hash) { throw "SHA-256 divergente: $($package.Name)" }
    $null = & $TarPath -tf $archive 2>&1
    if ($LASTEXITCODE -ne 0) { throw "O extrator não conseguiu ler zstd: $TarPath" }
    & $TarPath -xf $archive -C $IcarusRoot
    if ($LASTEXITCODE -ne 0) { throw "Extração falhou: $($package.Name)" }
    Write-Output "Verificado e extraído: $($package.Name)"
}
$binRoot = Join-Path $IcarusRoot 'ucrt64\bin'
$ivlRoot = Join-Path $IcarusRoot 'ucrt64\lib\ivl'
$iverilog = Join-Path $binRoot 'iverilog.exe'
$vvp = Join-Path $binRoot 'vvp.exe'
if (-not (Test-Path -LiteralPath $iverilog) -or -not (Test-Path -LiteralPath $vvp) -or -not (Test-Path -LiteralPath $ivlRoot -PathType Container)) { throw 'A extração não produziu a árvore Icarus esperada.' }
$env:PATH = $binRoot + ';' + $env:PATH
$env:IVL_ROOT = $ivlRoot
$versionOutput = & $iverilog -V 2>&1
$versionExit = $LASTEXITCODE
$versionOutput | Select-Object -First 1
if ($versionExit -ne 0) { throw "iverilog -V falhou (exit $versionExit)" }

