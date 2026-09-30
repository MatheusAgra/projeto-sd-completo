## Representação atual

Refatorado com config/layouts, troncos/ramificações físicos e símbolos canônicos coerentes entre BDF e BSF. O auditor geométrico lê o BDF final e compara portas e bits com o grafo/contrato; resultados atuais em docs/REFATORACAO_VISUAL_TECNICA.md e docs/refatoracao_tecnica.json. Regeneração determinística conferida. Análise/exportação Quartus, testes HDL novos e conferência visual pendentes. As verificações nativas descritas abaixo pertencem à revisão anterior.

> Estado da refatoração em 30/09/2026: este registro descreve a revisão ANTERIOR. Os BDF/BSF novos exigem novas exportações e testes. Veja docs/REFATORACAO_VISUAL_TECNICA.md; Quartus/Icarus e conferência visual permanecem pendentes.

# bin_bcd.bsf

## Objetivo

Símbolo gráfico da entidade `bin_bcd`, com as portas definidas no contrato congelado.

## Entradas e saídas

`MAG[4:0]` é entrada de cinco bits; `DEZ[3:0]` e `UNI[3:0]` são saídas de quatro bits cada.

## Funcionamento

O BSF representa a interface de `bin_bcd` e não contém a lógica de conversão. A implementação é o grafo do arquivo `bin_bcd.bdf`; `somador_subtrator_5bit` é sua dependência hierárquica.

## Exemplo

Uma instância conectada com `MAG=23` deve apresentar `DEZ=2` e `UNI=3`.

## Verificação

O Quartus gerou o símbolo a partir do HDL convertido do BDF. O teste de interface confirmou que nomes, direções e larguras coincidem com `interfaces.json`; a lógica funcional foi testada no HDL convertido pelo BDF, não no BSF, que é apenas interface gráfica.
