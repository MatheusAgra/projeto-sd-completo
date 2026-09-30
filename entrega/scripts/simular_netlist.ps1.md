> Fluxo atual: logs/HDL anteriores são históricos. A simulação modular exige docs/preparacao_atual.json com hashes atuais e exportação PASS. A netlist exige compilação atual registrada por validar_nativo.py. Use `python entrega/scripts/validar_nativo.py --quartus caminho/quartus --icarus-root caminho/iverilog` após instalar as ferramentas. Não foram executadas novas simulações nesta etapa.

# simular_netlist.ps1

Gera .vo funcional pelo EDA Netlist Writer apÃƒÂ³s a compilaÃƒÂ§ÃƒÂ£o dos BDF e simula no Icarus com cycloneive_atoms.v da instalaÃƒÂ§ÃƒÂ£o Quartus. Usa o testbench independente do topo em pasta isolada para preservar seu VCD modular. Aceita -IcarusRoot e -Quartus. Exemplo: scripts/simular_netlist.ps1. Passou nas 16384 verificaÃƒÂ§ÃƒÂµes (8192 entradas ÃƒÂºnicas), apÃƒÂ³s limpeza da netlist. O comando legado quartus_map --generate_functional_sim_netlist nÃƒÂ£o ÃƒÂ© usado porque falhou com erro 281041 para Cyclone IV E. NÃƒÂ£o aplica SDF e nÃƒÂ£o valida orÃƒÂ§amento fÃƒÂ­sico.
