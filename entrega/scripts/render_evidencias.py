import argparse
import json
import math
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from gerar_bdf import parse


ROOT = Path(__file__).resolve().parents[1]
FONT = 'C:/Windows/Fonts/arial.ttf'


def find(node, kind):
    return next((n for n in node if isinstance(n, list) and n[0] == kind), None)


def render_bdf(path, output):
    nodes = parse(path.read_text(encoding='utf-8'))
    bounds = []
    for node in nodes:
        rect = find(node, 'rect')
        if rect:
            bounds.append((int(rect[3]), int(rect[4])))
        for p in [n for n in node if isinstance(n, list) and n[0] == 'pt']:
            bounds.append((int(p[1]), int(p[2])))
    width = max(x for x, y in bounds) + 128
    height = max(y for x, y in bounds) + 128
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    def paint(node, ox=0, oy=0):
        if not node:
            return
        kind = node[0]
        if find(node, 'invisible'):
            return
        if kind == 'text':
            rect = find(node, 'rect')
            font = find(node, 'font')
            size = find(font, 'font_size') if font else None
            pixels = max(8, round(int(size[1]) * 1.33) if size else 12)
            value = json.loads(node[1])
            draw.text((ox + int(rect[1]), oy + int(rect[2])), value, fill='black', font=ImageFont.truetype(FONT, pixels))
        elif kind == 'line':
            points = [n for n in node if isinstance(n, list) and n[0] == 'pt']
            thickness = find(node, 'line_width')
            draw.line([(ox + int(p[1]), oy + int(p[2])) for p in points], fill='black', width=int(thickness[1]) if thickness else 1)
        elif kind in ('rectangle', 'circle'):
            rect = find(node, 'rect')
            box = [ox + int(rect[1]), oy + int(rect[2]), ox + int(rect[3]), oy + int(rect[4])]
            (draw.rectangle if kind == 'rectangle' else draw.ellipse)(box, outline='black', width=1)
        elif kind == 'arc':
            rect = find(node, 'rect')
            points = [n for n in node if isinstance(n, list) and n[0] == 'pt']
            box = [ox + int(rect[1]), oy + int(rect[2]), ox + int(rect[3]), oy + int(rect[4])]
            cx, cy = (int(rect[1]) + int(rect[3])) / 2, (int(rect[2]) + int(rect[4])) / 2
            rx, ry = (int(rect[3]) - int(rect[1])) / 2, (int(rect[4]) - int(rect[2])) / 2
            angles = [math.degrees(math.atan2((int(p[2]) - cy) / ry, (int(p[1]) - cx) / rx)) % 360 for p in points]
            if (angles[1] - angles[0]) % 360 > 180:
                angles.reverse()
            draw.arc(box, start=angles[0], end=angles[1], fill='black', width=1)
        elif kind in ('symbol', 'pin'):
            rect = find(node, 'rect')
            for child in [n for n in node if isinstance(n, list) and n[0] not in ('rect', 'pt')]:
                paint(child, int(rect[1]), int(rect[2]))
        elif kind == 'connector':
            points = [n for n in node if isinstance(n, list) and n[0] == 'pt']
            draw.line([(int(p[1]), int(p[2])) for p in points], fill='black', width=3 if find(node, 'bus') else 1)
            for child in [n for n in node if isinstance(n, list) and n[0] == 'text']:
                paint(child)
        elif kind == 'junction':
            pt = find(node, 'pt')
            x, y = int(pt[1]), int(pt[2])
            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill='black')
        elif kind == 'port':
            labels = [n for n in node if isinstance(n, list) and n[0] == 'text']
            if len(labels) > 1:
                paint(labels[1], ox, oy)
            for child in [n for n in node if isinstance(n, list) and n[0] == 'line']:
                paint(child, ox, oy)
        elif kind == 'drawing':
            for child in node[1:]:
                if isinstance(child, list):
                    paint(child, ox, oy)
    for node in nodes:
        paint(node)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    output.with_suffix(output.suffix + '.md').write_text(f'# {output.name}\n\nRenderizacao programatica das coordenadas, simbolos e conectores do BDF final `{path.name}`. Nao e screenshot da interface Quartus. A logica e validada pela compilacao e simulacao do BDF exportado; a conferencia na interface sera feita pelo usuario.\n', encoding='utf-8')


