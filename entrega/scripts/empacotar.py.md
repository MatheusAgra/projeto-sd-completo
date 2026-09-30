# empacotar.py

Cria ZIP com entrega/ como raiz, excluindo caches db/incremental_db, __pycache__, work e saÃ­das automÃ¡ticas modelsim nÃ£o selecionadas. Inclui fontes, documentos, evidÃªncias e relatÃ³rios nativos relevantes. --extract exige diretÃ³rio novo e rejeita travessia de caminho antes de extrair. Exemplo: python scripts/empacotar.py --extract tmp/recompilacao_zip. O teste de portabilidade requer compilar a cÃ³pia extraÃ­da e conferir pinos/estado, sem depender do banco original.
