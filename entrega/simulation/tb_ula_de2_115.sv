`timescale 1ns/1ps
module tb_ula_de2_115;
reg [12:0] SW;
wire [17:0] LEDR;
wire [8:0] LEDG;
wire [6:0] HEX0,HEX1,HEX2,HEX3,HEX4,HEX5,HEX6,HEX7;
integer a,b,s,av,bv,logical_value,mag,checks,pass;
reg [5:0] expected;
reg expected_status;
ula_de2_115 dut(.SW(SW),.LEDR(LEDR),.LEDG(LEDG),.HEX0(HEX0),.HEX1(HEX1),.HEX2(HEX2),.HEX3(HEX3),.HEX4(HEX4),.HEX5(HEX5),.HEX6(HEX6),.HEX7(HEX7));
function integer sm_value(input integer raw);
begin sm_value=(raw&16) ? -(raw&15) : (raw&15); end
endfunction
function [5:0] sm6(input integer value);
begin sm6=(value<0) ? (32 | -value) : value; end
endfunction
function [6:0] seg(input integer digit);
begin
    case(digit)
        0:seg=7'b1000000;
        1:seg=7'b1111001;
        2:seg=7'b0100100;
        3:seg=7'b0110000;
        4:seg=7'b0011001;
        5:seg=7'b0010010;
        6:seg=7'b0000010;
        7:seg=7'b1111000;
        8:seg=7'b0000000;
        9:seg=7'b0010000;
        default:seg=7'b1111111;
    endcase
end
endfunction
task check_case(input integer aa,input integer bb,input integer ss);
begin
    SW=(ss<<10)|(bb<<5)|aa;
    av=sm_value(aa); bv=sm_value(bb);
    expected=0; expected_status=0;
    case(ss)
        0:expected=sm6(av+bv);
        1:expected=sm6(av-bv);
        2:expected=(-bv)&63;
        3:expected_status=(av==bv);
        4:expected_status=(av>bv);
        5:expected_status=(av<bv);
        6,7:begin
            logical_value=(ss==6) ? (aa&bb) : (aa^bb);
            expected=((logical_value&16)<<1)|(logical_value&15);
        end
    endcase
    mag=expected&31;
    #10;
    if(LEDR!=={5'b0,SW} || LEDG!=={2'b0,expected_status,expected})
        $fatal(1,"top SW=%b LEDR=%b LEDG=%b F esperado=%b STATUS=%b",SW,LEDR,LEDG,expected,expected_status);
    if(HEX5!==seg((aa&15)/10) || HEX4!==seg((aa&15)%10) || HEX3!==seg((bb&15)/10) || HEX2!==seg((bb&15)%10))
        $fatal(1,"displays entradas SW=%b HEX5..2=%b %b %b %b",SW,HEX5,HEX4,HEX3,HEX2);
    if(HEX1!==((ss<2)?seg(mag/10):7'b1111111) || HEX0!==((ss<2)?seg(mag%10):7'b1111111) || HEX6!==7'b1111111 || HEX7!==7'b1111111)
        $fatal(1,"displays saida SW=%b HEX1=%b HEX0=%b HEX6=%b HEX7=%b",SW,HEX1,HEX0,HEX6,HEX7);
    checks=checks+1;
end
endtask
initial begin
    $dumpfile("waveforms/ula_de2_115.vcd");
    $dumpvars(1,tb_ula_de2_115);
    checks=0;
    for(a=0;a<32;a=a+1)
        for(b=0;b<32;b=b+1)
            for(s=0;s<8;s=s+1) check_case(a,b,s);
    if(checks!=8192) $fatal(1,"cobertura top inicial %0d",checks);
    for(s=7;s>=0;s=s-1)
        for(a=31;a>=0;a=a-1)
            for(b=31;b>=0;b=b-1) check_case(a,b,s);
    if(checks!=16384) $fatal(1,"cobertura top transicoes %0d",checks);
    $display("tb_ula_de2_115 PASS checks=%0d unique=8192",checks);
    $finish;
end
endmodule
