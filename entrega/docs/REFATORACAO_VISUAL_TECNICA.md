# Refatoração visual: implementação e verificações técnicas

Data local: 30/09/2026. Baseline Git: `ecfe0a4c1cb46b7ccc57f0a5f031f5bde0094e72`.

**Estado: implementação e checks offline concluídos nos 16 módulos; validação nativa e conferência visual pendentes.** O usuário orientou continuar somente onde Quartus/Icarus não são necessários enquanto instala as ferramentas. Não se declara aprovação técnica integral nem legibilidade aprovada.

## Alterações implementadas

Os 16 BDF e 16 BSF de `modulos/` foram regenerados. Fios escalares, fan-out, constantes, carry, barramentos e slices têm trajetos por contato físico no modelo geométrico auditado. No somador de um bit, os próprios XOR, AND e OR estão ligados por conectores reais. Somadores de cinco/seis bits conservam etapas e suas ligações Cout–Cin. Nenhum HDL comportamental substituiu BDF e a hierarquia foi preservada.

`config/layouts/` contém os 16 layouts independentes e sua documentação. `config/LAYOUTS.md` define o contrato. A reserva de corredores por terminal e troncos por rede é determinística e usa grade 8. Os rótulos identificam redes/taps; o validador não une componentes remotos por nomes iguais. Folhas extensas e cruzamentos internos permanecem sujeitos à revisão posterior. A maior extensão calculada nos candidatos foi 12008×6848 no mux; o topo ocupa 10392×10560 unidades. Nenhuma imagem foi inspecionada.

Os BSF canônicos usam a mesma definição de portas/geometria dos símbolos embutidos nos BDF. `preparar.py` exporta símbolos nativos somente para conferência em `simulation/generated/native_symbols/`, sem substituir os símbolos entregues. `config/primitivas/` preserva 13 símbolos extraídos dos BDF anteriores, com avisos legais; assim a geração e validação estrutural dispensam a instalação Quartus. O aviso Intel dos BSF também foi preservado.

Scripts compartilhados alterados: `gerar_bdf.py`, `preparar.py`, `integrar.py`, `documentar_apoio.py`, `verificar_entrega.py`, `simular.ps1`, `simular_netlist.ps1` e `auditar_fontes.py`. Novos: `layout_bdf.py`, `validar_geometria.py`, `test_validar_geometria.py`, `validar_refatoracao.py`, `validar_nativo.py`. Cada fonte tem documento correspondente. Os escritores de arquivos adotam LF explícito para preservar a reprodução byte a byte no Windows. O fluxo de simulação/entrega exige hashes de proveniência atual, impedindo a aprovação com HDL/logs/netlist históricos.

## Evidências efetivamente executadas

- Três frentes de metadados cobriram 7+4+5 módulos. Uma rodada independente implementou o auditor; o coordenador revisou e integrou as entregas, gerou os arquivos definitivos e repetiu os checks.
- Pilotos em ordem: somador_1bit, somador_subtrator_5bit e modulo2_soma_sub. Continuidade: 12/12, 31/31 e 25/25 destinos por bit, respectivamente. Exportação/testes nativos desses pilotos NÃO executados.
- Auditoria dos BDF finais: **16/16 PASS, 1020/1020 destinos por bit alcançados**, sem desconexões, curtos, erros de largura/contrato/labels/driver ou colisões detectadas nas verificações implementadas. Geometria dos terminais confrontada com os BSF e contratos. Cruzamentos interiores sem junction são registrados, sem união elétrica no modelo; sua interpretação nativa segue pendente.
- **26 testes de mutação PASS**: fan-out real, SW[12..0]→SW[9..5], montagem escalar em bus, gap de uma unidade, mesmo nome remoto, bit/ordem/faixa/largura errados, curtos escalares e bus-bus, sobreposição colinear, taps inválidos, portas deslocadas, duplicatas, tipo/direção/formal hierárquicos e colisões de fios/labels.
- Validador lógico: 16 módulos, 342 instâncias no grafo, PASS. BUF conserva a expansão em dois NOT; a contagem geométrica aparece por módulo abaixo.
- **36 invariantes byte a byte preservadas**: interfaces, 16 grafos JSON, CSV, QSF, QPF e 16 testbenches. Cadastro exclusivo de 16 BDF e 96 pinos/padrões I/O conferidos no QSF/CSV. Dispositivo, entidades, hierarquia, lógica e mapeamentos permanecem congelados.
- Regeneração determinística: **32/32 BDF/BSF idênticos byte a byte** em uma segunda geração isolada, além da execução de `preparar.py --generate-only` com auditoria dos finais.
- `integrar.py` executado em cópia isolada: core/topo e QSF/QPF idênticos byte a byte; 32 arquivos de layout intactos. A verificação encontrou perda do metadado LAST_QUARTUS_VERSION no fluxo anterior; o script agora o preserva e evita reescritas equivalentes.
- Sintaxe Python e PowerShell conferida. Auditoria de comentários/documentação registrada em `auditoria_fontes.json` após os documentos atuais.
- Três bloqueios de proveniência conferidos: verificação da entrega, simulação HDL e simulação da netlist recusaram o estado pendente antes de invocar as ferramentas. O registro pendente da entrega permaneceu intacto. Evidência em [bloqueios_proveniencia.json](bloqueios_proveniencia.json); esses checks negativos não constituem simulações nativas.

