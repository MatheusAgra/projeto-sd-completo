# Guia para futura conferência visual dos esquemas Quartus

Preparado em 30/09/2026. **Conferência visual não realizada.** Este documento orienta uma revisão posterior à execução do [plano de refatoração](PLANO_REFATORACAO_VISUAL_QUARTUS.md); não é evidência de aprovação dos arquivos atuais ou futuros.

Os layouts atuais usam corredores verticais exclusivos por terminal e troncos
horizontais contínuos em faixas reservadas. Essa escolha permite auditoria por
contato físico, mas gera folhas extensas e cruzamentos interiores sem junção.
A revisão futura deve avaliar especialmente a extensão dos caminhos, a leitura
do carry e a distinção entre cruzamento e tap. O modelo de taps/cruzamentos
ainda exige confirmação nativa depois da instalação do Quartus.

Antes da revisão, consultar
[REFATORACAO_VISUAL_TECNICA.md](../entrega/docs/REFATORACAO_VISUAL_TECNICA.md),
`entrega/docs/refatoracao_tecnica.json` e
`entrega/docs/validacao_nativa_atual.json`. HDL, SOF, ZIP, relatório e figuras
anteriores permanecem históricos até novas exportações/testes e atualização
da entrega. Não usar essas figuras como representação dos trajetos novos.

## 1. Objetivo

Verificar, no editor de esquemas do Quartus, que os fios podem ser seguidos entre suas origens e destinos e que os 16 módulos são legíveis. A inspeção deve chegar aos níveis internos, incluindo as portas XOR, AND e OR do somador de um bit; a aparência do topo não basta.

A auditoria geométrica e os testes funcionais serão consultados como evidências separadas. Um teste aprovado não comprova a qualidade visual, e uma linha que parece tocar uma porta não comprova sozinha sua conexão elétrica.

## 2. Preparação na ocasião da revisão

