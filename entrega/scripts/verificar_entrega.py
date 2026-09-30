import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from preparar import symbol_ports
from validar_estrutura import check
from empacotar import included_files
from validar_nativo import source_hashes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--manifest', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    interfaces = json.loads((root / 'config/interfaces.json').read_text(encoding='utf-8'))
    provenance_path = root / 'docs/preparacao_atual.json'
    if not provenance_path.is_file():
        raise ValueError('Falta proveniência atual dos BDF/HDL: execute preparar.py e a validação nativa')
    provenance = json.loads(provenance_path.read_text(encoding='utf-8'))
    if provenance.get('status') != 'PASS' or set(provenance['modules']) != set(interfaces):
        raise ValueError('Validação nativa dos BDF atuais pendente; logs/HDL anteriores não aprovam esta revisão')
    for name in interfaces:
        entry = provenance['modules'][name]
        for suffix, directory, field in [('.bdf', 'modulos', 'bdf_sha256'), ('.v', 'simulation/generated', 'verilog_sha256')]:
            actual_hash = hashlib.sha256((root / directory / (name + suffix)).read_bytes()).hexdigest()
            if actual_hash != entry[field]:
                raise ValueError(f'Proveniência divergente: {name}{suffix}')
    native_path = root / 'docs/validacao_nativa_atual.json'
    if not native_path.is_file():
        raise ValueError('Falta validação nativa atual: execute validar_nativo.py')
    native = json.loads(native_path.read_text(encoding='utf-8'))
    if native.get('status') != 'PASS' or native.get('sources') != source_hashes(root):
        raise ValueError('Compilação/simulações atuais pendentes ou fontes alteradas')
    if set(native.get('stages', {})) != {'offline', 'export', 'simulation', 'compilation', 'netlist'}:
        raise ValueError('Cobertura nativa incompleta')
    for stage in native['stages'].values():
        log_path = root / stage['log']
        if stage['status'] != 'PASS' or not log_path.is_file() or hashlib.sha256(log_path.read_bytes()).hexdigest() != stage['sha256']:
            raise ValueError('Evidência nativa divergente')
    check(root, Path('C:/intelFPGA_lite/21.1/quartus'))
    qsf = (root / 'ULA_DE2_115.qsf').read_text(encoding='utf-8')
    sources = re.findall(r'^set_global_assignment -name BDF_FILE (.+)$', qsf, flags=re.M)
    if set(sources) != {f'modulos/{n}.bdf' for n in interfaces} or len(sources) != 16:
        raise ValueError('Lista BDF do QSF divergente')
    if re.search(r'-name (VERILOG_FILE|SYSTEMVERILOG_FILE|VHDL_FILE|SOURCE_FILE|IP_FILE|QIP_FILE)', qsf):
        raise ValueError('Fonte extra no projeto sintetizado')
    for name, spec in interfaces.items():
        if symbol_ports(root / 'modulos' / f'{name}.bsf') != spec['ports']:
            raise ValueError(f'BSF divergente: {name}')
        source = (root / 'simulation/generated' / f'{name}.v').read_text(encoding='utf-8')
        without_comments = re.sub(r'/\*.*?\*/|//[^\n]*', '', source, flags=re.S)
        if re.search(r'\b(always|always_comb|always_ff|initial|posedge|negedge)\b', without_comments):
            raise ValueError(f'Estado/comportamento em export: {name}')
        for filename in (f'modulos/{name}.bdf', f'modulos/{name}.bsf', f'simulation/generated/{name}.v', f'simulation/tb_{name}.sv', f'simulation/waveforms/{name}.vcd', f'simulation/waveforms/{name}.png'):
            path = root / filename
            if not path.is_file() or not Path(str(path) + '.md').is_file():
                raise ValueError(f'Arquivo/documentacao ausente: {filename}')
        log = (root / 'docs/logs' / f'sim_{name}.log').read_text(encoding='utf-8-sig')
        if 'FATAL' in log or not re.search(r'PASS|passou', log):
            raise ValueError(f'Simulacao nao aprovada: {name}')
    pins = list(csv.DictReader((root / 'config/pinagem_de2_115.csv').open(encoding='utf-8')))
    actual = {}
    for line in (root / 'output_files/ULA_DE2_115.pin').read_text(encoding='utf-8').splitlines():
        columns = [c.strip() for c in line.split(':')]
        if len(columns) == 7 and re.fullmatch(r'(SW|LEDR|LEDG|HEX\d)\[\d+\]', columns[0]):
            actual[columns[0]] = columns
    if set(actual) != {p['sinal'] for p in pins}:
        raise ValueError('Cobertura fisica divergente no Fitter')
    for row in pins:
        found = actual[row['sinal']]
        if found[1] != row['pino'] or found[3] != row['padrao_io'] or found[6] != 'Y':
            raise ValueError(f'Pino/I/O nao respeitado: {row["sinal"]}: {found}')
    fit = (root / 'output_files/ULA_DE2_115.fit.summary').read_text(encoding='utf-8')
    for metric in ('Total registers', 'Total memory bits', 'Embedded Multiplier 9-bit elements', 'Total PLLs'):
        if not re.search(re.escape(metric) + r'\s*:\s*0(?:\s|$)', fit):
            raise ValueError(f'Recurso nao combinacional: {metric}')
    mapping = (root / 'output_files/ULA_DE2_115.map.rpt').read_text(encoding='utf-8')
    if re.search(r'Inferred latch|latch inferred', mapping, flags=re.I):
        raise ValueError('Latch inferido')
    compile_log = (root / 'docs/logs/compile_final.log').read_text(encoding='utf-8-sig')
    if 'Full Compilation was successful. 0 errors' not in compile_log:
        raise ValueError('Compilacao final nao aprovada')
    sof = root / 'output_files/ULA_DE2_115.sof'
    if not sof.is_file() or sof.stat().st_size == 0:
        raise ValueError('SOF ausente')
    result = {'status':'PASS', 'modules':16, 'pins_verified':len(pins), 'sequential_registers':0, 'memory_bits':0, 'dsp_elements':0, 'sof_sha256':hashlib.sha256(sof.read_bytes()).hexdigest()}
    (root / 'docs/verificacao_final.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    if args.manifest:
        files = {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in included_files(root) if p.name != 'manifest.json'}
        (root / 'manifest.json').write_text(json.dumps({'hash_algorithm':'SHA-256', 'files':files}, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
