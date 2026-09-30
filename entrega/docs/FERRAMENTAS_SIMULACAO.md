# Ferramentas de simulação

## Icarus Verilog portátil

A entrega usa o HDL exportado do BDF real somente para simulação. O Quartus Prime Lite 21.1 produziu o Verilog; a implementação sintetizada continua sendo formada pelos BDF. O pacote portátil do Icarus não faz parte do ZIP, que permanece sem os binários e bibliotecas da ferramenta. Depois de extrair o ZIP, o usuário pode obtê-lo localmente pelo script `scripts/obter_icarus.ps1`.

O pacote principal é Icarus Verilog 13.0 UCRT64, publicado no catálogo de pacotes MSYS2, com upstream indicado como `steveicarus/iverilog`. A documentação upstream orienta usuários Windows para os pacotes pré-compilados MSYS2. As dependências runtime também são baixadas como pacotes UCRT64 e extraídas no mesmo prefixo. A origem de cada pacote e seus hashes são verificáveis na página oficial do catálogo e abaixo.

| Pacote | SHA-256 |
|---|---|
| `mingw-w64-ucrt-x86_64-iverilog-1~13.0-2-any.pkg.tar.zst` | `fd4d7d7cb60cda1eb437f5476673503d92964cf47ce6c11b460eb3bd05c43582` |
| `mingw-w64-ucrt-x86_64-bzip2-1.0.8-4-any.pkg.tar.zst` | `f03a2174034ddd2d96cecd34f617c5f8e2ef86c812b8d2bb3b8875257f2c8bfa` |
| `mingw-w64-ucrt-x86_64-readline-8.3.003-1-any.pkg.tar.zst` | `de2423c2e10fcd88272a0ab2f833f6a082cfe613d4c17c2f548cc50a5d2190c4` |
| `mingw-w64-ucrt-x86_64-termcap-1.3.1-7-any.pkg.tar.zst` | `17b78eb63e89458a6ae4d56aa1dc357e1decb2f845b29fded79bccdd628d9d41` |
| `mingw-w64-ucrt-x86_64-zlib-1.3.2-2-any.pkg.tar.zst` | `841401182976d2f9e17e5c0ebaac51f2a8014140ea53d67625e91c8fb3c85ea0` |
| `mingw-w64-ucrt-x86_64-libatomic-16.2.0-4-any.pkg.tar.zst` | `81d960422f47c9cff742aa5a6dd6c587ba39e5da64738d903730e79577479582` |
| `mingw-w64-ucrt-x86_64-libgcc-16.2.0-4-any.pkg.tar.zst` | `de65b4adae899d9278427402e29d03860bacba481794460f3a1d078610cbb783` |
| `mingw-w64-ucrt-x86_64-libquadmath-16.2.0-4-any.pkg.tar.zst` | `75960aa837a7fc6dc8313afb11014bf7f42548ab6067498d0b561cc3c490b5b2` |
| `mingw-w64-ucrt-x86_64-libstdc++-16.2.0-4-any.pkg.tar.zst` | `2211dbbf1220287e49f5d66bb6cb09ee5a157901a485197553c9a940cc902d5b` |
| `mingw-w64-ucrt-x86_64-libwinpthread-14.0.0.r426.g4564ee4b5-1-any.pkg.tar.zst` | `f8de8153bbc0e47ba244a423c12c426fa1d9f56395117ecaa34c6ad6ebed6ca3` |

O runtime fica em `IcarusRoot/ucrt64/bin` (`iverilog.exe`, `vvp.exe`) e `IcarusRoot/ucrt64/lib/ivl`. No workspace de validação, o `IcarusRoot` usado foi `tmp/tools/iverilog`. `simular.ps1` aceita `-IcarusRoot <raiz>` para qualquer destino; o script define PATH e `IVL_ROOT` somente no processo em execução. Exemplo após extrair o ZIP e obter a ferramenta: `powershell -ExecutionPolicy Bypass -File entrega/scripts/simular.ps1 -IcarusRoot D:/tools/iverilog`.

A extração requer `tar.exe`/`bsdtar` com suporte a zstd. O script aceita `-TarPath` se o extrator não estiver no PATH. Os pacotes baixados ficam fora de `entrega`, em `IcarusRoot/packages`, para que uma compactação somente da pasta da entrega não carregue executáveis da ferramenta.

Fontes oficiais consultadas em 30/09/2026: [catálogo MSYS2 do Icarus](https://packages.msys2.org/packages/mingw-w64-ucrt-x86_64-iverilog), [documentação upstream de instalação](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/installation.rst), [gerência de pacotes MSYS2](https://www.msys2.org/docs/package-management/) e [repositório principal de pacotes](https://repo.msys2.org/mingw/ucrt64/).

## Questa / ModelSim

`simulation/run.do` permanece disponível para compilar os dezesseis Verilog exportados e executar os testbenches no Questa. O `vsim` instalado em `C:/intelFPGA_lite/21.1/questa_fse/win64` falhou no checkout da licença, retornando código 4. Não há alegação de execução Questa aprovada. Use `simular.ps1 -QuestaPath <pasta-ou-vsim.exe>` somente quando uma licença utilizável estiver disponível.

## Resultados registrados

As dezesseis baterias executaram no Icarus sobre HDL convertido pelo Quartus a partir dos BDF finais e passaram. Os logs ficam em `docs/logs/sim_<modulo>.log`, e os VCDs gerados pelas próprias simulações em `simulation/waveforms`. Entre as baterias desta frente: comparador, 4096 pares; lógica, 1024 pares; decodificador, oito seletores; mux, 512 estímulos.
