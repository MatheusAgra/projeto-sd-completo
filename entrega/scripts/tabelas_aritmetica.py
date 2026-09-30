import csv
from pathlib import Path

base=Path(__file__).resolve().parents[1]
out=base/'docs'/'tabelas'/'aritmetica'
out.mkdir(parents=True,exist_ok=True)

def write_csv(name,header,rows,description):
    p=out/name
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    p.with_suffix(p.suffix+'.md').write_text(description+'\n',encoding='utf-8')

def write_svg(name,content,description):
    p=out/name
    p.write_text(content,encoding='utf-8')
    p.with_suffix(p.suffix+'.md').write_text(description+'\n',encoding='utf-8')

rows=[]
for a in range(2):
    for b in range(2):
        for ci in range(2):
            p=a^b
            s=p^ci
            g=a&b
            h=p&ci
            co=g|h
            rows.append([a,b,ci,p,s,g,h,co])
write_csv('somador_1bit.csv',['A','B','Cin','P=A XOR B','S','G=A AND B','H=P AND Cin','Cout'],rows,'Tabela-verdade completa do somador de um bit. As oito linhas cobrem o domínio. As colunas P, G e H explicitam a decomposição de portas do grafo.')
rows=[]
for raw in range(32):
    sign=(raw>>4)&1
    mag=raw&15
    value=-mag if sign else mag
    c2=value&63
    rows.append([format(raw,'05b'),sign,format(mag,'04b'),value,format(c2,'06b')])
write_csv('sm_para_c2.csv',['SM[4:0]','sinal','magnitude[3:0]','valor decimal','C2[5:0]'],rows,'Tabela completa de 32 padrões do conversor sinal-magnitude para C2. O cálculo de referência usa o inteiro assinado e reduz a codificação C2 a seis bits; os dois padrões de zero têm valor e saída zero.')
rows=[]
for raw in range(64):
    value=raw-64 if raw&32 else raw
    mag=abs(value)
    out_sign=int(value<0 and (mag&31)!=0)
    f=(out_sign<<5)|(mag&31)
    in_domain=int(value!=-32)
    note='fora do domínio; regra efetiva gera zero' if value==-32 else ''
    rows.append([format(raw,'06b'),value,format((mag&31),'05b'),out_sign,format(f,'06b'),in_domain,note])
write_csv('c2_para_sm.csv',['R[5:0]','valor C2','magnitude efetiva[4:0]','sinal efetivo','F_SM[5:0]','no domínio -31..31','observação'],rows,'Tabela dos 64 padrões C2. Para −31..31, F_SM contém sinal e magnitude exatos. −32 não é representável: o circuito implementa magnitude ABS[4:0] e sinal R5 AND OR(R4..R0), portanto 100000 gera 000000. Isso descreve a saída efetiva fora do domínio, não uma conversão correta de −32.')
rows=[]
for raw in range(64):
    value=raw-64 if raw&32 else raw
    result=(-raw)&63
    signed_result=result-64 if result&32 else result
    rows.append([format(raw,'06b'),value,format(result,'06b'),signed_result])
write_csv('negador_c2_6bit.csv',['B_C2[5:0]','valor C2','NEG[5:0]','valor C2 de saída'],rows,'Tabela de 64 padrões do negador. A saída é o inverso aditivo módulo 64: NEG=(~B_C2+1) mod 64. O padrão −32 é ponto fixo da negação em seis bits.')

