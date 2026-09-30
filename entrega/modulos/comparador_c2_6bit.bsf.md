# comparador_c2_6bit.bsf

O BSF é o símbolo gráfico da entidade `comparador_c2_6bit`; não contém a lógica do comparador. A interface tem entradas de seis bits `A_C2[5..0]` e `B_C2[5..0]`, e saídas escalares `EQ`, `GT` e `LT`.

Exemplo: para A=−32 e B=−31, o bloco implementado no BDF afirma apenas `LT`.

Verificação: Quartus gerou o BSF a partir da entidade convertida sem erros ou avisos. Seus cinco nomes, direções e larguras coincidem com `config/interfaces.json`. A lógica e os 4096 casos funcionais foram verificados pela simulação do HDL exportado do BDF.
