# empacotar.py

Cria ZIP com entrega/ como raiz, excluindo caches db/incremental_db, __pycache__, work e saídas automáticas modelsim não selecionadas. Inclui fontes, documentos, evidências e relatórios nativos relevantes. --extract exige diretório novo e rejeita travessia de caminho antes de extrair. Exemplo: python scripts/empacotar.py --extract tmp/recompilacao_zip. O teste de portabilidade requer compilar a cópia extraída e conferir pinos/estado, sem depender do banco original.
