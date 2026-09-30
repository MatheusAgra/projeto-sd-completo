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


module mux_resultado_8x6(
	C0,
	C1,
	C2,
	C3,
	C4,
	C5,
	C6,
	C7,
	D,
	F
);


input wire	[5:0] C0;
input wire	[5:0] C1;
input wire	[5:0] C2;
input wire	[5:0] C3;
input wire	[5:0] C4;
input wire	[5:0] C5;
input wire	[5:0] C6;
input wire	[5:0] C7;
input wire	[7:0] D;
output wire	[5:0] F;

wire	[5:0] F_ALTERA_SYNTHESIZED;
wire	P_0_0;
wire	P_0_1;
wire	P_0_2;
wire	P_0_3;
wire	P_0_4;
wire	P_0_5;
wire	P_1_0;
wire	P_1_1;
wire	P_1_2;
wire	P_1_3;
wire	P_1_4;
wire	P_1_5;
wire	P_2_0;
wire	P_2_1;
wire	P_2_2;
wire	P_2_3;
wire	P_2_4;
wire	P_2_5;
wire	P_3_0;
wire	P_3_1;
wire	P_3_2;
wire	P_3_3;
wire	P_3_4;
wire	P_3_5;
wire	P_4_0;
wire	P_4_1;
wire	P_4_2;
wire	P_4_3;
wire	P_4_4;
wire	P_4_5;
wire	P_5_0;
wire	P_5_1;
wire	P_5_2;
wire	P_5_3;
wire	P_5_4;
wire	P_5_5;
wire	P_6_0;
wire	P_6_1;
wire	P_6_2;
wire	P_6_3;
wire	P_6_4;
wire	P_6_5;
wire	P_7_0;
wire	P_7_1;
wire	P_7_2;
wire	P_7_3;
wire	P_7_4;
wire	P_7_5;




assign	P_0_0 = C0[0] & D[0];

assign	P_0_1 = C0[1] & D[0];

assign	P_0_2 = C0[2] & D[0];

assign	P_0_3 = C0[3] & D[0];

assign	P_0_4 = C0[4] & D[0];

assign	P_0_5 = C0[5] & D[0];

assign	P_1_0 = C1[0] & D[1];

assign	P_1_1 = C1[1] & D[1];

assign	P_1_2 = C1[2] & D[1];

assign	P_1_3 = C1[3] & D[1];

assign	P_1_4 = C1[4] & D[1];

assign	P_1_5 = C1[5] & D[1];

assign	P_2_0 = C2[0] & D[2];

assign	P_2_1 = C2[1] & D[2];

assign	P_2_2 = C2[2] & D[2];

assign	P_2_3 = C2[3] & D[2];

assign	P_2_4 = C2[4] & D[2];

assign	P_2_5 = C2[5] & D[2];

assign	P_3_0 = C3[0] & D[3];

assign	P_3_1 = C3[1] & D[3];

assign	P_3_2 = C3[2] & D[3];

assign	P_3_3 = C3[3] & D[3];

assign	P_3_4 = C3[4] & D[3];

assign	P_3_5 = C3[5] & D[3];

assign	P_4_0 = C4[0] & D[4];

assign	P_4_1 = C4[1] & D[4];

assign	P_4_2 = C4[2] & D[4];

assign	P_4_3 = C4[3] & D[4];

assign	P_4_4 = C4[4] & D[4];

assign	P_4_5 = C4[5] & D[4];

assign	P_5_0 = C5[0] & D[5];

assign	P_5_1 = C5[1] & D[5];

assign	P_5_2 = C5[2] & D[5];

assign	P_5_3 = C5[3] & D[5];

assign	P_5_4 = C5[4] & D[5];

assign	P_5_5 = C5[5] & D[5];

assign	P_6_0 = C6[0] & D[6];

assign	P_6_1 = C6[1] & D[6];

assign	P_6_2 = C6[2] & D[6];

assign	P_6_3 = C6[3] & D[6];

assign	P_6_4 = C6[4] & D[6];

assign	P_6_5 = C6[5] & D[6];

assign	P_7_0 = C7[0] & D[7];

assign	P_7_1 = C7[1] & D[7];

assign	P_7_2 = C7[2] & D[7];

assign	P_7_3 = C7[3] & D[7];

assign	P_7_4 = C7[4] & D[7];

assign	P_7_5 = C7[5] & D[7];

assign	F_ALTERA_SYNTHESIZED[0] = P_0_0 | P_2_0 | P_1_0 | P_3_0 | P_5_0 | P_4_0 | P_6_0 | P_7_0;

assign	F_ALTERA_SYNTHESIZED[1] = P_0_1 | P_2_1 | P_1_1 | P_3_1 | P_5_1 | P_4_1 | P_6_1 | P_7_1;

assign	F_ALTERA_SYNTHESIZED[2] = P_0_2 | P_2_2 | P_1_2 | P_3_2 | P_5_2 | P_4_2 | P_6_2 | P_7_2;

assign	F_ALTERA_SYNTHESIZED[3] = P_0_3 | P_2_3 | P_1_3 | P_3_3 | P_5_3 | P_4_3 | P_6_3 | P_7_3;

assign	F_ALTERA_SYNTHESIZED[4] = P_0_4 | P_2_4 | P_1_4 | P_3_4 | P_5_4 | P_4_4 | P_6_4 | P_7_4;

assign	F_ALTERA_SYNTHESIZED[5] = P_0_5 | P_2_5 | P_1_5 | P_3_5 | P_5_5 | P_4_5 | P_6_5 | P_7_5;

assign	F = F_ALTERA_SYNTHESIZED;

endmodule
