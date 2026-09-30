# validar_nativo.py

Retoma as etapas dependentes das ferramentas. Exemplo:

```powershell
python entrega/scripts/validar_nativo.py --quartus C:/intelFPGA_lite/21.1/quartus --icarus-root C:/tools/iverilog
```

Antes de executar verifica quartus_map, quartus_sh, quartus_eda, iverilog e vvp.
Sem eles grava `docs/validacao_nativa_atual.json` como PENDING e falha com seus
caminhos. Não instala ferramentas. Com ferramentas disponíveis exporta os BDF
atuais em ordem hierárquica, testa os 16 HDL recém-exportados, compila o projeto
e simula a netlist mapeada. Depois chama `verificar_entrega.py`.

Registra hashes das fontes e de cada log produzido. O verificador de entrega
rejeita evidências antigas ou divergentes. A flag visual permanece PENDING;
nenhum comando desta sequência inspeciona o desenho ou screenshots.
