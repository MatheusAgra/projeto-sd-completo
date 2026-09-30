# display_decimal_2digitos.bsf

## Objetivo

Símbolo da entidade que combina conversão BCD, decodificação e máscara de habilitação.

## Entradas e saídas

`MAG[4:0]` e `ENABLE` são entradas; `DEZ_SEG[6:0]` e `UNI_SEG[6:0]` são saídas ativas em zero.

## Funcionamento

O BSF descreve apenas a interface visível do bloco. A hierarquia funcional e as portas de apagamento estão no BDF `display_decimal_2digitos`.

## Exemplo

Com `MAG=27`, ENABLE=1 apresenta dezena 2 e unidade 7; ENABLE=0 apaga ambos os displays.

## Verificação

O Quartus gerou o símbolo a partir do HDL convertido do BDF. Nomes, direções e larguras foram comparados com `interfaces.json`. A simulação funcional executada cobre o HDL convertido do BDF; o BSF representa somente a interface gráfica.
