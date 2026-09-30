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


module somador_subtrator_5bit(
	SUB,
	A,
	B,
	Cout,
	R
);


input wire	SUB;
input wire	[4:0] A;
input wire	[4:0] B;
output wire	Cout;
output wire	[4:0] R;

wire	[4:0] BX;
wire	[4:1] CARRY;
wire	[4:0] R_ALTERA_SYNTHESIZED;





somador_1bit	b2v_fa_0(
	.A(A[0]),
	.B(BX[0]),
	.Cin(SUB),
	.S(R_ALTERA_SYNTHESIZED[0]),
	.Cout(CARRY[1]));


somador_1bit	b2v_fa_1(
	.A(A[1]),
	.B(BX[1]),
	.Cin(CARRY[1]),
	.S(R_ALTERA_SYNTHESIZED[1]),
	.Cout(CARRY[2]));


somador_1bit	b2v_fa_2(
	.A(A[2]),
	.B(BX[2]),
	.Cin(CARRY[2]),
	.S(R_ALTERA_SYNTHESIZED[2]),
	.Cout(CARRY[3]));


somador_1bit	b2v_fa_3(
	.A(A[3]),
	.B(BX[3]),
	.Cin(CARRY[3]),
	.S(R_ALTERA_SYNTHESIZED[3]),
	.Cout(CARRY[4]));


somador_1bit	b2v_fa_4(
	.A(A[4]),
	.B(BX[4]),
	.Cin(CARRY[4]),
	.S(R_ALTERA_SYNTHESIZED[4]),
	.Cout(Cout));

assign	BX[0] = B[0] ^ SUB;

assign	BX[1] = B[1] ^ SUB;

assign	BX[2] = B[2] ^ SUB;

assign	BX[3] = B[3] ^ SUB;

assign	BX[4] = B[4] ^ SUB;

assign	R = R_ALTERA_SYNTHESIZED;

endmodule
