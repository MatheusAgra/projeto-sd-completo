> Evidência histórica anterior à refatoração dos BDF: não foi reexportada, ressimulada nem regenerada para esta geometria. Consulte docs/REFATORACAO_VISUAL_TECNICA.md.

# ula_de2_115.vo

Netlist funcional de tecnologia Cyclone IV E gerada pelo EDA Netlist Writer do Quartus 21.1 após a compilação dos BDF finais. É uma representação adicional da implementação mapeada e não é cadastrada no QSF. Interface: SW13, LEDR18, LEDG9 e oito HEX7, conforme o topo.

Foi simulada no Icarus 13.0 com a biblioteca nativa `quartus/eda/sim_lib/cycloneive_atoms.v`, usando o mesmo testbench independente do topo. Passou em 16384 verificações e 8192 entradas únicas. O VCD adicional é `ula_de2_115_netlist.vcd`; não substitui a simulação modular dos BDF exportados.

O fluxo legado `quartus_map --generate_functional_sim_netlist` falhou porque o simulador interno Quartus não suporta Cyclone IV E (erro 281041). O fluxo usado é `quartus_eda --simulation --tool=questa_oem --format=verilog --functional`, que passou com zero erros e avisos. A simulação externa Icarus é alternativa autorizada; não foi uma execução licenciada do Questa.

Os avisos de coerção de portas oe/devoe para inout vêm da biblioteca nativa de I/O conectada aos controles de dispositivo. Nenhum erro ocorreu; a tabela exaustiva do topo passou. Não há SDF aplicado nem afirmação de teste de temporização física.

Cabeçalho legal Intel preservado; comentários não legais são removidos por script que exige igualdade dos tokens funcionais, seguido de nova compilação/simulação. Consulte logs `netlist_eda.log`, `netlist_compile.log` e `netlist_sim.log`.
