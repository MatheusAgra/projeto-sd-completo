# Plano de refatoraÃ§Ã£o visual dos esquemas Quartus

Data: 30/09/2026. Estado: plano para execuÃ§Ã£o futura; nenhuma refatoraÃ§Ã£o, compilaÃ§Ã£o, simulaÃ§Ã£o ou conferÃªncia visual foi executada nesta tarefa de planejamento.

## 1. Resultado solicitado e limites aprovados

Refatorar a representaÃ§Ã£o dos circuitos do projeto ULA para DE2-115 para que suas conexÃµes possam ser acompanhadas por fios e barramentos contÃ­nuos no editor BDF do Quartus. Aplicar a melhoria em **todos os 16 mÃ³dulos e em todos os nÃ­veis internos**, atÃ© as portas lÃ³gicas de `somador_1bit`. Melhorar somente o topo ou os blocos externos nÃ£o atende ao pedido.

O GPT-6.1 Sol serÃ¡ o coordenador da execuÃ§Ã£o futura. Ele deverÃ¡ distribuir frentes independentes a agentes GPT-6 Luna com esforÃ§o de raciocÃ­nio `high`, integrar suas entregas e responder pela validaÃ§Ã£o tÃ©cnica. Este documento nÃ£o solicita iniciar esses agentes agora.

Preservar integralmente comportamento, interfaces, hierarquia, entidades, larguras, Ã­ndices de bits, pinagem e padrÃµes elÃ©tricos. Ã‰ permitido mudar posiÃ§Ãµes, dimensÃµes grÃ¡ficas dos sÃ­mbolos, espaÃ§amento e roteamento. Manter os nomes das redes como identificaÃ§Ã£o; substituir a dependÃªncia de nomes repetidos em trechos separados por continuidade geomÃ©trica dentro de cada BDF.

ConexÃµes entre nÃ­veis hierÃ¡rquicos continuam pelas portas dos mÃ³dulos. Dentro de cada mÃ³dulo, desenhar os trajetos correspondentes atÃ© suas primitivas ou blocos filhos, sem achatar a hierarquia ou inventar entidades.

**A conferÃªncia visual estÃ¡ adiada por instruÃ§Ã£o do usuÃ¡rio.** Durante a execuÃ§Ã£o tÃ©cnica, nÃ£o abrir esquemas para inspeÃ§Ã£o visual, nÃ£o avaliar screenshots e nÃ£o declarar legibilidade visual aprovada. Usar verificaÃ§Ãµes automÃ¡ticas estruturais e funcionais e entregar os circuitos prontos para revisÃ£o posterior com [GUIA_CONFERENCIA_VISUAL_QUARTUS.md](GUIA_CONFERENCIA_VISUAL_QUARTUS.md).

## 2. Contexto encontrado no projeto

- Projeto: `entrega/ULA_DE2_115.qpf`; configuraÃ§Ãµes: `entrega/ULA_DE2_115.qsf`.
- Quartus documentado: Prime Lite 21.1; dispositivo: EP4CE115F29C7, famÃ­lia Cyclone IV E.
- A implementaÃ§Ã£o sintetizada usa exclusivamente os 16 BDF de `entrega/modulos/`. Os Verilog de `entrega/simulation/generated/` sÃ£o derivados para simulaÃ§Ã£o, nÃ£o substitutos de implementaÃ§Ã£o.
- Contrato de portas: `entrega/config/interfaces.json`; conectividade lÃ³gica: `entrega/config/grafos/*.json`; pinagem: `entrega/config/pinagem_de2_115.csv`.
- O inventÃ¡rio dos grafos atuais contÃ©m 342 instÃ¢ncias. O emissor materializa `BUF` em dois NOT; a contagem geomÃ©trica resultante nÃ£o deve ser confundida com a contagem dos grafos.
- `entrega/scripts/gerar_bdf.py` gera cada ligaÃ§Ã£o com um trecho de 64 unidades e rÃ³tulo. Coloca as instÃ¢ncias em trÃªs colunas pela ordem da lista, independentemente do fluxo lÃ³gico. Os pequenos trechos com o mesmo nome formam uma rede elÃ©trica, mas nÃ£o um trajeto visual contÃ­nuo.
- O emissor tambÃ©m cria grupos de barramentos abaixo das instÃ¢ncias, separados visualmente dos consumidores. A refatoraÃ§Ã£o precisa integrar essas derivaÃ§Ãµes ao trajeto efetivo da rede.
- `entrega/scripts/preparar.py` regenera BDF, analisa e converte cada mÃ³dulo no Quartus, exporta HDL e substitui o BSF por um sÃ­mbolo nativo derivado do HDL. Esse fluxo pode desfazer ajustes manuais ou substituir a geometria dos sÃ­mbolos se nÃ£o for adaptado.
- `entrega/scripts/validar_estrutura.py` verifica os grafos JSON, suas larguras, fontes e ciclos. Atualmente isso nÃ£o prova continuidade geomÃ©trica nos BDF.
- `entrega/scripts/render_evidencias.py` lÃª os BDF para gerar figuras. Essas figuras sÃ£o documentaÃ§Ã£o programÃ¡tica, nÃ£o conferÃªncia do editor Quartus.

