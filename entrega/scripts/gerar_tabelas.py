import csv
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / 'docs' / 'tabelas'
GRAY = (0, 1, 3, 2)


def combine(a, b):
    differences = [index for index, pair in enumerate(zip(a, b)) if pair[0] != pair[1]]
    if len(differences) != 1:
        return None
    index = differences[0]
    if a[index] == '-' or b[index] == '-':
        return None
    return a[:index] + '-' + a[index + 1:]


def minimize(ones, variables):
    groups = {format(value, f'0{variables}b') for value in ones}
    primes = set()
    while groups:
        used = set()
        next_groups = set()
        ordered = sorted(groups)
        for index, left in enumerate(ordered):
            for right in ordered[index + 1:]:
                merged = combine(left, right)
                if merged is not None:
                    used.add(left)
                    used.add(right)
                    next_groups.add(merged)
        primes.update(groups - used)
        groups = next_groups
    minterms = set(ones)
    covers = {cube: {value for value in minterms if all(bit == '-' or int(bit) == int(value_bit) for bit, value_bit in zip(cube, format(value, f'0{variables}b')))} for cube in primes}
    selected = set()
    uncovered = set(minterms)
    while uncovered:
        essential = {cube for value in uncovered for cube in covers if value in covers[cube] and sum(value in covers[item] for item in covers) == 1}
        if essential:
            selected.update(essential)
            for cube in essential:
                uncovered -= covers[cube]
            continue
        candidates = [cube for cube in covers if covers[cube] & uncovered]
        for count in range(1, len(candidates) + 1):
            valid = [choice for choice in combinations(candidates, count) if uncovered <= set().union(*(covers[cube] for cube in choice))]
            if valid:
                best = min(valid, key=lambda choice: (sum(cube.count('0') + cube.count('1') for cube in choice), choice))
                selected.update(best)
                uncovered.clear()
                break
    return sorted(selected)


def segments(value):
    patterns = ('1000000', '1111001', '0100100', '0110000', '0011001', '0010010', '0000010', '1111000', '0000000', '0010000')
    return patterns[value] if value < 10 else '1111111'


def write_csv(name, headers, rows, description):
    path = ROOT / f'{name}.csv'
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(headers)
        writer.writerows(rows)
    (ROOT / f'{name}.csv.md').write_text(description + '\n', encoding='utf-8')


