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


module bin_bcd(
	MAG,
	DEZ,
	UNI
);


input wire	[4:0] MAG;
output wire	[3:0] DEZ;
output wire	[3:0] UNI;

wire	A10_HI;
wire	buf_dez0__buffer_net;
wire	buf_dez1__buffer_net;
wire	correction_bit_1__buffer_net;
wire	correction_bit_2__buffer_net;
wire	correction_bit_3__buffer_net;
wire	correction_bit_4__buffer_net;
wire	COUT_UNUSED;
wire	DEZ0_A;
wire	DEZ0_INTERNAL;
wire	[3:0] DEZ_ALTERA_SYNTHESIZED;
wire	[4:0] K;
wire	NT20;
wire	O10_MID;
wire	O20_MID;
wire	SUB_ONE;
wire	T10;
wire	T20;
wire	T30;
wire	[3:0] UNI_ALTERA_SYNTHESIZED;
wire	[4:0] UNI_RAW;
wire	unit_bit_0__buffer_net;
wire	unit_bit_1__buffer_net;
wire	unit_bit_2__buffer_net;
wire	unit_bit_3__buffer_net;




assign	A10_HI = MAG[3] & O10_MID;

assign	T20 = MAG[4] & O20_MID;

assign	T30 = MAG[4] & MAG[3] & MAG[2] & MAG[1];

assign	DEZ0_A = T10 & NT20;

assign	buf_dez0__buffer_net =  ~DEZ0_INTERNAL;

assign	DEZ_ALTERA_SYNTHESIZED[0] =  ~buf_dez0__buffer_net;

assign	buf_dez1__buffer_net =  ~T20;

assign	DEZ_ALTERA_SYNTHESIZED[1] =  ~buf_dez1__buffer_net;

assign	correction_bit_1__buffer_net =  ~DEZ0_INTERNAL;

assign	K[1] =  ~correction_bit_1__buffer_net;

assign	correction_bit_2__buffer_net =  ~T20;

assign	K[2] =  ~correction_bit_2__buffer_net;

assign	correction_bit_3__buffer_net =  ~DEZ0_INTERNAL;

assign	K[3] =  ~correction_bit_3__buffer_net;

assign	correction_bit_4__buffer_net =  ~T20;

assign	K[4] =  ~correction_bit_4__buffer_net;




assign	NT20 =  ~T20;

assign	T10 = A10_HI | MAG[4];

assign	O10_MID = MAG[1] | MAG[2];

assign	O20_MID = MAG[2] | MAG[3];

assign	DEZ0_INTERNAL = T30 | DEZ0_A;



somador_subtrator_5bit	b2v_subtract_tens(
	.SUB(SUB_ONE),
	.A(MAG),
	.B(K),
	
	.R(UNI_RAW));

assign	unit_bit_0__buffer_net =  ~UNI_RAW[0];

assign	UNI_ALTERA_SYNTHESIZED[0] =  ~unit_bit_0__buffer_net;

assign	unit_bit_1__buffer_net =  ~UNI_RAW[1];

assign	UNI_ALTERA_SYNTHESIZED[1] =  ~unit_bit_1__buffer_net;

assign	unit_bit_2__buffer_net =  ~UNI_RAW[2];

assign	UNI_ALTERA_SYNTHESIZED[2] =  ~unit_bit_2__buffer_net;

assign	unit_bit_3__buffer_net =  ~UNI_RAW[3];

assign	UNI_ALTERA_SYNTHESIZED[3] =  ~unit_bit_3__buffer_net;

assign	DEZ = DEZ_ALTERA_SYNTHESIZED;
assign	UNI = UNI_ALTERA_SYNTHESIZED;
assign	DEZ_ALTERA_SYNTHESIZED[2] = 0;
assign	DEZ_ALTERA_SYNTHESIZED[3] = 0;
assign	K[0] = 0;
assign	SUB_ONE = 1;

endmodule
