# gerar_pinagem.py

Extrai os pinos das pÃ¡ginas 36..39 do manual DE2-115 usando pypdf, cobrindo os 96 sinais declarados. Rejeita ausÃªncia ou duplicaÃ§Ã£o de sinal/pino. JP6 e pinos fixos 3,3 V usam 3.3-V LVTTL; JP7 e pinos fixos 2,5 V usam 2.5 V. Exemplo: python scripts/gerar_pinagem.py caminho/DE2_115_User_manual.pdf. O CSV foi conferido com as imagens do enunciado e com as atribuiÃ§Ãµes reais do Fitter. O manual externo Ã© necessÃ¡rio sÃ³ para regenerar o CSV, nÃ£o para compilar o projeto.