1. Registrar a revisão Git ou identificação do pacote que será examinado. Conferir se BDF, BSF e relatórios técnicos correspondem à mesma revisão.
2. Abrir `entrega/ULA_DE2_115.qpf` no Quartus Prime Lite 21.1, ou registrar a versão efetivamente usada.
3. Conferir o projeto e a entidade de topo `ula_de2_115`. Abrir os BDF de `entrega/modulos/`, evitando cópias antigas ou arquivos temporários.
4. Usar o repositório [Projeto-ULA](https://github.com/francisco-araujo07/Projeto-ULA) como referência de organização dos fios, não como referência funcional ou de pinagem.
5. Fazer uma vista geral da folha e depois ampliar portas, junções e taps. Avaliar rótulos em uma escala confortável de leitura, sem depender apenas da opção de ajustar a folha inteira à janela.
6. Conferir a hierarquia pelos blocos e abrir seus BDF correspondentes. Se navegar pela instância não estiver disponível, abrir o arquivo pelo nome. Não revisar apenas o símbolo BSF.
7. Manter uma revisão identificada durante toda a conferência. Se corrigir algo, registrar a nova revisão e repetir as verificações afetadas.

## 3. Checklist comum a todos os BDF

Para cada módulo, marcar os itens abaixo somente depois de examiná-los:

- [ ] Entradas, processamento e saídas têm organização reconhecível; as etapas não parecem distribuídas aleatoriamente.
- [ ] Todos os destinos consumidos podem ser alcançados seguindo um fio ou barramento desde sua origem, sem procurar outra ocorrência do nome em um trecho isolado.
- [ ] Os fios chegam exatamente às portas; não há pequenos espaços, endpoints deslocados ou linhas que apenas passam perto de um terminal.
- [ ] Ramificações têm conexão clara e junções apropriadas.
- [ ] Cruzamentos de redes diferentes não sugerem conexão indevida; trajetos paralelos não se sobrepõem.
- [ ] Os cruzamentos registrados em `unjoined_crossings` são claros ao leitor e concordam com a análise nativa; nenhum foi presumido como junção pela aparência.
- [ ] Barramentos são distinguíveis de fios escalares e suas larguras, nomes, fatias e bits podem ser lidos.
- [ ] Cada derivação chega ao bit e à porta esperados; o uso de nomes nos taps identifica o mapeamento sem ocultar um trajeto interrompido.
- [ ] Rótulos não encobrem portas, símbolos, fios, outros nomes ou junções.
- [ ] Os fios não atravessam o corpo dos blocos; controles, carry e dados têm corredores compreensíveis.
- [ ] As folhas extensas permitem seguir cada caminho em zoom confortável; o leitor não perde a origem ao navegar entre faixas ou colunas.
- [ ] GND/VCC e sinais com vários consumidores têm distribuição visível; terminais intencionalmente sem uso estão documentados.
- [ ] Não há elementos cortados nos limites da folha nem trechos soltos sem explicação.
- [ ] O símbolo BSF correspondente apresenta nomes, direções e larguras corretos e coincide com a interface usada pelos pais.
- [ ] Os BSF canônicos de `modulos/` coincidem com os símbolos embutidos; os BSF nativos de conferência em `simulation/generated/native_symbols/` não foram usados para substituir a geometria.
- [ ] Foram registrados problemas e evidências da revisão, ou foi registrado que nenhum problema visual foi encontrado nesse módulo.

Não usar nomes de redes para presumir ligação onde o desenho tem uma interrupção. Nomes devem ajudar a leitura; o trajeto deve mostrar a ligação.

## 4. Ordem e pontos específicos por módulo

| Ordem | BDF | O que acompanhar no desenho | Estado inicial |
|---:|---|---|---|
| 1 | `somador_1bit.bdf` | A/B até XOR e AND; `fa_P` até XOR e AND; Cin até os dois consumidores; `fa_G`/`fa_H` até OR; S e Cout até saídas. | Pendente |
| 2 | `somador_subtrator_5bit.bdf` | Cinco etapas por bit; cada Cout até o próximo Cin; SUB até as XOR e Cin inicial; A/B/BX/R por bit. Abrir `somador_1bit`. | Pendente |
| 3 | `somador_subtrator_6bit.bdf` | Seis etapas, carry contínuo, SUB e operandos; montagem de todos os bits de resultado. Abrir `somador_1bit`. | Pendente |
| 4 | `sm_para_c2.bdf` | Sinal/magnitude, XOR e cadeia de soma; constantes e formação dos seis bits. | Pendente |
| 5 | `c2_para_sm.bdf` | Caminhos de sinal e magnitude, lógica de seleção, somadores internos e saída. | Pendente |
| 6 | `negador_c2_6bit.bdf` | Inversão de cada bit, soma da constante e propagação de carry até a saída. | Pendente |
| 7 | `modulo2_soma_sub.bdf` | Entradas/SUB até somador; resultado até conversor; saída final. Abrir os dois filhos e seus descendentes. | Pendente |
| 8 | `comparador_c2_6bit.bdf` | Comparações por bit, sinal, reduções e saídas EQ/GT/LT; fan-out dos operandos. | Pendente |
| 9 | `logica_5bit.bdf` | AND e XOR de todos os cinco bits, incluindo sinal; composição `{L4,0,L3,L2,L1,L0}` e constante. | Pendente |
| 10 | `decodificador_operacao.bdf` | Três bits S, inversões e ramificações até D[7..0] e EXIBE_F. | Pendente |
| 11 | `mux_resultado_8x6.bdf` | Em cada uma das seis faixas, oito candidatos e seleção até OR e F; separar leitura dos controles e dados. | Pendente |
| 12 | `bin_bcd.bdf` | Entrada, conversão e montagem dos dígitos; barramentos e etapas aritméticas. Abrir somador/subtrator de cinco bits e depois somador de um bit. | Pendente |
| 13 | `bcd_7seg.bdf` | BCD, inversões compartilhadas e percurso até cada um dos sete segmentos. | Pendente |
| 14 | `display_decimal_2digitos.bdf` | MAG até bin_bcd; dezenas/unidades até dois bcd_7seg; ENABLE e saídas. Abrir os filhos. | Pendente |
| 15 | `ula_core.bdf` | A/B até conversões e operações; S até controle; candidatos até mux; comparação até STATUS; todos os filhos. | Pendente |
| 16 | `ula_de2_115.bdf` | SW até ULA/displays/espelhamento; F/STATUS até LEDG; HEX e habilitações; constantes. Abrir core e cadeia dos displays. | Pendente |

Em um módulo compartilhado, uma revisão completa do BDF cobre sua implementação interna, mas cada ocorrência no pai ainda precisa ter seus terminais e trajetos conferidos.

## 5. Inspeções de integração e arquivos auxiliares

- [ ] Os 16 BDF estão disponíveis e o QSF aponta para os arquivos corretos. QSF/QPF são configurações; sua ausência de fios gráficos é esperada.
- [ ] Símbolos hierárquicos têm nomes legíveis, espaçamento suficiente e portas sem ambiguidades.
- [ ] A entrada B do core corresponde à fatia SW[9..5], a entrada A a SW[4..0], e S a SW[12..10]; não há inversão visual ou elétrica dos bits.
- [ ] A cadeia de displays chega aos HEX corretos, com habilitação e polaridade conforme o contrato existente.
- [ ] É possível seguir carry em todos os somadores e seguir o sinal até suas saídas em todos os conversores.
- [ ] Figuras de documentação, se entregues, correspondem à revisão; a conferência decisiva foi feita nos BDF abertos no Quartus.
- [ ] Existem evidências técnicas atuais da auditoria geométrica, análise/exportação, simulações e compilação, sem reutilizar aprovação histórica para fontes alteradas.

## 6. Registro da revisão

Preencher apenas quando a conferência for efetivamente executada:

| Campo | Valor |
|---|---|
| Responsável | A preencher |
| Data e hora local | A preencher |
| Revisão Git/pacote | A preencher |
| Versão do Quartus | A preencher |
| Módulos examinados | A preencher — necessário 16/16 |
| Evidências técnicas consultadas | A preencher |
| Resultado visual | Pendente |
| Pendências | A preencher |

Para cada ocorrência, usar este registro:

| ID | Módulo/instância | Rede/porta e região da folha | Problema observado | Impacto | Evidência | Correção/revisão | Estado |
|---|---|---|---|---|---|---|---|
| A preencher | A preencher | A preencher | A preencher | Elétrico possível / legibilidade | Caminho do screenshot, se capturado | A preencher | Pendente |

Se forem capturados screenshots no futuro, identificar revisão, módulo e região; registrar uma vista geral e detalhes suficientes dos problemas. Não atribuir às figuras programáticas o status de screenshot do Quartus.

## 7. Aceitação futura e tratamento das correções

Aprovar a revisão visual somente depois de examinar os 16 BDF, chegar aos módulos interiores e confirmar trajetos legíveis, portas/taps claros, rótulos sem sobreposição e ausência de dependência de trechos isolados ligados apenas pelo nome.

Se uma correção mudar posição de portas, geometria de símbolos, conectores, barramentos, taps ou junções, repetir auditoria geométrica, análise/exportação nativa e testes dos módulos afetados e seus pais; ampliar para integração/compilação conforme o impacto. Alterações só em rótulos gráficos também precisam preservar os rótulos elétricos e ser verificadas quanto a cortes e sobreposição.

Registrar separadamente: aprovação técnica automática, aprovação visual e teste físico em placa. Este guia não inclui programação do FPGA, confirmação de jumpers ou teste em placa. Enquanto houver módulos não examinados ou problemas relevantes sem resolução, manter a conferência visual pendente.
