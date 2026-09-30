# verificar_entrega.py

Confere o QSF com somente 16 BDF, interfaces BSF, ausência de processo sequencial no HDL exportado, arquivos/documentos de módulo, logs de testes aprovados, os 96 pinos/I/O e marca de atribuição no arquivo .pin do Fitter, zero registradores/memória/DSP/PLL e .sof presente. --manifest grava hashes SHA-256 de arquivos, excluindo bancos e auxiliares não portáteis. Exemplo: python scripts/verificar_entrega.py --manifest. Passou; o resumo é docs/verificacao_final.json. Não substitui teste em placa.
