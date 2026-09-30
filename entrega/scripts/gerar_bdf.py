import argparse
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


def pin(name, direction, width, x, y):
    display = bname(name, width)
    end = 168 if direction == 'input' else 0
    result = ['pin', [direction], ['rect', x, y, x + 168, y + 16], txt(direction.upper(), 80 if direction == 'input' else 4, 0), txt(display, 4 if direction == 'input' else 80, 0), ['pt', end, 8], ['drawing', ['line', ['pt', end, 8], ['pt', 80, 8]]]]
    if direction == 'input':
        result.append(txt('VCC', 128, 7))
    return result


def primitive(name, quartus):
    bundled = Path(__file__).resolve().parents[1] / 'config/primitivas' / (name.lower() + '.bsf')
    paths = [bundled] if bundled.is_file() else list((quartus / 'libraries' / 'primitives').rglob(name.lower() + '.bsf'))
    if len(paths) != 1:
        raise ValueError(f'Primitiva ausente ou ambigua: {name}')
    content = paths[0].read_text(errors='replace')
    node = next(n for n in parse(content) if n[0] == 'symbol')
    notices = re.findall(r'/\*.*?\*/', content, flags=re.S)
    return node, notices


def emit(graph, interfaces, output, quartus, layouts=None):
    from layout_bdf import read_layout, build
    layouts = layouts or Path(__file__).resolve().parents[1] / 'config/layouts'
    layout = read_layout(graph, layouts / (graph['name'] + '.json'))
    nodes, notices = build(graph, interfaces, layout, quartus, (bname, block_symbol, primitive, pin, txt, q))
    output.mkdir(parents=True, exist_ok=True)
    content = '\n'.join(sorted(notices)) + '\n' + dump(['header', q('graphic'), ['version', q('1.4')]]) + '\n'
    content += '\n'.join(dump(n) for n in nodes) + '\n'
    (output / (graph['name'] + '.bdf')).write_text(content, encoding='utf-8', newline='\n')
    legal = (Path(__file__).resolve().parents[1] / 'config/simbolos_legal.txt').read_text(encoding='utf-8')
    symbol = legal + '\n' + dump(['header', q('symbol'), ['version', q('1.2')]]) + '\n' + dump(block_symbol(graph['name'], interfaces[graph['name']]['ports'])) + '\n'
    (output / (graph['name'] + '.bsf')).write_text(symbol, encoding='utf-8', newline='\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('graph', type=Path)
    parser.add_argument('--interfaces', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--layouts', type=Path)
    parser.add_argument('--quartus', type=Path, default=Path('C:/intelFPGA_lite/21.1/quartus'))
    args = parser.parse_args()
    emit(json.loads(args.graph.read_text(encoding='utf-8')), json.loads(args.interfaces.read_text(encoding='utf-8')), args.output, args.quartus, args.layouts)


if __name__ == '__main__':
    main()
