"""Contraste de pares usados en los componentes; no sustituye una auditoría WCAG completa."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def luminance(hex_):
    channels = [int(hex_[i:i+2], 16)/255 for i in (1,3,5)]
    linear = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in channels]
    return sum(v*w for v,w in zip(linear, [.2126,.7152,.0722]))
def contrast(a,b):
    x,y=sorted([luminance(a),luminance(b)],reverse=True)
    return (x+.05)/(y+.05)
pairs = [
    ('Texto principal','#1e352d','#ffffff',4.5),
    ('Texto secundario','#5d7067','#ffffff',4.5),
    ('Botón primario','#ffffff','#0b6b5b',4.5),
    ('Ayuda de login corregida','#5d705c','#fafcf7',4.5),
    ('Nota de inventario corregida','#536b58','#f6f8f5',4.5),
    ('Borde de campo corregido','#7c9186','#ffffff',3),
    ('Foco sobre fondo claro','#178473','#ffffff',3),
    ('Foco sobre navegación oscura','#178473','#102d27',3),
]
results=[dict(elemento=name,frente=a,fondo=b,ratio=round(contrast(a,b),2),minimo=threshold,cumple=contrast(a,b)>=threshold) for name,a,b,threshold in pairs]
report={'fecha':'2026-11-03','metodo':'Luminancia relativa sRGB WCAG 2.1; umbral evaluado sin redondear','antes':[{'elemento':'Borde de campo','ratio':round(contrast('#becdc7','#ffffff'),2),'minimo':3},{'elemento':'Texto de ayuda','ratio':round(contrast('#74826c','#fafcf7'),2),'minimo':4.5}],'despues':results}
out=ROOT/'S07_S08_A1/evidencias/contraste.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
assert all(item['cumple'] for item in results)
print(f'{len(results)} pares revisados cumplen su umbral de contraste.')
