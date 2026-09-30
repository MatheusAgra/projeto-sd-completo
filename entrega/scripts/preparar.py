import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from gerar_bdf import emit, parse
from validar_estrutura import check
from limpar_gerados import strip_nonlegal


def run(command, root, log):
    result = subprocess.run([str(p) for p in command], cwd=root, capture_output=True, text=True, errors='replace')
    log.write_text(result.stdout + result.stderr, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(f'{command}: codigo {result.returncode}; veja {log}')


def symbol_ports(path):
    node = next(n for n in parse(path.read_text(encoding='utf-8')) if n[0] == 'symbol')
    ports = {}
    for p in [n for n in node if isinstance(n, list) and n[0] == 'port']:
        label = next(n[1].strip('"') for n in p if n[0] == 'text')
        match = re.fullmatch(r'(\w+)(?:\[(\d+)\.\.(\d+)\])?', label)
        name, high, low = match.groups()
        direction = next(n[0] for n in p if n[0] in ('input', 'output'))
        ports[name] = {'direction': direction, 'width':int(high) - int(low) + 1 if high else 1}
    return ports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--quartus', type=Path, default=Path('C:/intelFPGA_lite/21.1/quartus'))
    parser.add_argument('--modules', nargs='*')
    args = parser.parse_args()
    root = args.root.resolve()
    interfaces = json.loads((root / 'config/interfaces.json').read_text(encoding='utf-8'))
    check(root, args.quartus)
    generated = root / 'simulation/generated'
    logs = root / 'docs/logs'
    generated.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    names = args.modules or list(interfaces)
    if any(name not in interfaces for name in names):
        raise ValueError('Modulo desconhecido')
    for name in names:
        graph = json.loads((root / 'config/grafos' / f'{name}.json').read_text(encoding='utf-8'))
        emit(graph, interfaces, root / 'modulos', args.quartus)
    executable = args.quartus / 'bin64/quartus_map.exe'
    for name in names:
        spec = interfaces[name]
        run([executable, 'ULA_DE2_115', '--analyze_file=modulos/' + name + '.bdf', '--part=EP4CE115F29C7'], root, logs / f'{name}_analyze.log')
        run([executable, 'ULA_DE2_115', '--convert_bdf_to_verilog=modulos/' + name + '.bdf'], root, logs / f'{name}_convert.log')
        source = root / 'modulos' / f'{name}.v'
        content = source.read_text(encoding='utf-8')
        content = strip_nonlegal(content)
        target = generated / f'{name}.v'
        target.write_text(content, encoding='utf-8')
        source.unlink()
        run([executable, 'ULA_DE2_115', '--generate_symbol=simulation/generated/' + name + '.v'], root, logs / f'{name}_symbol.log')
        native = root / f'{name}.bsf'
        native.write_text(strip_nonlegal(native.read_text(encoding='utf-8')), encoding='utf-8')
        if symbol_ports(native) != spec['ports']:
            raise ValueError(f'Simbolo nativo divergente: {name}')
        shutil.move(str(native), str(root / 'modulos' / f'{name}.bsf'))
        vports = {}
        for direction, width, port in re.findall(r'(input|output)\s+wire\s*(\[\d+:\d+\])?\s*(\w+)\s*;', content):
            numbers = re.findall(r'\d+', width)
            vports[port] = {'direction':direction, 'width':int(numbers[0]) - int(numbers[1]) + 1 if numbers else 1}
        if vports != spec['ports']:
            raise ValueError(f'HDL exportado divergente: {name}')
        (generated / f'{name}.v.md').write_text(f'# {name}.v\n\nHDL exportado nativamente do BDF `{name}.bdf` pelo Quartus 21.1. Usado apenas para simulacao e geracao do BSF; nao consta como fonte no QSF. Portas conferidas automaticamente contra `interfaces.json`. Implementacao estrutural derivada dos conectores reais.\n\nAviso legal Intel preservado. Metadados PROGRAM/VERSION/CREATED removidos sem alterar tokens funcionais. A validacao funcional se encontra em `docs/VALIDACAO.md`; exportacao nao equivale a simulacao.\n', encoding='utf-8')
        print(f'{name}: analyze/convert/symbol PASS', flush=True)


if __name__ == '__main__':
    main()
