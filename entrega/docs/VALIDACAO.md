# Validação efetivamente executada

Data local: 30/09/2026. Quartus Prime Lite 21.1 build 842, EP4CE115F29C7. Icarus Verilog 13.0 UCRT64 portátil, obtido dos pacotes oficiais MSYS2 com hashes conferidos. A execução batch de Questa 2021.2 falhou por licença inválida, código 4; não foi considerada teste aprovado. O usuário autorizou Icarus temporário e o fluxo ModelSim/Questa está preparado.

## Circuitos e interfaces

Os 16 BDF foram gerados com portas/primitivas e hierarquia estrutural, analisados e convertidos pelo Quartus. Os 16 BSF foram gerados pelo Quartus a partir do HDL exportado; suas portas e as portas do HDL coincidiram com `interfaces.json`. O QSF cadastra exclusivamente os 16 BDF. Nenhum HDL comportamental, IP aritmético ou banco histórico substitui os circuitos.

O verificador de grafos conferiu uma fonte por rede consumida, larguras, portas, fontes e ausência de ciclos hierárquicos/combinacionais. A revisão funcional final possui 342 instâncias no grafo, com BUF materializado como dois NOT. A exportação não equivale a simulação: os resultados abaixo vêm da execução do HDL nativamente convertido.

A revisão final inclui o posicionamento corrigido dos conectores dos pinos. Todos os 16 circuitos dessa revisão passaram análise, conversão BDF→Verilog e geração de BSF nativas com zero erros e zero avisos. Os testes e a compilação abaixo usam essa mesma revisão.

## Simulação do HDL exportado dos BDF

| Módulo | Casos executados | Resultado |
|---|---:|---|
| somador_1bit | 8 | Passou |
| sm_para_c2 | 32 | Passou |
| somador_subtrator_6bit | 8192 | Passou |
| c2_para_sm | 64, incluindo −32 fora do domínio | Passou |
| negador_c2_6bit | 64 | Passou |
| modulo2_soma_sub | 1922 pares/sub no domínio −15..15 | Passou |
| comparador_c2_6bit | 4096 | Passou |
| logica_5bit | 1024 | Passou |
| decodificador_operacao | 8 | Passou |
| mux_resultado_8x6 | 512 estímulos independentes | Passou |
| ula_core | 8192 | Passou |
| somador_subtrator_5bit | 2048 | Passou |
| bin_bcd | 32 | Passou |
| bcd_7seg | 16 | Passou |
| display_decimal_2digitos | 64 | Passou |
| ula_de2_115 | 16384 verificações, 8192 entradas únicas | Passou |

Os modelos usam inteiros e tabelas literais de segmentos, sem calcular expectativas a partir das equações do gerador. A integração verifica todos os LEDs, STATUS, espelhamento, polaridade, seis displays nos modos aprovados, apagamento de HEX6/7 e constantes. Inclui ambos os zeros, todos os negativos, ±15, ±30, fronteiras de dezenas e transições em duas ordens de estímulos.

VCDs reais completos e recortes PNG estão em `simulation/waveforms`. Os recortes são lidos dos VCDs observados, não fabricados a partir das expectativas. São evidência funcional; seus tempos de testbench não são atrasos medidos na DE2-115.

## Compilação física

A revisão final completou análise/síntese, fitting, assembly e EDA Netlist Writer com zero erros e 36 avisos na compilação completa. O Fitter informou 100 elementos lógicos, 100 funções combinacionais, 96 pinos, zero registradores, zero memória, zero multiplicadores e zero PLLs. A auditoria não encontrou latch inferido.

O `.sof` final possui SHA-256 `42e9b19a48a38a36f0bc3bc9fcd2d7a49ac828c207be5762bab68065b5e14069`. O arquivo corresponde à compilação original final, não a um protótipo histórico.

As 96 atribuições finais do Fitter foram comparadas automaticamente ao CSV: localização, padrão elétrico e marca de atribuição pelo usuário coincidiram integralmente. JP6=3,3 V e JP7=2,5 V são o perfil de referência; a conferência dos jumpers reais permanece física.

