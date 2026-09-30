module tb_bin_bcd;
    logic [4:0] MAG;
    wire [3:0] DEZ;
    wire [3:0] UNI;
    integer value;

    bin_bcd dut (.MAG(MAG), .DEZ(DEZ), .UNI(UNI));

    initial begin
        $dumpfile("waveforms/bin_bcd.vcd");
        $dumpvars(0, tb_bin_bcd);
        for (value = 0; value < 32; value = value + 1) begin
            MAG = value[4:0];
            #1;
            if (DEZ !== (value / 10) || UNI !== (value % 10))
                $fatal(1, "bin_bcd MAG=%0d DEZ=%0d UNI=%0d", value, DEZ, UNI);
        end
        $display("tb_bin_bcd passou em 32 vetores");
        $finish;
    end
endmodule
