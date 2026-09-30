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


module ula_de2_115(
	SW,
	HEX0,
	HEX1,
	HEX2,
	HEX3,
	HEX4,
	HEX5,
	HEX6,
	HEX7,
	LEDG,
	LEDR
);


input wire	[12:0] SW;
output wire	[6:0] HEX0;
output wire	[6:0] HEX1;
output wire	[6:0] HEX2;
output wire	[6:0] HEX3;
output wire	[6:0] HEX4;
output wire	[6:0] HEX5;
output wire	[6:0] HEX6;
output wire	[6:0] HEX7;
output wire	[8:0] LEDG;
output wire	[17:0] LEDR;

wire	EXIBE_F;
wire	[5:0] F;
wire	[6:0] HEX_ALTERA_SYNTHESIZED0;
wire	[6:0] HEX_ALTERA_SYNTHESIZED1;
wire	[6:0] HEX_ALTERA_SYNTHESIZED2;
wire	[6:0] HEX_ALTERA_SYNTHESIZED3;
wire	[6:0] HEX_ALTERA_SYNTHESIZED4;
wire	[6:0] HEX_ALTERA_SYNTHESIZED5;
wire	[6:0] HEX_ALTERA_SYNTHESIZED6;
wire	[6:0] HEX_ALTERA_SYNTHESIZED7;
wire	ledg_0__buffer_net;
wire	ledg_1__buffer_net;
wire	ledg_2__buffer_net;
wire	ledg_3__buffer_net;
wire	ledg_4__buffer_net;
wire	ledg_5__buffer_net;
wire	ledg_6__buffer_net;
wire	[8:0] LEDG_ALTERA_SYNTHESIZED;
wire	[17:0] LEDR_ALTERA_SYNTHESIZED;
wire	mag_a_0__buffer_net;
wire	mag_a_1__buffer_net;
wire	mag_a_2__buffer_net;
wire	mag_a_3__buffer_net;
wire	mag_b_0__buffer_net;
wire	mag_b_1__buffer_net;
wire	mag_b_2__buffer_net;
wire	mag_b_3__buffer_net;
wire	[4:0] MAGA;
wire	[4:0] MAGB;
wire	mirror_0__buffer_net;
wire	mirror_10__buffer_net;
wire	mirror_11__buffer_net;
wire	mirror_12__buffer_net;
wire	mirror_1__buffer_net;
wire	mirror_2__buffer_net;
wire	mirror_3__buffer_net;
wire	mirror_4__buffer_net;
wire	mirror_5__buffer_net;
wire	mirror_6__buffer_net;
wire	mirror_7__buffer_net;
wire	mirror_8__buffer_net;
wire	mirror_9__buffer_net;
wire	ONE;
wire	STATUS;





display_decimal_2digitos	b2v_display_a(
	.ENABLE(ONE),
	.MAG(MAGA),
	.DEZ_SEG(HEX_ALTERA_SYNTHESIZED5),
	.UNI_SEG(HEX_ALTERA_SYNTHESIZED4));


display_decimal_2digitos	b2v_display_b(
	.ENABLE(ONE),
	.MAG(MAGB),
	.DEZ_SEG(HEX_ALTERA_SYNTHESIZED3),
	.UNI_SEG(HEX_ALTERA_SYNTHESIZED2));


display_decimal_2digitos	b2v_display_f(
	.ENABLE(EXIBE_F),
	.MAG(F[4:0]),
	.DEZ_SEG(HEX_ALTERA_SYNTHESIZED1),
	.UNI_SEG(HEX_ALTERA_SYNTHESIZED0));
















assign	ledg_0__buffer_net =  ~F[0];

assign	LEDG_ALTERA_SYNTHESIZED[0] =  ~ledg_0__buffer_net;

assign	ledg_1__buffer_net =  ~F[1];

assign	LEDG_ALTERA_SYNTHESIZED[1] =  ~ledg_1__buffer_net;

assign	ledg_2__buffer_net =  ~F[2];

assign	LEDG_ALTERA_SYNTHESIZED[2] =  ~ledg_2__buffer_net;

assign	ledg_3__buffer_net =  ~F[3];

assign	LEDG_ALTERA_SYNTHESIZED[3] =  ~ledg_3__buffer_net;

assign	ledg_4__buffer_net =  ~F[4];

assign	LEDG_ALTERA_SYNTHESIZED[4] =  ~ledg_4__buffer_net;

assign	ledg_5__buffer_net =  ~F[5];

assign	LEDG_ALTERA_SYNTHESIZED[5] =  ~ledg_5__buffer_net;

assign	ledg_6__buffer_net =  ~STATUS;

assign	LEDG_ALTERA_SYNTHESIZED[6] =  ~ledg_6__buffer_net;








assign	mag_a_0__buffer_net =  ~SW[0];

assign	MAGA[0] =  ~mag_a_0__buffer_net;

assign	mag_a_1__buffer_net =  ~SW[1];

assign	MAGA[1] =  ~mag_a_1__buffer_net;

assign	mag_a_2__buffer_net =  ~SW[2];

assign	MAGA[2] =  ~mag_a_2__buffer_net;

assign	mag_a_3__buffer_net =  ~SW[3];

assign	MAGA[3] =  ~mag_a_3__buffer_net;

assign	mag_b_0__buffer_net =  ~SW[5];

assign	MAGB[0] =  ~mag_b_0__buffer_net;

