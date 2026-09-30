# Plano de execução da ULA no Quartus

Estudo realizado em 30/09/2026. Este documento planeja a implementação; não afirma que a ULA completa já foi construída ou validada. As escolhas de arquitetura e organização abaixo são propostas para execução, com as definições do usuário identificadas separadamente.

## 1. Objetivo e entregáveis

Construir uma ULA combinacional completa, exclusivamente com portas lógicas e blocos estruturais hierárquicos em BDF, integrada a displays e LEDs da DE2-115, para o FPGA EP4CE115F29C7. Entregar o projeto Quartus portátil, os BDF e BSF reais, documentação individual, testes, waveforms, relatório e arquivo de programação resultante da compilação final.

O agente deve criar e conectar os circuitos. Um conjunto de arquivos HDL funcionais acompanhado de um BDF decorativo não atende ao objetivo. BSF descreve a interface gráfica de um bloco; a implementação deve existir no BDF correspondente. O circuito principal deve instanciar e interligar os módulos efetivos.

Não é necessário usar Computer Use para confirmar abertura, aparência ou operação da interface do Quartus. O usuário fará essa conferência depois. A validação automática deve usar os comandos nativos e simulação. Não confundir validação pelo compilador com conferência visual do esquema.

## 2. Materiais estudados e estado atual

Fontes do projeto:

