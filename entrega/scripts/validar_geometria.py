import argparse
import copy
import json
import re
from collections import defaultdict
from pathlib import Path

from gerar_bdf import parse


def kids(node, tag):
    return [x for x in node if isinstance(x, list) and x and x[0] == tag]


def descendants(node, tag):
    found = []
    if isinstance(node, list):
        if node and node[0] == tag:
            found.append(node)
        for child in node:
            found.extend(descendants(child, tag))
    return found


def quoted(node):
    return json.loads(node)


def bits(net):
    m = re.fullmatch(r"([A-Za-z_]\w*)\[(\d+)(?:\.\.(\d+))?\]", net)
    if not m:
        return [net]
    base, a, b = m.groups()
    a, b = int(a), int(b or a)
    step = 1 if b >= a else -1
    return [f"{base}[{i}]" for i in range(a, b + step, step)]


def contains_ordered_slice(sequence, part):
    width = len(part)
    return any(sequence[i:i + width] == part for i in range(len(sequence) - width + 1))


def compatible_label(net, label):
    expected, actual = bits(net), bits(label)
    if len(expected) == 1:
        return net == label or net in actual
    match_expected = re.match(r"([A-Za-z_]\w*)\[", net)
    match_actual = re.match(r"([A-Za-z_]\w*)\[", label)
    if not match_expected or not match_actual or match_expected.group(1) != match_actual.group(1):
        return False
    return contains_ordered_slice(actual, expected) or contains_ordered_slice(expected, actual)


def expand(graph):
    result = []
    for src in graph["instances"]:
        if src["type"] != "BUF":
            result.append(src)
            continue
        mid = src["name"] + "__buffer_net"
        result.extend([
            {"name": src["name"] + "__inv", "type": "NOT", "connections": {"IN": src["connections"]["IN"], "OUT": mid}},
            {"name": src["name"] + "__out", "type": "NOT", "connections": {"IN": mid, "OUT": src["connections"]["OUT"]}},
        ])
    return result


class DSU:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.p[b] = a


