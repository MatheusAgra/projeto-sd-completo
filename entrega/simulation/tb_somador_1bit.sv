module tb_somador_1bit;
reg A;
reg B;
reg Cin;
wire S;
wire Cout;
integer a;
integer b;
integer c;
integer total;
integer checks;
somador_1bit dut(.A(A),.B(B),.Cin(Cin),.S(S),.Cout(Cout));
initial begin
  $dumpfile("waveforms/somador_1bit.vcd");
  $dumpvars(0,tb_somador_1bit);
  checks=0;
  for(a=0;a<2;a=a+1) begin
    for(b=0;b<2;b=b+1) begin
      for(c=0;c<2;c=c+1) begin
        A=a; B=b; Cin=c; #1;
        total=a+b+c;
        if ({Cout,S} !== total[1:0]) $fatal(1,"somador_1bit A=%0d B=%0d Cin=%0d obtido=%b esperado=%b",a,b,c,{Cout,S},total[1:0]);
        checks=checks+1;
      end
    end
  end
  if(checks!=8) $fatal(1,"cobertura incompleta: %0d",checks);
  $display("tb_somador_1bit PASS checks=%0d",checks);
  $finish;
end
endmodule
