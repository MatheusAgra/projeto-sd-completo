module tb_c2_para_sm;
reg [5:0] R;
wire [5:0] F_SM;
integer raw;
integer value;
integer magnitude;
integer checks;
reg [5:0] expected;
c2_para_sm dut(.R(R),.F_SM(F_SM));
initial begin
  $dumpfile("waveforms/c2_para_sm.vcd");
  $dumpvars(0,tb_c2_para_sm);
  checks=0;
  for(raw=0;raw<64;raw=raw+1) begin
    R=raw; #1;
    value=R[5] ? raw-64 : raw;
    magnitude=(value<0) ? -value : value;
    expected=((value<0 && (magnitude & 31)!=0) ? 32 : 0) | (magnitude & 31);
    if(F_SM !== expected) $fatal(1,"R=%b valor=%0d obtido=%b esperado=%b",R,value,F_SM,expected);
    checks=checks+1;
  end
  if(checks!=64) $fatal(1,"cobertura incompleta: %0d",checks);
  $display("tb_c2_para_sm PASS checks=%0d incluindo -32 fora do domínio",checks);
  $finish;
end
endmodule
