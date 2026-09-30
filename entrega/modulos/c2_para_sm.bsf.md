# c2_para_sm.bsf — documentação do símbolo

## Função do arquivo

O BSF é o símbolo de interface para instâncias hierárquicas da entidade `c2_para_sm`. Ele não contém a lógica; o circuito está no BDF correspondente, definido pelo grafo de portas da entrega. A conversão e conferência de correspondência entre os arquivos são responsabilidade da integração Quartus.

## Portas

R[5:0] é a entrada C2; F_SM[5] é o sinal e F_SM[4:0] é a magnitude.

## Relação com o circuito

Converte um resultado C2 de seis bits em sinal e magnitude de seis bits, normalizando zero. Um caminho calcula ABS=~R+1 por seis inversores e seis somadores completos com carry inicial 1. Um mux por portas AND/OR escolhe R[4:0] quando R5=0 e ABS[4:0] quando R5=1. O sinal é R5 AND OR(R4..R0). Assim, zero sempre sai 000000.

## Exemplo e limites

R=111110 representa −2 e sai F_SM=100010. R=000000 sai 000000. R=100000 (−32) produz 000000 pela truncagem da magnitude aos cinco bits e supressão do sinal quando os cinco bits baixos de R são zero. O domínio contratual é −31..+31. −32 não pode ser representado em sinal e magnitude de seis bits, permanece explicitamente fora do domínio e o comportamento de porta efetivo para esse padrão é 000000. Todos os 64 padrões são testados para caracterizar esse limite, sem alegar que −32 foi convertido corretamente.

## Dependências e verificação

O BSF expõe a interface gráfica da entidade, sem implementar lógica. O Quartus Prime Lite 21.1.0 gerou o símbolo correspondente após a análise e conversão do BDF, com zero erros e zero avisos; consulte o [log de geração do símbolo](../docs/logs/c2_para_sm_symbol.log). A execução do testbench valida o HDL exportado do BDF, não o desenho do BSF em isolamento: PASS — 64 casos. O resultado está em [sim_c2_para_sm.log](../docs/logs/sim_c2_para_sm.log), e o VCD correspondente em [c2_para_sm.vcd](../simulation/waveforms/c2_para_sm.vcd). As portas do símbolo continuam sujeitas à conferência da interface declarada no contrato.
