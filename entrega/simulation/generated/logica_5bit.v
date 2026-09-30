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


module logica_5bit(
	A_SM,
	B_SM,
	AND6,
	XOR6
);


input wire	[4:0] A_SM;
input wire	[4:0] B_SM;
output wire	[5:0] AND6;
output wire	[5:0] XOR6;

wire	[5:0] AND_ALTERA_SYNTHESIZED6;
wire	[5:0] XOR_ALTERA_SYNTHESIZED6;






assign	AND_ALTERA_SYNTHESIZED6[0] = A_SM[0] & B_SM[0];

assign	AND_ALTERA_SYNTHESIZED6[1] = A_SM[1] & B_SM[1];

assign	AND_ALTERA_SYNTHESIZED6[2] = A_SM[2] & B_SM[2];

assign	AND_ALTERA_SYNTHESIZED6[3] = A_SM[3] & B_SM[3];

assign	AND_ALTERA_SYNTHESIZED6[5] = A_SM[4] & B_SM[4];

assign	XOR_ALTERA_SYNTHESIZED6[0] = A_SM[0] ^ B_SM[0];

assign	XOR_ALTERA_SYNTHESIZED6[1] = A_SM[1] ^ B_SM[1];

assign	XOR_ALTERA_SYNTHESIZED6[2] = A_SM[2] ^ B_SM[2];

assign	XOR_ALTERA_SYNTHESIZED6[3] = A_SM[3] ^ B_SM[3];

assign	XOR_ALTERA_SYNTHESIZED6[5] = A_SM[4] ^ B_SM[4];

assign	AND6 = AND_ALTERA_SYNTHESIZED6;
assign	XOR6 = XOR_ALTERA_SYNTHESIZED6;
assign	AND_ALTERA_SYNTHESIZED6[4] = 0;
assign	XOR_ALTERA_SYNTHESIZED6[4] = 0;

endmodule
