import argparse
import csv
import re
from pathlib import Path
from pypdf import PdfReader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('manual', type=Path)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'config/pinagem_de2_115.csv')
    args = parser.parse_args()
    rows = []
    reader = PdfReader(args.manual)
    for page in range(35, 39):
        text = reader.pages[page].extract_text()
        for match in re.finditer(r'((?:SW|LEDR|LEDG|HEX\d)\[\d+\])\s+PIN_(\w+)\s+[^\n]+?\s+(2\.5V|3\.3V|Depending on JP[67])\s*(?:\n|$)', text):
            signal, location, standard = match.groups()
            if signal.startswith('SW') and int(signal[3:-1]) > 12:
                continue
            io = '3.3-V LVTTL' if standard in ('3.3V', 'Depending on JP6') else '2.5 V'
            rows.append({'sinal':signal, 'pino':location, 'padrao_io':io, 'origem':f'DE2-115 User Manual PDF pagina {page + 1}; {standard}; enunciado pagina 3'})
    required = {f'SW[{i}]' for i in range(13)} | {f'LEDR[{i}]' for i in range(18)} | {f'LEDG[{i}]' for i in range(9)} | {f'HEX{h}[{i}]' for h in range(8) for i in range(7)}
    if {r['sinal'] for r in rows} != required or len(rows) != len(required):
        raise ValueError('Pinagem incompleta ou duplicada')
    if len({r['pino'] for r in rows}) != len(rows):
        raise ValueError('Conflito de pinos')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['sinal', 'pino', 'padrao_io', 'origem'])
        writer.writeheader()
        writer.writerows(rows)
    print(f'{len(rows)} pinos extraidos')


if __name__ == '__main__':
    main()
