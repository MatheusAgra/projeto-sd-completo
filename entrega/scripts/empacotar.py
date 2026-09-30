import argparse
import json
import zipfile
from pathlib import Path


def included_files(root):
    excluded = {'db', 'incremental_db', '__pycache__', 'modelsim', 'work', 'renderer-probe-l9g61xfp'}
    included_outputs = {'.sof', '.rpt', '.summary', '.pin', '.md'}
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if not path.is_file() or any(p in excluded for p in relative.parts):
            continue
        if relative.parts[0] == 'output_files' and path.suffix not in included_outputs:
            continue
        yield path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--zip', type=Path)
    parser.add_argument('--extract', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    target = args.zip or root.parent / 'ULA_DE2_115.zip'
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as handle:
        for path in included_files(root):
            relative = path.relative_to(root)
            handle.write(path, str(Path('entrega') / relative).replace('\\', '/'))
    if args.extract:
        destination = args.extract.resolve()
        if destination.exists():
            raise ValueError('Pasta de extracao deve ser nova')
        destination.mkdir(parents=True)
        with zipfile.ZipFile(target) as handle:
            for item in handle.infolist():
                resolved = (destination / item.filename).resolve()
                if not resolved.is_relative_to(destination):
                    raise ValueError('Caminho fora da pasta de extracao')
            handle.extractall(destination)
    print(json.dumps({'zip':str(target), 'bytes':target.stat().st_size, 'extract':str(args.extract) if args.extract else None}))


if __name__ == '__main__':
    main()
