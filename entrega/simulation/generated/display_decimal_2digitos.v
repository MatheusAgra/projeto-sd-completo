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


module display_decimal_2digitos(
	ENABLE,
	MAG,
	DEZ_SEG,
	UNI_SEG
);


input wire	ENABLE;
input wire	[4:0] MAG;
output wire	[6:0] DEZ_SEG;
output wire	[6:0] UNI_SEG;

wire	[3:0] BCD_DEZ;
wire	[3:0] BCD_UNI;
wire	[6:0] DEZ_RAW;
wire	[6:0] DEZ_SEG_ALTERA_SYNTHESIZED;
wire	DISABLED;
wire	[6:0] UNI_RAW;
wire	[6:0] UNI_SEG_ALTERA_SYNTHESIZED;





bin_bcd	b2v_convert_mag(
	.MAG(MAG),
	.DEZ(BCD_DEZ),
	.UNI(BCD_UNI));


bcd_7seg	b2v_decode_dez(
	.BCD(BCD_DEZ),
	.SEG(DEZ_RAW));


bcd_7seg	b2v_decode_uni(
	.BCD(BCD_UNI),
	.SEG(UNI_RAW));

assign	DISABLED =  ~ENABLE;

assign	DEZ_SEG_ALTERA_SYNTHESIZED[0] = DISABLED | DEZ_RAW[0];

assign	DEZ_SEG_ALTERA_SYNTHESIZED[1] = DISABLED | DEZ_RAW[1];

assign	DEZ_SEG_ALTERA_SYNTHESIZED[2] = DISABLED | DEZ_RAW[2];

assign	DEZ_SEG_ALTERA_SYNTHESIZED[3] = DISABLED | DEZ_RAW[3];

assign	DEZ_SEG_ALTERA_SYNTHESIZED[4] = DISABLED | DEZ_RAW[4];

assign	DEZ_SEG_ALTERA_SYNTHESIZED[5] = DISABLED | DEZ_RAW[5];

assign	DEZ_SEG_ALTERA_SYNTHESIZED[6] = DISABLED | DEZ_RAW[6];

assign	UNI_SEG_ALTERA_SYNTHESIZED[0] = DISABLED | UNI_RAW[0];

assign	UNI_SEG_ALTERA_SYNTHESIZED[1] = DISABLED | UNI_RAW[1];

assign	UNI_SEG_ALTERA_SYNTHESIZED[2] = DISABLED | UNI_RAW[2];

assign	UNI_SEG_ALTERA_SYNTHESIZED[3] = DISABLED | UNI_RAW[3];

assign	UNI_SEG_ALTERA_SYNTHESIZED[4] = DISABLED | UNI_RAW[4];

assign	UNI_SEG_ALTERA_SYNTHESIZED[5] = DISABLED | UNI_RAW[5];

assign	UNI_SEG_ALTERA_SYNTHESIZED[6] = DISABLED | UNI_RAW[6];

assign	DEZ_SEG = DEZ_SEG_ALTERA_SYNTHESIZED;
assign	UNI_SEG = UNI_SEG_ALTERA_SYNTHESIZED;

endmodule
