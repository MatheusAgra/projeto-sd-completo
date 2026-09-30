import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validar_geometria import analyze


def node(text):
    return text


def fixture(directory):
    root = Path(directory)
    (root / "config" / "grafos").mkdir(parents=True, exist_ok=True)
    (root / "modulos").mkdir(exist_ok=True)
    ports = {"SW": {"direction": "input", "width": 13}}
    ports.update({f"Y{i}": {"direction": "output", "width": 1} for i in range(6)})
    (root / "config" / "interfaces.json").write_text(json.dumps({"toy": {"ports": ports}}), encoding="utf-8")
    instances = []
    for i in range(5):
        instances.append({"type": "NOT", "name": f"u{i}", "connections": {"IN": f"SW[{9-i}]", "OUT": f"Y{i}"}})
    instances.append({"type": "NOT", "name": "u5", "connections": {"IN": "SW[9]", "OUT": "Y5"}})
    graph = {"name": "toy", "instances": instances}
    (root / "config" / "grafos" / "toy.json").write_text(json.dumps(graph), encoding="utf-8")
    lines = ['(header "graphic" (version "1.4"))', '(pin (input) (rect 0 40 168 56) (text "INPUT" (rect 0 0 30 16)) (text "SW[12..0]" (rect 0 0 60 16)) (pt 168 8))', '(connector (text "SW[12..0]" (rect 168 20 240 36)) (pt 168 48) (pt 800 48) (bus))']
    for i in range(5):
        x = 200 + i * 100
        y = 180 + i * 100
        bit = 9 - i
        lines.append(f'(connector (text "SW[{bit}]" (rect {x} 24 {x+48} 40)) (pt {x} 48) (pt {x} {y+10}))')
        lines.append(f'(junction (pt {x} 48))')
        lines.append(f'(symbol (rect {x} {y} {x+40} {y+20}) (text "NOT" (rect 0 0 20 10)) (text "u{i}" (rect 0 10 20 20)) (port (pt 0 10) (input) (text "IN" (rect 0 0 10 10))) (port (pt 40 10) (output) (text "OUT" (rect 0 0 20 10))))')
        lines.append(f'(connector (text "Y{i}" (rect {x+40} {y-30} {x+56} {y-14})) (pt {x+40} {y+10}) (pt 1000 {y+10}))')
        lines.append(f'(pin (output) (rect 1000 {y+2} 1168 {y+18}) (text "OUTPUT" (rect 0 0 40 16)) (text "Y{i}" (rect 0 0 20 16)) (pt 0 8))')
    lines.extend(['(connector (text "SW[9]" (rect 200 0 248 16)) (pt 200 190) (pt 150 190))', '(junction (pt 200 190))', '(connector (pt 150 190) (pt 150 690))', '(connector (pt 150 690) (pt 250 690))', '(symbol (rect 250 680 290 700) (text "NOT" (rect 0 0 20 10)) (text "u5" (rect 0 10 20 20)) (port (pt 0 10) (input) (text "IN" (rect 0 0 10 10))) (port (pt 40 10) (output) (text "OUT" (rect 0 0 20 10))))', '(connector (text "Y5" (rect 290 650 306 666)) (pt 290 690) (pt 1000 690))', '(pin (output) (rect 1000 682 1168 698) (text "OUTPUT" (rect 0 0 40 16)) (text "Y5" (rect 0 0 20 16)) (pt 0 8))'])
    bdf = '\n'.join(lines) + '\n'
    path = root / "modulos" / "toy.bdf"
    path.write_text(bdf, encoding="utf-8")
    return root, path, bdf


