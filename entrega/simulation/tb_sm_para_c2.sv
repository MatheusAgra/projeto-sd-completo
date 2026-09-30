module tb_sm_para_c2;
reg [4:0] SM;
wire [5:0] C2;
integer raw;
integer value;
integer magnitude_input;
integer checks;
reg [5:0] expected;
sm_para_c2 dut(.SM(SM),.C2(C2));
initial begin
  $dumpfile("waveforms/sm_para_c2.vcd");
  $dumpvars(0,tb_sm_para_c2);
  checks=0;
  for(raw=0;raw<32;raw=raw+1) begin
    SM=raw; #1;
    magnitude_input=SM[3:0];
    value=SM[4] ? -magnitude_input : magnitude_input;
    expected=value;
    if(C2 !== expected) $fatal(1,"SM=%b obtido=%b esperado=%b valor=%0d",SM,C2,expected,value);
    checks=checks+1;
  end
  if(checks!=32) $fatal(1,"cobertura incompleta: %0d",checks);
  $display("tb_sm_para_c2 PASS checks=%0d",checks);
  $finish;
end
endmodule
