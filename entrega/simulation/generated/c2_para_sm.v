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


module c2_para_sm(
	R,
	F_SM
);


input wire	[5:0] R;
output wire	[5:0] F_SM;

wire	[5:0] ABS;
wire	[5:1] CARRY;
wire	Cout;
wire	[5:0] F_SM_ALTERA_SYNTHESIZED;
wire	GND;
wire	MAG_NONZERO;
wire	MAG_OR_01;
wire	MAG_OR_0123;
wire	MAG_OR_23;
wire	NEG_0;
wire	NEG_1;
wire	NEG_2;
wire	NEG_3;
wire	NEG_4;
wire	[5:0] NOT_R;
wire	NOT_SIGN;
wire	POS_0;
wire	POS_1;
wire	POS_2;
wire	POS_3;
wire	POS_4;
wire	VCC;





somador_1bit	b2v_fa_abs_0(
	.A(NOT_R[0]),
	.B(GND),
	.Cin(VCC),
	.S(ABS[0]),
	.Cout(CARRY[1]));


somador_1bit	b2v_fa_abs_1(
	.A(NOT_R[1]),
	.B(GND),
	.Cin(CARRY[1]),
	.S(ABS[1]),
	.Cout(CARRY[2]));


somador_1bit	b2v_fa_abs_2(
	.A(NOT_R[2]),
	.B(GND),
	.Cin(CARRY[2]),
	.S(ABS[2]),
	.Cout(CARRY[3]));


somador_1bit	b2v_fa_abs_3(
	.A(NOT_R[3]),
	.B(GND),
	.Cin(CARRY[3]),
	.S(ABS[3]),
	.Cout(CARRY[4]));


somador_1bit	b2v_fa_abs_4(
	.A(NOT_R[4]),
	.B(GND),
	.Cin(CARRY[4]),
	.S(ABS[4]),
	.Cout(CARRY[5]));


somador_1bit	b2v_fa_abs_5(
	.A(NOT_R[5]),
	.B(GND),
	.Cin(CARRY[5]),
	.S(ABS[5])
	);


assign	NOT_R[0] =  ~R[0];

assign	NOT_R[1] =  ~R[1];

assign	NOT_R[2] =  ~R[2];

assign	NOT_R[3] =  ~R[3];

assign	NOT_R[4] =  ~R[4];

assign	NOT_R[5] =  ~R[5];

assign	NOT_SIGN =  ~R[5];

assign	F_SM_ALTERA_SYNTHESIZED[0] = NEG_0 | POS_0;

assign	F_SM_ALTERA_SYNTHESIZED[1] = NEG_1 | POS_1;

assign	F_SM_ALTERA_SYNTHESIZED[2] = NEG_2 | POS_2;

assign	F_SM_ALTERA_SYNTHESIZED[3] = NEG_3 | POS_3;

assign	F_SM_ALTERA_SYNTHESIZED[4] = NEG_4 | POS_4;

assign	NEG_0 = ABS[0] & R[5];

assign	NEG_1 = ABS[1] & R[5];

assign	NEG_2 = ABS[2] & R[5];

assign	NEG_3 = ABS[3] & R[5];

assign	NEG_4 = ABS[4] & R[5];

assign	MAG_OR_01 = R[1] | R[0];

assign	MAG_OR_0123 = MAG_OR_23 | MAG_OR_01;

assign	MAG_NONZERO = R[4] | MAG_OR_0123;

assign	MAG_OR_23 = R[3] | R[2];

assign	POS_0 = R[0] & NOT_SIGN;

assign	POS_1 = R[1] & NOT_SIGN;

assign	POS_2 = R[2] & NOT_SIGN;

assign	POS_3 = R[3] & NOT_SIGN;

assign	POS_4 = R[4] & NOT_SIGN;

assign	F_SM_ALTERA_SYNTHESIZED[5] = R[5] & MAG_NONZERO;


assign	F_SM = F_SM_ALTERA_SYNTHESIZED;
assign	GND = 0;
assign	VCC = 1;

endmodule
