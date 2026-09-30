import argparse
import json
import re
from collections import Counter
from pathlib import Path
from gerar_bdf import parse, primitive


def bits(net):
    match = re.fullmatch(r'([A-Za-z_][A-Za-z_0-9]*)\[(\d+)(?:\.\.(\d+))?\]', net)
    if not match:
        if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', net):
            raise ValueError(f'Rede invalida: {net}')
        return [net]
    name, high, low = match.groups()
    return [f'{name}[{i}]' for i in range(int(low or high), int(high) + 1)]


def check(root, quartus):
    interfaces = json.loads((root / 'config/interfaces.json').read_text(encoding='utf-8'))
    graphs = {}
    dependencies = {}
    for name, spec in interfaces.items():
        path = root / 'config/grafos' / (name + '.json')
        graph = json.loads(path.read_text(encoding='utf-8'))
        if graph['name'] != name:
            raise ValueError(f'Entidade divergente: {path}')
        graphs[name] = graph
        drivers = Counter()
        consumers = set()
        dependency = set()
        instance_names = set()
        for port, data in spec['ports'].items():
            net = port if data['width'] == 1 else f'{port}[{data["width"] - 1}..0]'
            if data['direction'] == 'input':
                drivers.update(bits(net))
            else:
                consumers.update(bits(net))
        wire_dependencies = {}
        for inst in graph['instances']:
            if inst['name'] in instance_names:
                raise ValueError(f'Instancia duplicada: {name}.{inst["name"]}')
            instance_names.add(inst['name'])
            if inst['type'] in interfaces:
                ports = interfaces[inst['type']]['ports']
                dependency.add(inst['type'])
            elif inst['type'] == 'BUF':
                ports = {'IN':{'direction':'input','width':1},'OUT':{'direction':'output','width':1}}
            else:
                node, notices = primitive(inst['type'], quartus)
                ports = {}
                for p in [n for n in node if isinstance(n, list) and n[0] == 'port']:
                    label = next(n[1].strip('"') for n in p if n[0] == 'text')
                    direction = next(n[0] for n in p if n[0] in ('input', 'output'))
                    ports[label] = {'direction':direction, 'width':1}
            if set(ports) != set(inst['connections']):
                raise ValueError(f'Portas divergentes: {name}.{inst["name"]}')
            inputs, outputs = [], []
            for port, data in ports.items():
                nets = bits(inst['connections'][port])
                if len(nets) != data['width']:
                    raise ValueError(f'Largura: {name}.{inst["name"]}.{port}')
                if data['direction'] == 'input':
                    consumers.update(nets)
                    inputs.extend(nets)
                else:
                    drivers.update(nets)
                    outputs.extend(nets)
            for net in outputs:
                wire_dependencies[net] = inputs
        missing = consumers - set(drivers)
        multiple = [net for net, count in drivers.items() if count != 1]
        if missing or multiple:
            raise ValueError(f'{name}: sem driver={sorted(missing)}; multiplos={multiple}')
        visited, active = set(), set()
        def visit(net):
            if net in active:
                raise ValueError(f'Ciclo combinacional em {name}: {net}')
            if net in visited:
                return
            active.add(net)
            for child in wire_dependencies.get(net, []):
                visit(child)
            active.remove(net)
            visited.add(net)
        for net in wire_dependencies:
            visit(net)
        dependencies[name] = dependency
    visited, active = set(), set()
    def module(name):
        if name in active:
            raise ValueError(f'Ciclo hierarquico: {name}')
        if name in visited:
            return
        active.add(name)
        for child in dependencies[name]:
            module(child)
        active.remove(name)
        visited.add(name)
    for name in interfaces:
        module(name)
    print(json.dumps({'modules':len(graphs), 'instances':sum(len(g['instances']) for g in graphs.values()), 'status':'PASS'}, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--quartus', type=Path, default=Path('C:/intelFPGA_lite/21.1/quartus'))
    args = parser.parse_args()
    check(args.root, args.quartus)


if __name__ == '__main__':
    main()
