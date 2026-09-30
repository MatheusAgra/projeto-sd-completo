module tb_somador_subtrator_6bit;
reg [5:0] A;
reg [5:0] B;
reg SUB;
wire [5:0] R;
wire Cout;
integer a;
integer b;
integer sub;
integer total;
integer checks;
reg [6:0] expected;
somador_subtrator_6bit dut(.A(A),.B(B),.SUB(SUB),.R(R),.Cout(Cout));
initial begin
  $dumpfile("waveforms/somador_subtrator_6bit.vcd");
  $dumpvars(0,tb_somador_subtrator_6bit);
  checks=0;
  for(a=0;a<64;a=a+1) begin
    for(b=0;b<64;b=b+1) begin
      for(sub=0;sub<2;sub=sub+1) begin
        A=a; B=b; SUB=sub; #1;
        total=a+(b ^ (sub ? 63 : 0))+sub;
        expected=total;
        if({Cout,R} !== expected) $fatal(1,"A=%0d B=%0d SUB=%0d obtido=%b esperado=%b",a,b,sub,{Cout,R},expected);
        checks=checks+1;
      end
    end
  end
  if(checks!=8192) $fatal(1,"cobertura incompleta: %0d",checks);
  $display("tb_somador_subtrator_6bit PASS checks=%0d",checks);
  $finish;
end
endmodule
