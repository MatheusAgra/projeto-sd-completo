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


module comparador_c2_6bit(
	A_C2,
	B_C2,
	EQ,
	GT,
	LT
);


input wire	[5:0] A_C2;
input wire	[5:0] B_C2;
output wire	EQ;
output wire	GT;
output wire	LT;

wire	EQ_ALTERA_SYNTHESIZED;
wire	EQ_OR_LT;
wire	EQBIT_0;
wire	EQBIT_1;
wire	EQBIT_2;
wire	EQBIT_3;
wire	EQBIT_4;
wire	EQBIT_5;
wire	EQHI_0;
wire	EQHI_1;
wire	EQHI_2;
wire	LT_ALTERA_SYNTHESIZED;
wire	NA_0;
wire	NA_1;
wire	NA_2;
wire	NA_3;
wire	NA_4;
wire	NAS;
wire	NBS;
wire	NEG_A_LT;
wire	NEG_BOTH;
wire	NEG_LT;
wire	POS_LT;
wire	ULT;
wire	ULT_HIGH;
wire	ULT_LOW;
wire	ULT_TERM_0;
wire	ULT_TERM_1;
wire	ULT_TERM_2;
wire	ULT_TERM_3;
wire	ULT_TERM_4;




assign	EQ_ALTERA_SYNTHESIZED = EQBIT_2 & EQBIT_0 & EQBIT_1 & EQBIT_3 & EQBIT_4 & EQBIT_5;

assign	EQBIT_0 = A_C2[0] ~^ B_C2[0];

assign	EQBIT_1 = A_C2[1] ~^ B_C2[1];

assign	EQBIT_2 = A_C2[2] ~^ B_C2[2];

assign	EQBIT_3 = A_C2[3] ~^ B_C2[3];

assign	EQBIT_4 = A_C2[4] ~^ B_C2[4];

assign	EQBIT_5 = A_C2[5] ~^ B_C2[5];

assign	EQ_OR_LT = LT_ALTERA_SYNTHESIZED | EQ_ALTERA_SYNTHESIZED;

assign	EQHI_0 = EQBIT_4 & EQBIT_3 & EQBIT_2 & EQBIT_1;

assign	EQHI_1 = EQBIT_4 & EQBIT_3 & EQBIT_2;

assign	EQHI_2 = EQBIT_4 & EQBIT_3;

assign	NEG_A_LT = A_C2[5] & NBS;

assign	NEG_BOTH = A_C2[5] & B_C2[5];

assign	NEG_LT = NEG_BOTH & ULT;

assign	NA_0 =  ~A_C2[0];

assign	NA_1 =  ~A_C2[1];

assign	NA_2 =  ~A_C2[2];

assign	NA_3 =  ~A_C2[3];

assign	NA_4 =  ~A_C2[4];

assign	NAS =  ~A_C2[5];

assign	NBS =  ~B_C2[5];

assign	POS_LT = NAS & NBS & ULT;

assign	GT =  ~EQ_OR_LT;

assign	LT_ALTERA_SYNTHESIZED = POS_LT | NEG_LT | NEG_A_LT;

assign	ULT = ULT_HIGH | ULT_LOW;

assign	ULT_TERM_0 = EQHI_0 & NA_0 & B_C2[0];

assign	ULT_TERM_1 = EQHI_1 & NA_1 & B_C2[1];

assign	ULT_TERM_2 = EQHI_2 & NA_2 & B_C2[2];

assign	ULT_TERM_3 = EQBIT_4 & NA_3 & B_C2[3];

assign	ULT_TERM_4 = NA_4 & B_C2[4];

assign	ULT_HIGH = ULT_TERM_0 | ULT_TERM_1;

assign	ULT_LOW = ULT_TERM_3 | ULT_TERM_2 | ULT_TERM_4;

assign	EQ = EQ_ALTERA_SYNTHESIZED;
assign	LT = LT_ALTERA_SYNTHESIZED;

endmodule
