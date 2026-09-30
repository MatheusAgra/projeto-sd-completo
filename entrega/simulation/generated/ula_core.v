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


module ula_core(
	A,
	B,
	S,
	STATUS,
	EXIBE_F,
	F
);


input wire	[4:0] A;
input wire	[4:0] B;
input wire	[2:0] S;
output wire	STATUS;
output wire	EXIBE_F;
output wire	[5:0] F;

wire	[5:0] AC2;
wire	[5:0] ARIT;
wire	[5:0] BC2;
wire	[7:0] D;
wire	EQ;
wire	EQS;
wire	[5:0] F_ALTERA_SYNTHESIZED;
wire	GT;
wire	GTS;
wire	[5:0] LAND;
wire	LT;
wire	LTS;
wire	[5:0] LXOR;
wire	[5:0] NEG;
wire	[5:0] ZERO;





modulo2_soma_sub	b2v_aritmetica(
	.SUB(S[0]),
	.A_C2(AC2),
	.B_C2(BC2),
	.F_SM(ARIT));


comparador_c2_6bit	b2v_comparacao(
	.A_C2(AC2),
	.B_C2(BC2),
	.EQ(EQ),
	.GT(GT),
	.LT(LT));


decodificador_operacao	b2v_controle(
	.S(S),
	.EXIBE_F(EXIBE_F),
	.D(D));


sm_para_c2	b2v_conv_a(
	.SM(A),
	.C2(AC2));


sm_para_c2	b2v_conv_b(
	.SM(B),
	.C2(BC2));


logica_5bit	b2v_logica(
	.A_SM(A),
	.B_SM(B),
	.AND6(LAND),
	.XOR6(LXOR));


negador_c2_6bit	b2v_negacao_b(
	.B_C2(BC2),
	.NEG(NEG));


mux_resultado_8x6	b2v_selecao(
	.C0(ARIT),
	.C1(ARIT),
	.C2(NEG),
	.C3(ZERO),
	.C4(ZERO),
	.C5(ZERO),
	.C6(LAND),
	.C7(LXOR),
	.D(D),
	.F(F_ALTERA_SYNTHESIZED));

assign	EQS = D[3] & EQ;

assign	STATUS = GTS | LTS | EQS;

assign	GTS = D[4] & GT;

assign	LTS = D[5] & LT;







assign	F = F_ALTERA_SYNTHESIZED;
assign	ZERO[0] = 0;
assign	ZERO[1] = 0;
assign	ZERO[2] = 0;
assign	ZERO[3] = 0;
assign	ZERO[4] = 0;
assign	ZERO[5] = 0;

endmodule
