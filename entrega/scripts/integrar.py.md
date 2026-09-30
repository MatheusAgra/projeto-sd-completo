# integrar.py

Regenera os grafos core/topo e QSF/QPF a partir dos contratos e CSV congelados. Os layouts permanecem separados em config/layouts e não são sobrescritos. Usa somente BDF para síntese. Após executar, validar_refatoracao.py deve conferir hashes das invariantes e a reprodução dos BDF/BSF; preparar.py aplica a ordem filhos antes de pais.

Na prova isolada atual, os grafos core/topo e QSF/QPF ficaram idênticos byte a byte e 32 arquivos de layout permaneceram intactos. LAST_QUARTUS_VERSION é preservado; arquivos já equivalentes não são reescritos. Evidência em docs/integracao_refatoracao.json.
