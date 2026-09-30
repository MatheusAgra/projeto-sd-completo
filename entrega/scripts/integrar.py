import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def instance(kind, name, **connections):
    return {'type': kind, 'name': name, 'connections': connections}


def save(name, instances):
    path = ROOT / 'config' / 'grafos' / (name + '.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({'name': name, 'instances': instances}, indent=2) + '\n', encoding='utf-8')


def main():
    core = [
        instance('sm_para_c2', 'conv_a', SM='A[4..0]', C2='AC2[5..0]'),
        instance('sm_para_c2', 'conv_b', SM='B[4..0]', C2='BC2[5..0]'),
        instance('modulo2_soma_sub', 'aritmetica', A_C2='AC2[5..0]', B_C2='BC2[5..0]', SUB='S[0]', F_SM='ARIT[5..0]'),
        instance('negador_c2_6bit', 'negacao_b', B_C2='BC2[5..0]', NEG='NEG[5..0]'),
        instance('comparador_c2_6bit', 'comparacao', A_C2='AC2[5..0]', B_C2='BC2[5..0]', EQ='EQ', GT='GT', LT='LT'),
        instance('logica_5bit', 'logica', A_SM='A[4..0]', B_SM='B[4..0]', AND6='LAND[5..0]', XOR6='LXOR[5..0]'),
        instance('decodificador_operacao', 'controle', S='S[2..0]', D='D[7..0]', EXIBE_F='EXIBE_F'),
        instance('mux_resultado_8x6', 'selecao', C0='ARIT[5..0]', C1='ARIT[5..0]', C2='NEG[5..0]', C3='ZERO[5..0]', C4='ZERO[5..0]', C5='ZERO[5..0]', C6='LAND[5..0]', C7='LXOR[5..0]', D='D[7..0]', F='F[5..0]'),
        instance('AND2', 'status_eq', IN1='D[3]', IN2='EQ', OUT='EQS'),
        instance('AND2', 'status_gt', IN1='D[4]', IN2='GT', OUT='GTS'),
        instance('AND2', 'status_lt', IN1='D[5]', IN2='LT', OUT='LTS'),
        instance('OR3', 'status_final', IN1='EQS', IN2='GTS', IN3='LTS', OUT='STATUS')
    ]
    core += [{'type': 'GND', 'name': f'zero_{i}', 'connections': {'1': f'ZERO[{i}]'}} for i in range(6)]
    save('ula_core', core)
    top = [
        instance('ula_core', 'ula', A='SW[4..0]', B='SW[9..5]', S='SW[12..10]', F='F[5..0]', STATUS='STATUS', EXIBE_F='EXIBE_F'),
        instance('display_decimal_2digitos', 'display_a', MAG='MAGA[4..0]', ENABLE='ONE', DEZ_SEG='HEX5[6..0]', UNI_SEG='HEX4[6..0]'),
        instance('display_decimal_2digitos', 'display_b', MAG='MAGB[4..0]', ENABLE='ONE', DEZ_SEG='HEX3[6..0]', UNI_SEG='HEX2[6..0]'),
        instance('display_decimal_2digitos', 'display_f', MAG='F[4..0]', ENABLE='EXIBE_F', DEZ_SEG='HEX1[6..0]', UNI_SEG='HEX0[6..0]'),
        {'type':'VCC', 'name':'habilitacao_entradas', 'connections':{'1':'ONE'}}
    ]
    for i in range(4):
        top.append(instance('BUF', f'mag_a_{i}', IN=f'SW[{i}]', OUT=f'MAGA[{i}]'))
        top.append(instance('BUF', f'mag_b_{i}', IN=f'SW[{i + 5}]', OUT=f'MAGB[{i}]'))
    for target in ('MAGA[4]', 'MAGB[4]'):
        top.append({'type':'GND', 'name':'zero_' + target.split('[')[0], 'connections':{'1':target}})
    for i in range(18):
        top.append(instance('BUF', f'mirror_{i}', IN=f'SW[{i}]', OUT=f'LEDR[{i}]') if i < 13 else {'type':'GND', 'name':f'ledr_off_{i}', 'connections':{'1':f'LEDR[{i}]'}})
    for i in range(9):
        if i < 7:
            top.append(instance('BUF', f'ledg_{i}', IN=f'F[{i}]' if i < 6 else 'STATUS', OUT=f'LEDG[{i}]'))
        else:
            top.append({'type':'GND', 'name':f'ledg_off_{i}', 'connections':{'1':f'LEDG[{i}]'}})
    for display in (6, 7):
        for bit in range(7):
            top.append({'type':'VCC', 'name':f'hex_off_{display}_{bit}', 'connections':{'1':f'HEX{display}[{bit}]'}})
    save('ula_de2_115', top)
    interfaces = json.loads((ROOT / 'config/interfaces.json').read_text(encoding='utf-8'))
    pins = list(csv.DictReader((ROOT / 'config/pinagem_de2_115.csv').open(encoding='utf-8')))
    qsf = ['set_global_assignment -name FAMILY "Cyclone IV E"', 'set_global_assignment -name DEVICE EP4CE115F29C7', 'set_global_assignment -name TOP_LEVEL_ENTITY ula_de2_115', 'set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files', 'set_global_assignment -name NUM_PARALLEL_PROCESSORS 4', 'set_global_assignment -name EDA_SIMULATION_TOOL "Questa Intel FPGA (Verilog)"', 'set_global_assignment -name EDA_OUTPUT_DATA_FORMAT "VERILOG HDL" -section_id eda_simulation', 'set_global_assignment -name EDA_TIME_SCALE "1 ps" -section_id eda_simulation']
    qsf += [f'set_global_assignment -name BDF_FILE modulos/{name}.bdf' for name in interfaces]
    for row in pins:
        qsf += [f'set_location_assignment PIN_{row["pino"]} -to {row["sinal"]}', f'set_instance_assignment -name IO_STANDARD "{row["padrao_io"]}" -to {row["sinal"]}']
    (ROOT / 'ULA_DE2_115.qsf').write_text('\n'.join(qsf) + '\n', encoding='utf-8')
    (ROOT / 'ULA_DE2_115.qpf').write_text('QUARTUS_VERSION = "21.1"\nPROJECT_REVISION = "ULA_DE2_115"\n', encoding='utf-8')


if __name__ == '__main__':
    main()
