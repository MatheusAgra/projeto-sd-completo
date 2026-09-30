# decodificador_operacao.bsf

O BSF é o símbolo de interface da entidade `decodificador_operacao`; não implementa suas equações. Ele expõe `S[2..0]` como entrada de três bits, `D[7..0]` como saída de oito bits e `EXIBE_F` como saída escalar.

Exemplo: S=`101` seleciona D5 no BDF e mantém `EXIBE_F=0`.

Verificação: geração pelo Quartus concluída sem erros ou avisos. As três portas, direções e larguras coincidem com `config/interfaces.json`; o BDF foi testado nos oito valores de S.
