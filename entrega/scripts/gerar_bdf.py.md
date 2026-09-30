# gerar_bdf.py

Gera um BDF real e um BSF a partir de um grafo JSON de instâncias e de um contrato de portas. A entrada é o caminho do grafo, `--interfaces`, `--output` e opcionalmente `--quartus`.

Cada conexão é um trecho elétrico que termina na coordenada da porta. Redes de mesmo nome conectam trechos separados no Quartus. Vetores usam `[alto..baixo]` e conectores de barramento. As portas do módulo possuem os mesmos nomes elétricos que suas redes. O desenho distribui os símbolos numa grade com espaçamento calculado pela altura máxima.

Primitivas usam os símbolos da biblioteca instalada do Quartus; blocos hierárquicos usam as portas do contrato. Os avisos de copyright das primitivas são preservados no BDF. O símbolo não implementa lógica: o corpo elétrico está no BDF.

`BUF` é uma operação de ligação do grafo, materializada por dois inversores NOT em série, porque a biblioteca instalada não possui `buf.bsf`. Não cria entidade auxiliar nem HDL oculto. O Quartus pode eliminar esses pares durante a otimização. Nomes de instância recebem sufixos `__inv` e `__out`, com rede intermediária `__buffer_net`.

Exemplo de execução: `python entrega/scripts/gerar_bdf.py tmp/gerador_probe/somador_1bit.json --interfaces tmp/gerador_probe/interfaces.json --output tmp/gerador_probe`.

A aceitação requer leitura e conversão nativas do Quartus, além de simulação do HDL exportado. O estado efetivamente verificado é registrado em `docs/STATUS_EXECUCAO.md`; a simples execução deste gerador não comprova a função nem a completude do circuito.
