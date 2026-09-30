import argparse
import csv
import hashlib
import json
import re
import uuid
from pathlib import Path
from gerar_bdf import emit
from preparar import dependency_order, symbol_ports
from validar_estrutura import check


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    interfaces = json.loads((root / 'config/interfaces.json').read_text(encoding='utf-8'))
    baseline = json.loads((root / 'docs/refatoracao_baseline.json').read_text(encoding='utf-8'))
    frozen = {p:h for p,h in baseline['files'].items() if (p.startswith('config/grafos/') and p.endswith('.json')) or p in ['config/interfaces.json', 'config/pinagem_de2_115.csv', 'ULA_DE2_115.qsf', 'ULA_DE2_115.qpf'] or (p.startswith('simulation/tb_') and p.endswith('.sv'))}
    for path, expected in frozen.items():
        if digest(root / path) != expected:
            raise ValueError(f'Invariante funcional alterada: {path}')
    check(root, Path('C:/intelFPGA_lite/21.1/quartus'))
    qsf = (root / 'ULA_DE2_115.qsf').read_text(encoding='utf-8')
    sources = re.findall(r'^set_global_assignment -name BDF_FILE (.+)$', qsf, flags=re.M)
    if len(sources) != 16 or set(sources) != {f'modulos/{name}.bdf' for name in interfaces}:
        raise ValueError('Cadastro BDF divergente')
    if re.search(r'-name (VERILOG_FILE|SYSTEMVERILOG_FILE|VHDL_FILE|SOURCE_FILE|IP_FILE|QIP_FILE)', qsf):
        raise ValueError('Fonte extra no QSF')
    pins = list(csv.DictReader((root / 'config/pinagem_de2_115.csv').open(encoding='utf-8')))
    locations = dict(re.findall(r'^set_location_assignment PIN_(\w+) -to (\S+)$', qsf, flags=re.M))
    actual = {signal:pin for pin,signal in locations.items()}
    standards = dict((signal,standard) for standard,signal in re.findall(r'^set_instance_assignment -name IO_STANDARD "([^"]+)" -to (\S+)$', qsf, flags=re.M))
    if len(pins) != 96 or len(actual) != 96 or len(standards) != 96:
        raise ValueError('Cobertura de pinos divergente')
    for row in pins:
        if actual.get(row['sinal']) != row['pino'] or standards.get(row['sinal']) != row['padrao_io']:
            raise ValueError(f'Pinagem/I/O divergente: {row["sinal"]}')
    order = dependency_order(root, interfaces, list(interfaces))
    from validar_geometria import audit
    geometry = audit(root, names=order)
    if geometry['status'] != 'PASS':
        raise ValueError('Auditoria geomÃ©trica dos BDF finais falhou')
    reproducible = []
    work = root.parent / 'tmp'
    work.mkdir(exist_ok=True)
    output = work / ('regeneracao_' + uuid.uuid4().hex)
    output.mkdir()
    for name in order:
        graph = json.loads((root / 'config/grafos' / (name + '.json')).read_text(encoding='utf-8'))
        emit(graph, interfaces, output, Path('C:/intelFPGA_lite/21.1/quartus'), root / 'config/layouts')
        for suffix in ('.bdf', '.bsf'):
            if digest(output / (name + suffix)) != digest(root / 'modulos' / (name + suffix)):
                raise ValueError(f'RegeneraÃ§Ã£o divergente: {name}{suffix}')
            reproducible.append('modulos/' + name + suffix)
        if symbol_ports(output / (name + '.bsf')) != interfaces[name]['ports']:
            raise ValueError(f'Contrato BSF divergente: {name}')
    instance_count = sum(len(json.loads((root / 'config/grafos' / (name + '.json')).read_text(encoding='utf-8'))['instances']) for name in order)
    record = {'status':'PASS_OFFLINE_PENDING_NATIVE', 'visual':'PENDING', 'frozen_files_verified':len(frozen), 'modules':len(order), 'graph_instances':instance_count, 'pins_qsf_csv_verified':len(pins), 'dependency_order':order, 'reproducible':reproducible, 'geometry':geometry,
              'sources':{p:digest(root / p) for p in reproducible}, 'pending':['Quartus analyze/convert/native symbol contracts', '16 testbenches on newly exported HDL', 'Full compilation and Fitter pin/resource/warning comparison', 'Functional mapped netlist simulation', 'Future visual inspection of 16 BDF']}
    path = root / 'docs/refatoracao_tecnica.json'
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ['sources', 'geometry', 'reproducible']}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
