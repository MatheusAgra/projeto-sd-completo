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


module bcd_7seg(
	BCD,
	SEG
);


input wire	[3:0] BCD;
output wire	[6:0] SEG;

wire	NBCD0;
wire	NBCD1;
wire	NBCD2;
wire	NBCD3;
wire	OR_D_FIRST;
wire	P_0001;
wire	P_000x;
wire	P_00x1;
wire	P_11xx;
wire	P_1x1x;
wire	P_x010;
wire	P_x01x;
wire	P_x100;
wire	P_x101;
wire	P_x10x;
wire	P_x110;
wire	P_x111;
wire	P_xx11;
wire	[6:0] SEG_ALTERA_SYNTHESIZED;




assign	NBCD0 =  ~BCD[0];

assign	NBCD1 =  ~BCD[1];

assign	NBCD2 =  ~BCD[2];

assign	NBCD3 =  ~BCD[3];

assign	SEG_ALTERA_SYNTHESIZED[0] = P_x100 | P_1x1x | P_11xx | P_0001;

assign	SEG_ALTERA_SYNTHESIZED[1] = P_x101 | P_1x1x | P_11xx | P_x110;

assign	SEG_ALTERA_SYNTHESIZED[2] = P_1x1x | P_11xx | P_x010;

assign	OR_D_FIRST = P_x100 | P_0001 | P_1x1x | P_x111;

assign	SEG_ALTERA_SYNTHESIZED[3] = P_11xx | OR_D_FIRST;

assign	SEG_ALTERA_SYNTHESIZED[4] = P_x10x | P_1x1x | BCD[0];

assign	SEG_ALTERA_SYNTHESIZED[5] = P_xx11 | P_00x1 | P_11xx | P_x01x;

assign	SEG_ALTERA_SYNTHESIZED[6] = P_x111 | P_1x1x | P_11xx | P_000x;

assign	P_0001 = NBCD3 & NBCD2 & NBCD1 & BCD[0];

assign	P_000x = NBCD3 & NBCD2 & NBCD1;

assign	P_00x1 = NBCD3 & NBCD2 & BCD[0];

assign	P_11xx = BCD[3] & BCD[2];

assign	P_1x1x = BCD[3] & BCD[1];

assign	P_x010 = NBCD2 & BCD[1] & NBCD0;

assign	P_x01x = NBCD2 & BCD[1];

assign	P_x100 = BCD[2] & NBCD1 & NBCD0;

assign	P_x101 = BCD[2] & NBCD1 & BCD[0];

assign	P_x10x = BCD[2] & NBCD1;

assign	P_x110 = BCD[2] & BCD[1] & NBCD0;

assign	P_x111 = BCD[2] & BCD[1] & BCD[0];

assign	P_xx11 = BCD[1] & BCD[0];

assign	SEG = SEG_ALTERA_SYNTHESIZED;

endmodule