Os resultados anteriores descritos em `entrega/docs/VALIDACAO.md` constituem o histÃ³rico da implementaÃ§Ã£o atual. NÃ£o representam validaÃ§Ã£o de arquivos que venham a ser refatorados.

## 3. ReferÃªncia de desenho

Usar como inspiraÃ§Ã£o o repositÃ³rio indicado pelo usuÃ¡rio: [francisco-araujo07/Projeto-ULA](https://github.com/francisco-araujo07/Projeto-ULA).

Arquivos consultados como referÃªncia de estrutura:

- [somador_1bit.bdf](https://github.com/francisco-araujo07/Projeto-ULA/blob/main/somador_1bit.bdf): segmentos horizontais e verticais com extremidades coincidentes ligam entradas, portas XOR/AND/OR e saÃ­das.
- [somador_5bit.bdf](https://github.com/francisco-araujo07/Projeto-ULA/blob/main/somador_5bit.bdf): cadeia de somadores de um bit com segmentos explÃ­citos entre etapas de carry.
- [And_5bits.bdf](https://github.com/francisco-araujo07/Projeto-ULA/blob/main/And_5bits.bdf): distribuiÃ§Ã£o de operandos por barramentos e derivaÃ§Ãµes identificadas por bit.

Essa observaÃ§Ã£o vem da leitura textual dos arquivos, sem inspeÃ§Ã£o visual. Na execuÃ§Ã£o futura, registrar a revisÃ£o consultada para que a referÃªncia seja reproduzÃ­vel. Aproveitar o padrÃ£o de desenho; nÃ£o importar a lÃ³gica, interfaces ou configuraÃ§Ãµes do QSF desse outro projeto. Em particular, o projeto local possui `somador_subtrator_5bit`, e nÃ£o um mÃ³dulo chamado `somador_5bit`.

## 4. InventÃ¡rio e intenÃ§Ã£o de layout

Todos os arquivos abaixo ficam em `entrega/modulos/` e tÃªm seu BSF correspondente. Os nÃºmeros indicam instÃ¢ncias no grafo atual, antes da expansÃ£o de BUF.

| MÃ³dulo BDF | InstÃ¢ncias | OrganizaÃ§Ã£o e ligaÃ§Ãµes prioritÃ¡rias |
|---|---:|---|
| `somador_1bit.bdf` | 5 | A/B/Cin Ã  esquerda; XOR da soma e AND/OR do carry em trajetos distintos; S/Cout Ã  direita; ramificaÃ§Ãµes fÃ­sicas de A, B e `fa_P`. |
| `sm_para_c2.bdf` | 13 | XOR por bit e cadeia de somadores; carry contÃ­nuo; sinal e constantes visivelmente distribuÃ­dos. |
| `somador_subtrator_6bit.bdf` | 12 | Seis etapas ordenadas por bit; barramentos A/B/R, derivaÃ§Ãµes BX, SUB e carry ligados por trajetos completos. |
| `c2_para_sm.bdf` | 35 | Separar graficamente conversÃ£o de magnitude e tratamento de sinal, preservando todos os blocos e fios internos. |
| `negador_c2_6bit.bdf` | 14 | InversÃ£o seguida da cadeia de soma; seis bits e constantes com caminhos rastreÃ¡veis. |
| `modulo2_soma_sub.bdf` | 2 | ConexÃ£o fÃ­sica de resultado entre somador/subtrator e conversor; operandos, SUB e saÃ­da ligados aos pinos. |
| `comparador_c2_6bit.bdf` | 32 | Agrupar comparaÃ§Ã£o por bit e reduÃ§Ã£o dos resultados; distinguir caminhos de EQ/GT/LT e sinal. |
| `logica_5bit.bdf` | 12 | Cinco faixas de bit; redes AND/XOR e composiÃ§Ã£o das saÃ­das, mantendo `{L4,0,L3,L2,L1,L0}`. |
| `decodificador_operacao.bdf` | 12 | S e inversÃµes Ã  esquerda, decodificaÃ§Ã£o ao centro, D e EXIBE_F Ã  direita; fan-out explÃ­cito. |
| `mux_resultado_8x6.bdf` | 54 | Seis faixas de saÃ­da com oito candidatos por bit; separar corredores de dados e seleÃ§Ã£o. |
| `ula_core.bdf` | 18 | ConversÃµes, operaÃ§Ãµes, controle, mux e STATUS agrupados por funÃ§Ã£o, com barramentos contÃ­nuos entre blocos. |
| `somador_subtrator_5bit.bdf` | 10 | Cinco etapas com `Cout` de uma etapa ligado ao `Cin` da seguinte; XOR de B com SUB prÃ³ximos a cada etapa. |
| `bin_bcd.bdf` | 24 | Fluxo da conversÃ£o em etapas; conexÃµes com somador/subtrator de cinco bits e montagem de dezenas/unidades. |
| `bcd_7seg.bdf` | 25 | Compartilhar inversÃµes por corredores e agrupar lÃ³gica por segmento, sem simplificar equaÃ§Ãµes. |
| `display_decimal_2digitos.bdf` | 18 | ConversÃ£o BCD, dois decodificadores e habilitaÃ§Ã£o; fios entre estÃ¡gios e saÃ­das dos dois dÃ­gitos. |
| `ula_de2_115.bdf` | 56 | SW Ã  esquerda, ULA e displays ao centro, LED/HEX Ã  direita; explicitar espelhamentos, habilitaÃ§Ã£o e constantes. |

Dimensionar a folha para acomodar os circuitos densos. NÃ£o comprimir blocos a ponto de sobrepor fios/rÃ³tulos e nÃ£o substituir trajetos complexos por conectividade apenas nominal.

## 5. Arquivos a revisar e responsabilidade de cada formato

| Conjunto | Trabalho previsto |
|---|---|
| `entrega/modulos/*.bdf` | Reposicionar todos os elementos e desenhar redes contÃ­nuas, barramentos, derivaÃ§Ãµes e junÃ§Ãµes. |
| `entrega/modulos/*.bsf` | Conferir portas e geometria dos sÃ­mbolos, ajustando o desenho se necessÃ¡rio. O BSF representa o sÃ­mbolo; a lÃ³gica interna permanece no BDF. |
| `entrega/ULA_DE2_115.qsf` e `.qpf` | Conferir cadastro dos 16 BDF, revisÃ£o, entidade de topo, dispositivo e atribuiÃ§Ãµes; editar somente se houver necessidade decorrente do fluxo. Esses formatos nÃ£o armazenam fios grÃ¡ficos. |
| `entrega/scripts/gerar_bdf.py` | Substituir grade arbitrÃ¡ria/trechos isolados por posicionamento e roteamento determinÃ­sticos. |
| `entrega/scripts/preparar.py` | Tornar geraÃ§Ã£o/exportaÃ§Ã£o/BSF compatÃ­veis com a geometria escolhida e evitar sobrescritas que invalidem trajetos. |
| Novos auxiliares de layout e validaÃ§Ã£o | Manter metadados de desenho separados da conectividade funcional; implementar auditoria geomÃ©trica dos BDF finais. |
| `entrega/scripts/validar_estrutura.py` | Reusar a validaÃ§Ã£o lÃ³gica existente; nÃ£o apresentÃ¡-la como prova de continuidade grÃ¡fica. |
| `entrega/scripts/integrar.py` | Conferir que regeneraÃ§Ã£o de core/topo/QSF/QPF conserva contratos e encontra os metadados de layout. |
| `entrega/scripts/render_evidencias.py` | Adaptar apenas se necessÃ¡rio para reproduzir novos trajetos e limites da folha sem corte de elementos; sua saÃ­da nÃ£o aprova legibilidade. |
| `entrega/scripts/documentar_apoio.py` e documentos `.md` associados | Atualizar descriÃ§Ãµes de geraÃ§Ã£o/conectividade; impedir que uma regeneraÃ§Ã£o documental restaure explicaÃ§Ãµes ou resultados obsoletos. |
| HDL exportado, netlist e resultados derivados | Regenerar a partir dos BDF efetivamente refatorados durante a validaÃ§Ã£o tÃ©cnica; nÃ£o editar HDL para compensar um erro de desenho. |
| Manifesto, pacote e documentaÃ§Ã£o de entrega | Atualizar quando houver nova entrega validada, preservando a distinÃ§Ã£o entre resultados histÃ³ricos, resultados tÃ©cnicos novos e revisÃ£o visual pendente. |

NÃ£o alterar `interfaces.json`, conexÃµes dos grafos ou CSV de pinagem para facilitar o desenho. Se um problema funcional anterior for encontrado, registrÃ¡-lo separadamente; sua correÃ§Ã£o nÃ£o pertence a este plano visual.

## 6. CoordenaÃ§Ã£o por GPT-6.1 Sol e GPT-6 Luna/high

O coordenador deve anunciar os arquivos de cada frente e fornecer a cada Luna este plano, o contrato congelado, o formato de layout definido e os critÃ©rios de aceitaÃ§Ã£o. Manter no mÃ¡ximo trÃªs Lunas ativos se a sessÃ£o permitir quatro agentes incluindo o principal; usar rodadas adicionais para completar as frentes.

| Frente | ResponsÃ¡vel e entregas | Limites de escrita |
|---|---|---|
| IntegraÃ§Ã£o | Sol: baseline, contrato de layout, `gerar_bdf.py`, `preparar.py`, sÃ­mbolos compartilhados, integraÃ§Ã£o e validaÃ§Ã£o final. | Arquivos compartilhados e relatÃ³rios finais. |
| AritmÃ©tica | Luna/high: layout de `somador_1bit`, somadores/subtratores 5/6 bits, conversores SM/C2, negador e mÃ³dulo de soma/subtraÃ§Ã£o. | Metadados de layout de seus sete mÃ³dulos e respectivas notas. |
| Controle e lÃ³gica | Luna/high: comparador, lÃ³gica 5 bits, decodificador e mux. | Metadados de layout de seus quatro mÃ³dulos e respectivas notas. |
| Displays e integraÃ§Ã£o | Luna/high: `bin_bcd`, `bcd_7seg`, display de dois dÃ­gitos, core e topo. | Metadados de seus mÃ³dulos, respeitando que `bin_bcd` pertence a esta frente e usa o somador de cinco bits da frente aritmÃ©tica. |
| Auditoria independente | Luna/high em rodada posterior: validador geomÃ©trico e casos de teste significativos. | Novo validador e seus testes/documentaÃ§Ã£o; sem alterar o emissor ou contratos para fazer uma verificaÃ§Ã£o passar. |

A divisÃ£o total deve permanecer 7 + 4 + 5 = 16, sem dupla propriedade.

Para arquivos novos, usar uma organizaÃ§Ã£o como `entrega/config/layouts/<modulo>.json`, com documento `.json.md` correspondente. O Sol define e documenta o esquema antes de distribuir escrita. Um Luna pode propor mudanÃ§a no gerador comum, mas somente o Sol a integra. A geraÃ§Ã£o definitiva dos BDF e BSF ocorre sob controle do Sol, evitando que agentes concorrentes sobrescrevam fontes e logs.

Cada Luna deverÃ¡ devolver: arquivos alterados, decisÃµes de posicionamento, redes difÃ­ceis, verificaÃ§Ãµes automÃ¡ticas realizadas, dependÃªncias e limitaÃ§Ãµes. Nenhum agente deverÃ¡ executar ou declarar a conferÃªncia visual nesta fase. O Sol nÃ£o delega a responsabilidade de preservar a funÃ§Ã£o nem aceita respostas sem evidÃªncias tÃ©cnicas.

## 7. SequÃªncia de execuÃ§Ã£o futura

### Etapa A â€” Congelar a referÃªncia funcional

1. Ler as instruÃ§Ãµes vigentes do projeto e conferir mudanÃ§as locais antes de editar.
2. Registrar revisÃ£o Git e hashes de BDF/BSF, interfaces, grafos, QSF/QPF, CSV e testbenches. Preservar uma cÃ³pia identificada dos HDL exportados e resultados existentes para comparaÃ§Ã£o.
3. Confirmar disponibilidade do Quartus e simulador, sem instalar ferramentas automaticamente. O fluxo documentado usa Icarus; Questa tem falha histÃ³rica de licenÃ§a. Relatar o estado real encontrado.
4. Extrair dependÃªncias diretamente dos grafos e ordenar geraÃ§Ã£o/integraÃ§Ã£o pelos filhos antes dos pais. Conferir os 16 mÃ³dulos, inclusive o somador de cinco bits usado por `bin_bcd`.
5. Registrar como invariantes as decisÃµes atuais: operaÃ§Ã£o 010 provisoriamente âˆ’B em C2 de seis bits; AND/XOR nos cinco bits incluindo sinal; alinhamento lÃ³gico existente; F=0 nas comparaÃ§Ãµes; mapeamento SW/LED/HEX e suas polaridades. NÃ£o resolver a pendÃªncia do professor durante o trabalho visual.

### Etapa B â€” Definir posicionamento e roteamento

1. Separar quatro responsabilidades: leitura da conectividade, geometria dos sÃ­mbolos/pinos, posicionamento e roteamento de redes.
2. Expandir cada rede em terminais de origem e destinos, com largura e mapeamento de bits. Aplicar a mesma expansÃ£o de BUF em dois NOT e conservar redes intermediÃ¡rias.
3. Obter coordenadas globais de portas usando a posiÃ§Ã£o da instÃ¢ncia e as coordenadas locais reais do sÃ­mbolo embutido no BDF. NÃ£o assumir que o BSF nativo final tem o mesmo tamanho ou offsets do sÃ­mbolo provisÃ³rio de `block_symbol()`.
4. Definir uma fonte coerente para a geometria dos sÃ­mbolos usados pelo emissor e para os BSF entregues. Se sÃ­mbolos nativos forem normalizados, fazÃª-lo de modo reproduzÃ­vel e conservar portas. Evitar dependÃªncia circular entre exportar BDF, gerar BSF e rerotear BDF.
5. Posicionar entradas predominantemente Ã  esquerda e saÃ­das Ã  direita. Ordenar etapas aritmÃ©ticas pelo fluxo de carry e organizar os demais blocos por funÃ§Ã£o/dependÃªncia, nÃ£o pela posiÃ§Ã£o no JSON.
6. Usar grade consistente, segmentos ortogonais, corredores reservados, margem para rÃ³tulos e distÃ¢ncia dos corpos dos sÃ­mbolos. Separar corredores de dados e controles quando isso reduzir colisÃµes.
7. Para cada rede escalar, construir um trajeto contÃ­nuo entre a origem e todos os destinos, com Ã¡rvore de ramificaÃ§Ãµes. NÃ£o acrescentar apenas linhas decorativas: usar conectores elÃ©tricos reais do BDF.
8. Para barramentos, construir trajetos fÃ­sicos contÃ­nuos e derivaÃ§Ãµes vÃ¡lidas no formato Quartus. RÃ³tulos de bits/fatias continuam necessÃ¡rios para mapear as derivaÃ§Ãµes; isso nÃ£o autoriza barramentos ou fios isolados unidos apenas pelo nome.
9. Modelar explicitamente fatias como `SW[9..5]` ligadas a uma porta B de cinco bits, preservando ordem e significado de cada bit. NÃ£o normalizar Ã­ndices externos como se comeÃ§assem sempre em zero.
10. Inserir junÃ§Ãµes somente onde hÃ¡ conexÃ£o elÃ©trica pretendida. Em cruzamentos de redes diferentes, preferir desvio geomÃ©trico; nÃ£o confiar na ausÃªncia de um ponto para impedir curto em situaÃ§Ãµes ambÃ­guas do formato.
11. Ligar GND/VCC e fan-out por trajetos reais. Se houver uma saÃ­da intencionalmente sem consumidor, conservar e documentar essa condiÃ§Ã£o; nÃ£o inventar destino funcional para cumprir uma mÃ©trica.
12. Produzir a mesma geometria na regeneraÃ§Ã£o com as mesmas entradas. Se o roteador nÃ£o encontrar um caminho vÃ¡lido, falhar com diagnÃ³stico da rede, sem voltar silenciosamente Ã  conexÃ£o apenas por nome.

### Etapa C â€” Implementar pilotos tÃ©cnicos

Usar, em ordem, `somador_1bit`, `somador_subtrator_5bit` e `modulo2_soma_sub` como pilotos. Eles cobrem portas primitivas, fan-out, cadeia hierÃ¡rquica, barramentos e ligaÃ§Ã£o entre blocos.

No `somador_1bit`, exigir os trajetos fÃ­sicos de A/B atÃ© XOR e AND, de `fa_P` atÃ© o segundo XOR e AND, de Cin atÃ© seus consumidores, e de `fa_G`/`fa_H` atÃ© OR e Cout. No somador de cinco bits, exigir a ligaÃ§Ã£o de cada `Cout` ao `Cin` seguinte, de SUB Ã s cinco XOR e ao Cin inicial, dos operandos aos bits corretos e de R aos terminais de saÃ­da.

Analisar e exportar os pilotos no Quartus, conferir portas e executar seus testes existentes sobre o HDL recÃ©m-exportado. O piloto avanÃ§a com evidÃªncia tÃ©cnica; sua revisÃ£o visual continua pendente.

### Etapa D â€” Distribuir e integrar os 16 layouts

1. Distribuir as trÃªs frentes de mÃ³dulos apÃ³s estabilizar o formato de layout e o emissor dos pilotos.
2. Receber metadados por mÃ³dulo, verificar consistÃªncia automaticamente e integrar por dependÃªncia.
3. Aplicar o mesmo requisito aos mÃ³dulos densos: comparador, mux, decodificaÃ§Ã£o de segmentos, core e topo. NÃ£o criar exceÃ§Ã£o para conectividade nominal porque a folha fica maior.
4. Regenerar os 16 BDF/BSF pelo fluxo atualizado. Conferir que `preparar.py` nÃ£o descarta o layout nem muda a geometria de portas de forma incompatÃ­vel apÃ³s os fios serem calculados.
5. Conferir QSF/QPF e fontes cadastradas; manter exclusivamente os BDF na sÃ­ntese e os mesmos pinos/dispositivo.

### Etapa E â€” Validar automaticamente

Implementar auditoria geomÃ©trica que leia os **BDF finais**, alÃ©m do validador lÃ³gico de grafos existente. Ela deve:

- Construir componentes por contato geomÃ©trico vÃ¡lido entre segmentos, terminais e junÃ§Ãµes; identificar redes sem usar nomes repetidos como atalho para unir trechos separados.
- Tratar barramentos e derivaÃ§Ãµes com seu mapeamento semÃ¢ntico de bits, mantendo redes escalares diferentes separadas dentro do mesmo vetor. A semÃ¢ntica exata dos taps deve ser confirmada por anÃ¡lise/exportaÃ§Ã£o nativa do Quartus.
- Exigir que cada destino consumido seja alcanÃ§Ã¡vel fisicamente a partir da sua origem; identificar rÃ³tulos iguais em componentes separados, terminais fora do fio e gaps entre extremidades.
- Comparar a conectividade recuperada com os grafos congelados apÃ³s a expansÃ£o de BUF, incluindo top-level pins, direÃ§Ãµes, larguras, slices e constantes.
- Rejeitar mistura de redes, drivers extras, junÃ§Ãµes indevidas, taps trocados, sobreposiÃ§Ã£o colinear de redes distintas e cruzamentos que possam produzir conexÃ£o nÃ£o desejada.
- Detectar segmentos atravessando o corpo de sÃ­mbolos e colisÃµes entre rÃ³tulos/portas/fios, respeitando as regiÃµes de acesso aos terminais. Relatar as ocorrÃªncias com mÃ³dulo, rede e coordenadas.
- Gerar relatÃ³rio por mÃ³dulo com destinos previstos/alcanÃ§ados, redes desconectadas, curtos, problemas de largura e colisÃµes. ExceÃ§Ãµes intencionais precisam de justificativa explÃ­cita; nenhum destino consumido pode ser excepcionado.

Os testes do novo validador devem incluir defeitos reais: gap de uma unidade, dois trechos separados com nome igual, ligaÃ§Ã£o ao bit errado, curto entre redes, tap invÃ¡lido e porta deslocada. Casos vÃ¡lidos devem incluir fan-out e fatias de barramento. NÃ£o testar somente a serializaÃ§Ã£o do prÃ³prio gerador.

Depois da auditoria geomÃ©trica:

1. Executar `validar_estrutura.py` e anÃ¡lise nativa de todos os BDF.
2. Exportar novamente os 16 HDL a partir dos BDF refatorados e verificar interfaces BSF/HDL contra o contrato.
3. Executar todos os 16 testbenches existentes, conservando suas expectativas independentes. NÃ£o simular apenas HDL antigo ou produzido diretamente dos JSON.
4. Comparar comportamento anterior e posterior nos domÃ­nios cobertos pelos testes. NÃ£o exigir igualdade textual do Verilog ou igualdade de hash do SOF como prova de equivalÃªncia funcional.
5. Compilar o projeto completo e comparar dispositivo, fontes, pinos, padrÃµes I/O, estado combinacional e avisos com o baseline. Investigar novos avisos e diferenÃ§as de recursos; nÃ£o impor identidade de placement fÃ­sico como requisito visual.
6. Executar a simulaÃ§Ã£o da netlist funcional regenerada com o testbench do topo e os demais verificadores de entrega aplicÃ¡veis.
7. Regenerar uma segunda vez e conferir estabilidade de BDF/layout e interfaces. Caso metadados nativos variem, separar essa variaÃ§Ã£o da geometria elÃ©trica; confirmar que nenhum fio se perdeu.

Os registros histÃ³ricos indicam 8 casos do somador de um bit, 2048 do somador/subtrator de cinco bits, 8192 do de seis bits, 8192 do core e 16384 verificaÃ§Ãµes do topo. Preservar a cobertura documentada de todos os mÃ³dulos e registrar contagens efetivamente executadas no novo estado. Resultados histÃ³ricos nÃ£o podem preencher relatÃ³rios novos.

Os comandos existentes podem orientar o fluxo futuro: `python entrega/scripts/validar_estrutura.py`, `python entrega/scripts/preparar.py`, `./entrega/scripts/simular.ps1`, `./entrega/scripts/compilar.ps1` e `./entrega/scripts/simular_netlist.ps1`. Confirmar argumentos e caminhos reais antes de executar; `preparar.py` Ã© uma operaÃ§Ã£o de escrita e somente deve rodar apÃ³s adaptar o gerador.

### Etapa F â€” Atualizar documentaÃ§Ã£o e entregar para revisÃ£o futura

1. Documentar cada BDF/BSF e scripts auxiliares alterados nos `.md` associados, conforme a cobertura exigida por `auditar_fontes.py`. Preservar cabeÃ§alhos legais e as regras de documentaÃ§Ã£o do projeto.
2. Atualizar status e validaÃ§Ãµes com revisÃ£o, data, arquivos e evidÃªncias reais. Identificar explicitamente o estado: **refatoraÃ§Ã£o tÃ©cnica concluÃ­da; conferÃªncia visual pendente**.
3. Disponibilizar o guia de conferÃªncia visual no pacote de entrega quando ele for atualizado. Deixar os campos de avaliaÃ§Ã£o visual em branco ou pendentes.
4. Se as figuras programÃ¡ticas forem regeneradas, identificÃ¡-las como documentaÃ§Ã£o da revisÃ£o correspondente e nÃ£o como screenshots ou prova de inspeÃ§Ã£o. NÃ£o revisar visualmente essas figuras nesta fase.
5. Se houver nova entrega portÃ¡til, atualizar manifesto e pacote depois dos testes e reproduzir a validaÃ§Ã£o pelas fontes extraÃ­das. Preservar as evidÃªncias antigas como histÃ³rico identificado.
6. Informar claramente qualquer verificaÃ§Ã£o que nÃ£o pÃ´de ser executada. NÃ£o usar o adiamento visual para omitir verificaÃ§Ãµes automÃ¡ticas possÃ­veis, nem declarar aprovaÃ§Ã£o tÃ©cnica completa se falta uma etapa necessÃ¡ria.

## 8. CritÃ©rios de aceitaÃ§Ã£o

- Os 16 BDF foram contemplados, inclusive todos os mÃ³dulos interiores e as cinco portas de `somador_1bit`.
- Cada conexÃ£o lÃ³gica consumida dentro de um BDF possui um caminho elÃ©trico geomÃ©trico contÃ­nuo, incluindo fan-out, controles, constantes e derivaÃ§Ãµes de barramento.
- NÃ£o hÃ¡ uniÃ£o remota de terminais consumidos sustentada somente por nomes iguais em trechos separados.
- Portas, bit order, interfaces, hierarquia, lÃ³gica, pinagem e padrÃµes elÃ©tricos foram preservados.
- Os sÃ­mbolos entregues e as instÃ¢ncias nos BDF tÃªm geometria de terminais coerente; exportar sÃ­mbolos ou regenerar fontes nÃ£o desfaz o desenho.
- Auditoria geomÃ©trica, anÃ¡lise Quartus, testes dos 16 mÃ³dulos, compilaÃ§Ã£o e simulaÃ§Ã£o da netlist possuem evidÃªncias atuais de sucesso, ou suas pendÃªncias impedem a declaraÃ§Ã£o correspondente.
- NÃ£o hÃ¡ novos curtos, gaps, taps incorretos ou colisÃµes geomÃ©tricas nÃ£o justificadas.
- Os arquivos novos/alterados tÃªm documentaÃ§Ã£o correspondente e o processo de geraÃ§Ã£o reproduz o layout.
- O guia visual cobre todos os mÃ³dulos, permanece sem aprovaÃ§Ã£o preenchida e explica como revisar a legibilidade posteriormente no Quartus.
- A entrega separa aprovaÃ§Ã£o tÃ©cnica automÃ¡tica de aprovaÃ§Ã£o visual. Como a conferÃªncia visual foi adiada, a legibilidade percebida no editor continua pendente atÃ© a revisÃ£o futura.

## 9. Prompt para iniciar a execuÃ§Ã£o futura

> VocÃª Ã© o GPT-6.1 Sol responsÃ¡vel por executar `docs/PLANO_REFATORACAO_VISUAL_QUARTUS.md`. Leia o contexto e congele os contratos funcionais antes de editar. Coordene agentes GPT-6 Luna com esforÃ§o `high` nas frentes delimitadas pelo plano; impeÃ§a escrita concorrente em geradores, contratos, fontes finais e logs. Refatore a geraÃ§Ã£o e os layouts dos 16 BDF para que todas as conexÃµes consumidas sejam trajetos elÃ©tricos visÃ­veis e contÃ­nuos, inclusive nos nÃ­veis interiores atÃ© `somador_1bit` e nas cadeias de cinco e seis bits. Inspire-se nos esquemas de francisco-araujo07/Projeto-ULA sem importar sua lÃ³gica. Preserve comportamento, interfaces, hierarquia, larguras, Ã­ndices, pinagem e padrÃµes elÃ©tricos. Ajuste BSF e fluxo de geraÃ§Ã£o conforme necessÃ¡rio e confira QSF/QPF. Valide geometria dos BDF finais, exportaÃ§Ã£o nativa, testes dos 16 mÃ³dulos, compilaÃ§Ã£o e netlist funcional. NÃ£o realize conferÃªncia visual nesta fase: mantenha `docs/GUIA_CONFERENCIA_VISUAL_QUARTUS.md` pronto para uma revisÃ£o posterior e declare essa revisÃ£o pendente. Atualize documentos e resultados somente com evidÃªncias realmente obtidas. Persista atÃ© concluir o escopo tÃ©cnico autorizado ou registrar precisamente os bloqueios e o estado reproduzÃ­vel para retomada.
