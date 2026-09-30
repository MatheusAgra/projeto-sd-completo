import argparse
import copy
import json
import re
from pathlib import Path


def parse(text):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+', re.sub(r'/\*.*?\*/|//[^\n]*', '', text, flags=re.S))
    stack = [[]]
    for token in tokens:
        if token == '(':
            node = []
            stack[-1].append(node)
            stack.append(node)
        elif token == ')':
            stack.pop()
        else:
            stack[-1].append(token)
    if len(stack) != 1:
        raise ValueError('Parenteses incompletos')
    return stack[0]


def dump(node):
    return '(' + ' '.join(dump(x) if isinstance(x, list) else str(x) for x in node) + ')'


def q(value):
    return json.dumps(str(value), ensure_ascii=False)


def txt(value, x, y, width=None):
    return ['text', q(value), ['rect', x, y, x + (width or max(16, len(value) * 7)), y + 16], ['font', q('Arial'), ['font_size', 8]]]


def bname(name, width):
    return name if width == 1 else f'{name}[{width - 1}..0]'


def block_symbol(name, ports):
    inputs = [(n, p) for n, p in ports.items() if p['direction'] == 'input']
    outputs = [(n, p) for n, p in ports.items() if p['direction'] == 'output']
    height = max(len(inputs), len(outputs)) * 32 + 64
    node = ['symbol', ['rect', 0, 0, 320, height], txt(name, 24, 0), txt('inst', 24, height - 20)]
    for direction, items in [('input', inputs), ('output', outputs)]:
        for i, (port, spec) in enumerate(items):
            x, y = (0 if direction == 'input' else 320), 32 + i * 32
            display = bname(port, spec['width'])
            line = ['line', ['pt', x, y], ['pt', 16 if x == 0 else 304, y]]
            if spec['width'] > 1:
                line.append(['line_width', 3])
            node.append(['port', ['pt', x, y], [direction], txt(display, 0, 0), txt(display, 20 if x == 0 else 208, y - 8), line])
    node.append(['drawing', ['rectangle', ['rect', 16, 16, 304, height - 32]]])
    return node


def connector(net, x, y, direction, width):
    end = x + (64 if direction == 'output' else -64)
    result = ['connector', txt(net, min(x, end), y - 20), ['pt', x, y], ['pt', end, y]]
    if width > 1:
        result.append(['bus'])
    return result


def pin(name, direction, width, x, y):
    display = bname(name, width)
    end = 168 if direction == 'input' else 0
    result = ['pin', [direction], ['rect', x, y, x + 168, y + 16], txt(direction.upper(), 80, 0), txt(display, 4 if direction == 'input' else 80, 0), ['pt', end, 8], ['drawing', ['line', ['pt', end, 8], ['pt', 80, 8]]]]
    if direction == 'input':
        result.append(txt('VCC', 128, 7))
    return result


def primitive(name, quartus):
    paths = list((quartus / 'libraries' / 'primitives').rglob(name.lower() + '.bsf'))
    if len(paths) != 1:
        raise ValueError(f'Primitiva ausente ou ambigua: {name}')
    content = paths[0].read_text(errors='replace')
    node = next(n for n in parse(content) if n[0] == 'symbol')
    notices = re.findall(r'/\*.*?\*/', content, flags=re.S)
    return node, notices