def read_vcd(path, ports):
    scope = []
    signals = {}
    history = {}
    timestamps = []
    time = 0
    timescale = ''
    in_timescale = False
    with path.open(encoding='utf-8') as handle:
        for line in handle:
            line = line.strip()
            if line.startswith('$scope'):
                scope.append(line.split()[2])
            elif line.startswith('$upscope'):
                scope.pop()
            elif line.startswith('$timescale'):
                in_timescale = True
            elif in_timescale:
                if line == '$end':
                    in_timescale = False
                else:
                    timescale += line
            elif line.startswith('$var'):
                tokens = line.split()
                signal = tokens[4]
                if len(scope) == 1 and signal in ports:
                    signals[signal] = tokens[3]
                    history.setdefault(tokens[3], [])
            elif line.startswith('#'):
                time = int(line[1:])
                timestamps.append(time)
            elif line.startswith(('b', 'B')):
                value, code = line[1:].split()
                if code in history:
                    history[code].append((time, value))
            elif line and line[0] in '01xXzZ' and line[1:] in history:
                history[line[1:]].append((time, line[0]))
    return signals, history, timestamps, timescale


def render_vcd(name, spec, output, integration=False):
    source = ROOT / 'simulation/waveforms' / f'{name}.vcd'
    signals, history, timestamps, timescale = read_vcd(source, spec['ports'])
    if not signals or not timestamps:
        raise ValueError(f'VCD sem sinais ou tempo: {source}')
    unique = sorted(set(timestamps))
    if integration:
        start_index = min(3959, len(unique) - 2)
        selected = unique[start_index:start_index + 17]
    else:
        selected = unique[:25]
    start, end = selected[0], selected[-1]
    if end == start:
        end += 1
    width, height = 1700, 120 + len(signals) * 72
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT, 20)
    small = ImageFont.truetype(FONT, 16)
    draw.text((20, 12), f'{name}  VCD real  intervalo {start}..{end}  escala {timescale}', fill='black', font=font)
    left, right = 160, width - 30
    def xx(t):
        return left + (t - start) * (right - left) / (end - start)
    for tick in selected:
        draw.line((xx(tick), 55, xx(tick), height - 25), fill='#dddddd')
        if len(selected) <= 17 or selected.index(tick) % 2 == 0:
            label = format(tick / 1000, 'g') if timescale == '1ps' else str(tick)
            draw.text((xx(tick) - 12, 50), label, fill='black', font=small)
    if timescale == '1ps':
        draw.text((15, 50), 'tempo ns', fill='black', font=small)
    for row, (signal, code) in enumerate(signals.items()):
        y = 100 + row * 72
        draw.text((15, y - 5), signal, fill='black', font=font)
        entries = history[code]
        value = 'x'
        for t, val in entries:
            if t <= start:
                value = val
            else:
                break
        changes = [(start, value)] + [(t, val) for t, val in entries if start < t < end] + [(end, '')]
        for index in range(len(changes) - 1):
            t, val = changes[index]
            next_t = changes[index + 1][0]
            x1, x2 = xx(t), xx(next_t)
            if spec['ports'][signal]['width'] == 1:
                level = y - 10 if val == '1' else y + 20
                draw.line((x1, level, x2, level), fill='#174a7e', width=2)
                if index:
                    draw.line((x1, y - 10, x1, y + 20), fill='#174a7e', width=2)
            else:
                draw.rectangle((x1, y - 10, x2, y + 24), outline='#174a7e', width=2)
                value_text = ('0x' + format(int(val, 2), 'X')) if re.fullmatch('[01]+', val) else val
                if x2 - x1 > len(value_text) * 9 + 8:
                    draw.text((x1 + 4, y - 5), value_text, fill='black', font=small)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    output.with_suffix(output.suffix + '.md').write_text(f'# {output.name}\n\nRecorte do VCD realmente executado `{source.name}`, intervalo {start}..{end}, timescale {timescale}. Barramentos exibidos em hexadecimal. Dados lidos do arquivo de simulacao, nao do modelo esperado. O VCD completo preserva toda a bateria. Este recorte nao e analise temporal pos-fitting.\n', encoding='utf-8')
    source.with_suffix('.vcd.md').write_text(f'# {source.name}\n\nWaveform registrada pelo simulador durante `tb_{name}.sv` contra o Verilog efetivamente exportado do BDF. Timescale {timescale}; contem valores observados e mudancas da bateria executada. Resultado e contagem em `docs/logs/sim_{name}.log` e `docs/VALIDACAO.md`.\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--circuits-only', action='store_true')
    args = parser.parse_args()
    interfaces = json.loads((ROOT / 'config/interfaces.json').read_text(encoding='utf-8'))
    for name, spec in interfaces.items():
        render_bdf(ROOT / 'modulos' / f'{name}.bdf', ROOT / 'docs/diagramas' / f'{name}.png')
        if not args.circuits_only:
            render_vcd(name, spec, ROOT / 'simulation/waveforms' / f'{name}.png')
    if not args.circuits_only:
        render_vcd('ula_de2_115', interfaces['ula_de2_115'], ROOT / 'simulation/waveforms/ula_integracao.png', integration=True)


if __name__ == '__main__':
    main()
