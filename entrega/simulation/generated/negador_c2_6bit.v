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


module negador_c2_6bit(
	B_C2,
	NEG
);


input wire	[5:0] B_C2;
output wire	[5:0] NEG;

wire	[5:1] CARRY;
wire	Cout;
wire	GND;
wire	[5:0] NEG_ALTERA_SYNTHESIZED;
wire	[5:0] NOT_B;
wire	VCC;





somador_1bit	b2v_fa_0(
	.A(NOT_B[0]),
	.B(GND),
	.Cin(VCC),
	.S(NEG_ALTERA_SYNTHESIZED[0]),
	.Cout(CARRY[1]));


somador_1bit	b2v_fa_1(
	.A(NOT_B[1]),
	.B(GND),
	.Cin(CARRY[1]),
	.S(NEG_ALTERA_SYNTHESIZED[1]),
	.Cout(CARRY[2]));


somador_1bit	b2v_fa_2(
	.A(NOT_B[2]),
	.B(GND),
	.Cin(CARRY[2]),
	.S(NEG_ALTERA_SYNTHESIZED[2]),
	.Cout(CARRY[3]));


somador_1bit	b2v_fa_3(
	.A(NOT_B[3]),
	.B(GND),
	.Cin(CARRY[3]),
	.S(NEG_ALTERA_SYNTHESIZED[3]),
	.Cout(CARRY[4]));


somador_1bit	b2v_fa_4(
	.A(NOT_B[4]),
	.B(GND),
	.Cin(CARRY[4]),
	.S(NEG_ALTERA_SYNTHESIZED[4]),
	.Cout(CARRY[5]));


somador_1bit	b2v_fa_5(
	.A(NOT_B[5]),
	.B(GND),
	.Cin(CARRY[5]),
	.S(NEG_ALTERA_SYNTHESIZED[5])
	);


assign	NOT_B[0] =  ~B_C2[0];

assign	NOT_B[1] =  ~B_C2[1];

assign	NOT_B[2] =  ~B_C2[2];

assign	NOT_B[3] =  ~B_C2[3];

assign	NOT_B[4] =  ~B_C2[4];

assign	NOT_B[5] =  ~B_C2[5];


assign	NEG = NEG_ALTERA_SYNTHESIZED;
assign	GND = 0;
assign	VCC = 1;

endmodule
