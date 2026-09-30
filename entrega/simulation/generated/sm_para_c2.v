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


module sm_para_c2(
	SM,
	C2
);


input wire	[4:0] SM;
output wire	[5:0] C2;

wire	[5:0] C_ALTERA_SYNTHESIZED2;
wire	[5:1] CARRY;
wire	Cout;
wire	GND;
wire	[5:0] X;





somador_1bit	b2v_fa_0(
	.A(X[0]),
	.B(GND),
	.Cin(SM[4]),
	.S(C_ALTERA_SYNTHESIZED2[0]),
	.Cout(CARRY[1]));


somador_1bit	b2v_fa_1(
	.A(X[1]),
	.B(GND),
	.Cin(CARRY[1]),
	.S(C_ALTERA_SYNTHESIZED2[1]),
	.Cout(CARRY[2]));


somador_1bit	b2v_fa_2(
	.A(X[2]),
	.B(GND),
	.Cin(CARRY[2]),
	.S(C_ALTERA_SYNTHESIZED2[2]),
	.Cout(CARRY[3]));


somador_1bit	b2v_fa_3(
	.A(X[3]),
	.B(GND),
	.Cin(CARRY[3]),
	.S(C_ALTERA_SYNTHESIZED2[3]),
	.Cout(CARRY[4]));


somador_1bit	b2v_fa_4(
	.A(X[4]),
	.B(GND),
	.Cin(CARRY[4]),
	.S(C_ALTERA_SYNTHESIZED2[4]),
	.Cout(CARRY[5]));


somador_1bit	b2v_fa_5(
	.A(X[5]),
	.B(GND),
	.Cin(CARRY[5]),
	.S(C_ALTERA_SYNTHESIZED2[5])
	);


assign	X[0] = SM[0] ^ SM[4];

assign	X[1] = SM[1] ^ SM[4];

assign	X[2] = SM[2] ^ SM[4];

assign	X[3] = SM[3] ^ SM[4];

assign	X[4] = GND ^ SM[4];

assign	X[5] = GND ^ SM[4];

assign	C2 = C_ALTERA_SYNTHESIZED2;
assign	GND = 0;

endmodule
