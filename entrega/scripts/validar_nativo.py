import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


def source_hashes(root):
    paths = list((root / 'modulos').glob('*.bdf')) + list((root / 'modulos').glob('*.bsf'))
    paths += [root / 'ULA_DE2_115.qsf', root / 'ULA_DE2_115.qpf', root / 'config/interfaces.json', root / 'config/pinagem_de2_115.csv']
    paths += list((root / 'config/grafos').glob('*.json')) + list((root / 'simulation').glob('tb_*.sv'))
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--quartus', type=Path, default=Path('C:/intelFPGA_lite/21.1/quartus'))
    parser.add_argument('--icarus-root', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    icarus = (args.icarus_root or root.parent / 'tmp/tools/iverilog').resolve()
    binroot = icarus / 'ucrt64/bin' if (icarus / 'ucrt64/bin/iverilog.exe').is_file() else icarus
    required = [args.quartus / 'bin64/quartus_map.exe', args.quartus / 'bin64/quartus_sh.exe', args.quartus / 'bin64/quartus_eda.exe', binroot / 'iverilog.exe', binroot / 'vvp.exe']
    missing = [str(p) for p in required if not p.is_file()]
    report_path = root / 'docs/validacao_nativa_atual.json'
    record = {'status':'PENDING', 'stages':{}, 'missing_tools':missing, 'visual':'PENDING', 'sources':source_hashes(root)}
    report_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
    if missing:
        raise FileNotFoundError('Etapas nativas não executadas; ferramentas ausentes: ' + ', '.join(missing))
    shell = shutil.which('pwsh') or shutil.which('powershell')
    if not shell:
        raise FileNotFoundError('PowerShell não encontrado')
    python = shutil.which('python')
    scripts = root / 'scripts'
    stages = [
        ('offline', [python, str(scripts / 'validar_refatoracao.py'), '--root', str(root)], 'refatoracao_offline.log'),
        ('export', [python, str(scripts / 'preparar.py'), '--root', str(root), '--quartus', str(args.quartus), '--export-only'], 'refatoracao_export.log'),
        ('simulation', [shell, '-NoProfile', '-File', str(scripts / 'simular.ps1'), '-IcarusRoot', str(icarus)], 'refatoracao_simulacao.log'),
        ('compilation', [shell, '-NoProfile', '-File', str(scripts / 'compilar.ps1'), '-Quartus', str(args.quartus / 'bin64')], 'compile_final.log'),
        ('netlist', [shell, '-NoProfile', '-File', str(scripts / 'simular_netlist.ps1'), '-Quartus', str(args.quartus), '-IcarusRoot', str(icarus)], 'refatoracao_netlist.log')
    ]
    for stage, command, filename in stages:
        result = subprocess.run(command, cwd=root, capture_output=True, text=True, errors='replace')
        logfile = root / 'docs/logs' / filename
        logfile.write_text(result.stdout + result.stderr, encoding='utf-8', newline='\n')
        record['stages'][stage] = {'status':'PASS' if result.returncode == 0 else 'FAIL', 'log':logfile.relative_to(root).as_posix(), 'sha256':hashlib.sha256(logfile.read_bytes()).hexdigest()}
        if source_hashes(root) != record['sources']:
            record['status'] = 'FAIL'
            record['stages'][stage]['status'] = 'FAIL_SOURCE_CHANGED'
            report_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
            raise RuntimeError(f'Fontes alteradas durante {stage}; validação interrompida')
        report_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
        if result.returncode:
            raise RuntimeError(f'{stage}: código {result.returncode}; veja {logfile}')
        print(stage + ': PASS', flush=True)
    record['status'] = 'PASS'
    report_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
    result = subprocess.run([python, str(scripts / 'verificar_entrega.py'), '--root', str(root)], cwd=root)
    record['delivery_check'] = 'PASS' if result.returncode == 0 else 'FAIL'
    if result.returncode:
        record['status'] = 'FAIL'
    report_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
    if result.returncode:
        raise RuntimeError('Verificação final da entrega falhou')


if __name__ == '__main__':
    main()
