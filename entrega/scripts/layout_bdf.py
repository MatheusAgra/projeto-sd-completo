import copy
import json
import re
from collections import defaultdict
from pathlib import Path


def children(node, tag):
    return [x for x in node if isinstance(x, list) and x and x[0] == tag]


def expanded(graph):
    instances = []
    for original in graph['instances']:
        inst = copy.deepcopy(original)
        inst['layout_name'] = original['name']
        inst['part'] = 0
        if inst['type'] == 'BUF':
            temporary = inst['name'] + '__buffer_net'
            instances.extend([
                dict(inst, type='NOT', name=inst['name'] + '__inv', connections={'IN':inst['connections']['IN'], 'OUT':temporary}),
                dict(inst, type='NOT', name=inst['name'] + '__out', part=1, connections={'IN':temporary, 'OUT':inst['connections']['OUT']})
            ])
        else:
            instances.append(inst)
    return instances


def net_bits(net):
    match = re.fullmatch(r'(\w+)\[(\d+)(?:\.\.(\d+))?\]', net)
    if not match:
        if not re.fullmatch(r'[A-Za-z_]\w*', net):
            raise ValueError(f'Rede inválida: {net}')
        return [net]
    base, high, low = match.groups()
    high, low = int(high), int(low or high)
    if high < low:
        raise ValueError(f'Índices inválidos: {net}')
    return [f'{base}[{i}]' for i in range(low, high + 1)]


def read_layout(graph, path):
    layout = json.loads(path.read_text(encoding='utf-8'))
    if layout.get('version') != 1 or layout.get('module') != graph['name']:
        raise ValueError(f'Contrato de layout divergente: {path}')
    places = layout['instances']
    if set(places) != {i['name'] for i in graph['instances']}:
        raise ValueError(f'Instâncias do layout divergentes: {path}')
    if any(len(p) != 2 or any(type(v) != int or v < 0 for v in p) for p in places.values()):
        raise ValueError(f'Coordenadas inválidas: {path}')
    if len(set(map(tuple, places.values()))) != len(places):
        raise ValueError(f'Células repetidas: {path}')
    return layout


