# compilar.ps1

Executa quartus_sh --flow compile ULA_DE2_115 na raiz do projeto e falha se o processo retornar erro. Aceita -Quartus para o bin64 instalado. A compilação real inclui análise/síntese, fitting, assembly, TimeQuest e EDA writer. Não programa a placa. Exemplo: scripts/compilar.ps1. A revisão final passou com zero erros; os avisos são indexados e explicados em docs/VALIDACAO.md.
