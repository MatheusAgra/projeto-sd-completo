# gerar_relatorio.py

## Objetivo

Monta `relatorio/RELATORIO.docx` com especificação, visão geral da arquitetura, interfaces, pinagem organizada por vetor, tabelas e reduções BCD, somador e conversores aritméticos, controle, mapa de Karnaugh, circuitos e waveforms de cada módulo, waveform integrada e resultados registrados em `docs/VALIDACAO.md`.

## Entradas e saídas

Usa `config/interfaces.json`, `config/pinagem_de2_115.csv`, `docs/OPERACAO_010_ALTERNATIVAS.md`, documentos BDF/BSF em `modulos`, tabelas, mapas e reduções em `docs/tabelas`, `docs/VALIDACAO.md`, `docs/diagramas/visao_geral.svg`, imagens PNG ou SVG dos 16 circuitos em `docs/diagramas` e imagens PNG de waveforms em `simulation/waveforms`. Exige `ula_integracao.png` para o sistema. Diagramas altos são recortados em painéis de largura de página, com legendas numeradas, sem remover partes do circuito. Os pinos SW, LEDR, LEDG e HEX são listados por grupo, bit, uso, pino físico e padrão de I/O. Escreve um único DOCX no caminho de saída configurado.

## Funcionamento

A execução interrompe antes de salvar o relatório se faltar qualquer resultado de validação, documento de módulo, tabela ou imagem esperada. As imagens SVG dos mapas são rasterizadas com Sharp pelo Node do runtime bundled. A capa deixa campos em branco para os integrantes, professor e disciplina; esses dados não são inferidos. O conteúdo de validação é incorporado a partir do arquivo da entrega, para não declarar compilação ou simulação sem evidência registrada.

## Exemplo

A partir da raiz do projeto, usando o Python bundled: `python entrega/scripts/gerar_relatorio.py`. Os diretórios de circuitos, waveforms, validação e saída podem ser substituídos pelos argumentos documentados por `--help`.

## Verificação

O script foi preparado para usar `python-docx`, Pillow e o Node bundled com Sharp. `py_compile` e `--help` passaram no Python bundled. O DOCX foi gerado e validado em OOXML: pacote ZIP íntegro, referências de imagem resolvidas, 74 inserções de imagem, 40 tabelas, 96 atribuições de pinos e campos de identificação em branco. A inspeção visual pelo `render_docx.py` da skill `documents` permanece pendente: no runtime Windows, `soffice.exe` não está no PATH e a alternativa permitida aguarda decisão. Nenhuma aprovação visual é declarada.


