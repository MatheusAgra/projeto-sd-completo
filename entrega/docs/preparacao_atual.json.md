# preparacao_atual.json

Proveniência por módulo, escrita pelo fluxo de geração/exportação. Contém hash
do BDF atual e estado da análise/exportação nativa. O hash do Verilog só aparece
após nova exportação bem-sucedida. `--generate-only` mantém native=PENDING.
HDL antigo em simulation/generated não pode ser usado como prova de função
dos BDF novos. `verificar_entrega.py` confere a proveniência antes de aprovar.
