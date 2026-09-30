# ULA_DE2_115.qsf

Configura Cyclone IV E EP4CE115F29C7, topo `ula_de2_115`, saída `output_files`, os 16 BDF e os 96 pinos físicos. As fontes são relativas à pasta do projeto. O HDL exportado não é cadastrado, evitando entidades duplicadas.

As atribuições de I/O vêm de `config/pinagem_de2_115.csv`. O perfil usa JP6=3,3 V e JP7=2,5 V. O circuito é combinacional e não recebe clock nem restrição de clock fictícia. A ausência de orçamento temporal definido é registrada na validação.

Exemplo: `quartus_sh --flow compile ULA_DE2_115`. O projeto precisa passar análise, síntese, fitting e assembly; o `.sof` só corresponde à versão final se esses passos forem executados após as últimas mudanças.