def range_fixture(directory, wrong_bit=False):
    root = Path(directory)
    (root / "config" / "grafos").mkdir(parents=True, exist_ok=True)
    (root / "modulos").mkdir(exist_ok=True)
    ports = {"SW": {"direction": "input", "width": 13}, "Y": {"direction": "output", "width": 5}}
    (root / "config" / "interfaces.json").write_text(json.dumps({"range": {"ports": ports}}), encoding="utf-8")
    instances = [{"type": "VECTOR5", "name": "slice", "connections": {"P": "SW[9..5]", "Q": "T[4..0]"}}]
    for i in range(5):
        instances.append({"type": "NOT", "name": f"u{i}", "connections": {"IN": f"T[{i}]", "OUT": f"Y[{i}]"}})
    (root / "config" / "grafos" / "range.json").write_text(json.dumps({"name": "range", "instances": instances}), encoding="utf-8")
    (root / "config" / "primitivas" ).mkdir(parents=True, exist_ok=True)
    primitive_symbol = '(header "symbol" (version "1.2"))\n(symbol (rect 0 0 320 64) (text "VECTOR5") (text "inst") (port (pt 0 32) (input) (text "P[4..0]")) (port (pt 320 32) (output) (text "Q[4..0]")))\n'
    (root / "config" / "primitivas" / "vector5.bsf").write_text(primitive_symbol, encoding="utf-8")
    not_symbol = '(header "symbol" (version "1.2"))\n(symbol (rect 0 0 40 20) (text "NOT") (text "inst") (port (pt 0 10) (input) (text "IN")) (port (pt 40 10) (output) (text "OUT")))\n'
    (root / "config" / "primitivas" / "not.bsf").write_text(not_symbol, encoding="utf-8")
    lines = ['(header "graphic" (version "1.4"))', '(pin (input) (rect 0 40 168 56) (text "INPUT") (text "SW[12..0]") (pt 168 8))', '(connector (text "SW[12..0]" (rect 168 20 240 36)) (pt 168 48) (pt 600 48) (bus))']
    for i, bit in enumerate(range(9, 4, -1)):
        x, x2, y = 220 + i * 60, 720 + i * 40, 180 + i * 20
        label = bit + 1 if wrong_bit and i == 0 else bit
        lines.extend([f'(connector (text "SW[{label}]" (rect {x} 20 {x+48} 36)) (pt {x} 48) (pt {x} {y}))', f'(junction (pt {x} 48))', f'(connector (pt {x} {y}) (pt {x2} {y}))', f'(connector (pt {x2} {y}) (pt {x2} 300))', f'(junction (pt {x2} 300))'])
    lines.extend(['(connector (text "SW[9..5]" (rect 700 276 772 292)) (pt 700 300) (pt 900 300) (bus))', '(junction (pt 700 300))', '(connector (pt 700 300) (pt 700 392) (bus))', '(symbol (rect 700 360 1020 424) (text "VECTOR5") (text "slice") (port (pt 0 32) (input) (text "P[4..0]" (rect 0 0 40 16)) (line (pt 0 32) (pt 16 32) (line_width 3))) (port (pt 320 32) (output) (text "Q[4..0]" (rect 0 0 40 16)) (line (pt 320 32) (pt 304 32) (line_width 3))))', '(connector (text "T[4..0]" (rect 1020 368 1072 384)) (pt 1020 392) (pt 1400 392) (bus))'])
    for i in range(5):
        x, y = 1050 + i * 50, 480 + i * 40
        lines.extend([f'(connector (text "T[{i}]" (rect {x} 400 {x+40} 416)) (pt {x} 392) (pt {x} {y}))', f'(junction (pt {x} 392))', f'(symbol (rect {x} {y-10} {x+40} {y+10}) (text "NOT") (text "u{i}") (port (pt 0 10) (input) (text "IN")) (port (pt 40 10) (output) (text "OUT")))', f'(connector (text "Y[{i}]" (rect {1500+i*40} {y-30} {1540+i*40} {y-14})) (pt {x+40} {y}) (pt {1500+i*40} {y}))', f'(connector (pt {1500+i*40} {y}) (pt {1500+i*40} 900))', f'(junction (pt {1500+i*40} 900))'])
    lines.extend(['(connector (text "Y[4..0]" (rect 1500 876 1560 892)) (pt 1500 900) (pt 1800 900) (bus))', '(pin (output) (rect 1800 892 1968 908) (text "OUTPUT") (text "Y[4..0]") (pt 0 8))'])
    path = root / "modulos" / "range.bdf"
    path.write_text('\n'.join(lines) + '\n', encoding="utf-8")
    return root, path