assign	mag_b_1__buffer_net =  ~SW[6];

assign	MAGB[1] =  ~mag_b_1__buffer_net;

assign	mag_b_2__buffer_net =  ~SW[7];

assign	MAGB[2] =  ~mag_b_2__buffer_net;

assign	mag_b_3__buffer_net =  ~SW[8];

assign	MAGB[3] =  ~mag_b_3__buffer_net;

assign	mirror_0__buffer_net =  ~SW[0];

assign	LEDR_ALTERA_SYNTHESIZED[0] =  ~mirror_0__buffer_net;

assign	mirror_10__buffer_net =  ~SW[10];

assign	LEDR_ALTERA_SYNTHESIZED[10] =  ~mirror_10__buffer_net;

assign	mirror_11__buffer_net =  ~SW[11];

assign	LEDR_ALTERA_SYNTHESIZED[11] =  ~mirror_11__buffer_net;

assign	mirror_12__buffer_net =  ~SW[12];

assign	LEDR_ALTERA_SYNTHESIZED[12] =  ~mirror_12__buffer_net;

assign	mirror_1__buffer_net =  ~SW[1];

assign	LEDR_ALTERA_SYNTHESIZED[1] =  ~mirror_1__buffer_net;

assign	mirror_2__buffer_net =  ~SW[2];

assign	LEDR_ALTERA_SYNTHESIZED[2] =  ~mirror_2__buffer_net;

assign	mirror_3__buffer_net =  ~SW[3];

assign	LEDR_ALTERA_SYNTHESIZED[3] =  ~mirror_3__buffer_net;

assign	mirror_4__buffer_net =  ~SW[4];

assign	LEDR_ALTERA_SYNTHESIZED[4] =  ~mirror_4__buffer_net;

assign	mirror_5__buffer_net =  ~SW[5];

assign	LEDR_ALTERA_SYNTHESIZED[5] =  ~mirror_5__buffer_net;

assign	mirror_6__buffer_net =  ~SW[6];

assign	LEDR_ALTERA_SYNTHESIZED[6] =  ~mirror_6__buffer_net;

assign	mirror_7__buffer_net =  ~SW[7];

assign	LEDR_ALTERA_SYNTHESIZED[7] =  ~mirror_7__buffer_net;

assign	mirror_8__buffer_net =  ~SW[8];

assign	LEDR_ALTERA_SYNTHESIZED[8] =  ~mirror_8__buffer_net;

assign	mirror_9__buffer_net =  ~SW[9];

assign	LEDR_ALTERA_SYNTHESIZED[9] =  ~mirror_9__buffer_net;


ula_core	b2v_ula(
	.A(SW[4:0]),
	.B(SW[9:5]),
	.S(SW[12:10]),
	.STATUS(STATUS),
	.EXIBE_F(EXIBE_F),
	.F(F));



assign	HEX0 = HEX_ALTERA_SYNTHESIZED0;
assign	HEX1 = HEX_ALTERA_SYNTHESIZED1;
assign	HEX2 = HEX_ALTERA_SYNTHESIZED2;
assign	HEX3 = HEX_ALTERA_SYNTHESIZED3;
assign	HEX4 = HEX_ALTERA_SYNTHESIZED4;
assign	HEX5 = HEX_ALTERA_SYNTHESIZED5;
assign	HEX6 = HEX_ALTERA_SYNTHESIZED6;
assign	HEX7 = HEX_ALTERA_SYNTHESIZED7;
assign	LEDG = LEDG_ALTERA_SYNTHESIZED;
assign	LEDR = LEDR_ALTERA_SYNTHESIZED;
assign	HEX_ALTERA_SYNTHESIZED6[0] = 1;
assign	HEX_ALTERA_SYNTHESIZED6[1] = 1;
assign	HEX_ALTERA_SYNTHESIZED6[2] = 1;
assign	HEX_ALTERA_SYNTHESIZED6[3] = 1;
assign	HEX_ALTERA_SYNTHESIZED6[4] = 1;
assign	HEX_ALTERA_SYNTHESIZED6[5] = 1;
assign	HEX_ALTERA_SYNTHESIZED6[6] = 1;
assign	HEX_ALTERA_SYNTHESIZED7[0] = 1;
assign	HEX_ALTERA_SYNTHESIZED7[1] = 1;
assign	HEX_ALTERA_SYNTHESIZED7[2] = 1;
assign	HEX_ALTERA_SYNTHESIZED7[3] = 1;
assign	HEX_ALTERA_SYNTHESIZED7[4] = 1;
assign	HEX_ALTERA_SYNTHESIZED7[5] = 1;
assign	HEX_ALTERA_SYNTHESIZED7[6] = 1;
assign	LEDG_ALTERA_SYNTHESIZED[7] = 0;
assign	LEDG_ALTERA_SYNTHESIZED[8] = 0;
assign	LEDR_ALTERA_SYNTHESIZED[13] = 0;
assign	LEDR_ALTERA_SYNTHESIZED[14] = 0;
assign	LEDR_ALTERA_SYNTHESIZED[15] = 0;
assign	LEDR_ALTERA_SYNTHESIZED[16] = 0;
assign	LEDR_ALTERA_SYNTHESIZED[17] = 0;
assign	MAGA[4] = 0;
assign	MAGB[4] = 0;
assign	ONE = 1;

endmodule