def build(graph, interfaces, layout, quartus, api):
    bname, block_symbol, primitive, pin, txt, q = api
    objects, notices = [], set()
    ports = interfaces[graph['name']]['ports']
    instances = expanded(graph)
    signal_names = {net.split('[')[0].lower() for inst in instances for net in inst['connections'].values()} | {n.lower() for n in ports}
    max_col = max((p[0] for p in layout['instances'].values()), default=0) * 2 + 2
    pin_rows = defaultdict(int)
    for name, spec in ports.items():
        col = 0 if spec['direction'] == 'input' else max_col + 2
        row = pin_rows[col]
        pin_rows[col] += 1
        node = pin(name, spec['direction'], spec['width'], 0, 0)
        pt = children(node, 'pt')[0]
        objects.append({'node':node, 'col':col, 'row':row, 'w':168, 'h':24, 'key':name,
                        'terminals':[{'net':bname(name, spec['width']), 'pt':list(map(int, pt[1:])), 'side':'right' if spec['direction'] == 'input' else 'left'}]})
    for inst in instances:
        kind = inst['type']
        if kind in interfaces:
            node = block_symbol(kind, interfaces[kind]['ports'])
        else:
            node, headers = primitive(kind, quartus)
            notices.update(headers)
        node = copy.deepcopy(node)
        if inst['name'].lower() in signal_names:
            inst['name'] += '__inst'
        labels = children(node, 'text')
        labels[1][1] = q(inst['name'])
        if not children(labels[1], 'invisible'):
            r = children(labels[1], 'rect')[0]
            r[3] = int(r[1]) + max(16, len(inst['name']) * 7)
        r = children(node, 'rect')[0]
        w, h = int(r[3]) - int(r[1]), int(r[4]) - int(r[2])
        r[1:] = [0, 0, w, h]
        terms = []
        for port in children(node, 'port'):
            pt = list(map(int, children(port, 'pt')[0][1:]))
            name = json.loads(children(port, 'text')[0][1]).split('[')[0]
            if pt[0] == 0:
                side = 'left'
            elif pt[0] == w:
                side = 'right'
            elif pt[1] == 0:
                side = 'top'
            elif pt[1] == h:
                side = 'bottom'
            else:
                raise ValueError(f'Porta interior sem acesso: {kind}.{name}')
            terms.append({'net':inst['connections'][name], 'pt':pt, 'side':side})
        col, row = layout['instances'][inst['layout_name']]
        bound_w = (max([w] + [int(children(t, 'rect')[0][3]) for t in labels if not children(t, 'invisible')]) + 7) // 8 * 8
        bound_h = (max([h] + [int(children(t, 'rect')[0][4]) for t in labels if not children(t, 'invisible')]) + 7) // 8 * 8
        objects.append({'node':node, 'col':col * 2 + 2 + inst['part'], 'row':row, 'w':bound_w, 'h':bound_h, 'key':inst['name'], 'terminals':terms})
    nets = defaultdict(list)
    for obj in objects:
        for terminal in obj['terminals']:
            terminal['row'] = obj['row']
            nets[terminal['net']].append(terminal)
    vectors = {net:net_bits(net) for net in nets if len(net_bits(net)) > 1}
    taps = []
    for bit in sorted({bit for bits in vectors.values() for bit in bits}):
        buses = [net for net, bits in vectors.items() if bit in bits]
        if bit in nets or len(buses) > 1:
            nets.setdefault(bit, [])
            for bus in buses:
                taps.append((bus, bit))
    taps_x = {pair:512 + i * 24 for i, pair in enumerate(taps)}
    first_col_x = 576 + len(taps) * 24
    counts, widths = defaultdict(lambda:defaultdict(int)), defaultdict(int)
    for obj in objects:
        widths[obj['col']] = max(widths[obj['col']], obj['w'])
        for t in obj['terminals']:
            counts[obj['col']]['left' if t['side'] == 'left' else 'right'] += 1
    starts, x = {}, first_col_x
    for col in range(max_col + 3):
        left = 64 + counts[col]['left'] * 24
        starts[col] = x + left
        x += left + widths[col] + 64 + counts[col]['right'] * 24 + 64
    net_rows = {net:min(t['row'] for t in terminals) for net, terminals in nets.items() if terminals}
    for net in nets:
        if net not in net_rows:
            net_rows[net] = min(net_rows[bus] for bus, bit in taps if bit == net)
    by_row = defaultdict(list)
    for net in sorted(nets):
        by_row[net_rows[net]].append(net)
    row_heights = defaultdict(lambda:64)
    for obj in objects:
        row_heights[obj['row']] = max(row_heights[obj['row']], obj['h'])
    rows, track_y, y = {}, {}, 64
    for row in range(max(o['row'] for o in objects) + 1):
        for i, net in enumerate(by_row[row]):
            track_y[net] = y + 32 + i * 32
        rows[row] = y + 96 + len(by_row[row]) * 32
        y = rows[row] + row_heights[row] + 128
    nodes = []
    counters = defaultdict(lambda:defaultdict(int))
    for obj in objects:
        ox, oy = starts[obj['col']], rows[obj['row']]
        rect = children(obj['node'], 'rect')[0]
        w, h = int(rect[3]) - int(rect[1]), int(rect[4]) - int(rect[2])
        rect[1:] = [ox, oy, ox + w, oy + h]
        nodes.append(obj['node'])
        for t in obj['terminals']:
            px, py = ox + t['pt'][0], oy + t['pt'][1]
            side = 'left' if t['side'] == 'left' else 'right'
            counters[obj['col']][side] += 1
            index = counters[obj['col']][side]
            ex = ox - 32 - index * 24 if side == 'left' else ox + widths[obj['col']] + 32 + index * 24
            path = [(px, py)]
            if t['side'] == 'top':
                path.append((px, oy - 32))
            elif t['side'] == 'bottom':
                path.append((px, oy + h + 32))
            path.extend([(ex, path[-1][1]), (ex, track_y[t['net']])])
            t['escape'] = ex
            for a, b in zip(path, path[1:]):
                if a != b:
                    node = ['connector', ['pt', *a], ['pt', *b]]
                    if len(net_bits(t['net'])) > 1:
                        node.append(['bus'])
                    nodes.append(node)
    junctions = set()
    for net in sorted(nets):
        xs = [t['escape'] for t in nets[net]] + [taps_x[pair] for pair in taps if net in pair]
        if not xs:
            raise ValueError(f'Rede sem terminais/taps: {net}')
        yy = track_y[net]
        stops = sorted(set([256] + xs))
        for i, (a, b) in enumerate(zip(stops, stops[1:])):
            node = ['connector', ['pt', a, yy], ['pt', b, yy]]
            if i == 0:
                node.insert(1, txt(net, 256, yy - 20))
            if len(net_bits(net)) > 1:
                node.append(['bus'])
            nodes.append(node)
        for xx in xs:
            junctions.add((xx, yy))
    for bus, bit in taps:
        xx = taps_x[(bus, bit)]
        nodes.append(['connector', ['pt', xx, track_y[bus]], ['pt', xx, track_y[bit]]])
        junctions.update([(xx, track_y[bus]), (xx, track_y[bit])])
    nodes.extend(['junction', ['pt', *pt]] for pt in sorted(junctions))
    return nodes, notices
