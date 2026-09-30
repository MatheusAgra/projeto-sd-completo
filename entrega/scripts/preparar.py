import argparse
import json
import re
import shutil
import subprocess
import hashlib
from pathlib import Path
from gerar_bdf import emit, parse
from validar_estrutura import check
from limpar_gerados import strip_nonlegal


def dependency_order(root, interfaces, selected):
    ordered, visited, active = [], set(), set()
    def visit(name):
        if name in visited:
            return
        if name in active:
            raise ValueError(f'Ciclo hierárquico: {name}')
        active.add(name)
        graph = json.loads((root / 'config/grafos' / (name + '.json')).read_text(encoding='utf-8'))
        for inst in graph['instances']:
            if inst['type'] in interfaces:
                visit(inst['type'])
        active.remove(name)
        visited.add(name)
        ordered.append(name)
    for name in selected:
        visit(name)
    return ordered


def run(command, root, log):
    result = subprocess.run([str(p) for p in command], cwd=root, capture_output=True, text=True, errors='replace')
    log.write_text(result.stdout + result.stderr, encoding='utf-8', newline='\n')
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
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--generate-only', action='store_true')
    mode.add_argument('--export-only', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    interfaces = json.loads((root / 'config/interfaces.json').read_text(encoding='utf-8'))
    check(root, args.quartus)
    generated = root / 'simulation/generated'
    logs = root / 'docs/logs'
    generated.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    selected = args.modules or list(interfaces)
    if any(name not in interfaces for name in selected):
        raise ValueError('Modulo desconhecido')
    names = dependency_order(root, interfaces, selected)
    if not args.export_only:
        for name in names:
            graph = json.loads((root / 'config/grafos' / f'{name}.json').read_text(encoding='utf-8'))
            emit(graph, interfaces, root / 'modulos', args.quartus, root / 'config/layouts')
    from validar_geometria import audit
    geometry = audit(root, names=names)
    if geometry['status'] != 'PASS':
        raise ValueError('Auditoria geométrica falhou antes da exportação')
    record_path = root / 'docs/preparacao_atual.json'
    record = json.loads(record_path.read_text(encoding='utf-8')) if record_path.is_file() else {'modules':{}}
    for name in names:
        record['modules'][name] = {'bdf_sha256':hashlib.sha256((root / 'modulos' / (name + '.bdf')).read_bytes()).hexdigest(), 'native':'PENDING'}
    record['status'] = 'PENDING_NATIVE'
    record_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
    if args.generate_only:
        print(f'Geração e auditoria geométrica: {len(names)} módulos; validação nativa pendente', flush=True)
        return
    executable = args.quartus / 'bin64/quartus_map.exe'
    if not executable.is_file():
        raise FileNotFoundError(f'Quartus ausente: {executable}; use --generate-only ou --quartus caminho. HDL/logs antigos não validam os BDF atuais.')
    for name in names:
        spec = interfaces[name]
        run([executable, 'ULA_DE2_115', '--analyze_file=modulos/' + name + '.bdf', '--part=EP4CE115F29C7'], root, logs / f'{name}_analyze.log')
        run([executable, 'ULA_DE2_115', '--convert_bdf_to_verilog=modulos/' + name + '.bdf'], root, logs / f'{name}_convert.log')
        source = root / 'modulos' / f'{name}.v'
        content = source.read_text(encoding='utf-8')
        content = strip_nonlegal(content)
        target = generated / f'{name}.v'
        target.write_text(content, encoding='utf-8', newline='\n')
        source.unlink()
        run([executable, 'ULA_DE2_115', '--generate_symbol=simulation/generated/' + name + '.v'], root, logs / f'{name}_symbol.log')
        native = root / f'{name}.bsf'
        native.write_text(strip_nonlegal(native.read_text(encoding='utf-8')), encoding='utf-8', newline='\n')
        if symbol_ports(native) != spec['ports']:
            raise ValueError(f'Simbolo nativo divergente: {name}')
        native_dir = generated / 'native_symbols'
        native_dir.mkdir(exist_ok=True)
        shutil.move(str(native), str(native_dir / f'{name}.bsf'))
        (native_dir / f'{name}.bsf.md').write_text(f'# {name}: BSF nativo de conferência\n\nPortas conferidas contra o contrato. A geometria canônica entregue permanece em modulos/{name}.bsf e é a mesma embutida nos BDF; este símbolo nativo não a substitui.\n', encoding='utf-8', newline='\n')
        vports = {}
        for direction, width, port in re.findall(r'(input|output)\s+wire\s*(\[\d+:\d+\])?\s*(\w+)\s*;', content):
            numbers = re.findall(r'\d+', width)
            vports[port] = {'direction':direction, 'width':int(numbers[0]) - int(numbers[1]) + 1 if numbers else 1}
        if vports != spec['ports']:
            raise ValueError(f'HDL exportado divergente: {name}')
        (generated / f'{name}.v.md').write_text(f'# {name}.v\n\nHDL exportado nativamente do BDF `{name}.bdf` pelo Quartus 21.1. Usado apenas para simulacao e geracao do BSF; nao consta como fonte no QSF. Portas conferidas automaticamente contra `interfaces.json`. Implementacao estrutural derivada dos conectores reais.\n\nAviso legal Intel preservado. Metadados PROGRAM/VERSION/CREATED removidos sem alterar tokens funcionais. A validacao funcional se encontra em `docs/VALIDACAO.md`; exportacao nao equivale a simulacao.\n', encoding='utf-8', newline='\n')
        record['modules'][name].update(native='PASS', verilog_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
        record['status'] = 'PASS' if set(record['modules']) == set(interfaces) and all(p['native'] == 'PASS' for p in record['modules'].values()) else 'PENDING_NATIVE'
        record_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
        print(f'{name}: analyze/convert/symbol PASS; geometria BSF canônica preservada', flush=True)


if __name__ == '__main__':
    main()
