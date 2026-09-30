# Operação 010: leitura provisória e alternativas

O enunciado chama 010 de complemento a dois de B e também exige F em sinal e magnitude. Essas afirmações não fixam uma única leitura. O professor ainda não resolveu a semântica. Conforme a decisão do usuário, esta revisão interpreta B numericamente, nega esse valor e mostra o padrão C2 de seis bits: +3→111101, −3→000011, +15→110001, −15→001111 e ambos os zeros→000000.

Representar B em C2 é outra operação: +3→000011 e −3→111101. Ela somente troca a codificação SM por C2, sem negar o valor. Complementar diretamente os cinco bits SM também não implementa a decisão: 10011 é SM de −3 e não um inteiro C2 de cinco bits.

## Caminho entregue

Em `modulos/ula_core.bdf`, `conv_b` recebe B em SM e fornece BC2. `negacao_b`, entidade `negador_c2_6bit`, recebe BC2 em `B_C2` e fornece NEG. A instância `selecao`, entidade `mux_resultado_8x6`, recebe NEG em sua porta C2, candidato selecionado por D[2]. Seu F vai aos seis LEDs F do topo. Os displays de F permanecem apagados, pois EXIBE_F só responde em 000/001.

## Procedimento para mostrar a negação em sinal e magnitude

1. Em `scripts/integrar.py`, acrescente ao grafo de `ula_core` a instância `instance('c2_para_sm', 'negacao_em_sm', R='NEG[5..0]', F_SM='NEG_SM[5..0]')`.
2. Na instância `selecao` do mesmo script, troque somente `C2='NEG[5..0]'` por `C2='NEG_SM[5..0]'`. Mantenha `negacao_b`: o valor continua negado.
3. Execute `python scripts/integrar.py` na raiz da entrega para regenerar `config/grafos/ula_core.json` e QPF/QSF; depois `python scripts/preparar.py` para regenerar BDF, converter pelo Quartus e conferir/regenerar BSF.
4. Em `simulation/tb_ula_core.sv`, troque a expectativa do caso 2 de `(-bv)&63` para `sm6(-bv)`. Em `simulation/tb_ula_de2_115.sv`, faça a mesma troca no caso 2. A saída para +3 passa a 100011; −3 continua 000011. Não altere os testes isolados do negador, pois sua função continua C2 modular.
5. Atualize os documentos `ula_core.bdf.md`, `ula_core.bsf.md`, `ula_de2_115.bdf.md`, `config/grafos/ula_core.json.md`, ambos os `.sv.md`, `interfaces.json.md`, `VISAO_GERAL.md`, `DECISOES_E_PENDENCIAS.md`, este documento e o relatório. As larguras e portas externas ficam iguais; o BSF do core e do topo deve ser regenerado e conferido, mas sua interface não muda. O BSF de c2_para_sm é reutilizado; sua implementação não muda.
6. Execute todos os testes por `scripts/simular.ps1`, incluindo as 8192 entradas únicas do core/topo; compile por `scripts/compilar.ps1`; confira pinagem, ausência de estado, `.sof`, hashes e documentos; gere novo ZIP, extraia em outra pasta e recompile. Substitua os VCD/recortes de simulação e o relatório pelos produzidos nessa revisão.

Nenhuma troca na habilitação de displays é necessária: F continua apagado em 010. QSF não recebe o HDL exportado como fonte. A nova instância é um conversor BDF real, não uma mudança exclusiva na expectativa do teste.

## Para somente representar B em C2

Trocar a conexão C2 do mux de NEG para BC2 implementaria a representação de B, sem negação. Essa não é a hipótese entregue nem a variante SM acima. Os testes e documentos precisam mudar semanticamente nesse caso; por exemplo +3 passaria a 000011. Toda variante exige regeneração e nova validação do circuito efetivo.
