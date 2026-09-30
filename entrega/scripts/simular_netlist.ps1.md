# simular_netlist.ps1

Gera .vo funcional pelo EDA Netlist Writer após a compilação dos BDF e simula no Icarus com cycloneive_atoms.v da instalação Quartus. Usa o testbench independente do topo em pasta isolada para preservar seu VCD modular. Aceita -IcarusRoot e -Quartus. Exemplo: scripts/simular_netlist.ps1. Passou nas 16384 verificações (8192 entradas únicas), após limpeza da netlist. O comando legado quartus_map --generate_functional_sim_netlist não é usado porque falhou com erro 281041 para Cyclone IV E. Não aplica SDF e não valida orçamento físico.
