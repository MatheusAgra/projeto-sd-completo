module tb_logica_5bit;
logic [4:0] A_SM, B_SM;
wire [5:0] AND6, XOR6;
logic [4:0] ref_and, ref_xor;
logic [5:0] expected_and, expected_xor;
integer ai, bi, tested;
logica_5bit dut(.A_SM(A_SM), .B_SM(B_SM), .AND6(AND6), .XOR6(XOR6));
initial begin
    $dumpfile("waveforms/logica_5bit.vcd");
    $dumpvars(0, tb_logica_5bit);
    tested = 0;
    for (ai = 0; ai < 32; ai = ai + 1) begin
        for (bi = 0; bi < 32; bi = bi + 1) begin
            A_SM = ai[4:0];
            B_SM = bi[4:0];
            #1;
            ref_and = A_SM & B_SM;
            ref_xor = A_SM ^ B_SM;
            expected_and = {ref_and[4], 1'b0, ref_and[3:0]};
            expected_xor = {ref_xor[4], 1'b0, ref_xor[3:0]};
            if (AND6 !== expected_and || XOR6 !== expected_xor)
                $fatal(1, "A=%b B=%b AND6=%b expected=%b XOR6=%b expected=%b", A_SM, B_SM, AND6, expected_and, XOR6, expected_xor);
            tested = tested + 1;
        end
    end
    $display("PASS logica_5bit: %0d pares", tested);
    $finish;
end
endmodule