Relatório consolidado e hashes: [refatoracao_tecnica.json](refatoracao_tecnica.json). Testes: [refatoracao_testes_geometria.log](logs/refatoracao_testes_geometria.log). Integração: [integracao_refatoracao.json](integracao_refatoracao.json). Baseline: [refatoracao_baseline.json](refatoracao_baseline.json).

## Cobertura por módulo

| Módulo | Destinos alcançados/previstos | Símbolos BDF | Cruzamentos sem junção | Auditoria offline | Visual |
|---|---:|---:|---:|---|---|
| `somador_1bit` | 12/12 | 5 | 43 | PASS | Pendente |
| `sm_para_c2` | 36/36 | 13 | 305 | PASS | Pendente |
| `somador_subtrator_6bit` | 37/37 | 12 | 414 | PASS | Pendente |
| `c2_para_sm` | 71/71 | 35 | 949 | PASS | Pendente |
| `negador_c2_6bit` | 30/30 | 14 | 290 | PASS | Pendente |
| `modulo2_soma_sub` | 25/25 | 2 | 17 | PASS | Pendente |
| `comparador_c2_6bit` | 73/73 | 32 | 1043 | PASS | Pendente |
| `logica_5bit` | 32/32 | 12 | 215 | PASS | Pendente |
| `decodificador_operacao` | 38/38 | 12 | 203 | PASS | Pendente |
| `mux_resultado_8x6` | 150/150 | 54 | 6275 | PASS | Pendente |
| `ula_core` | 127/127 | 18 | 383 | PASS | Pendente |
| `somador_subtrator_5bit` | 31/31 | 10 | 297 | PASS | Pendente |
| `bin_bcd` | 58/58 | 34 | 872 | PASS | Pendente |
| `bcd_7seg` | 74/74 | 25 | 1176 | PASS | Pendente |
| `display_decimal_2digitos` | 56/56 | 18 | 644 | PASS | Pendente |
| `ula_de2_115` | 170/170 | 84 | 4717 | PASS | Pendente |

Destinos incluem entradas de instâncias e saídas do módulo, por bit; os drivers não são contados como consumidores. Saídas sem consumidor são conservadas do grafo, não exceções para destinos desconectados:

- `sm_para_c2.fa_5.Cout`: `Cout`.
- `c2_para_sm.fa_abs_5.S`: `ABS[5]`.
- `c2_para_sm.fa_abs_5.Cout`: `Cout`.
- `negador_c2_6bit.fa_5.Cout`: `Cout`.
- `modulo2_soma_sub.soma_sub.Cout`: `COUT`.
- `bin_bcd.subtract_tens.R`: `UNI_RAW[4]`.
- `bin_bcd.subtract_tens.Cout`: `COUT_UNUSED`.

