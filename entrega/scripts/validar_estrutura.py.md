# validar_estrutura.py

Confere os 16 grafos: entidade e fonte presentes, nomes de instância únicos, aridade/direção/largura de portas, drivers únicos em cada rede consumida e ausência de ciclos combinacionais e hierárquicos. Expande bus ou bit para redes individuais; BUF é conexão lógica que o emissor materializa em dois NOT. Exemplo: python scripts/validar_estrutura.py. Passou nos 16 módulos e 342 instâncias; não substitui análise Quartus nem simulação do BDF exportado.