def hierarchy_fixture(directory):
    root = Path(directory)
    (root / "config" / "grafos").mkdir(parents=True, exist_ok=True)
    (root / "modulos").mkdir(exist_ok=True)
    ports = {"P": {"direction": "input", "width": 2}, "Q": {"direction": "output", "width": 2}}
    interfaces = {"top": {"ports": {}}, "child": {"ports": ports}}
    (root / "config" / "interfaces.json").write_text(json.dumps(interfaces), encoding="utf-8")
    (root / "config" / "grafos" / "top.json").write_text(json.dumps({"name": "top", "instances": [{"type": "child", "name": "u", "connections": {"P": "I[1..0]", "Q": "O[1..0]"}}]}), encoding="utf-8")
    (root / "config" / "grafos" / "child.json").write_text(json.dumps({"name": "child", "instances": []}), encoding="utf-8")
    symbol = '(symbol (rect 0 0 320 64) (text "child") (text "u") (port (pt 0 32) (input) (text "P[1..0]")) (port (pt 320 32) (output) (text "Q[1..0]")))'
    (root / "modulos" / "child.bsf").write_text('(header "symbol" (version "1.2"))\n' + symbol + '\n', encoding="utf-8")
    (root / "modulos" / "top.bdf").write_text('(header "graphic" (version "1.4"))\n' + symbol + '\n', encoding="utf-8")
    (root / "modulos" / "top.bsf").write_text('(header "symbol" (version "1.2"))\n(symbol (rect 0 0 320 64) (text "top") (port (pt 0 32) (input) (text "X")) (port (pt 320 32) (output) (text "Y")))\n', encoding="utf-8")
    return root, root / "modulos" / "top.bdf"


