# mux_resultado_8x6.bsf

O BSF expõe a interface gráfica do multiplexador `mux_resultado_8x6`; não contém lógica de seleção. As entradas C0–C7 têm seis bits cada, D tem oito bits e F tem seis bits.

Exemplo: se D3 for o único bit ativo, o BDF encaminha C3 a F.

Verificação: símbolo gerado pelo Quartus sem erros ou avisos. Os dez nomes, direções e larguras coincidem com `config/interfaces.json`; a seleção foi verificada no HDL convertido do BDF.