- `Projeto_Primeira_Unidade_2026_2.pdf`, quatro páginas, na raiz. Foram lidos o texto e as imagens, incluindo a tabela das operações e a pinagem.
- [Pasta do Drive fornecida pelo usuário](https://drive.google.com/drive/folders/1oW1BSgOzj0mFPLoNP_ph5wCtc_VbQrTy).
- Subpasta `PROJETO ULA NOVO`, seus arquivos de projeto, módulos e relatórios selecionados. Cópias de estudo estão em `tmp/drive/PROJETO_ULA`; não são a entrega final.
- Manual oficial da DE2-115, disponível em `tmp/pdfs/DE2_115_User_manual.pdf` e no link da seção de referências.

Na raiz local havia apenas o enunciado. No Drive existe um protótipo de soma/subtração:

| Arquivo existente | Papel observado | Providência no plano |
|---|---|---|
| `somador_1bit.bdf` | Somador completo com XOR, AND e OR | Validar oito casos e aproveitar a estrutura se correta |
| `sm_para_c2.bdf` | Entrada SM de cinco bits para C2 de seis bits | Testar todos os 32 padrões, incluindo ambos os zeros |
| `somador_subtrator_6bit.bdf` | Ripple carry de seis bits e inversão condicional de B | Testar soma/subtração e cadeia de carry |
| `c2_para_sm.bdf` | Resultado C2 para sinal e magnitude | Confirmar faixa e tratamento de zero |
| `bin_bcd.bdf` | Magnitude de cinco bits para dois dígitos BCD | Testar os 32 valores; revisar a implementação antes de reutilizar |
| `modulo2_soma_sub.bdf` | Integra somente conversão, soma/subtração e BCD | Separar caminho aritmético do controle geral e dos displays |
| `bcd_7seg.vhd` | Decodificação comportamental por seleção de constantes | Substituir por BDF com equações e portas |
| `PROJETO_ULA.qsf` | Dispositivo correto, topo `modulo2_soma_sub` | Criar configuração final limpa com topo, fontes e pinagem corretos |
| `PROJETO_ULA.qpf` | Projeto criado no Quartus 20.1.1 | Criar projeto final reproduzível, compatível com a versão usada |

Constatações concretas:

- O topo existente recebe A, B e somente S0. Não implementa o seletor completo, comparações, operação 010, AND/XOR, status, displays de A/B ou saídas físicas completas.
- O QSF estudado não contém `set_location_assignment`. Escolher o FPGA não configura os pinos da placa.
- `bcd_7seg.vhd` está listado como fonte, mas não aparece instanciado no topo BDF estudado.
- O QSF referencia `db/PROJETO_ULA.cmp.rdb` como `SOURCE_FILE`. A entrega deve depender das fontes reais, sem necessidade desse banco antigo.
- Existem versões duplicadas em diferentes pastas do Drive, inclusive BDF de tamanhos diferentes. Não combinar versões por nome sem comparar conteúdo e interfaces.
- Os relatórios históricos indicam compilação bem-sucedida do protótipo: 38 elementos lógicos, zero registradores e 25 pinos. Esses relatórios comprovam a compilação daquela revisão, não a correção nem a completude da ULA solicitada.
- Os avisos históricos de `DEZ[3]` e `DEZ[2]` constantes em zero são plausíveis: as dezenas válidas vão de 0 a 3. Cada aviso final deve ser avaliado pelo significado, sem simplesmente exigir ausência de qualquer aviso.

A inspeção estrutural dos conversores e somador não substitui testes funcionais. Nenhum módulo herdado deve ser declarado correto apenas pela leitura.

## 3. Contrato funcional

### 3.1. Formatos numéricos

Entradas: `A[4:0]` e `B[4:0]`, em sinal e magnitude. O bit 4 é o sinal; os bits 3..0 são a magnitude. A faixa numérica é −15 a +15. `00000` e `10000` representam zero nas operações numéricas.

Saída aritmética: `F[5:0]`, com sinal em F5 e magnitude em F4..F0. Soma e subtração produzem valores de −30 a +30. O resultado zero deve ser normalizado para `000000`.

Não aumentar A/B por simples extensão do bit de sinal da codificação SM. Primeiro converter a magnitude e o sinal para C2 de seis bits.

### 3.2. Operações

| S2 S1 S0 | Operação | F nos LEDs | STATUS | Displays de F |
|---|---|---|---|---|
| 000 | A + B | Resultado em SM de seis bits | 0 | Magnitude decimal |
| 001 | A − B | Resultado em SM de seis bits | 0 | Magnitude decimal |
| 010 | Complemento a dois de B | Padrão C2 de seis bits de −B, hipótese adotada | 0 | Apagados |
| 011 | A = B | `000000`, proposta para saída não utilizada | Resultado da comparação | Apagados |
| 100 | A > B | `000000`, proposta para saída não utilizada | Resultado da comparação | Apagados |
| 101 | A < B | `000000`, proposta para saída não utilizada | Resultado da comparação | Apagados |
| 110 | A AND B | Operação sobre os cinco bits brutos, inclusive sinal | 0 | Apagados |
| 111 | A XOR B | Operação sobre os cinco bits brutos, inclusive sinal | 0 | Apagados |

Os displays de A/B continuam mostrando suas magnitudes, de 00 a 15, em todas as operações. A regra de apagamento é aplicada aos displays do resultado. Os sinais de A/B aparecem nos LEDs que replicam as entradas.

### 3.3. Operação 010: decisão provisória e documentação obrigatória

O usuário determinou mostrar um padrão em complemento de dois e apontou como interpretação provável `B=+3 → F=111101`, representando −3. Pediu explicitamente documentar a indecisão. Portanto a hipótese de execução é:

1. Interpretar B numericamente a partir de sinal e magnitude.
2. Converter B para C2 de seis bits.
3. Calcular `(~B_C2 + 1) mod 64` e encaminhar seus seis bits diretamente a F.

Exemplos: +3 → `111101`; −3 → `000011`; +15 → `110001`; −15 → `001111`; qualquer zero → `000000`.

Não complementar diretamente os cinco bits SM brutos. Por exemplo, a entrada SM `10011` significa −3; complementar esse padrão como inteiro de cinco bits tem outro significado.

Essa escolha cria uma exceção à frase do enunciado que exige F sempre em sinal e magnitude. Ela atende à preferência expressa pelo usuário, mas deve permanecer marcada como interpretação provisória a confirmar com o professor. Não esconder a divergência.

Criar `docs/OPERACAO_010_ALTERNATIVAS.md` com:

- A dúvida do enunciado e o exemplo +3 → `111101` usado nesta implementação.
- Diferença entre negar B e somente representar o próprio B em C2. A segunda leitura daria +3 → `000011` e não é a hipótese adotada.
- Como mudar para a segunda opção solicitada pelo usuário: manter a negação de B em C2, encaminhá-la a um conversor C2→SM e conectar essa saída ao candidato 010 do multiplexador. +3 passaria a `100011` e −3 a `000011`.
- Arquivos e conexões exatos afetados, incluindo o BDF, BSF caso a interface mude, documentação, modelo de referência e testes.
- Como regenerar e testar a variante; não basta trocar a expectativa do teste sem alterar o circuito.
- Os displays de F permanecem apagados na operação 010 em qualquer variante.

### 3.4. AND/XOR e a passagem de cinco para seis bits

Definição confirmada pelo usuário: aplicar a operação aos cinco bits, inclusive o sinal. Usar A/B brutos para preservar o caráter bit a bit, mesmo quando a entrada tem magnitude zero.

Proposta de alocação em F: para o resultado lógico `L[4:0]`, usar `F={L4,0,L3,L2,L1,L0}`. Assim o sinal permanece na posição de sinal do vetor de saída e o novo bit de magnitude fica em zero. Documentar esse alinhamento como escolha de integração; não usar indistintamente `F={0,L}`.

Não normalizar o sinal do resultado lógico quando a magnitude for zero: isso alteraria a operação bit a bit aprovada. Exemplo: `10000 AND 10000 → F=100000`. Esse padrão deve ser preservado nos LEDs, embora represente zero negativo se interpretado como SM.

### 3.5. Inconsistências do enunciado a registrar

- F possui seis bits. A menção a sete LEDs para replicá-lo não altera essa largura; a proposta usa seis LEDs para F e um separado para STATUS.
- Cada display exige sete sinais, `HEXn[6:0]`, apesar do trecho que menciona vetores de seis bits.
- A magnitude de F tem cinco bits; o bit de sinal não entra no conversor decimal. O bit F4 não deve ser confundido com o carry final do somador interno.
- O projeto é combinacional e não requer clock, reset digital ou máquina de estados.

## 4. Arquitetura e módulos propostos

Para cada linha abaixo criar quatro arquivos: `<nome>.bdf`, `<nome>.bdf.md`, `<nome>.bsf` e `<nome>.bsf.md`. Usar o mesmo nome de entidade, arquivo e símbolo. As larguras devem estar registradas num contrato compartilhado antes da execução paralela.

| Nome | Interface principal | Construção e responsabilidade |
|---|---|---|
| `somador_1bit` | A, B, Cin → S, Cout | Dois XOR, dois AND e um OR |
| `sm_para_c2` | SM5 → C2_6 | Conversão SM→C2 de seis bits, inclusive zeros |
| `somador_subtrator_6bit` | A6, B6, SUB → R6, Cout | Seis somadores completos e XOR condicionais |
| `c2_para_sm` | R6 → F_SM6 | Valor absoluto e sinal para a faixa representável |
| `negador_c2_6bit` | B_C2_6 → NEG6 | Inversão e soma de um, usando portas/somadores |
| `modulo2_soma_sub` | A_C2_6, B_C2_6, SUB → F_SM6 | Caminho aritmético; interface nova explicitamente documentada |
| `comparador_c2_6bit` | A_C2_6, B_C2_6 → EQ, GT, LT | Comparação signed com portas, sem comparação do SM bruto |
| `logica_5bit` | A_SM5, B_SM5 → AND6, XOR6 | Cinco AND e cinco XOR, com alinhamento de saída documentado |
| `decodificador_operacao` | S3 → D8, EXIBE_F | Oito mintermos e habilitação somente para 000/001 |
| `mux_resultado_8x6` | Oito candidatos6, D8 → F6 | AND/OR por bit, usando seleção one-hot |
| `ula_core` | A5, B5, S3 → F6, STATUS, EXIBE_F | Integra conversores, aritmética, negação, comparação e lógica |
| `somador_subtrator_5bit` | A5, B5, SUB → R5, Cout | Cinco somadores; apoio estrutural à conversão decimal |
| `bin_bcd` | MAG5 → DEZ4, UNI4 | Limiar 10/20/30 e subtração da dezena em portas |
| `bcd_7seg` | BCD4 → SEG7 | Equações Booleanas dos sete segmentos, ativas em zero |
| `display_decimal_2digitos` | MAG5, ENABLE → DEZ_SEG7, UNI_SEG7 | bin_bcd, dois decodificadores e máscara de apagamento |
| `ula_de2_115` | SW13 → LEDR18, LEDG9, HEX0..7 | Circuito principal completo conectado à placa |

Os 16 módulos implicam 32 arquivos BDF/BSF e 32 documentos individuais. Essa decomposição pode ser refinada após aprovação, desde que a documentação cubra cada arquivo efetivamente entregue. O BSF do topo pode ser gerado para completude, embora ele não seja instanciado por outro bloco.

### 4.1. Equações e limites que o agente deve respeitar

Somador completo: `P=A XOR B`; `S=P XOR Cin`; `Cout=(A AND B) OR (P AND Cin)`.

SM→C2: formar `Z={0,0,M3,M2,M1,M0}`, aplicar XOR de cada bit com o sinal s e somar s por uma cadeia de somadores. Isso calcula `C2=(Z XOR {6{s}})+s`. O sinal SM não deve ser inserido como parte da magnitude.

Soma/subtração: `R=A_C2+(B_C2 XOR {6{SUB}})+SUB`. O carry final não é o sinal nem um indicador correto de overflow signed. A soma/subtração das entradas válidas cabe em seis bits C2.

C2→SM: se R5=1, obter a magnitude de `~R+1`; senão usar R. Para resultados representáveis, produzir sinal `R5 AND OR(R4..R0)` e magnitude de cinco bits. O padrão C2 `100000` vale −32 e não cabe em SM com cinco bits de magnitude. É fora do domínio desse conversor e inalcançável nas operações previstas; documentar e testar essa limitação, sem alegar conversão correta de todos os 64 padrões.

Comparação: igualdade por XNOR e AND de todos os bits. Se os sinais C2 diferirem, o operando com sinal 1 é menor. Se forem iguais, comparar lexicograficamente os cinco bits inferiores por portas. Obter GT como `NOT(EQ OR LT)`. Essa construção também permite testar isoladamente todos os pares de valores C2 de seis bits.

Controle: `EXIBE_F=NOT(S2) AND NOT(S1)`; `STATUS=(D3 AND EQ) OR (D4 AND GT) OR (D5 AND LT)`. Nas demais operações STATUS=0. Os candidatos do mux são soma/sub, NEG6, zeros para as três comparações e AND6/XOR6. Soma e sub podem compartilhar o mesmo candidato aritmético controlado por S0.

Conversão decimal proposta: derivar em portas `T10=(MAG>=10)`, `T20=(MAG>=20)`, `T30=(MAG>=30)` a partir das 32 linhas da tabela. Gerar dezenas `DEZ0=(T10 AND NOT T20) OR T30`, `DEZ1=T20`, `DEZ2=DEZ3=0`. Selecionar K entre 0,10,20,30 com portas e calcular `UNI=MAG-K` pelo somador/subtrator de cinco bits. Tratar 31 deterministamente como 31 no conversor genérico, embora F aritmético nunca alcance esse valor.

Decodificação de segmentos: construir tabela para dígitos 0..9, obter equações simplificadas e implementar em portas. Definir entradas BCD 10..15 como apagadas; não usá-las como don't-care se o contrato promete esse apagamento. `SEG[6:0]={g,f,e,d,c,b,a}`, com bit 0 associado ao segmento a. Aplicar `SEG_FINAL[i]=SEG[i] OR NOT(ENABLE)`.

O agente deve apresentar tabelas, reduções e mapas de Karnaugh aplicáveis. Não exigir um mapa impraticável de toda a ULA; documentar os blocos combinacionais básicos e as cadeias hierárquicas.

## 5. Integração proposta na DE2-115

Validar esta organização com o usuário antes de fixar o contrato físico. O enunciado informa pinos, mas não estabelece toda a distribuição de operandos pelos recursos da placa.

| Recurso | Uso proposto |
|---|---|
| SW[3:0], SW[4] | Magnitude e sinal de A |
| SW[8:5], SW[9] | Magnitude e sinal de B |
| SW[12:10] | S[2:0], com S0 em SW10 |
| LEDR[12:0] | Replicação das treze chaves usadas |
| LEDR[17:13] | Zero |
| LEDG[5:0] | F[5:0]; em aritmética LEDG5 indica sinal |
| LEDG[6] | STATUS |
| LEDG[8:7] | Zero |
| HEX5 / HEX4 | Dezena / unidade da magnitude de A |
| HEX3 / HEX2 | Dezena / unidade da magnitude de B |
| HEX1 / HEX0 | Dezena / unidade de F, só para soma/subtração |
| HEX7 / HEX6 | Apagados |

O topo proposto tem SW[12:0] e todas as saídas acima; não precisa declarar clock, KEY nem SW[17:13]. Replicar os sinais das entradas sem alterar os bits usados pelas operações lógicas. Para os displays de entrada, estender cada magnitude de quatro para cinco bits com zero.

Criar `config/pinagem_de2_115.csv`, com sinal, pino, padrão de I/O e origem. Transcrever todos os pinos usados a partir da página 3 do enunciado e conferir com as tabelas do manual. A atribuição deve cobrir também saídas constantes fisicamente declaradas.

Exemplos conferidos: SW0→AB28, SW4→AB27, SW9→AB25, SW10→AC24, SW12→AB23; LEDG0→E21, LEDG5→G20, LEDG6→G22; HEX0[0]→G18. A tabela completa deve ser gerada no arquivo de pinagem, sem inferir os demais pinos por sequência.

O manual distingue I/O fixo de 2,5 V e I/O condicionado por JP6/JP7. Os padrões de referência são JP6 em 3,3 V e JP7 em 2,5 V. Não aplicar 3,3-V LVTTL indiscriminadamente a todos os sinais. Registrar o perfil assumido e deixar a conferência física dos jumpers para o usuário antes de programar a placa. [Manual oficial da DE2-115](https://www.terasic.com.tw/attachment/archive/502/DE2_115_User_manual.pdf).

## 6. Geração real de BDF e BSF

### 6.1. Ambiente constatado

- Quartus Prime Lite 21.1.0, build 842, em `C:/intelFPGA_lite/21.1/quartus/bin64`.
- Projeto histórico criado no Quartus Lite 20.1.1. Não afirmar compatibilidade regressiva sem testar essa versão.
- Questa Intel Starter FPGA Edition 2021.2 em `C:/intelFPGA_lite/21.1/questa_fse/win64`.
- A compilação Verilog da pequena amostra passou; a execução de `vsim` falhou ao obter licença. Resolver esse pré-requisito ou validar uma alternativa antes de prometer simulação concluída.
- Os executáveis Quartus não estavam acessíveis pelo PATH consultado. Usar os caminhos completos ou uma configuração de ambiente restrita à execução.

### 6.2. Escrever BDF sem depender da interface gráfica

BDF/BSF são textos estruturados com cabeçalhos, símbolos, portas, coordenadas, conectores, barramentos e junções. Os arquivos fornecidos são amostras reais do formato. Os avisos internos do Quartus tornam especialmente importante validar qualquer geração textual.

Procedimento proposto:

1. Usar uma amostra canônica como referência de sintaxe, não inventar um formato semelhante.
2. Representar cada circuito primeiro num grafo de portas e redes com larguras explícitas.
3. Emitir BDF com nomes únicos, portas posicionadas corretamente, ligações terminando nas coordenadas elétricas e junções apenas onde há conexão.
4. Manter nomes de bus como `[5..0]` no BDF e conferir o mapeamento para `[5:0]` no HDL convertido.
5. Separar desenho e conexões: um cruzamento visual ou nome desenhado não basta para presumir conexão elétrica.
6. Definir uma grade e espaçamento legíveis; não sobrepor símbolos ou escrever textos explicativos dentro dos circuitos.
7. Validar o arquivo no Quartus a cada bloco concluído, e novamente na hierarquia integrada.

Criar um gerador reutilizável e um verificador estrutural, ambos sem comentários e com `.md` individual. Eles devem detectar rede sem driver, múltiplos drivers, porta incompatível, largura errada, nome de módulo duplicado, fonte ausente e dependência circular. A aceitação pelo Quartus continua sendo obrigatória.

### 6.3. Comandos comprovados numa cópia do somador

Os exemplos abaixo foram executados sobre uma cópia temporária do `somador_1bit.bdf`; não sobre a ULA completa. Execute em diretório isolado com projeto de apoio válido.

```powershell
& 'C:/intelFPGA_lite/21.1/quartus/bin64/quartus_map.exe' probe --analyze_file=somador_1bit.bdf --part=EP4CE115F29C7
& 'C:/intelFPGA_lite/21.1/quartus/bin64/quartus_map.exe' probe --convert_bdf_to_verilog=somador_1bit.bdf
& 'C:/intelFPGA_lite/21.1/quartus/bin64/quartus_map.exe' probe --generate_symbol=somador_1bit.v
```

A conversão e a geração do símbolo passaram sem erros e sem avisos nessa amostra. A análise passou sem erros, com avisos de configuração do projeto de apoio. O BSF gerado apresentou A/B/Cin/Cout/S corretamente.

No Quartus 21.1 testado, `--generate_symbol=somador_1bit.bdf` falhou com Error 12073. Portanto gerar o símbolo a partir do HDL convertido pelo próprio Quartus, ou emitir BSF pela mesma definição de portas e validar sua correspondência. Não planejar a geração direta de BSF a partir de BDF por esse comando.

Os `.v` convertidos são auxiliares de geração/simulação e não substituem os BDF como fontes sintetizadas do projeto. Não cadastrar no QSF o BDF e o HDL convertido com a mesma entidade. Converter também os módulos dependentes para simular a hierarquia funcional.

Manter Lite/Standard compatível com BDF. A documentação atual registra retirada da síntese de BDF no Pro a partir de 23.3; migrar para Pro recente frustraria esta exigência. [Documentação oficial de conversão de BDF](https://docs.altera.com/r/docs/683463/26.1/quartus-prime-pro-edition-user-guide/converting-symbolic-bdf-files-to-acceptable-file-formats).

## 7. Arquivos de apoio e organização da entrega

Estrutura proposta, com os 16 módulos enumerados na seção 4:

```text
entrega/
  README.md
  ULA_DE2_115.qpf
  ULA_DE2_115.qpf.md
  ULA_DE2_115.qsf
  ULA_DE2_115.qsf.md
  modulos/
    <nome>.bdf
    <nome>.bdf.md
    <nome>.bsf
    <nome>.bsf.md
  config/
    interfaces.json
    interfaces.json.md
    pinagem_de2_115.csv
    pinagem_de2_115.csv.md
  scripts/
    gerar_bdf.py
    gerar_bdf.py.md
    validar_estrutura.py
    validar_estrutura.py.md
    gerar_tabelas.py
    gerar_tabelas.py.md
    verificar_entrega.py
    verificar_entrega.py.md
    compilar.ps1
    compilar.ps1.md
    simular.ps1
    simular.ps1.md
  simulation/
    tb_<nome>.sv
    tb_<nome>.sv.md
    tb_ula_de2_115.sv
    tb_ula_de2_115.sv.md
    run.do
    run.do.md
    generated/
      <nome>.v
      <nome>.v.md
    waveforms/
      <nome>.vcd
      <nome>.vcd.md
      <nome>.png
      <nome>.png.md
  docs/
    VISAO_GERAL.md
    OPERACAO_010_ALTERNATIVAS.md
    DECISOES_E_PENDENCIAS.md
    VALIDACAO.md
    COMO_ABRIR_E_PROGRAMAR.md
    STATUS_EXECUCAO.md
    tabelas/
    diagramas/
  relatorio/
    RELATORIO.md
  output_files/
    ULA_DE2_115.sof
    ULA_DE2_115.sof.md
  manifest.json
  manifest.json.md
ULA_DE2_115.zip
ULA_DE2_115.zip.md
```

O prefixo `tb_<nome>` deve cobrir os módulos, inclusive controle, display e integração, com possibilidade de um mesmo script executar os testes por grupos. Se forem entregues VWF, WLF, netlist `.vo`, diagramas SVG, tabelas CSV ou outros arquivos de circuito/simulação, adicionar o respectivo `<arquivo.ext>.md`.

Não existe obrigação recursiva de documentar um `.md` com outro `.md`. Caches `db`, `incremental_db`, biblioteca compilada de simulação e logs internos não são módulos ou esquemas: podem ficar fora da entrega portátil e ter explicação geral. Os relatórios relevantes de compilação devem ser preservados e indexados em `VALIDACAO.md`.

Configuração final: família `Cyclone IV E`, dispositivo EP4CE115F29C7, entidade principal `ula_de2_115`, lista explícita dos BDF, caminhos relativos, pasta de saída e todas as atribuições de pinos/I/O. QPF/QSF não devem depender de caminho absoluto pessoal ou de banco compilado pré-existente.

Não inventar clock de 50 MHz para um circuito combinacional. O enunciado não define orçamento de atraso; informar os limites da análise temporal e os caminhos de entrada a saída disponíveis. Se forem propostas restrições SDC, validar o orçamento com o usuário e documentar o arquivo; não criar restrições artificiais apenas para ocultar avisos.

O relatório do enunciado é uma entrega adicional aos `.md` individuais: capa com identificação real dos alunos, visão geral em blocos, tabelas/reduções/mapas aplicáveis, circuitos e waveforms dos módulos, integração e waveform geral, conclusão. Solicitar os dados da capa antes de fechar o relatório; não inventar identificação. Preparar versão imprimível após validar o conteúdo e o formato desejado com o usuário.

## 8. Política de comentários e documentação individual

Nos arquivos finais de implementação e automação, não incluir comentários didáticos, cabeçalhos explicativos, TODO, docstrings ou notas no desenho. Permitir nomes de entidade, redes, instâncias e portas, pois são parte do funcionamento. BDF e BSF devem ser esquemas reais, sem blocos de texto usados como explicação.

O Quartus pode gerar cabeçalhos e comentários automaticamente. Diferenciar as cópias originais de estudo da entrega. Preparar as fontes autorais finais sem comentários; auditar os arquivos gerados também. Não apagar avisos de licença/copyright cuja preservação seja obrigatória: registrar uma incompatibilidade dessa exigência se ela existir, em vez de declarar que não há comentários. Uma limpeza permitida deve preservar tokens, strings e nomes e ser seguida de nova leitura/compilação. O arquivo aprovado para entrega deve ser exatamente o validado.

Nome obrigatório da documentação: `<arquivo completo>.md`, na mesma pasta. Exemplo: `bin_bcd.bdf.md` e `bin_bcd.bsf.md` são documentos distintos. Um único `bin_bcd.md` para ambos não satisfaz a regra pedida.

Cada documento deve conter objetivo, entradas/saídas e larguras, funcionamento, dependências, um exemplo e como foi verificado. No BSF, explicar também sua relação com a entidade e a correspondência das portas; não atribuir lógica ao símbolo.

Escala sugerida de explicação:

- Somador de um bit e BSF simples: alguns parágrafos e equações essenciais.
- Conversores, comparador, mux e decodificador: explicar representação, sinais intermediários, equações e casos extremos.
- `bin_bcd`: explicar limiares, seleção da correção decimal, subtração e os limites 9/10/19/20/29/30/31.
- Caminho aritmético, `ula_core` e topo: explicar o trajeto completo dos sinais, cada seleção, integração física e a diferença de formato da operação 010.

Os documentos precisam explicar o arquivo entregue, e ser atualizados quando o circuito mudar. Evitar descrições genéricas repetidas que apenas renomeiam o módulo.

## 9. Ordem de execução e marcos

### Etapa 0: decisões e pré-requisitos

Apresentar para validação a arquitetura, alinhamento lógico em F e distribuição na placa. Registrar a operação 010 como hipótese provisória já indicada pelo usuário. Resolver a licença de simulação ou combinar uma alternativa capaz de executar o HDL exportado. A existência do executável não comprova licença válida.

Se necessário, comparar duas opções: regularizar o Questa instalado para integrar a simulação ao Quartus, ou usar simulador externo compatível para os `.v` convertidos. A instalação/ativação não foi realizada neste estudo. Não exigir Computer Use para decidir ou validar isso.

Saída: `DECISOES_E_PENDENCIAS.md` e `interfaces.json` com portas e representações congeladas.

### Etapa 1: fontes e ferramentas de geração

Preservar as cópias recebidas fora da entrega. Definir a revisão que serve de referência e comparar duplicatas antes de reutilizar algo. Criar gerador e verificador; reproduzir o somador mínimo; obter análise Quartus e BSF coerente.

Saída: infraestrutura de geração validada em um módulo mínimo e documentação correspondente.

### Etapa 2: módulos básicos e aritméticos

Implementar/validar somador de um bit, conversões, somador/subtrator de seis bits, negador e caminho aritmético. Gerar BSF depois de fixar cada interface. Testar zero, sinais opostos, carry em vários estágios e extremos ±30.

Saída: blocos numéricos reais, símbolos sincronizados e testes passando.

### Etapa 3: operações restantes e controle

Criar comparador, AND/XOR de cinco bits, decodificador e mux. Integrar `ula_core` e documentar a exceção C2 da operação 010. Verificar que cada seletor tem exatamente um candidato selecionado e que STATUS não permanece aceso de uma operação anterior.

Saída: 8192 combinações de A/B/S conferidas no circuito exportado da hierarquia BDF.

### Etapa 4: conversão decimal e displays

Criar a conversão binária→BCD, decodificador BCD→sete segmentos e bloco decimal de dois displays. Substituir o decoder comportamental existente por portas. Instanciar três conjuntos: A, B e F, com habilitação somente no resultado.

Saída: todos os dígitos, polaridade, ordem de segmentos e apagamento verificados.

### Etapa 5: circuito principal e configuração da placa

Montar `ula_de2_115.bdf` com todos os caminhos reais, LED mirrors, status e constantes. Gerar QPF/QSF e pinagem a partir do contrato. Executar análise/síntese, fitting e assembly.

```powershell
& 'C:/intelFPGA_lite/21.1/quartus/bin64/quartus_sh.exe' --flow compile ULA_DE2_115
```

Esse é o comando planejado para executar na raiz da entrega; a ULA final ainda não existe e esse fluxo completo não foi executado neste estudo.

Saída: compilação final, pinagem do Fitter conferida, circuito combinacional sem estado e `.sof` novo correspondente às fontes finais.

### Etapa 6: simulação da integração e evidências

Simular o topo exportado do BDF, sem substituí-lo por uma ULA reescrita no testbench. Para netlist mapeada, conferir a ajuda da versão instalada e as bibliotecas Cyclone IV necessárias. A ajuda local oferece o fluxo abaixo, que ainda deve ser executado no projeto final:

```powershell
& 'C:/intelFPGA_lite/21.1/quartus/bin64/quartus_map.exe' ULA_DE2_115 --generate_functional_sim_netlist
& 'C:/intelFPGA_lite/21.1/quartus/bin64/quartus_eda.exe' ULA_DE2_115 --simulation --tool=questa_oem --format=verilog --functional
```

Usar o HDL convertido para testes funcionais dos módulos e, quando o simulador e as bibliotecas permitirem, repetir a bateria no netlist nativo final. O EDA Netlist Writer é o mecanismo oficial para gerar `.vo`/`.vho`; os parâmetros efetivos devem seguir a versão 21.1 local. [Guia oficial de geração de netlist para simulação](https://docs.altera.com/r/docs/730191/25.3/questa-edition-simulation-user-guide/step-1-generate-gate-level-netlists-for-simulation).

Salvar waveforms reais de todos os módulos e do sistema. Renderizar recortes legíveis programaticamente a partir dos resultados de simulação; não fabricar traços a partir das respostas esperadas. Não é preciso screenshot da interface nem Computer Use. Um VWF pode ser entrega adicional, mas não substitui teste automático e waveform efetivamente executada.

### Etapa 7: documentação, relatório e pacote

Atualizar os documentos ao lado de cada arquivo, montar diagramas a partir da hierarquia e gerar relatório. Auditar cobertura de `.md` e ausência de comentários conforme seção 8. Registrar hashes/revisão das fontes e do `.sof`.

Extrair o ZIP em diretório novo e recompilar pelas fontes para comprovar independência de bancos antigos e caminhos pessoais. Não programar a placa automaticamente: o usuário fará a conferência visual e física posteriormente.

## 10. Testes e critérios de aceitação

Os testes precisam comparar a implementação real com um modelo independente. Usar inteiros assinados no modelo de referência e uma tabela explícita de segmentos; não reutilizar as equações ou o grafo do gerador para calcular o esperado.

| Bloco | Cobertura mínima |
|---|---|
| Somador completo | Oito combinações de A/B/Cin |
| SM→C2 | Todos os 32 padrões SM, com dois zeros |
| C2→SM | Todos os valores representáveis −31..31; −32 explicitamente fora do domínio |
| Somador/subtrator de seis bits | 64×64×2 padrões, resultado módulo 64 e carry; testes numéricos separados no domínio da ULA |
| Negador | 64 padrões módulo 64, observando o caso −32; domínio de B incluindo zeros |
| Comparador C2 | 64×64 pares, comparação signed independente |
| AND/XOR | 32×32 pares, incluindo sinal e zero de magnitude |
| Seletor | Oito seletores; uma saída one-hot ativa e EXIBE_F correto |
| Mux | Cada seletor e cada bit/candidato isolado, evitando ocultar fios trocados por candidatos iguais |
| Somador/subtrator de cinco bits | 32×32×2 padrões e carry |
| Binário→BCD | 0..31, fronteiras de dezenas |
| BCD→sete segmentos | 16 padrões; 0..9 corretos e 10..15 apagados |
| Display decimal | 32 magnitudes × duas habilitações |
| ULA/core e topo | 32×32×8 = 8192 casos por integração, mais verificação física das saídas |

No teste do topo conferir F nos LEDs, STATUS, espelhamento de A/B/S, seis displays ativos nos seus modos, HEX6/7 apagados e demais LEDs constantes. Para operação 010 comparar o padrão C2, não interpretá-lo como SM. Incluir troca de seletor com A/B constantes e mudança de A/B com S constante.

Casos dirigidos indispensáveis: +15+15=+30, −15−15=−30, +15−(−15)=+30, −15−(+15)=−30, cancelamento de sinais, ambos os zeros, comparação de negativos com magnitudes diferentes, resultados 9/10/19/20/29/30 e todas as oito operações.

Critérios finais:

- Todos os BDF passam por leitura/análise nativa e a hierarquia compila integralmente.
- BSF e portas instanciadas coincidem com as fontes finais.
- O projeto sintetizado usa os BDF; não contém implementação comportamental oculta, IP aritmético, ROM ou DSP para substituir as portas.
- Não há registradores, latches ou clock no circuito da ULA.
- Nenhum erro de compilação, pino necessário sem atribuição, conflito de pinos, largura incompatível, driver múltiplo ou rede funcional sem driver.
- Avisos têm justificativa individual; constantes intencionais são distinguíveis de falhas.
- Simulação executada e testes aprovados, com logs e waveforms; licença inválida deve resultar em pendência, não em aprovação.
- Cada fonte, esquema, símbolo e arquivo de simulação entregue tem seu próprio `.md`.
- A entrega final atende à política de comentários ou identifica objetivamente qualquer impedimento de cabeçalho obrigatório.
- O ZIP recompila extraído em outra pasta, e o `.sof` corresponde à última versão validada.
- Conferência gráfica pelo usuário e teste em placa permanecem identificados como etapas posteriores, sem alegar que ocorreram.

## 11. Subagentes Luna no high

O usuário autorizou subagentes Luna com esforço high. Usar `gpt-6-luna` com `reasoning_effort=high`, se disponível, mantendo um agente principal responsável pela integração e aceitação. Este estudo já usou dois subagentes nessa configuração para revisar arquitetura e testar o fluxo Quartus.

Após congelar interfaces, dividir o trabalho em três frentes: aritmética/conversores; comparação/lógica/controle; BCD/displays. O principal cuida de QPF/QSF, gerador compartilhado, contrato de portas, integração e verificação final. Limitar a concorrência aos slots disponíveis.

Cada subagente edita apenas seus módulos, testes e documentos. Um único responsável modifica o gerador e o contrato; ninguém muda interfaces silenciosamente. Ao entregar, informar arquivos, portas, testes executados e pendências. O principal recompila e testa a integração: sucesso isolado de um subagente não aprova o sistema.

## 12. Uso, checkpoints e resets

Intenção expressa do usuário: quando restarem 2% de limite, consumir um reset existente para continuar o projeto, sem nova pergunta. Essa intenção deve ficar registrada, mas não pode ser apresentada como capacidade irrestrita do agente.

Limite operacional da ferramenta disponível neste estudo: `consume_usage_reset` exige confirmação explícita do usuário para cada uso. Uma autorização permanente não substitui essa confirmação por consumo. Não contornar a regra por Computer Use, outro endpoint ou script. A dispensa de Computer Use para conferir o Quartus não altera essa exigência.

Procedimento compatível:

1. Consultar `get_usage_limits` em marcos de trabalho e com maior atenção quando estiver perto do limite. Usar dados atuais, compartilhados pela conta.
2. Calcular restante como `max(0,100-usedPercent)`. Na falta de indicação de uma janela específica, observar as janelas principais de cinco horas e semanal; não aplicar o percentual a limite de contexto ou contagem de tokens do chat.
3. Ao identificar uma dessas janelas com 2% ou menos restantes, salvar `STATUS_EXECUCAO.md` com arquivos concluídos, última compilação/teste, decisões e próximos passos.
4. Solicitar confirmação específica para consumir um reset naquele momento, explicando que a exigência vem da ferramenta `consume_usage_reset`.
5. Após confirmação, usar uma chave de idempotência única para esse consumo. Reutilizar a mesma chave em tentativa incerta; não consumir outro reset por repetir a chamada.
6. `reset` e `alreadyRedeemed` concluem a tentativa. `noCredit` e `nothingToReset` não autorizam inventar sucesso ou comprar créditos. Consultar os limites novamente e registrar o resultado.

Não há autorização implícita para compras nem para consumir indefinidamente vários resets. Este estudo não consumiu reset. Os endpoints oficiais de leitura de limites e consumo idempotente estão descritos no [Codex App Server](https://learn.chatgpt.com/docs/app-server#api-overview-1); a exigência de confirmação por uso vem da ferramenta disponível, não de uma regra inventada para este projeto.

## 13. Pendências antes de fechar a implementação

- Validar arquitetura e distribuição física propostas com o usuário.
- Manter explicitamente provisória a leitura de 010, conforme pedido; confirmar com o professor quando possível.
- Registrar aprovação do alinhamento do resultado lógico de cinco para seis bits.
- Resolver a execução da simulação: licença Questa atualmente indisponível ou alternativa combinada.
- Confirmar o perfil elétrico real da placa antes de programá-la.
- Obter identificação dos alunos e definir formato imprimível do relatório.

Essas pendências não impedem preparar e revisar módulos independentes. Não concluir a entrega como totalmente validada enquanto faltar simulação efetiva. A abertura gráfica via Computer Use não é requisito de conclusão do agente.

## 14. Referências

- Enunciado local: `Projeto_Primeira_Unidade_2026_2.pdf`.
- [Materiais de referência no Drive](https://drive.google.com/drive/folders/1oW1BSgOzj0mFPLoNP_ph5wCtc_VbQrTy).
- [Manual oficial da DE2-115](https://www.terasic.com.tw/attachment/archive/502/DE2_115_User_manual.pdf), tabelas de pinagem e jumpers.
- [Documentação oficial de conversão de BDF](https://docs.altera.com/r/docs/683463/26.1/quartus-prime-pro-edition-user-guide/converting-symbolic-bdf-files-to-acceptable-file-formats).
- [Documentação oficial do EDA Netlist Writer](https://docs.altera.com/r/docs/730191/25.3/questa-edition-simulation-user-guide/step-1-generate-gate-level-netlists-for-simulation).
- Ajuda local do Quartus 21.1: `quartus_map --help=convert_bdf_to_verilog`, `--help=generate_symbol`, `--help=analyze_file` e ajuda de `quartus_eda`. Os comandos de conversão/análise/símbolo foram verificados numa amostra, sem inferir que a ULA final foi testada.
- [Codex App Server: limites e resets](https://learn.chatgpt.com/docs/app-server#api-overview-1).
