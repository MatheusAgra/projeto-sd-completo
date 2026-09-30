module tb_mux_resultado_8x6;
logic [5:0] C0, C1, C2, C3, C4, C5, C6, C7;
logic [7:0] D;
wire [5:0] F;
integer si, value, tested;
mux_resultado_8x6 dut(.C0(C0), .C1(C1), .C2(C2), .C3(C3), .C4(C4), .C5(C5), .C6(C6), .C7(C7), .D(D), .F(F));
initial begin
    $dumpfile("waveforms/mux_resultado_8x6.vcd");
    $dumpvars(0, tb_mux_resultado_8x6);
    tested = 0;
    C0 = 0; C1 = 0; C2 = 0; C3 = 0; C4 = 0; C5 = 0; C6 = 0; C7 = 0;
    for (si = 0; si < 8; si = si + 1) begin
        D = 8'b1 << si;
        for (value = 0; value < 64; value = value + 1) begin
            C0 = 0; C1 = 0; C2 = 0; C3 = 0; C4 = 0; C5 = 0; C6 = 0; C7 = 0;
            case (si)
                0: C0 = value[5:0];
                1: C1 = value[5:0];
                2: C2 = value[5:0];
                3: C3 = value[5:0];
                4: C4 = value[5:0];
                5: C5 = value[5:0];
                6: C6 = value[5:0];
                7: C7 = value[5:0];
            endcase
            #1;
            if (F !== value[5:0])
                $fatal(1, "D=%b candidato C%0d=%02h F=%02h expected=%02h", D, si, value[5:0], F, value[5:0]);
            tested = tested + 1;
        end
    end
    $display("PASS mux_resultado_8x6: %0d estímulos um-hot", tested);
    $finish;
end
endmodule
