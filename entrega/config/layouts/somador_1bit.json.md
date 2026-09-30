# Layout de `somador_1bit`

As cinco instâncias do grafo estão mapeadas uma única vez. A cadeia XOR da soma ocupa a faixa superior; AND/OR de carry ocupa a inferior, com o estágio final à direita.

O roteador deve ligar A e B aos XOR e AND correspondentes, `fa_P` ao XOR seguinte e ao AND de carry, e `Cin` ao XOR e ao AND. `fa_G` e `fa_H` convergem ao OR que produz `Cout`. Esses fan-outs precisam ser ramificações físicas contínuas, preservando os nomes das redes.

Os pinos externos A, B e Cin entram pela esquerda; S e Cout saem pela direita conforme as portas e coordenadas dos símbolos. Todas as saídas intermediárias são consumidas. O JSON define apenas células relativas; passo, coordenadas de pinos e rotas dependem do emissor e da geometria final dos símbolos.

Este documento registra intenção de posicionamento, não análise Quartus, continuidade geométrica validada ou aprovação visual.
