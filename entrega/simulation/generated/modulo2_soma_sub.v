// Copyright (C) 2021  Intel Corporation. All rights reserved.
// Your use of Intel Corporation's design tools, logic functions 
// and other software and tools, and any partner logic 
// functions, and any output files from any of the foregoing 
// (including device programming or simulation files), and any 
// associated documentation or information are expressly subject 
// to the terms and conditions of the Intel Program License 
// Subscription Agreement, the Intel Quartus Prime License Agreement,
// the Intel FPGA IP License Agreement, or other applicable license
// agreement, including, without limitation, that your use is for
// the sole purpose of programming logic devices manufactured by
// Intel and sold by Intel or its authorized distributors.  Please
// refer to the applicable agreement for further details, at
// https://fpgasoftware.intel.com/eula.


module modulo2_soma_sub(
	SUB,
	A_C2,
	B_C2,
	F_SM
);


input wire	SUB;
input wire	[5:0] A_C2;
input wire	[5:0] B_C2;
output wire	[5:0] F_SM;

wire	COUT;
wire	[5:0] F_SM_ALTERA_SYNTHESIZED;
wire	[5:0] R_C2;





c2_para_sm	b2v_conversor(
	.R(R_C2),
	.F_SM(F_SM_ALTERA_SYNTHESIZED));


somador_subtrator_6bit	b2v_soma_sub(
	.SUB(SUB),
	.A(A_C2),
	.B(B_C2),
	
	.R(R_C2));

assign	F_SM = F_SM_ALTERA_SYNTHESIZED;

endmodule