class GeometriaTest(unittest.TestCase):
    def result(self, edit=None):
        temp_root = Path(__file__).resolve().parents[2] / "tmp" / "geometry_audit_fixture"
        temp_root.mkdir(parents=True, exist_ok=True)
        root, path, source = fixture(temp_root)
        if edit:
            path.write_text(edit(source), encoding="utf-8")
        return analyze(root, "toy", path)

    def test_fanout_and_bus_slices_are_connected(self):
        result = self.result()
        self.assertEqual([], result["disconnected"])
        self.assertEqual([], result["shorts"])
        self.assertEqual([], result["label_mismatches"])
        self.assertEqual(12, result["consumed"])
        self.assertEqual(12, result["reachable"])

    def test_full_vector_to_external_slice_and_scalar_bus_assembly(self):
        root = Path(__file__).resolve().parents[2] / "tmp" / "geometry_range_fixture"
        root.mkdir(parents=True, exist_ok=True)
        root, path = range_fixture(root)
        result = analyze(root, "range", path)
        self.assertEqual(15, result["consumed"])
        self.assertEqual(15, result["reachable"])
        self.assertEqual([], result["disconnected"])
        self.assertEqual([], result["errors"])

    def test_wrong_source_bus_slice_bit_does_not_reach_destination(self):
        root = Path(__file__).resolve().parents[2] / "tmp" / "geometry_range_fixture_wrong"
        root.mkdir(parents=True, exist_ok=True)
        root, path = range_fixture(root, wrong_bit=True)
        result = analyze(root, "range", path)
        self.assertTrue(result["disconnected"] or result["label_mismatches"])

    def test_one_unit_gap_is_detected(self):
        result = self.result(lambda s: s.replace("(pt 240 190) (pt 1000 190)", "(pt 241 190) (pt 1000 190)"))
        self.assertTrue(result["disconnected"] or result["errors"])

    def test_equal_remote_labels_do_not_join(self):
        def mutate(s):
            return s.replace("(pt 240 190) (pt 1000 190)", "(pt 240 190) (pt 400 190)") + '\n(connector (text "Y0" (rect 420 200 436 216)) (pt 401 190) (pt 1000 190))\n'
        result = self.result(mutate)
        self.assertTrue(result["disconnected"])

    def test_wrong_bit_tap_label_is_detected(self):
        result = self.result(lambda s: s.replace('text "SW[9]"', 'text "SW[TEMP]"').replace('text "SW[8]"', 'text "SW[9]"').replace('text "SW[TEMP]"', 'text "SW[8]"'))
        self.assertTrue(result["label_mismatches"] or result["disconnected"])

    def test_wrong_bus_width_is_detected(self):
        result = self.result(lambda s: s.replace('(pt 168 48) (pt 800 48) (bus)', '(pt 168 48) (pt 800 48)'))
        self.assertTrue(result["disconnected"] or result["errors"])

    def test_bus_bit_order_is_checked(self):
        result = self.result(lambda s: s.replace('text "SW[12..0]"', 'text "SW[0..12]"', 1))
        self.assertTrue(result["label_mismatches"])

    def test_short_between_outputs_is_detected(self):
        def mutate(s):
            return s + '\n(connector (pt 250 190) (pt 250 290))\n(connector (pt 250 290) (pt 350 290))\n(junction (pt 250 190))\n(junction (pt 250 290))\n(junction (pt 350 290))\n'
        result = self.result(mutate)
        self.assertTrue(result["shorts"])

    def test_missing_tap_junction_is_detected(self):
        result = self.result(lambda s: s.replace('(junction (pt 200 48))', ''))
        self.assertTrue(result["disconnected"] or result["label_mismatches"])

    def test_displaced_symbol_port_is_detected(self):
        result = self.result(lambda s: s.replace('(pt 0 10) (input)', '(pt 0 11) (input)', 1))
        self.assertTrue(result["errors"] or result["disconnected"])

    def test_displaced_primitive_output_pin_is_detected(self):
        result = self.result(lambda s: s.replace('(pt 40 10) (output)', '(pt 40 11) (output)', 1))
        self.assertTrue(result["errors"] or result["disconnected"])

    def test_wire_crossing_symbol_body_is_reported(self):
        result = self.result(lambda s: s + '\n(connector (pt 190 185) (pt 250 185))\n')
        self.assertTrue(any(item["kind"] == "wire_through_symbol" for item in result["collisions"]))

    def test_label_collision_with_wire_is_reported(self):
        result = self.result(lambda s: s.replace('text "Y0" (rect 240 150 256 166)', 'text "Y0" (rect 400 280 416 296)', 1))
        self.assertTrue(any(item["kind"] == "wire_through_label" for item in result["collisions"]))

    def test_conflicting_label_on_connected_component_is_reported(self):
        result = self.result(lambda s: s + '\n(connector (text "WRONG" (rect 500 160 548 176)) (pt 500 190) (pt 700 190))\n')
        self.assertTrue(result["label_mismatches"])

    def test_expected_and_incompatible_scalar_labels_are_both_checked(self):
        result = self.result(lambda s: s + '\n(connector (text "WRONG" (rect 500 160 548 176)) (pt 500 190) (pt 700 190))\n')
        self.assertTrue(any("WRONG" in item["labels"] and "Y0" in item["labels"] for item in result["label_mismatches"]))

    def test_collinear_overlap_between_different_nets_is_a_short(self):
        def mutate(s):
            return s + '\n(connector (text "Y1" (rect 500 160 516 176)) (pt 500 190) (pt 700 190))\n(connector (pt 700 190) (pt 700 290))\n'
        result = self.result(mutate)
        self.assertTrue(result["shorts"] or result["label_mismatches"])

    def test_bus_bus_physical_join_of_different_vectors_is_a_short(self):
        root = Path(__file__).resolve().parents[2] / "tmp" / "geometry_range_fixture_bus_short"
        root.mkdir(parents=True, exist_ok=True)
        root, path = range_fixture(root)
        with path.open("a", encoding="utf-8") as stream:
            stream.write('\n(connector (pt 700 300) (pt 1020 300) (bus))\n(junction (pt 700 300))\n(connector (pt 1020 300) (pt 1020 392) (bus))\n(junction (pt 1020 392))\n')
        result = analyze(root, "range", path)
        self.assertTrue(any(item.get("kind") == "bus_short" for item in result["shorts"]))

    def test_hierarchical_embedded_symbol_width_is_exact(self):
        root = Path(__file__).resolve().parents[2] / "tmp" / "geometry_hierarchy_width"
        root.mkdir(parents=True, exist_ok=True)
        root, path = hierarchy_fixture(root)
        path.write_text(path.read_text(encoding="utf-8").replace('text "P[1..0]"', 'text "P[4..0]"'), encoding="utf-8")
        result = analyze(root, "top", path)
        self.assertTrue(any("largura real do símbolo u.P" in error or "geometria de símbolo embutido" in error for error in result["errors"]))

    def test_hierarchical_symbol_direction_is_checked(self):
        root = Path(__file__).resolve().parents[2] / "tmp" / "geometry_hierarchy_direction"
        root.mkdir(parents=True, exist_ok=True)
        root, path = hierarchy_fixture(root)
        path.write_text(path.read_text(encoding="utf-8").replace('(port (pt 0 32) (input)', '(port (pt 0 32) (output)'), encoding="utf-8")
        result = analyze(root, "top", path)
        self.assertTrue(any("direção u.P" in error or "geometria de símbolo embutido" in error for error in result["errors"]))

    def test_hierarchical_bsf_formal_range_is_checked_against_contract(self):
        root = Path(__file__).resolve().parents[2] / "tmp" / "geometry_hierarchy_bsf_formal"
        root.mkdir(parents=True, exist_ok=True)
        root, path = hierarchy_fixture(root)
        bsf = root / "modulos" / "child.bsf"
        bsf.write_text(bsf.read_text(encoding="utf-8").replace('text "P[1..0]"', 'text "P[4..0]"'), encoding="utf-8")
        result = analyze(root, "top", path)
        self.assertTrue(any("contrato BSF divergente child.P" in error for error in result["errors"]))

    def test_top_pin_formal_range_is_checked_against_interface(self):
        result = self.result(lambda s: s.replace('text "SW[12..0]"', 'text "SW[11..0]"', 1))
        self.assertTrue(any("formal do pin SW" in error for error in result["errors"]))

    def test_hierarchical_instance_type_is_checked(self):
        root = Path(__file__).resolve().parents[2] / "tmp" / "geometry_hierarchy_type"
        root.mkdir(parents=True, exist_ok=True)
        root, path = hierarchy_fixture(root)
        path.write_text(path.read_text(encoding="utf-8").replace('text "child"', 'text "wrong_type"'), encoding="utf-8")
        result = analyze(root, "top", path)
        self.assertTrue(any("tipo divergente" in error or "BSF de símbolo filho ausente" in error for error in result["errors"]))

    def test_duplicate_instance_names_are_not_hidden_by_indexing(self):
        result = self.result(lambda s: s + '\n(symbol (rect 1200 800 1240 820) (text "NOT") (text "u0") (port (pt 0 10) (input) (text "IN")) (port (pt 40 10) (output) (text "OUT")))\n')
        self.assertTrue(any("instância duplicado" in error for error in result["errors"]))

    def test_unmatched_component_with_conflicting_labels_is_reported(self):
        result = self.result(lambda s: s + '\n(connector (text "ORPHAN_A" (rect 1200 20 1264 36)) (pt 1200 48) (pt 1300 48))\n(connector (text "ORPHAN_B" (rect 1250 20 1314 36)) (pt 1250 48) (pt 1350 48))\n')
        self.assertTrue(any("ORPHAN_A" in item["labels"] and "ORPHAN_B" in item["labels"] for item in result["label_mismatches"]))

    def test_bus_endpoint_contact_without_junction_is_invalid_tap(self):
        root = Path(__file__).resolve().parents[2] / "tmp" / "geometry_range_fixture_endpoint_tap"
        root.mkdir(parents=True, exist_ok=True)
        root, path = range_fixture(root)
        source = path.read_text(encoding="utf-8").replace('(junction (pt 700 300))', '')
        source += '\n(connector (pt 640 300) (pt 700 300) (bus))\n(connector (pt 700 300) (pt 700 340))\n'
        path.write_text(source, encoding="utf-8")
        result = analyze(root, "range", path)
        self.assertTrue(any(item.get("kind") == "bus_scalar_contact_without_junction" for item in result["collisions"]))


if __name__ == "__main__":
    unittest.main()