def geom(bdf):
    nodes = parse(bdf.read_text(encoding="utf-8", errors="replace"))
    symbols, pins, segments, junctions, labels, label_rects = [], [], [], set(), defaultdict(set), []
    for n in nodes:
        if not isinstance(n, list) or not n:
            continue
        if n[0] == "symbol":
            rect = kids(n, "rect")[0]
            ox, oy = int(rect[1]), int(rect[2])
            name = quoted(kids(n, "text")[1][1])
            terms = {}
            for port in kids(n, "port"):
                pt = kids(port, "pt")[0]
                local = (int(pt[1]), int(pt[2]))
                ptxt = kids(port, "text")
                display = quoted(ptxt[0][1])
                pname = display.split("[")[0]
                direction = "input" if any(isinstance(x, list) and x and x[0] == "input" for x in port) else "output"
                width = len(bits(display))
                line_widths = descendants(port, "line_width")
                if width == 1 and any(len(x) > 1 and int(x[1]) > 1 for x in line_widths):
                    width = 2
                terms[pname] = ((ox + local[0], oy + local[1]), direction, width, display)
            symbols.append((name, terms, (ox, oy, int(rect[3]), int(rect[4])), quoted(kids(n, "text")[0][1])))
        elif n[0] == "pin":
            direction = n[1][0]
            ptxt = kids(n, "text")
            name = quoted(ptxt[1][1])
            base = name.split("[")[0]
            pt = kids(n, "pt")[0]
            rect = kids(n, "rect")[0]
            bounds = tuple(map(int, rect[1:]))
            pins.append((base, direction, (int(rect[1]) + int(pt[1]), int(rect[2]) + int(pt[2])), name, bounds))
        elif n[0] == "junction":
            pt = kids(n, "pt")[0]
            junctions.add((int(pt[1]), int(pt[2])))
        elif n[0] == "connector":
            pts = kids(n, "pt")
            if len(pts) < 2:
                continue
            a, b = tuple(map(int, pts[0][1:])), tuple(map(int, pts[1][1:]))
            if a[0] != b[0] and a[1] != b[1]:
                segments.append({"a": a, "b": b, "bus": bool(kids(n, "bus")), "node": n})
                continue
            label = None
            texts = kids(n, "text")
            if texts:
                label = quoted(texts[0][1])
                rect = kids(texts[0], "rect")
                if rect:
                    label_rects.append((label, tuple(map(int, rect[0][1:])), len(segments)))
            segments.append({"a": a, "b": b, "bus": bool(kids(n, "bus")), "label": label, "node": n})
    dsu = DSU()
    points = defaultdict(set)
    terminal_positions = [pt for _, terms, rect, kind in symbols for pt, direction, width, display in terms.values()]
    terminal_positions.extend(pt for _, direction, pt, display, bounds in pins)
    for i, s in enumerate(segments):
        a, b = s["a"], s["b"]
        points[i].update([a, b])
        points[i].update(p for p in terminal_positions if onseg(p, a, b))
    for i, s in enumerate(segments):
        a, b = s["a"], s["b"]
        for j, t in enumerate(segments):
            for p in (t["a"], t["b"]):
                if onseg(p, a, b):
                    points[i].add(p)
        for p in junctions:
            if onseg(p, a, b):
                points[i].add(p)
    for i, s in enumerate(segments):
        ps = sorted(points[i], key=lambda p: (p[0], p[1]) if s["a"][0] != s["b"][0] else (p[1], p[0]))
        for p in ps:
            dsu.find((p, s["bus"]))
        for a, b in zip(ps, ps[1:]):
            dsu.union((a, s["bus"]), (b, s["bus"]))
    tap_pairs = set()
    for p in junctions:
        for i, s in enumerate(segments):
            if onseg(p, s["a"], s["b"]):
                dsu.find((p, s["bus"]))
    for i, s in enumerate(segments):
        for j, t in enumerate(segments[:i]):
            for p in (s["a"], s["b"]):
                if onseg(p, t["a"], t["b"]) and s["bus"] == t["bus"]:
                    dsu.union((p, s["bus"]), (p, t["bus"]))
            for p in (t["a"], t["b"]):
                if onseg(p, s["a"], s["b"]) and s["bus"] == t["bus"]:
                    dsu.union((p, s["bus"]), (p, t["bus"]))
    for s in segments:
        if s.get("label"):
            labels[dsu.find((s["a"], s["bus"]))].add(s["label"])
    for p in junctions:
        scalar_roots, bus_roots = set(), set()
        for s in segments:
            if onseg(p, s["a"], s["b"]):
                (bus_roots if s["bus"] else scalar_roots).add(dsu.find((p, s["bus"])))
        for sr in scalar_roots:
            scalar_labels = {s["label"] for s in segments if s.get("label") and not s["bus"] and dsu.find((s["a"], s["bus"])) == sr}
            for br in bus_roots:
                bus_labels = {s["label"] for s in segments if s.get("label") and s["bus"] and dsu.find((s["a"], s["bus"])) == br}
                if any(slabel in bits(blabel) for slabel in scalar_labels for blabel in bus_labels):
                    tap_pairs.update((sr, br, slabel, blabel) for slabel in scalar_labels for blabel in bus_labels if slabel in bits(blabel))
    labels = defaultdict(set)
    for s in segments:
        if s.get("label"):
            labels[dsu.find((s["a"], s["bus"]))].add(s["label"])
    return symbols, pins, segments, junctions, dsu, labels, tap_pairs, label_rects, nodes


def onseg(p, a, b):
    return (a[0] == b[0] == p[0] and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])) or (a[1] == b[1] == p[1] and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]))


def symbol_signature(node):
    rect = kids(node, "rect")[0]
    ox, oy = int(rect[1]), int(rect[2])
    result = {}
    for port in kids(node, "port"):
        texts = kids(port, "text")
        display = quoted(texts[0][1])
        name = display.split("[")[0]
        pt = kids(port, "pt")[0]
        direction = "input" if any(isinstance(x, list) and x and x[0] == "input" for x in port) else "output"
        result[name] = ((int(pt[1]) - ox, int(pt[2]) - oy), direction, len(bits(display)), display)
    return result


