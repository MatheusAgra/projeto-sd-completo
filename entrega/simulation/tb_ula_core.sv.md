# tb_ula_core.sv

Testa o core efetivamente exportado dos BDF: 32 padrões de A × 32 de B × 8 operações = 8192 casos. O modelo interpreta SM por inteiros, calcula soma/subtração/negação e comparações numéricas, e só então codifica o esperado. AND/XOR usam os bits brutos e o alinhamento aprovado.

O caso 010 espera `(-B_numérico)&63`, provisoriamente; ambos os zeros numéricos tornam-se zero. Soma/subtração normalizam zero; lógica preserva o sinal bruto. Compara F, STATUS e EXIBE_F após 10 ns funcionais. Este intervalo não é orçamento de atraso físico.

Exemplo coberto: A=+15, B=−15, S=001 produz +30. O VCD real é escrito somente pela execução do simulador. Consulte `docs/VALIDACAO.md` para resultados efetivamente executados.
