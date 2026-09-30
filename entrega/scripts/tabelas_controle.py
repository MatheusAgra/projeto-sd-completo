import argparse
from pathlib import Path


def emit(output):
    output.mkdir(parents=True, exist_ok=True)
    logic = [
        '# Mapas e tabela de logica_5bit',
        '',
        'A operacao bit a bit recebe os cinco bits brutos de sinal e magnitude. Para cada posicao i, `A_AND_B[i] = A_SM[i] AND B_SM[i]` e `A_XOR_B[i] = A_SM[i] XOR B_SM[i]`.',
        '',
        '## Tabela de verdade por bit',
        '',
        '| A | B | AND | XOR |',
        '|---:|---:|---:|---:|',
        '| 0 | 0 | 0 | 0 |',
        '| 0 | 1 | 0 | 1 |',
        '| 1 | 0 | 0 | 1 |',
        '| 1 | 1 | 1 | 0 |',
        '',
        '## Mapas de Karnaugh de duas variaveis',
        '',
        'Colunas em ordem Gray B=0,1; linhas A=0,1.',
        '',
        '| AND\\ A/B | B=0 | B=1 |',
        '|---|---:|---:|',
        '| A=0 | 0 | 0 |',
        '| A=1 | 0 | 1 |',
        '',
        '| XOR\\ A/B | B=0 | B=1 |',
        '|---|---:|---:|',
        '| A=0 | 0 | 1 |',
        '| A=1 | 1 | 0 |',
        '',
        '## Alinhamento da saida',
        '',
        'Para `L[4..0]`, ambas as saidas usam `{L4,0,L3,L2,L1,L0}`. O bit de sinal original e preservado; o novo bit de magnitude e zero. A operacao nao normaliza `10000`: `10000 AND 10000 = 100000`.',
        ''
    ]
    decoder = [
        '# Tabela de controle de decodificador_operacao',
        '',
        'Para cada seletor `S[2..0]`, exatamente `D[S]` fica ativo. `EXIBE_F = NOT(S2) AND NOT(S1)`, habilitando F somente para as operacoes 000 e 001.',
        '',
        '| S2 S1 S0 | D[7..0] | EXIBE_F |',
        '|---|---|---:|'
    ]
    for value in range(8):
        decoder.append(f"| {value:03b} | {1 << value:08b} | {int(value < 2)} |")
    decoder.extend(['', '## Mintermos', '', *[f'- `D{i} = ' + ' AND '.join(('S' + str(bit)) if ((i >> bit) & 1) else ('NOT S' + str(bit)) for bit in (2, 1, 0)) + '`.' for i in range(8)], '- `EXIBE_F = NOT S2 AND NOT S1`.', ''])
    (output / 'mapa_logica_5bit.md').write_text('\n'.join(logic), encoding='utf-8')
    (output / 'tabela_decodificador_operacao.md').write_text('\n'.join(decoder), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    emit(args.output if args.output else root / 'docs' / 'tabelas')


if __name__ == '__main__':
    main()
