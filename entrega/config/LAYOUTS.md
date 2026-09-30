# Contrato de layout BDF, versão 1

Os grafos, interfaces e pinagem são imutáveis nesta refatoração. Cada arquivo
`layouts/<entidade>.json` contém `version: 1`, `module`, `instances` e `notes`.
`instances` mapeia **todos os nomes originais do grafo** para `[coluna, faixa]`,
inteiros não negativos. Nenhum par pode se repetir. O emissor calcula o passo
físico a partir dos símbolos reais e reserva corredores de roteamento. BUF
ocupa duas posições adjacentes dentro da mesma célula, sem mudar sua função.
`notes` explica agrupamentos, redes difíceis e saídas sem consumidor.

O emissor é responsável pelas coordenadas finais, entradas à esquerda, saídas
à direita, geometria única de BSF/blocos embutidos, conectores ortogonais,
fan-out e taps. Metadados não podem alterar redes, portas ou larguras. Todos os
trajetos consumidos devem existir por contato geométrico. Cruzamentos
perpendiculares internos sem junção não unem redes; extremidades, junções e
sobreposições colineares são contatos. Cada derivação de vetor deve identificar
os índices externos reais, inclusive SW[9..5] e SW[12..10].

O coordenador edita scripts compartilhados, gera BDF/BSF e mantém evidências.
Agentes das três frentes editam somente seus JSON e documentos JSON.md.
Nenhum agente inspeciona imagens nem aprova legibilidade nesta etapa.

Geometria e semântica de cruzamentos/taps exigem confirmação nativa no Quartus;
uma auditoria Python não substitui essa etapa quando a ferramenta está ausente.

## Roteamento determinístico

Cada coluna reserva canais verticais distintos para **cada terminal**, fora
dos corpos e dos textos de instância. Cada rede tem um tronco horizontal em
uma faixa reservada acima de seus primeiros terminais. As faixas têm passo
32 e os canais passo 24; dimensões de células são arredondadas à grade 8.
O tronco termina exatamente no último canal da própria rede: prolongá-lo até
um canal vizinho pode criar um curto por extremidade sobre segmento.

Uma expressão vetorial completa compartilha um tronco de barramento contínuo.
Bits escalares e fatias diferentes da mesma origem recebem taps físicos
identificados pelos índices externos. O bit é levado por um condutor escalar
entre os barramentos correspondentes, conservando SW[9..5] e SW[12..10].
Junções aparecem somente nos acessos de sua própria rede e nos taps
intencionais. Cruzamentos interiores de canais de redes distintas permanecem
sem junção ou extremidade naquele ponto. Este modelo é auditado geometricamente;
a confirmação da interpretação elétrica pelo Quartus continua obrigatória.

Não há fallback para trechos isolados por nome. A contrapartida da reserva de
canais é uma folha extensa e vários cruzamentos internos; o tamanho, os
trajetos longos e a legibilidade precisam ser examinados na revisão futura,
sem aprovação visual inferida do resultado automático.