O TimeQuest executou `report_path` nativo e produziu vinte caminhos entre entradas e saídas, modelo Slow 1200mV 85C. O maior atraso reportado foi 23,788 ns, de SW[5] a HEX0[1], com onze níveis lógicos. É uma estimativa do modelo do FPGA, sem orçamento de aprovação definido e sem medição física. Consulte `output_files/caminhos_entrada_saida.rpt`.

## Netlist funcional do Quartus

O EDA Netlist Writer exportou a netlist funcional mapeada para Cyclone IV E com zero erros e zero avisos. Essa netlist, juntamente com a biblioteca oficial `cycloneive_atoms.v`, passou no Icarus pelas mesmas 16.384 verificações do circuito principal, cobrindo 8.192 entradas únicas. A waveform real está em `simulation/waveforms/ula_de2_115_netlist.vcd`.

O comando legado de geração para o simulador interno foi rejeitado por incompatibilidade com Cyclone IV E; seu log foi preservado em `netlist_map.log`. O fluxo aprovado usa `quartus_eda`. A biblioteca nativa apresentou avisos de coerção de portas oe/devoe pelo Icarus, preservados em `netlist_compile.log`. Isso não constitui suporte oficial de Icarus pelo Quartus nem simulação temporal com SDF.

## Portabilidade

O ZIP candidato foi extraído em `tmp/recompilacao_candidato/entrega`, sem bancos do projeto. As fontes foram recompiladas nessa pasta por `scripts/compilar.ps1`: zero erros, 36 avisos. A pinagem e os recursos foram auditados novamente. A comparação SHA-256 das fontes identifica a correspondência com a entrega. O registro do pacote final deve ser consultado em `docs/PACOTE_VALIDADO.md`; ele distingue o pacote fechado do candidato.

## Avisos e limites

As constantes de LEDs não usados e HEX6/7 são intencionais. Os segmentos constantes das dezenas de A/B são coerentes com a faixa 00..15. Os 36 avisos foram preservados. A classificação e os valores constantes estão em `docs/AVISOS_COMPILACAO.md`, sem supressão.

O Fitter usa drive strength e slew rate padrão; o aviso 15714 refere-se a esses parâmetros não explicitados, não a ausência de localização ou padrão de I/O. O enunciado não fixa orçamento temporal. Não foram inventados clock ou SDC para remover avisos; TimeQuest registra ausência de clock/SDC e não há fechamento temporal contra requisito definido.

Aviso de LogicLock: recurso de licença de assinatura não usado nesta implementação. A licença de síntese Lite e a execução de Icarus são distintas da licença Questa que falhou.

Avisos legais Intel/Altera dos símbolos/primitivas/HDL foram preservados. Arquivos autorais não contêm comentários didáticos, TODO ou docstrings; os cabeçalhos legais gerados constituem exceção documentada à ausência literal de comentários. Não se declara remoção dos avisos cuja preservação é necessária.

## Índice das evidências

`docs/logs/*_analyze.log`, `*_convert.log` e `*_symbol.log` registram o fluxo nativo dos módulos. `sim_*.log` e `sim_suite.log` registram os testes executados. `compile_final.log` registra a compilação final original; `recompile_zip.log` registra a recompilação do candidato. `netlist_eda.log`, `netlist_compile.log` e `netlist_sim.log` registram a netlist funcional adicional. `caminhos_sta.log` registra a análise de caminhos. Os relatórios nativos `.map.rpt`, `.fit.rpt`, `.asm.rpt`, `.sta.rpt`, `.flow.rpt`, suas sínteses e a `.pin` estão em `output_files`.

`verificacao_final.json` audita fontes, símbolos, pinos e ausência de recursos de estado. `auditoria_fontes.json` registra cobertura documental, política de comentários e comparação das fontes extraídas. `manifest.json` contém hashes dos arquivos empacotados.

## Pendências reais

Relatório DOCX em preparação; renderizador visual ausente no runtime Windows, alternativa proposta ao usuário. A conferência visual do DOCX ainda não foi feita. Capa sem identificação real por escolha do usuário, que preencherá os dados.

Operação 010 continua provisória, sem confirmação do professor. Conferência visual da interface Quartus e teste físico não foram feitos pelo agente e serão feitos pelo usuário.
