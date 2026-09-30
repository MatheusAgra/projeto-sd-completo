# layout_bdf.py

Separa posicionamento/roteamento do emissor BDF. Valida todos os nomes originais
e células únicas dos layouts versão 1. Expande BUF em dois NOT como no baseline.
Calcula cada terminal a partir do símbolo realmente embutido, inclusive GND/VCC
com portas verticais. Entradas ficam à esquerda e saídas à direita.

Reserva corredores por coluna e faixas horizontais por rede. Fan-out é uma
árvore física, com conectores e junções. Vetores usam barramentos e condutores
por bit nos taps e slices, conservando índices externos. Não há associação
remota por nomes como substituto de um trajeto. Veja `config/LAYOUTS.md`.

A auditoria independente lê os BDF finais, sem importar este roteador. Detectou
um prolongamento de tronco que criava curto; a correção termina o tronco no
último acesso da própria rede. A geometria é determinística e não depende do
BSF exportado posteriormente pelo Quartus. Legibilidade e interpretação nativa
de cruzamentos/taps permanecem sujeitas às etapas futuras documentadas.
