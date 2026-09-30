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


module decodificador_operacao(
	S,
	EXIBE_F,
	D
);


input wire	[2:0] S;
output wire	EXIBE_F;
output wire	[7:0] D;

wire	[7:0] D_ALTERA_SYNTHESIZED;
wire	NS_0;
wire	NS_1;
wire	NS_2;




assign	D_ALTERA_SYNTHESIZED[0] = NS_2 & NS_1 & NS_0;

assign	D_ALTERA_SYNTHESIZED[1] = NS_2 & NS_1 & S[0];

assign	D_ALTERA_SYNTHESIZED[2] = NS_2 & S[1] & NS_0;

assign	D_ALTERA_SYNTHESIZED[3] = NS_2 & S[1] & S[0];

assign	D_ALTERA_SYNTHESIZED[4] = S[2] & NS_1 & NS_0;

assign	D_ALTERA_SYNTHESIZED[5] = S[2] & NS_1 & S[0];

assign	D_ALTERA_SYNTHESIZED[6] = S[2] & S[1] & NS_0;

assign	D_ALTERA_SYNTHESIZED[7] = S[2] & S[1] & S[0];

assign	NS_0 =  ~S[0];

assign	NS_1 =  ~S[1];

assign	NS_2 =  ~S[2];

assign	EXIBE_F = NS_2 & NS_1;

assign	D = D_ALTERA_SYNTHESIZED;

endmodule
