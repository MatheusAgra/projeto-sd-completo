# test_validar_geometria.py

Testes independentes do validador geométrico. Os BDF são fixtures temporários, não serializações obtidas do gerador de layout.

Os casos exercitam fan-out real em `SW[9]`, taps dos bits externos `SW[9..5]`, entrada vetorial de cinco bits por taps escalares, montagem de uma saída vetorial por taps escalares, e mutações de gap unitário, labels remotos repetidos e incompatíveis na mesma rede, bit/faixa/ordem errados, barramento sem marca de bus, junction removida, curto entre fios e barramentos, overlap colinear, contato bus-scalar sem junction, pinos de porta primitiva deslocados, símbolos hierárquicos com faixa/direção incorretas e fios/labels sobre símbolos ou trajetos.

Executar com `python -m unittest discover -s entrega/scripts -p 'test_validar_geometria.py' -v`. Esses testes validam o modelo geométrico Python. A confirmação das regras elétricas de bus/tap/cruzamento continua dependente da análise nativa do Quartus.
