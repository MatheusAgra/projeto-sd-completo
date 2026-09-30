# Layout de decodificador_operacao

Contrato: `version=1`; células `[coluna, faixa]` únicas; instâncias correspondem integralmente ao grafo original.

As três inversões de S ocupam a primeira coluna. Os oito mintermos permanecem em ordem por índice D[0] a D[7], em oito faixas; `show_f` fica separado como saída de habilitação. Cada bit de S e cada NS correspondente tem fan-out entre vários mintermos, e NS_2/NS_1 também alimentam EXIBE_F.

Validação do metadado: 12 nomes originais presentes, sem nomes extras e sem células duplicadas. A coordenada é uma sugestão de agrupamento ao emissor; não representa por si só prova de continuidade elétrica.

Conferência visual no Quartus: pendente, conforme instrução da refatoração. Este documento registra somente a organização lógica proposta.
