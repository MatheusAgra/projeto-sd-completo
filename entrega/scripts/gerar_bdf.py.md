# gerar_bdf.py

Emite BDF elétrico e BSF canônico do grafo congelado, contrato de interfaces e config/layouts/<módulo>.json. Posições e conectores são calculados por layout_bdf.py. Não conecta destinos remotos só por nome: troncos, ramificações, barramentos e taps possuem contato geométrico.

Exemplo: `python entrega/scripts/gerar_bdf.py entrega/config/grafos/somador_1bit.json --interfaces entrega/config/interfaces.json --output tmp/piloto`.

--layouts seleciona metadados; --quartus fornece biblioteca alternativa somente se a primitiva não estiver no cache versionado. As 13 primitivas usadas estão preservadas textualmente em config/primitivas, com desenho, portas e avisos legais do baseline. Funciona sem Quartus.

Hierarquia usa exatamente o mesmo block_symbol para o BSF entregue e os símbolos embutidos nos BDF. O BSF nativo posterior é conferência de contrato e não substitui essa geometria. BUF continua dois NOT com os nomes e rede intermediária preservados. Símbolos canônicos mantêm o aviso legal Intel de config/simbolos_legal.txt.

Geração individual não valida o resultado. preparar.py audita os BDF antes de exportar; validar_refatoracao.py também compara regeneração byte a byte e invariantes. Quartus, testes do HDL exportado, compilação e netlist continuam obrigatórios. Conferência visual permanece pendente.
