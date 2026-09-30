module tb_bcd_7seg;
    logic [3:0] BCD;
    wire [6:0] SEG;
    integer value;

    bcd_7seg dut (.BCD(BCD), .SEG(SEG));

    function automatic [6:0] expected_segments(input logic [3:0] digit);
        case (digit)
            4'd0: expected_segments = 7'b1000000;
            4'd1: expected_segments = 7'b1111001;
            4'd2: expected_segments = 7'b0100100;
            4'd3: expected_segments = 7'b0110000;
            4'd4: expected_segments = 7'b0011001;
            4'd5: expected_segments = 7'b0010010;
            4'd6: expected_segments = 7'b0000010;
            4'd7: expected_segments = 7'b1111000;
            4'd8: expected_segments = 7'b0000000;
            4'd9: expected_segments = 7'b0010000;
            default: expected_segments = 7'b1111111;
        endcase
    endfunction

    initial begin
        $dumpfile("waveforms/bcd_7seg.vcd");
        $dumpvars(0, tb_bcd_7seg);
        for (value = 0; value < 16; value = value + 1) begin
            BCD = value[3:0];
            #1;
            if (SEG !== expected_segments(BCD))
                $fatal(1, "bcd_7seg BCD=%0d SEG=%07b", value, SEG);
        end
        $display("tb_bcd_7seg passou em 16 vetores");
        $finish;
    end
endmodule
