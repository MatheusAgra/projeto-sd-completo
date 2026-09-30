# obter_icarus.ps1

Obtém o Icarus Verilog 13.0 e as dependências runtime a partir dos pacotes MSYS2 UCRT64 registrados na página `docs/FERRAMENTAS_SIMULACAO.md`. O script confere SHA-256 antes de extrair arquivos `.pkg.tar.zst` para a pasta temporária `tmp/tools/iverilog`; não altera o PATH global e não coloca binários no ZIP da entrega.

Exemplo na raiz do projeto: `powershell -ExecutionPolicy Bypass -File entrega/scripts/obter_icarus.ps1`. Para outro destino, use `-IcarusRoot D:/tools/iverilog`. O extrator pode ser indicado em `-TarPath`; requer `tar`/`bsdtar` que leia zstd, como o `tar.exe` disponível neste computador.

Após extração, execute `powershell -ExecutionPolicy Bypass -File entrega/scripts/simular.ps1 -IcarusRoot D:/tools/iverilog`. A ferramenta Icarus e os runtime libraries devem permanecer disponíveis nessa pasta durante a simulação.

Verificação: os dez pacotes listados tiveram seus hashes comparados com o catálogo oficial MSYS2 quando obtidos. A instalação desta máquina compilou e executou um probe e, na sequência, as dezesseis baterias sobre o HDL exportado do Quartus passaram. Questa continua preparada via `run.do`, mas sua licença não produziu uma execução válida.
