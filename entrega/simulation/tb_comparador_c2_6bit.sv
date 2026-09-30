module tb_comparador_c2_6bit;
logic [5:0] A_C2, B_C2;
wire EQ, GT, LT;
integer ai, bi, av, bv, tested;
function automatic integer signed_value(input logic [5:0] value);
    begin
        if (value[5]) signed_value = -((~value + 6'd1) & 6'h3f);
        else signed_value = value;
    end
endfunction
comparador_c2_6bit dut(.A_C2(A_C2), .B_C2(B_C2), .EQ(EQ), .GT(GT), .LT(LT));
initial begin
    $dumpfile("waveforms/comparador_c2_6bit.vcd");
    $dumpvars(0, tb_comparador_c2_6bit);
    tested = 0;
    for (ai = 0; ai < 64; ai = ai + 1) begin
        for (bi = 0; bi < 64; bi = bi + 1) begin
            A_C2 = ai[5:0];
            B_C2 = bi[5:0];
            #1;
            av = signed_value(A_C2);
            bv = signed_value(B_C2);
            if (EQ !== (av == bv) || GT !== (av > bv) || LT !== (av < bv))
                $fatal(1, "A=%b (%0d) B=%b (%0d) EQ/GT/LT=%b%b%b", A_C2, av, B_C2, bv, EQ, GT, LT);
            tested = tested + 1;
        end
    end
    $display("PASS comparador_c2_6bit: %0d pares signed C2", tested);
    $finish;
end
endmodule
