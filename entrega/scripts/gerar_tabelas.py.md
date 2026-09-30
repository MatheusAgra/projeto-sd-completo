# gerar_tabelas.py

## Objetivo

Gera tabelas verdade CSV, mapas de Karnaugh SVG e reduções Booleanas documentadas dos módulos binário→BCD e BCD→sete segmentos, além da tabela de cobertura do display de dois dígitos.

## Entradas e saídas

Não recebe argumentos. Escreve arquivos e respectivos documentos em `entrega/docs/tabelas`.

## Funcionamento

A tabela binário→BCD usa divisão inteira independente para registrar 0..31; a tabela BCD→7 segmentos usa padrões literais ativos em zero e fixa 10..15 como apagados. A redução das sete funções usa Quine–McCluskey sem don't-cares. Os mapas usam ordem Gray 00, 01, 11, 10; as funções de limiar apresentam duas camadas para MAG[4].

## Exemplo

Executado a partir da raiz do projeto: `python entrega/scripts/gerar_tabelas.py` recria os CSV, SVG e Markdown acompanhados de `.ext.md`.

## Verificação

A execução do gerador produz os artefatos listados. Isso não executa os testbenches nem valida o HDL convertido pelo Quartus.
