import argparse
import ast
import hashlib
import io
import json
import re
import tokenize
from pathlib import Path


def files(root):
    excluded = {'db', 'incremental_db', '__pycache__', 'modelsim', 'work', 'renderer-probe-l9g61xfp'}
    return [p for p in root.rglob('*') if p.is_file() and not any(x in excluded for x in p.relative_to(root).parts)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--compare', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    legal = []
    checked = []
    extensions = {'.py', '.ps1', '.tcl', '.do', '.sv', '.v', '.vo', '.bdf', '.bsf', '.qpf', '.qsf', '.json', '.csv', '.png', '.svg', '.vcd', '.sof', '.pin', '.docx'}
    sources = files(root)
    for path in sources:
        relative = path.relative_to(root).as_posix()
        if path.suffix in extensions and path.name != 'manifest.json' and not Path(str(path) + '.md').is_file():
            raise ValueError(f'Documentacao ausente: {relative}')
        if path.suffix == '.py':
            content = path.read_text(encoding='utf-8-sig')
            if any(t.type == tokenize.COMMENT for t in tokenize.generate_tokens(io.StringIO(content).readline)):
                raise ValueError(f'Comentario Python: {relative}')
            for node in ast.walk(ast.parse(content)):
                if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and ast.get_docstring(node):
                    raise ValueError(f'Docstring: {relative}')
            checked.append(relative)
        if path.suffix in {'.v', '.vo', '.sv', '.bdf', '.bsf'}:
            content = path.read_text(encoding='utf-8-sig')
            pattern = r'"(?:\\.|[^"\\])*"|//[^\n]*(?:\n[ \t]*//[^\n]*)*|/\*.*?\*/'
            for match in re.finditer(pattern, content, flags=re.S):
                block = match.group()
                if block.startswith('"'):
                    continue
                if 'Copyright' not in block and 'License Agreement' not in block:
                    raise ValueError(f'Comentario nao legal: {relative}: {block[:80]}')
                legal.append(relative)
            checked.append(relative)
        if path.suffix in {'.ps1', '.tcl', '.do', '.qpf', '.qsf'}:
            content = path.read_text(encoding='utf-8-sig')
            if re.search(r'^\s*#|<#', content, flags=re.M):
                raise ValueError(f'Comentario de script: {relative}')
            checked.append(relative)
    compared = []
    if args.compare:
        other = args.compare.resolve()
        for path in sources:
            if path.suffix not in {'.bdf', '.bsf', '.qpf', '.qsf', '.sv', '.v'}:
                continue
            relative = path.relative_to(root)
            destination = other / relative
            if not destination.is_file() or hashlib.sha256(path.read_bytes()).digest() != hashlib.sha256(destination.read_bytes()).digest():
                raise ValueError(f'Fonte extraida divergente: {relative}')
            compared.append(relative.as_posix())
    result = {'status':'PASS', 'comment_audit_files':len(checked), 'legal_header_files':sorted(set(legal)), 'compared_source_files':len(compared), 'documentation_coverage':'PASS'}
    (root / 'docs/auditoria_fontes.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
