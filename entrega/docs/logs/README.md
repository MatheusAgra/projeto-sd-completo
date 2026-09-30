# Logs de compilação e simulação

`compile_<modulo>.log` e `sim_<modulo>.log` guardam as saídas do fluxo Icarus. `compile_all.log` e `sim_<modulo>.log` podem ser produzidos pela alternativa Questa em `run.do`.

Em 30/09/2026, os dezesseis HDL convertidos pelo Quartus e seus testbenches executaram no Icarus. Os dezesseis logs de simulação registraram PASS; os logs individuais indicam a cobertura de cada módulo. As quatro baterias desta frente cobriram 4096 pares do comparador, 1024 pares da lógica, oito seletores do decodificador e 512 estímulos do mux. Os VCDs correspondentes são artefatos gravados pelas simulações.

Questa não foi executado com licença válida. `run.do` continua preparado para quando o checkout de licença estiver funcional.

`*_analyze.log`, `*_convert.log` e `*_symbol.log` registram a leitura, exportação e geração de símbolos nativas. `compile_final.log` é a compilação original final e `recompile_zip.log` a compilação das fontes extraídas do candidato. `netlist_eda.log`, `netlist_compile.log`, `netlist_cleanup.log` e `netlist_sim.log` registram a exportação e simulação funcional da netlist mapeada. `netlist_map.log` preserva a tentativa legada incompatível com o dispositivo. `caminhos_sta.log` registra o relatório adicional de caminhos combinacionais. As contagens e justificativas estão em `../VALIDACAO.md` e `../AVISOS_COMPILACAO.md`.
