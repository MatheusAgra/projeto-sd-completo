> Histórico anterior à refatoração visual. O ZIP, manifesto, SOF, relatório, figuras e logs anteriores não representam os BDF atuais. Os novos checks e pendências estão em docs/REFATORACAO_VISUAL_TECNICA.md.

# manifest.json

Hashes SHA-256 dos arquivos selecionados da entrega. Permite detectar alteracao apos a verificacao. Nao possui hash de si proprio para evitar recursao. Bancos, work e saidas auxiliares modelsim nao selecionadas ficam fora. O pacote deve ser extraido e recompilado pelas fontes, com o SOF correspondente registrado em VALIDACAO.md.