def kmap_svg(name, maps, title):
    width = 520
    height = 160 + len(maps) * 210
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>', f'<text x="20" y="28" font-family="Arial" font-size="18">{title}</text>']
    for index, (label, layers) in enumerate(maps):
        y0 = 60 + index * 210
        parts.append(f'<text x="20" y="{y0}" font-family="Arial" font-size="14">{label}</text>')
        for layer, values in enumerate(layers):
            x0 = 38 + layer * 250
            label_layer = f'MAG[4]={layer}' if len(layers) == 2 else 'BCD[1:0] colunas'
            row_label = 'MAG[3:2] linhas' if len(layers) == 2 else 'BCD[3:2] linhas'
            parts.append(f'<text x="{x0 + 45}" y="{y0 + 20}" font-family="Arial" font-size="12">{label_layer}</text>')
            parts.append(f'<text x="{x0 + 1}" y="{y0 + 39}" font-family="Arial" font-size="8">{row_label}</text>')
            for column, gray in enumerate(GRAY):
                parts.append(f'<text x="{x0 + 48 + column * 42}" y="{y0 + 40}" font-family="Arial" font-size="10">{gray:02b}</text>')
            for row, gray_row in enumerate(GRAY):
                parts.append(f'<text x="{x0 + 5}" y="{y0 + 62 + row * 30}" font-family="Arial" font-size="10">{gray_row:02b}</text>')
                for column, gray_column in enumerate(GRAY):
                    value = values[gray_row * 4 + gray_column]
                    x = x0 + 32 + column * 42
                    y = y0 + 46 + row * 30
                    parts.append(f'<rect x="{x}" y="{y}" width="42" height="30" fill="none" stroke="#333"/>')
                    parts.append(f'<text x="{x + 18}" y="{y + 20}" font-family="Arial" font-size="14">{value}</text>')
    parts.append('</svg>')
    (ROOT / f'{name}.svg').write_text(''.join(parts), encoding='utf-8')
    (ROOT / f'{name}.svg.md').write_text('Mapa de Karnaugh com linhas e colunas em ordem Gray 00, 01, 11, 10. No mapa de cinco variáveis, cada camada fixa MAG[4] e usa MAG[3:2] nas linhas e MAG[1:0] nas colunas. No mapa de quatro variáveis, BCD[3:2] ocupa as linhas e BCD[1:0] as colunas.\n', encoding='utf-8')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    bcd_rows = []
    threshold_rows = []
    for value in range(32):
        t10, t20, t30 = int(value >= 10), int(value >= 20), int(value >= 30)
        tens, units = divmod(value, 10)
        bcd_rows.append([value, format(value, '05b'), t10, t20, t30, format(tens, '04b'), format(units, '04b')])
        threshold_rows.append([value, format(value, '05b'), t10, t20, t30])
    write_csv('bin_bcd_tabela', ['MAG_decimal', 'MAG_binario', 'T10', 'T20', 'T30', 'DEZ', 'UNI'], bcd_rows, 'Tabela completa de MAG=0..31. DEZ e UNI vêm de divisão inteira do valor decimal, sem reutilizar a lógica de portas. 31 é mantido como 31, produzindo DEZ=3 e UNI=1.')
    write_csv('bin_bcd_limites', ['MAG_decimal', 'MAG_binario', 'T10', 'T20', 'T30'], threshold_rows, 'Tabela verdade completa dos predicados de limiar T10=(MAG>=10), T20=(MAG>=20) e T30=(MAG>=30).')
    seg_rows = []
    for value in range(16):
        pattern = segments(value)
        seg_rows.append([value, format(value, '04b'), pattern, *pattern])
    write_csv('bcd_7seg_tabela', ['BCD_decimal', 'BCD', 'SEG_gfedcba', 'g', 'f', 'e', 'd', 'c', 'b', 'a'], seg_rows, 'Tabela literal de referência com SEG[6:0]={g,f,e,d,c,b,a}, ativo em zero. Dígitos 0..9 usam os segmentos convencionais; códigos 10..15 apagam tudo com 1111111, sem estados indiferentes.')
    display_rows = []
    for value in range(32):
        tens, units = divmod(value, 10)
        for enable in (0, 1):
            decade = segments(tens) if enable else '1111111'
            unit = segments(units) if enable else '1111111'
            display_rows.append([value, enable, tens, units, decade, unit])
    write_csv('display_decimal_2digitos_tabela', ['MAG', 'ENABLE', 'DEZ', 'UNI', 'DEZ_SEG_gfedcba', 'UNI_SEG_gfedcba'], display_rows, 'Cobertura combinacional de 32 magnitudes por dois estados de ENABLE. ENABLE=0 força os dois vetores a 1111111; ENABLE=1 mostra DEZ=MAG/10 e UNI=MAG%10.')
    qmaps = []
    for label, bit in (('T10', 10), ('T20', 20), ('T30', 30)):
        layer_values = [[int((value >= bit)) for value in range(layer * 16, layer * 16 + 16)] for layer in range(2)]
        qmaps.append((label, layer_values))
    kmap_svg('bin_bcd_kmaps', qmaps, 'Binário para BCD: mapas dos limiares')
    segment_maps = []
    for segment_index, label in enumerate('gfedcba'):
        values = [int(segments(value)[segment_index] == '1') for value in range(16)]
        segment_maps.append((f'SEG[{6 - segment_index}] ({label})', [values]))
    kmap_svg('bcd_7seg_kmaps', segment_maps, 'BCD para sete segmentos: mapas completos')
    reductions = ['# Reduções Booleanas', '', '## `bin_bcd`', '', 'As comparações são simplificadas para:', '', '- `T10 = MAG[4] OR (MAG[3] AND (MAG[2] OR MAG[1]))`', '- `T20 = MAG[4] AND (MAG[3] OR MAG[2])`', '- `T30 = MAG[4] AND MAG[3] AND MAG[2] AND MAG[1]`', '- `DEZ[0] = (T10 AND NOT T20) OR T30`; `DEZ[1]=T20`; `DEZ[3:2]=0`.', '- O seletor de correção produz `K[4]=T20`, `K[3]=DEZ[0]`, `K[2]=T20`, `K[1]=DEZ[0]`, `K[0]=0`; `UNI=MAG-K` via `somador_subtrator_5bit` com `SUB=1`.', '', 'A tabela e os mapas cobrem os 32 valores. Em 31, DEZ=3, K=30 e UNI=1.', '', '## `bcd_7seg`', '', 'Variáveis: `x=BCD[3]`, `y=BCD[2]`, `z=BCD[1]`, `w=BCD[0]`. Os conjuntos de mintermos em que cada saída ativa em zero assume 1 são:']
    for segment_index, label in enumerate('gfedcba'):
        ones = [value for value in range(16) if segments(value)[segment_index] == '1']
        cubes = minimize(ones, 4)
        terms = []
        for cube in cubes:
            factors = [name if bit == '1' else f'!{name}' for bit, name in zip(cube, 'xyzw') if bit != '-']
            terms.append('(' + ' AND '.join(factors) + ')')
        reductions.append(f'- `SEG[{6 - segment_index}] ({label})`: mintermos 1 `{ones}`; SOP simplificada: ' + ' OR '.join(terms) + '.')
    reductions.extend(['', 'Os mintermos 10..15 aparecem nas saídas iguais a 1, o que implementa explicitamente display apagado para códigos BCD inválidos. Não há dont-cares. A implementação no grafo usa a forma soma de produtos com inversores compartilhados para as quatro entradas.'])
    (ROOT / 'reducoes_bcd_displays.md').write_text('\n'.join(reductions) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
