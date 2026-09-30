`timescale 1ns/1ps
module tb_ula_core;
reg [4:0] A, B;
reg [2:0] S;
wire [5:0] F;
wire STATUS, EXIBE_F;
integer a, b, s, av, bv, result, logical_value, checks;
reg [5:0] expected;
reg expected_status;
ula_core dut(.A(A),.B(B),.S(S),.F(F),.STATUS(STATUS),.EXIBE_F(EXIBE_F));
function integer sm_value(input integer raw);
begin sm_value=(raw&16) ? -(raw&15) : (raw&15); end
endfunction
function [5:0] sm6(input integer value);
begin sm6=(value<0) ? (32 | -value) : value; end
endfunction
initial begin
    $dumpfile("waveforms/ula_core.vcd");
    $dumpvars(1,tb_ula_core);
    checks=0;
    for(a=0;a<32;a=a+1) begin
        for(b=0;b<32;b=b+1) begin
            for(s=0;s<8;s=s+1) begin
                A=a; B=b; S=s;
                av=sm_value(a); bv=sm_value(b);
                expected=0; expected_status=0;
                case(s)
                    0: expected=sm6(av+bv);
                    1: expected=sm6(av-bv);
                    2: expected=(-bv)&63;
                    3: expected_status=(av==bv);
                    4: expected_status=(av>bv);
                    5: expected_status=(av<bv);
                    6,7: begin
                        logical_value=(s==6) ? (a&b) : (a^b);
                        expected=((logical_value&16)<<1)|(logical_value&15);
                    end
                endcase
                #10;
                if(F!==expected || STATUS!==expected_status || EXIBE_F!==(s<2))
                    $fatal(1,"core A=%b B=%b S=%b F=%b esperado=%b STATUS=%b esperado=%b EXIBE_F=%b",A,B,S,F,expected,STATUS,expected_status,EXIBE_F);
                checks=checks+1;
            end
        end
    end
    if(checks!=8192) $fatal(1,"cobertura core %0d",checks);
    $display("tb_ula_core PASS checks=%0d",checks);
    $finish;
end
endmodule
