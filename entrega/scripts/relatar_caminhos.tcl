package require ::quartus::project
package require ::quartus::sta
project_open ULA_DE2_115
create_timing_netlist
update_timing_netlist
report_path -from [all_inputs] -to [all_outputs] -npaths 20 -show_routing -file output_files/caminhos_entrada_saida.rpt
delete_timing_netlist
project_close