def emit(graph, interfaces, output, quartus):
    graph = copy.deepcopy(graph)
    instances = []
    for inst in graph['instances']:
        if inst['type'] == 'BUF':
            temporary = inst['name'] + '__buffer_net'
            instances.extend([
                {'type':'NOT', 'name':inst['name'] + '__inv', 'connections':{'IN':inst['connections']['IN'], 'OUT':temporary}},
                {'type':'NOT', 'name':inst['name'] + '__out', 'connections':{'IN':temporary, 'OUT':inst['connections']['OUT']}}
            ])
        else:
            instances.append(inst)
    graph['instances'] = instances
    name = graph['name']
    ports = interfaces[name]['ports']
    signal_names = {net.split('[')[0].lower() for inst in instances for net in inst['connections'].values()} | {n.lower() for n in ports}
    for inst in instances:
        if inst['name'].lower() in signal_names:
            inst['name'] += '__inst'
    nodes = [['header', q('graphic'), ['version', q('1.4')]]]
    notices = set()
    for index, (port, spec) in enumerate(ports.items()):
        x, y = 64, 48 + index * 64
        nodes.append(pin(port, spec['direction'], spec['width'], x, y))
        wire_direction = 'output' if spec['direction'] == 'input' else 'input'
        nodes.append(connector(bname(port, spec['width']), x + (168 if spec['direction'] == 'input' else 0), y + 8, wire_direction, spec['width']))
    row_height = 256
    for inst in graph['instances']:
        if inst['type'] in interfaces:
            symbol = block_symbol(inst['type'], interfaces[inst['type']]['ports'])
        else:
            symbol, headers = primitive(inst['type'], quartus)
            notices.update(headers)
        rect = next(n for n in symbol if isinstance(n, list) and n[0] == 'rect')
        row_height = max(row_height, int(rect[4]) - int(rect[2]) + 96)
    for index, inst in enumerate(graph['instances']):
        if inst['type'] in interfaces:
            symbol = block_symbol(inst['type'], interfaces[inst['type']]['ports'])
        else:
            symbol, headers = primitive(inst['type'], quartus)
        symbol = copy.deepcopy(symbol)
        rect = next(n for n in symbol if isinstance(n, list) and n[0] == 'rect')
        width, height = int(rect[3]) - int(rect[1]), int(rect[4]) - int(rect[2])
        x, y = 480 + index % 3 * 640, 64 + index // 3 * row_height
        rect[1:] = [x, y, x + width, y + height]
        labels = [n for n in symbol if isinstance(n, list) and n[0] == 'text']
        labels[1][1] = q(inst['name'])
        nodes.append(symbol)
        for p in [n for n in symbol if isinstance(n, list) and n[0] == 'port']:
            pt = next(n for n in p if n[0] == 'pt')
            direction = next(n[0] for n in p if n[0] in ('input', 'output'))
            label = next(n[1].strip('"') for n in p if n[0] == 'text')
            port = label.split('[')[0]
            net = inst['connections'][port]
            bits = interfaces[inst['type']]['ports'][port]['width'] if inst['type'] in interfaces else 1
            nodes.append(connector(net, x + int(pt[1]), y + int(pt[2]), direction, bits))
    groups = {}
    for net in [n for inst in instances for n in inst['connections'].values()] + [bname(n, p['width']) for n, p in ports.items()]:
        match = re.fullmatch(r'(\w+)\[(\d+)(?:\.\.(\d+))?\]', net)
        if match:
            base, high, low = match.groups()
            groups.setdefault(base, set()).update(range(int(low or high), int(high) + 1))
    start_y = 64 + ((len(instances) + 2) // 3) * row_height + 64
    for index, (base, indices) in enumerate(groups.items()):
        y = start_y + index * 96
        low, high = min(indices), max(indices)
        nodes.append(connector(f'{base}[{high}..{low}]', 480, y, 'output', high - low + 1))
        nodes.append(['connector', ['pt', 544, y], ['pt', 640 + len(indices) * 80, y], ['bus']])
        for offset, bit in enumerate(sorted(indices)):
            x = 640 + offset * 80
            nodes.append(['connector', txt(f'{base}[{bit}]', x + 4, y + 24), ['pt', x, y], ['pt', x, y + 48]])
            nodes.append(['junction', ['pt', x, y]])
    output.mkdir(parents=True, exist_ok=True)
    (output / f'{name}.bdf').write_text('\n'.join(sorted(notices)) + '\n' + '\n'.join(dump(n) for n in nodes) + '\n', encoding='utf-8')
    (output / f'{name}.bsf').write_text(dump(['header', q('symbol'), ['version', q('1.2')]]) + '\n' + dump(block_symbol(name, ports)) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('graph', type=Path)
    parser.add_argument('--interfaces', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--quartus', type=Path, default=Path('C:/intelFPGA_lite/21.1/quartus'))
    args = parser.parse_args()
    emit(json.loads(args.graph.read_text(encoding='utf-8')), json.loads(args.interfaces.read_text(encoding='utf-8')), args.output, args.quartus)


if __name__ == '__main__':
    main()
