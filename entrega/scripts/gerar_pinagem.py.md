# gerar_pinagem.py

Extrai os pinos das páginas 36..39 do manual DE2-115 usando pypdf, cobrindo os 96 sinais declarados. Rejeita ausência ou duplicação de sinal/pino. JP6 e pinos fixos 3,3 V usam 3.3-V LVTTL; JP7 e pinos fixos 2,5 V usam 2.5 V. Exemplo: python scripts/gerar_pinagem.py caminho/DE2_115_User_manual.pdf. O CSV foi conferido com as imagens do enunciado e com as atribuições reais do Fitter. O manual externo é necessário só para regenerar o CSV, não para compilar o projeto.
