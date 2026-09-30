module tb_decodificador_operacao;
logic [2:0] S;
wire [7:0] D;
wire EXIBE_F;
logic [7:0] expected_d;
integer si, tested;
decodificador_operacao dut(.S(S), .D(D), .EXIBE_F(EXIBE_F));
initial begin
    $dumpfile("waveforms/decodificador_operacao.vcd");
    $dumpvars(0, tb_decodificador_operacao);
    tested = 0;
    for (si = 0; si < 8; si = si + 1) begin
        S = si[2:0];
        expected_d = 8'b1 << si;
        #1;
        if (D !== expected_d || EXIBE_F !== (si < 2))
            $fatal(1, "S=%b D=%b expected=%b EXIBE_F=%b expected=%b", S, D, expected_d, EXIBE_F, (si < 2));
        tested = tested + 1;
    end
    $display("PASS decodificador_operacao: %0d seletores", tested);
    $finish;
end
endmodule
