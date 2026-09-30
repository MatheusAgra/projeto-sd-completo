# preparar.py

Gera os BDF reais, analisa cada arquivo no Quartus, exporta Verilog, gera o BSF nativo e confere as portas do BSF/HDL contra o contrato. Retira fontes Verilog intermediárias da pasta de síntese; auxiliares ficam em simulation/generated e não entram no QSF. Mantém logs individuais. Exemplo: python scripts/preparar.py; --modules permite refazer blocos específicos. --root e --quartus ajustam caminhos. As 16 análises/conversões/símbolos passaram. Comentários não legais são removidos, preservando avisos de copyright/licença.
