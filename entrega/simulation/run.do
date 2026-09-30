onerror {quit -f -code 1}
set sim_dir [file dirname [file normalize [info script]]]
set entrega_dir [file normalize [file join $sim_dir ..]]
set project_dir [file normalize [file join $entrega_dir ..]]
set generated_dir [file join $sim_dir generated]
set logs_dir [file join $entrega_dir docs logs]
set work_dir [file normalize [file join $project_dir tmp tools iverilog questa_work]]
set modules {somador_1bit sm_para_c2 somador_subtrator_6bit c2_para_sm negador_c2_6bit modulo2_soma_sub comparador_c2_6bit logica_5bit decodificador_operacao mux_resultado_8x6 ula_core somador_subtrator_5bit bin_bcd bcd_7seg display_decimal_2digitos ula_de2_115}
file mkdir $logs_dir
if {![file exists $generated_dir]} {error "HDL export directory missing: $generated_dir"}
set sources [lsort [glob -nocomplain -directory $generated_dir *.v]]
set testbenches {}
foreach module $modules {
    set tb [file join $sim_dir "tb_$module.sv"]
    if {![file exists $tb]} {error "Testbench missing: $tb"}
    lappend testbenches $tb
}
if {[llength $sources] != 16} {error "Expected 16 exported Verilog modules, found [llength $sources]"}
if {![file exists $work_dir]} {vlib $work_dir}
vmap work $work_dir
transcript file [file join $logs_dir compile_all.log]
set compile_command [concat [list vlog -sv] $sources $testbenches]
eval $compile_command
cd $sim_dir
foreach module $modules {
    transcript file [file join $logs_dir "sim_$module.log"]
    vsim -c "work.tb_$module"
    run -all
    quit -sim
}
transcript file [file join $logs_dir run_complete.log]
echo {All 16 module testbenches completed.}
quit -f -code 0