def svg_start(width,height,title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="white"/><text x="24" y="32" font-family="Arial,sans-serif" font-size="20" font-weight="bold">{title}</text>'
def map_svg():
    w,h=760,370
    s=[svg_start(w,h,'Mapas de Karnaugh do somador de um bit')]
    cols=['00','01','11','10']
    funcs=[('S',lambda a,b,c:a^b^c,40),('Cout',lambda a,b,c:(a&b)|(a&c)|(b&c),400)]
    for name,fn,x0 in funcs:
        s.append(f'<text x="{x0+145}" y="72" text-anchor="middle" font-family="Arial" font-size="17">{name}; linhas A, colunas B Cin (Gray)</text>')
        x=x0+70; y=110; cw=58; ch=58
        s.append(f'<text x="{x0+25}" y="{y+ch+4}" font-family="Arial" font-size="14">A</text>')
        for j,c in enumerate(cols): s.append(f'<text x="{x+j*cw+cw/2}" y="{y-10}" text-anchor="middle" font-family="Arial" font-size="14">{c}</text>')
        for a in range(2):
            s.append(f'<text x="{x-18}" y="{y+a*ch+ch/2+5}" text-anchor="middle" font-family="Arial" font-size="14">{a}</text>')
            for j,c in enumerate(cols):
                b=int(c[0]); ci=int(c[1]); v=fn(a,b,ci)
                xx=x+j*cw; yy=y+a*ch
                s.append(f'<rect x="{xx}" y="{yy}" width="{cw}" height="{ch}" fill="#f4f7fb" stroke="#263445"/>')
                s.append(f'<text x="{xx+cw/2}" y="{yy+ch/2+7}" text-anchor="middle" font-family="Arial" font-size="20">{v}</text>')
        if name=='Cout':
            s.append(f'<rect x="{x+cw}" y="{y+ch}" width="{2*cw}" height="{ch}" rx="16" fill="none" stroke="#d97706" stroke-width="4" stroke-opacity="0.8"/>')
            s.append(f'<rect x="{x+2*cw}" y="{y+ch}" width="{2*cw}" height="{ch}" rx="16" fill="none" stroke="#0891b2" stroke-width="4" stroke-opacity="0.8"/>')
            s.append(f'<rect x="{x+2*cw}" y="{y}" width="{cw}" height="{2*ch}" rx="16" fill="none" stroke="#7c3aed" stroke-width="4" stroke-opacity="0.8"/>')
        equation='S = A XOR B XOR Cin' if name=='S' else 'Cout = A·B + A·Cin + B·Cin'
        s.append(f'<text x="{x0+145}" y="290" text-anchor="middle" font-family="Arial" font-size="15">{equation}</text>')
    s.append('<text x="24" y="340" font-family="Arial" font-size="13">Cout também é G + P·Cin, com P=A XOR B e G=A·B; essa forma corresponde à cadeia de portas.</text>')
    s.append('</svg>')
    return ''.join(s)
write_svg('kmap_somador_1bit.svg',map_svg(),'Dois mapas 2×4. As colunas B Cin estão em código Gray 00, 01, 11, 10. Para S, os uns são isolados e a forma compacta é a paridade de três entradas, implementada por dois XOR. No mapa Cout, os contornos destacam os grupos A·Cin (âmbar), A·B (ciano) e B·Cin (roxo); o ponto A=1, B=1, Cin=1 participa de três grupos. A soma dos implicantes é AB + A·Cin + B·Cin. O circuito usa a forma fatorada G + P·Cin, com P=A XOR B e G=A·B.')

def chain_svg(name,title,n,mode):
    cw=92; gap=18; left=38; top=100; height=240; width=left*2+n*(cw+gap)-gap
    s=[svg_start(width,height,title)]
    if mode=='sub':
        s.append(f'<rect x="{left}" y="48" width="150" height="38" rx="5" fill="#eaf2ff" stroke="#24364b"/><text x="{left+75}" y="72" text-anchor="middle" font-family="Arial" font-size="14">BX[i]=B[i] XOR SUB</text>')
        s.append(f'<text x="{left+185}" y="72" font-family="Arial" font-size="14">Cin₀=SUB; para i&gt;0, Cinᵢ=Coutᵢ₋₁</text>')
        labels=[f'FA bit {i}' for i in range(n)]
        footer='R[i]=Sᵢ; Cout final é carry unsigned da soma transformada.'
    elif mode=='sm':
        s.append(f'<rect x="{left}" y="48" width="180" height="38" rx="5" fill="#eaf2ff" stroke="#24364b"/><text x="{left+90}" y="72" text-anchor="middle" font-family="Arial" font-size="14">X[i]=Z[i] XOR s</text>')
        s.append(f'<text x="{left+215}" y="72" font-family="Arial" font-size="14">Z=00M; Cin₀=s; B_FA=0</text>')
        labels=[f'FA bit {i}' for i in range(n)]
        footer='C2=(Z XOR {6{s}})+s; as saídas Sᵢ formam C2[i].'
    elif mode=='neg':
        s.append(f'<rect x="{left}" y="48" width="150" height="38" rx="5" fill="#eaf2ff" stroke="#24364b"/><text x="{left+75}" y="72" text-anchor="middle" font-family="Arial" font-size="14">N[i]=NOT R[i]</text>')
        s.append(f'<text x="{left+185}" y="72" font-family="Arial" font-size="14">Cin₀=1; B_FA=0</text>')
        labels=[f'FA bit {i}' for i in range(n)]
        footer='ABS=~R+1; C2→SM seleciona R ou ABS e descarta ABS[5].'
    elif mode=='negator':
        s.append(f'<rect x="{left}" y="48" width="150" height="38" rx="5" fill="#eaf2ff" stroke="#24364b"/><text x="{left+75}" y="72" text-anchor="middle" font-family="Arial" font-size="14">N[i]=NOT B_C2[i]</text>')
        s.append(f'<text x="{left+185}" y="72" font-family="Arial" font-size="14">Cin₀=1; B_FA=0</text>')
        labels=[f'FA bit {i}' for i in range(n)]
        footer='NEG=~B_C2+1 módulo 64; o carry final é descartado.'
    for i,label in enumerate(labels):
        x=left+i*(cw+gap)
        s.append(f'<rect x="{x}" y="{top}" width="{cw}" height="70" rx="6" fill="#f4f7fb" stroke="#263445"/>')
        s.append(f'<text x="{x+cw/2}" y="{top+28}" text-anchor="middle" font-family="Arial" font-size="15">{label}</text>')
        s.append(f'<text x="{x+cw/2}" y="{top+51}" text-anchor="middle" font-family="Arial" font-size="12">A,B,Cin → S,Cout</text>')
        if i<n-1:
            x1=x+cw; x2=x+cw+gap
            s.append(f'<path d="M{x1} {top+35} H{x2}" stroke="#183b66" stroke-width="2" marker-end="url(#arrow)"/>')
            s.append(f'<text x="{x1+gap/2}" y="{top+25}" text-anchor="middle" font-family="Arial" font-size="10">C{i+1}</text>')
    s.insert(1,'<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#183b66"/></marker></defs>')
    s.append(f'<text x="{left}" y="215" font-family="Arial" font-size="14">{footer}</text>')
    s.append(f'<text x="{left}" y="240" font-family="Arial" font-size="13">A propagação é do bit menos significativo (i=0) ao mais significativo (i={n-1}).</text>')
    s.append('</svg>')
    return ''.join(s)
for name,title,n,mode,description in [
('cadeia_sm_para_c2.svg','Conversão SM para C2 por ripple',6,'sm','Seis somadores completos recebem X[i], zero e o carry anterior. O carry inicial é o sinal SM[4]. Os quatro bits baixos de Z vêm da magnitude; Z[5:4]=00. A imagem mostra o caminho de carry, não substitui as ligações individuais descritas no grafo.'),
('cadeia_somador_subtrator_6bit.svg','Somador/subtrator de seis bits',6,'sub','SUB controla seis XOR em B e também Cin₀. Com SUB=0, o circuito calcula A+B; com SUB=1, calcula A+~B+1. Cada Cout alimenta o Cin do próximo bit, e o último Cout é exposto.'),
('cadeia_somador_subtrator_5bit.svg','Somador/subtrator de cinco bits',5,'sub','A cadeia de cinco estágios aplica B XOR SUB e Cin₀=SUB. R conserva os cinco bits baixos; Cout é o bit seguinte do cálculo unsigned transformado.'),
('cadeia_negador_c2_6bit.svg','Negação C2 por complemento e incremento',6,'negator','Seis NOT formam ~B_C2, seguido de seis somadores completos com Cin₀=1 e operandos B_FA=0. O carry final é descartado para obter negação módulo 64. −32 permanece ponto fixo.'),
('cadeia_c2_para_sm.svg','Valor absoluto e seleção C2 para SM',6,'neg','A metade esquerda calcula ABS=~R+1 em seis estágios. Em seguida, cinco muxes AND/OR escolhem R[4:0] para número não negativo ou ABS[4:0] para número negativo; sinal=R5 AND OR(R4..R0). Para −32, o resultado efetivo é zero e o caso permanece fora do domínio.')]:
    svg=chain_svg(name,title,n,mode)
    write_svg(name,svg,description)