Essas sete saídas/bits já eram não consumidos no baseline. Não foram inventados destinos nem feitas simplificações funcionais.

## Modelo e limites da auditoria

Componentes são construídos por contato geométrico, endpoints e junções; bus mantém canais separados por índice. Taps exigem contato físico e mapeamento do bit. Cruzamentos ortogonais estritamente interiores sem junction não unem redes nesse modelo. Labels são conferidos nos componentes e taps, nunca utilizados para juntar componentes remotos. Colisões são calculadas a partir de retângulos/segmentos dos BDF e não constituem uma avaliação visual da fonte/tipografia no editor.

O auditor encontrou e o gerador corrigiu um curto real: prolongar um tronco 24 unidades além do último acesso fazia seu endpoint tocar o canal da rede vizinha. Testes e auditoria foram repetidos após a correção. As fontes finais não usam esse prolongamento.

A interpretação desse formato pelo Quartus e a equivalência funcional executada ainda não foram confirmadas no novo estado. Checks Python sobre contratos/grafos/geometria não substituem análise/exportação nativa ou simulação.

## Pendências por ausência de ferramentas

`validar_nativo.py` verificou os caminhos esperados, gravou [validacao_nativa_atual.json](validacao_nativa_atual.json) como PENDING com `stages` vazio e terminou com FileNotFoundError. O registro está em [refatoracao_ferramentas_ausentes.log](logs/refatoracao_ferramentas_ausentes.log). Ausentes: quartus_map.exe, quartus_sh.exe, quartus_eda.exe sob C:/intelFPGA_lite/21.1/quartus/bin64 e iverilog.exe/vvp.exe no runtime local tmp/tools/iverilog. Não foram instaladas ferramentas pelo agente.

| Etapa | Estado atual |
|---|---|
| Análise/exportação nativa dos 16 BDF e contratos HDL/BSF nativos | Pendente Quartus |
| Semântica nativa de junções, cruzamentos, barramentos e taps | Pendente Quartus |
| 16 testbenches existentes sobre HDL recém-exportado | Pendente Quartus + Icarus |
| Comparação de comportamento coberto com baseline | Pendente simulações novas |
| Compilação completa e pinagem/recursos/avisos do Fitter | Pendente Quartus |
| Netlist funcional recém-gerada e testbench do topo | Pendente Quartus + Icarus |
| Nova emissão de SOF/manifesto/ZIP e portabilidade | Pendente validação nativa; pacote antigo é histórico |
| Conferência visual nos 16 BDF | Pendente, adiada por instrução explícita |
| Placa/jumpers/teste físico | Não executado; fora desta etapa |

Os HDL, netlist, SOF, imagens, DOCX, manifesto, ZIP e resultados de compilação/simulação existentes são históricos. `docs/historico_pre_refatoracao/` preserva os documentos e logs anteriores. Não foram usados como resultado atual. As figuras antigas não representam o novo roteamento e não foram regeneradas ou inspecionadas nesta etapa.

## Retomada reproduzível

Após instalar as duas ferramentas, execute com seus caminhos reais:

```powershell
python entrega/scripts/validar_refatoracao.py
python entrega/scripts/validar_nativo.py --quartus C:/intelFPGA_lite/21.1/quartus --icarus-root C:/tools/iverilog
```

O segundo comando executa checks offline, exportação dos BDF atuais em ordem de dependência, 16 testes do HDL novo, compilação, netlist funcional e verificação de entrega. Mantém logs/hashes atuais e falha ao detectar alteração de fontes ou etapa malsucedida. `preparar.py --export-only` pode exportar sem refazer o layout; `--generate-only` reproduz BDF/BSF sem usar Quartus. Atualizar o relatório e publicar novo pacote somente depois de registrar os resultados reais. Não abrir esquemas para inspeção visual durante essa retomada técnica.

O guia atualizado está em [GUIA_CONFERENCIA_VISUAL_QUARTUS.md](GUIA_CONFERENCIA_VISUAL_QUARTUS.md); os campos de aprovação permanecem em branco e os 16 módulos pendentes. Nenhum screenshot, aprovação de legibilidade ou teste de placa foi realizado nesta sessão.
