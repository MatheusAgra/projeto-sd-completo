module tb_modulo2_soma_sub;
reg [5:0] A_C2;
reg [5:0] B_C2;
reg SUB;
wire [5:0] F_SM;
integer a;
integer b;
integer sub;
integer av;
integer bv;
integer result;
integer checks;
reg [5:0] expected;
modulo2_soma_sub dut(.A_C2(A_C2),.B_C2(B_C2),.SUB(SUB),.F_SM(F_SM));
function integer signed_value;
  input [5:0] bits;
  begin
    signed_value=bits;
    if(bits[5]) signed_value=signed_value-64;
  end
endfunction
function [5:0] encode_sm;
  input integer signed n;
  integer magnitude;
  begin
    magnitude=(n<0) ? -n : n;
    encode_sm=((n<0 && magnitude!=0) ? 32 : 0) | (magnitude & 31);
  end
endfunction
initial begin
  $dumpfile("waveforms/modulo2_soma_sub.vcd");
  $dumpvars(0,tb_modulo2_soma_sub);
  checks=0;
  for(a=-15;a<=15;a=a+1) begin
    for(b=-15;b<=15;b=b+1) begin
      for(sub=0;sub<2;sub=sub+1) begin
        A_C2=a; B_C2=b; SUB=sub; #1;
        av=signed_value(A_C2); bv=signed_value(B_C2);
        result=sub ? av-bv : av+bv;
        expected=encode_sm(result);
        if(F_SM !== expected) $fatal(1,"A=%0d B=%0d SUB=%0d obtido=%b esperado=%b",av,bv,sub,F_SM,expected);
        checks=checks+1;
      end
    end
  end
  if(checks!=1922) $fatal(1,"cobertura incompleta: %0d",checks);
  $display("tb_modulo2_soma_sub PASS checks=%0d",checks);
  $finish;
end
endmodule