def analyze(root, module, bdf_path):
    interfaces = json.loads((root / "config/interfaces.json").read_text(encoding="utf-8"))
    graph = json.loads((root / "config/grafos" / f"{module}.json").read_text(encoding="utf-8"))
    ports = interfaces[module]["ports"]
    symbols, pins, segments, junctions, dsu, labels, tap_pairs, label_rects, nodes = geom(bdf_path)
    errors = []
    symbol_names = [name for name, terms, rect, kind in symbols]
    pin_names = [display for _, _, _, display, _ in pins]
    for label, values in [("instância", symbol_names), ("pin", pin_names)]:
        seen = set()
        for value in values:
            key = value.casefold()
            if key in seen:
                errors.append(f"{label} duplicado (case-insensitive): {value}")
            seen.add(key)
    for node in nodes:
        if not isinstance(node, list) or not node or node[0] != "symbol":
            continue
        seen_ports = set()
        for port_node in kids(node, "port"):
            texts = kids(port_node, "text")
            if not texts:
                continue
            formal = quoted(texts[0][1])
            key = formal.casefold()
            if key in seen_ports:
                errors.append(f"porta duplicada no símbolo {quoted(kids(node, 'text')[1][1])}: {formal}")
            seen_ports.add(key)
    symbol_map = {name.removesuffix("__inst"): (name, terms, rect, kind) for name, terms, rect, kind in symbols}
    pin_map = {name: (direction, pt, display) for name, direction, pt, display, bounds in pins}
    expected = defaultdict(list)
    terminals = []
    for pname, spec in ports.items():
        if pname not in pin_map:
            errors.append(f"terminal ausente pin {pname}")
            continue
        direction, pt, display = pin_map[pname]
        if direction != spec["direction"]:
            errors.append(f"direção de pin {pname}: {direction} != {spec['direction']}")
        actual_width = len(bits(display))
        if actual_width != spec["width"]:
            errors.append(f"largura do pin {pname}: {actual_width} != {spec['width']}")
        formal = pname if spec["width"] == 1 else f"{pname}[{spec['width']-1}..0]"
        if display != formal:
            errors.append(f"formal do pin {pname}: {display} != {formal}")
        expected[pname].extend(bits(pname if spec["width"] == 1 else f"{pname}[{spec['width']-1}..0]"))
        terminals.append(("pin", "pin", pname, pt, spec["width"], direction))
    for inst in expand(graph):
        if inst["name"] not in symbol_map:
            errors.append(f"instância ausente {inst['name']}")
            continue
        actual_name, terms, rect, kind = symbol_map[inst["name"]]
        expected_ports = set(inst["connections"])
        if set(terms) != expected_ports:
            errors.append(f"portas divergentes {inst['name']}: BDF {sorted(terms)}, grafo {sorted(expected_ports)}")
        if kind.upper() != inst["type"].upper():
            errors.append(f"tipo divergente {inst['name']}: BDF {kind}, grafo {inst['type']}")
        for port, signal in inst["connections"].items():
            if port not in terms:
                errors.append(f"porta ausente {inst['name']}.{port}")
                continue
            pt, direction, symbol_width, formal = terms[port]
            width = len(bits(signal))
            required_direction = interfaces[kind]["ports"].get(port, {}).get("direction") if kind in interfaces else direction
            if direction != required_direction:
                errors.append(f"direção {inst['name']}.{port}: símbolo {direction}, contrato {required_direction}")
            expected_formal = port if symbol_width == 1 else f"{port}[{symbol_width-1}..0]"
            if formal != expected_formal:
                errors.append(f"formal de porta {inst['name']}.{port}: {formal} != {expected_formal}")
            if kind in interfaces:
                required_width = interfaces[kind]["ports"].get(port, {}).get("width")
                if required_width != width:
                    errors.append(f"largura {inst['name']}.{port}: grafo {width}, contrato filho {required_width}")
                if symbol_width != required_width:
                    errors.append(f"largura real do símbolo {inst['name']}.{port}: {symbol_width} != contrato filho {required_width}")
                if symbol_width != width:
                    errors.append(f"largura símbolo/grafo {inst['name']}.{port}: {symbol_width} != {width}")
            elif width > 1 and symbol_width == 1:
                errors.append(f"largura {inst['name']}.{port}: vetor {width} ligado a terminal escalar")
            if width == 1 and symbol_width > 1:
                errors.append(f"largura {inst['name']}.{port}: escalar ligado a terminal vetorial")
            terminals.append(("instance", inst["name"], port, pt, width, "unknown"))
            expected[signal].extend(bits(signal))
        if kind in interfaces:
            bsf_path = bdf_path.parent / f"{kind}.bsf"
            if not bsf_path.is_file():
                bsf_path = root / "modulos" / f"{kind}.bsf"
            if not bsf_path.is_file():
                bsf_path = root / "config" / "primitivas" / f"{kind.lower()}.bsf"
            if bsf_path.is_file():
                bsf_nodes = parse(bsf_path.read_text(encoding="utf-8", errors="replace"))
                bsf_symbol = next((n for n in bsf_nodes if isinstance(n, list) and n and n[0] == "symbol"), None)
                if bsf_symbol:
                    bsf_signature = symbol_signature(bsf_symbol)
                    child_ports = interfaces[kind]["ports"]
                    bdf_signature = {p: ((pt[0] - rect[0], pt[1] - rect[1]), direction, width, formal) for p, (pt, direction, width, formal) in terms.items()}
                    if bdf_signature != bsf_signature:
                        errors.append(f"geometria de símbolo embutido divergente {kind} em {inst['name']}")
                    if set(bsf_signature) != set(child_ports):
                        errors.append(f"portas BSF divergentes {kind} em {inst['name']}")
                    for pname, spec in child_ports.items():
                        if pname not in bsf_signature:
                            continue
                        _, direction, width, formal = bsf_signature[pname]
                        expected_formal = pname if spec["width"] == 1 else f"{pname}[{spec['width']-1}..0]"
                        if direction != spec["direction"] or width != spec["width"] or formal != expected_formal:
                            errors.append(f"contrato BSF divergente {kind}.{pname} em {inst['name']}")
            else:
                errors.append(f"BSF de símbolo filho ausente {kind}")
        else:
            bsf_path = bdf_path.parent / f"{kind.lower()}.bsf"
            if not bsf_path.is_file():
                bsf_path = root / "config" / "primitivas" / f"{kind.lower()}.bsf"
            if bsf_path.is_file():
                bsf_nodes = parse(bsf_path.read_text(encoding="utf-8", errors="replace"))
                bsf_symbol = next((n for n in bsf_nodes if isinstance(n, list) and n and n[0] == "symbol"), None)
                if bsf_symbol:
                    bsf_signature = symbol_signature(bsf_symbol)
                    bdf_signature = {p: ((pt[0] - rect[0], pt[1] - rect[1]), direction, width, formal) for p, (pt, direction, width, formal) in terms.items()}
                    if bdf_signature != bsf_signature:
                        errors.append(f"porta/geometria de primitiva divergente {kind} em {inst['name']}")
            else:
                errors.append(f"BSF de primitiva ausente {kind}")
    by_point = defaultdict(list)
    for i, s in enumerate(segments):
        for p in (s["a"], s["b"]):
            by_point[(p, s["bus"])].append(s)
    def attached(pt):
        found = []
        for i, s in enumerate(segments):
            if onseg(pt, s["a"], s["b"]):
                found.append(dsu.find((pt, s["bus"])))
        return set(found)
    locations = defaultdict(list)
    for kind, owner, port, pt, width, direction in terminals:
        roots = attached(pt)
        if not roots:
            errors.append(f"terminal desconectado {owner}.{port} @ {pt}")
        locations[(owner, port)] = roots
    terminal_net = {}
    for pname, spec in ports.items():
        if pname in pin_map:
            terminal_net[("pin", pname)] = pin_map[pname][2]
    expected_symbol_names = {inst["name"] for inst in expand(graph)}
    extra_symbols = sorted(set(symbol_map) - expected_symbol_names)
    for name in extra_symbols:
        errors.append(f"instância extra no BDF {name}")
    expected_pin_names = set(ports)
    for name in sorted(set(pin_map) - expected_pin_names):
        errors.append(f"pin extra no BDF {name}")
    for inst in expand(graph):
        for port, signal in inst["connections"].items():
            terminal_net[(inst["name"], port)] = signal
    by_signal_roots = defaultdict(set)
    for (owner, port), roots in locations.items():
        net = terminal_net.get((owner, port))
        if net is None:
            continue
        for rootid in roots:
            by_signal_roots[net].add(rootid)
    disconnected = []
    net_roots = defaultdict(list)
    for (owner, port), roots in locations.items():
        net = terminal_net.get((owner, port))
        if net:
            net_roots[net].extend(roots)
    channel_dsu = DSU()
    for sr, br, slabel, blabel in tap_pairs:
        channel_dsu.union((sr, slabel), (br, slabel))
    sources = defaultdict(list)
    destinations = defaultdict(list)
    signal_drivers = defaultdict(set)
    for pname, spec in ports.items():
        if pname not in pin_map:
            continue
        _, _, signal = pin_map[pname]
        role = "source" if spec["direction"] == "input" else "sink"
        for rootid in locations.get(("pin", pname), set()):
            if spec["width"] > 1 and not rootid[1]:
                errors.append(f"largura do barramento no pin {pname}: fio escalar")
            for bit in bits(signal):
                channel = channel_dsu.find((rootid, bit))
                if role == "source":
                    sources[bit].append(channel)
                    signal_drivers[bit].add("pin:" + pname)
                else:
                    destinations[bit].append((channel, "pin:" + pname))
    for inst in expand(graph):
        terms = symbol_map.get(inst["name"], (None, {}, None, None))[1]
        for port, signal in inst["connections"].items():
            if port not in terms:
                continue
            role = terms[port][1]
            for rootid in locations.get((inst["name"], port), set()):
                if len(bits(signal)) > 1 and not rootid[1]:
                    errors.append(f"largura da rede vetorial {inst['name']}.{port}: fio escalar")
                if len(bits(signal)) == 1 and rootid[1]:
                    errors.append(f"largura da rede escalar {inst['name']}.{port}: barramento sem tap")
                for bit in bits(signal):
                    channel = channel_dsu.find((rootid, bit))
                    if role == "output":
                        sources[bit].append(channel)
                        signal_drivers[bit].add(inst["name"] + "." + port)
                    else:
                        destinations[bit].append((channel, inst["name"] + "." + port))
    consumed = sum(len(bits(signal)) for inst in expand(graph) for port, signal in inst["connections"].items() if port in symbol_map.get(inst["name"], (None, {}, None, None))[1] and symbol_map[inst["name"]][1][port][1] == "input")
    consumed += sum(spec["width"] for spec in ports.values() if spec["direction"] == "output")
    reachable = 0
    for bit, sinks in destinations.items():
        for channel, destination in sinks:
            if channel in sources.get(bit, []):
                reachable += 1
            else:
                disconnected.append({"signal": bit, "destination": destination, "reason": "origem não alcançada geometricamente"})
    missing_drivers = []
    for bit in sorted({b for net in net_roots for b in bits(net)}):
        if destinations.get(bit) and not sources.get(bit):
            missing_drivers.append({"signal": bit, "coordinate": list(destinations[bit][0][0][0])})
    intentional_unused = []
    for inst in expand(graph):
        terms = symbol_map.get(inst["name"], (None, {}, None, None))[1]
        for port, signal in inst["connections"].items():
            if port in terms and terms[port][1] == "output":
                for bit in bits(signal):
                    if not destinations.get(bit):
                        intentional_unused.append({"signal": bit, "driver": inst["name"] + "." + port})
    vector_roots = {net: set(roots) for net, roots in net_roots.items() if len(bits(net)) > 1}
    for net, roots in net_roots.items():
        if len(bits(net)) != 1:
            continue
        for bus, bus_component_roots in vector_roots.items():
            valid = any(sr in roots and br in bus_component_roots and slabel == net and blabel == bus for sr, br, slabel, blabel in tap_pairs)
            if net in bits(bus) and not valid:
                disconnected.append({"signal": net, "bus": bus, "reason": "tap geométrico ausente"})
    roots_to_nets = defaultdict(set)
    bus_roots_to_nets = defaultdict(set)
    for (owner, port), roots in locations.items():
        net = terminal_net.get((owner, port))
        if not net:
            continue
        for rootid in roots:
            if len(bits(net)) == 1:
                if not rootid[1]:
                    roots_to_nets[rootid].add(net)
            else:
                if rootid[1]:
                    bus_roots_to_nets[rootid].add(net)
    shorts = []
    for channel, nets in roots_to_nets.items():
        if len(nets) > 1:
            shorts.append({"kind": "scalar_short", "signals": sorted(nets), "coordinate": list(channel[0])})
    for channel, nets in bus_roots_to_nets.items():
        incompatible = sorted(nets)
        if any(not compatible_label(a, b) for i, a in enumerate(incompatible) for b in incompatible[i + 1:]):
            shorts.append({"kind": "bus_short", "signals": incompatible, "coordinate": list(channel[0])})
    label_mismatches = []
    for rootid, names in labels.items():
        ordered = sorted(names)
        for index, first in enumerate(ordered):
            for second in ordered[index + 1:]:
                if not compatible_label(first, second):
                    label_mismatches.append({"terminal": None, "signal": None, "labels": ordered, "coordinate": list(rootid[0])})
                    break
            else:
                continue
            break
    for (owner, port), roots in locations.items():
        net = terminal_net.get((owner, port))
        if not net:
            continue
        for r in roots:
            names = labels.get(r, set())
            if names and any(not compatible_label(net, name) for name in names):
                label_mismatches.append({"terminal": f"{owner}.{port}", "signal": net, "labels": sorted(names), "coordinate": list(r[0])})
    collisions = []
    bodies = [(name, rect) for name, terms, rect, kind in symbols]
    bodies.extend((name, bounds) for name, direction, pt, display, bounds in pins)
    for s in segments:
        a, b = s["a"], s["b"]
        for name, rect in bodies:
            x1, y1, x2, y2 = rect
            if a[1] == b[1]:
                intersects = y1 < a[1] < y2 and max(min(a[0], b[0]), x1) < min(max(a[0], b[0]), x2)
            elif a[0] == b[0]:
                intersects = x1 < a[0] < x2 and max(min(a[1], b[1]), y1) < min(max(a[1], b[1]), y2)
            else:
                intersects = False
            if intersects:
                collisions.append({"kind": "wire_through_symbol", "symbol": name, "segment": [list(a), list(b)]})
    for i, (label, rect, segment_index) in enumerate(label_rects):
        x1, y1, x2, y2 = rect
        for j, s in enumerate(segments):
            if j == segment_index:
                continue
            if max(min(s["a"][0], s["b"][0]), x1) <= min(max(s["a"][0], s["b"][0]), x2) and max(min(s["a"][1], s["b"][1]), y1) <= min(max(s["a"][1], s["b"][1]), y2):
                collisions.append({"kind": "wire_through_label", "label": label, "segment": [list(s["a"]), list(s["b"])]})
        for other, other_rect, other_index in label_rects[i + 1:]:
            if max(x1, other_rect[0]) < min(x2, other_rect[2]) and max(y1, other_rect[1]) < min(y2, other_rect[3]):
                collisions.append({"kind": "label_overlap", "labels": [label, other], "coordinate": [max(x1, other_rect[0]), max(y1, other_rect[1])]})
    crossing_points = set()
    for i, left in enumerate(segments):
        for right in segments[i + 1:]:
            if left["a"][0] == left["b"][0] == right["a"][0] == right["b"][0] or left["a"][1] == left["b"][1] == right["a"][1] == right["b"][1]:
                continue
            vertical = left if left["a"][0] == left["b"][0] else right
            horizontal = right if vertical is left else left
            point = (vertical["a"][0], horizontal["a"][1])
            if onseg(point, vertical["a"], vertical["b"]) and onseg(point, horizontal["a"], horizontal["b"]):
                interior_v = point not in (vertical["a"], vertical["b"])
                interior_h = point not in (horizontal["a"], horizontal["b"])
                if point not in junctions and vertical["bus"] != horizontal["bus"] and not (interior_v and interior_h):
                    collisions.append({"kind": "bus_scalar_contact_without_junction", "coordinate": list(point)})
                root_v = dsu.find((vertical["a"], vertical["bus"]))
                root_h = dsu.find((horizontal["a"], horizontal["bus"]))
                if interior_v and interior_h and point not in junctions and root_v != root_h:
                    crossing_points.add((point, root_v, root_h))
    unjoined_crossings = [{"kind": "crossing_without_junction", "coordinate": list(point)} for point, root_v, root_h in sorted(crossing_points, key=lambda item: item[0])]
    for name, spec in ports.items():
        if name not in pin_map:
            continue
        if spec["width"] < 1:
            errors.append(f"largura inválida {name}")
    bsf = bdf_path.with_suffix(".bsf")
    if bsf.exists():
        bsf_nodes = parse(bsf.read_text(encoding="utf-8", errors="replace"))
        bsf_sym = next((x for x in bsf_nodes if isinstance(x, list) and x and x[0] == "symbol"), None)
        if bsf_sym:
            bsf_ports = {}
            for p in kids(bsf_sym, "port"):
                ptxt = kids(p, "text")
                display = quoted(ptxt[0][1])
                pname = display.split("[")[0]
                pt = tuple(map(int, kids(p, "pt")[0][1:]))
                direction = "input" if any(isinstance(x, list) and x and x[0] == "input" for x in p) else "output"
                bsf_ports[pname] = (pt, len(bits(display)), direction, display)
            if set(bsf_ports) != set(ports):
                errors.append("BSF ports divergentes")
            for pname, (p, width, direction, display) in bsf_ports.items():
                if pname in ports:
                    if width != ports[pname]["width"]:
                        errors.append(f"BSF width divergente {pname}: {width} != {ports[pname]['width']}")
                    formal = pname if ports[pname]["width"] == 1 else f"{pname}[{ports[pname]['width']-1}..0]"
                    if display != formal:
                        errors.append(f"BSF formal divergente {pname}: {display} != {formal}")
                    if direction != ports[pname]["direction"]:
                        errors.append(f"BSF direction divergente {pname}: {direction} != {ports[pname]['direction']}")
    return {
        "module": module,
        "consumed": consumed,
        "reachable": reachable,
        "disconnected": disconnected,
        "shorts": shorts,
        "width_errors": [e for e in errors if "largura" in e or "BSF" in e],
        "collisions": collisions,
        "unjoined_crossings": unjoined_crossings,
        "native_semantics_pending": bool(unjoined_crossings),
        "missing_drivers": missing_drivers,
        "intentional_unused": intentional_unused,
        "errors": errors,
        "label_mismatches": label_mismatches,
        "geometry": {"segments": len(segments), "junctions": len(junctions), "symbols": len(symbols), "pins": len(pins)},
    }


def audit(root, names=None, bdf_dir=None):
    root = Path(root).resolve()
    interfaces = json.loads((root / "config/interfaces.json").read_text(encoding="utf-8"))
    selected = names or list(interfaces)
    results = []
    for module in selected:
        if bdf_dir:
            base = Path(bdf_dir)
            nested = base / module / f"{module}.bdf"
            bdf = nested if nested.is_file() else base / f"{module}.bdf"
        else:
            bdf = root / "modulos" / f"{module}.bdf"
        results.append(analyze(root, module, bdf))
    failed = any(r["errors"] or r["shorts"] or r["disconnected"] or r["width_errors"] or r["label_mismatches"] or r["missing_drivers"] or r["collisions"] for r in results)
    return {"status": "FAIL" if failed else "PASS", "modules": results}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--modules", nargs="*")
    parser.add_argument("--bdf-dir", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    output = audit(root, args.modules, args.bdf_dir)
    output["ok"] = output["status"] == "PASS"
    data = json.dumps(output, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(data + "\n", encoding="utf-8", newline="\n")
    print(data)
    raise SystemExit(0 if output["ok"] else 1)


if __name__ == "__main__":
    main()
