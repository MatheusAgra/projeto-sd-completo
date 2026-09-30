module tb_negador_c2_6bit;
reg [5:0] B_C2;
wire [5:0] NEG;
integer raw;
integer value;
integer checks;
reg [5:0] expected;
negador_c2_6bit dut(.B_C2(B_C2),.NEG(NEG));
initial begin
  $dumpfile("waveforms/negador_c2_6bit.vcd");
  $dumpvars(0,tb_negador_c2_6bit);
  checks=0;
  for(raw=0;raw<64;raw=raw+1) begin
    B_C2=raw; #1;
    value=-raw;
    expected=value;
    if(NEG !== expected) $fatal(1,"B_C2=%b obtido=%b esperado=%b",B_C2,NEG,expected);
    checks=checks+1;
  end
  if(checks!=64) $fatal(1,"cobertura incompleta: %0d",checks);
  $display("tb_negador_c2_6bit PASS checks=%0d",checks);
  $finish;
end
endmodule
