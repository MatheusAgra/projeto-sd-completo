# Avisos da compilação final

O Quartus preservou 36 avisos em `logs/compile_final.log`. Nenhum foi suprimido. Esta classificação explica cada código e cada saída constante. A licença de simulação é tratada separadamente em `FERRAMENTAS_SIMULACAO.md`.

| Código | Ocorrências | Significado nesta implementação |
|---|---:|---|
| 13024 | 1 | Resumo das saídas constantes listadas individualmente abaixo |
| 13410 | 27 | Constantes intencionais de segmentos e LEDs |
| 292013 | 1 | LogicLock requer assinatura; o circuito não usa regiões LogicLock e a compilação Lite completou |
| 15714 | 1 | Drive strength e slew rate permanecem nos padrões do Fitter; todas as 96 localizações e padrões de I/O estão atribuídos |
| 332012 | 2, Critical Warning | SDC ausente; o enunciado não define orçamento temporal e não foi criado clock artificial |
| 332068 | 4 | Ausência de clocks coerente com circuito combinacional; nenhum fechamento temporal contra requisito é alegado |

| Saída(s), código 13410 | Valor | Justificativa |
|---|---|---|
| HEX3[6], HEX5[6] | VCC | Segmento g apagado nas dezenas 0/1 das entradas 00..15 |
| HEX3[2], HEX3[1], HEX5[2], HEX5[1] | GND | Segmentos c/b acesos nas dezenas 0/1 das entradas 00..15 |
| HEX6[6], HEX6[5], HEX6[4], HEX6[3], HEX6[2], HEX6[1], HEX6[0] | VCC | Display HEX6 completamente apagado, ativo em zero |
| HEX7[6], HEX7[5], HEX7[4], HEX7[3], HEX7[2], HEX7[1], HEX7[0] | VCC | Display HEX7 completamente apagado, ativo em zero |
| LEDG[8], LEDG[7] | GND | LEDs verdes não utilizados apagados |
| LEDR[17], LEDR[16], LEDR[15], LEDR[14], LEDR[13] | GND | LEDs vermelhos não utilizados apagados |

A soma 1+27+1+1+2+4 é 36. Os avisos de I/O não são evidência de falta de pino: a tabela `.pin` do Fitter foi comparada integralmente ao CSV. Os valores padrão de drive/slew não foram substituídos por escolhas sem requisito elétrico validado. A conferência de JP6/JP7 e o teste físico permanecem pendentes.

`scripts/relatar_caminhos.tcl` produziu um relatório adicional TimeQuest sem restrições inventadas: maior atraso estimado 23,788 ns entre SW[5] e HEX0[1], Slow 1200mV 85C. Essa execução teve zero erros e um aviso próprio de ausência de SDC; não muda a contagem da compilação completa.

A simulação da netlist mapeada teve avisos do Icarus sobre coerção de portas oe/devoe da biblioteca oficial. O log foi preservado; os testes passaram, mas não há alegação de suporte oficial de Icarus pelo Quartus. O diagnóstico TBBmalloc de substituição de alocação, quando presente no runtime, não é um aviso de lógica nem foi contado como erro de projeto.
