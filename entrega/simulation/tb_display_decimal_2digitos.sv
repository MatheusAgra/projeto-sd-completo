module tb_display_decimal_2digitos;
    logic [4:0] MAG;
    logic ENABLE;
    wire [6:0] DEZ_SEG;
    wire [6:0] UNI_SEG;
    integer value;
    integer enable_value;
    reg [6:0] expected_dez;
    reg [6:0] expected_uni;

    display_decimal_2digitos dut (.MAG(MAG), .ENABLE(ENABLE), .DEZ_SEG(DEZ_SEG), .UNI_SEG(UNI_SEG));

    function automatic [6:0] expected_segments(input integer digit);
        case (digit)
            0: expected_segments = 7'b1000000;
            1: expected_segments = 7'b1111001;
            2: expected_segments = 7'b0100100;
            3: expected_segments = 7'b0110000;
            4: expected_segments = 7'b0011001;
            5: expected_segments = 7'b0010010;
            6: expected_segments = 7'b0000010;
            7: expected_segments = 7'b1111000;
            8: expected_segments = 7'b0000000;
            9: expected_segments = 7'b0010000;
            default: expected_segments = 7'b1111111;
        endcase
    endfunction

    initial begin
        $dumpfile("waveforms/display_decimal_2digitos.vcd");
        $dumpvars(0, tb_display_decimal_2digitos);
        for (enable_value = 0; enable_value < 2; enable_value = enable_value + 1) begin
            ENABLE = enable_value[0];
            for (value = 0; value < 32; value = value + 1) begin
                MAG = value[4:0];
                expected_dez = ENABLE ? expected_segments(value / 10) : 7'b1111111;
                expected_uni = ENABLE ? expected_segments(value % 10) : 7'b1111111;
                #1;
                if (DEZ_SEG !== expected_dez || UNI_SEG !== expected_uni)
                    $fatal(1, "display MAG=%0d ENABLE=%b DEZ=%07b UNI=%07b", value, ENABLE, DEZ_SEG, UNI_SEG);
            end
        end
        $display("tb_display_decimal_2digitos passou em 64 vetores");
        $finish;
    end
endmodule
