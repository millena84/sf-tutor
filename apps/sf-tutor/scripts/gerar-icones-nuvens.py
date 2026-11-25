#!/usr/bin/env python3
"""Gera os ícones do nó central e das nuvens (desenhos próprios, estilo do mascote Desbugando) em public/icones/nuvens/.

Não são logos da Salesforce: são objetos simples (headset, megafone, sacola...) com o contorno ameixa do bug,
preenchimentos claros, olhinhos e bochechas rosa (issue #142). A cor de fundo de cada nuvem segue a escala
PALETA_NUVEM de src/cores.ts, na ordem das nuvens em catalogo/salesforce.json; se essa ordem ou a paleta mudar,
atualize ORDEM/PAL aqui e rode de novo. Uso: python3 scripts/gerar-icones-nuvens.py
"""
import os
PAL=['#4c388a','#227084','#792c6a','#195e47','#375487','#62327a','#1d6765','#9b6bff','#3ee6f2','#ff4fb8','#2bbe6a','#6ca8f8','#cd5ddc','#34d2ae']
ORDEM=['nuv:platform-core','nuv:sales-cloud','nuv:service-cloud','nuv:data-360','nuv:experience-cloud','nuv:field-service','nuv:revenue','nuv:industries','nuv:marketing','nuv:commerce','nuv:tableau','nuv:mulesoft','nuv:slack','nuv:add-ons']
NOMES={'nuv:platform-core':'Agentforce 360 Platform','nuv:sales-cloud':'Agentforce Sales','nuv:service-cloud':'Agentforce Service','nuv:data-360':'Data 360','nuv:experience-cloud':'Experience Cloud','nuv:field-service':'Field Service and Operations','nuv:revenue':'Revenue Management','nuv:industries':'Industries','nuv:marketing':'Agentforce Marketing','nuv:commerce':'Agentforce Commerce','nuv:tableau':'Tableau','nuv:mulesoft':'MuleSoft','nuv:slack':'Slack','nuv:add-ons':'Add-ons','centro':'Ecossistema (nó central)'}
def lum(h):
    c=[int(h[i:i+2],16)/255 for i in (1,3,5)]; c=[x/12.92 if x<=.03928 else ((x+.055)/1.055)**2.4 for x in c]
    return .2126*c[0]+.7152*c[1]+.0722*c[2]
def tinta(bg):
    L=lum(bg); cb=(1.05)/(L+.05); cn=(L+.05)/(lum('#0B0F2A')+.05)
    return '#FFFFFF' if cb>=cn else '#0B0F2A'
P='#4A1D4F'; B='#FFFFFF'; L1='#F3E8FF'; L2='#E5DEFF'; R='#FF8CC6'
def face(cx, cy, s=1.0):
    e=3.6*s; r=1.7*s
    return (f'<circle cx="{cx-e}" cy="{cy}" r="{r}" fill="{P}" stroke="none"/><circle cx="{cx+e}" cy="{cy}" r="{r}" fill="{P}" stroke="none"/>'
            f'<circle cx="{cx-e+0.6*s}" cy="{cy-0.6*s}" r="{0.55*s}" fill="#fff" stroke="none"/><circle cx="{cx+e+0.6*s}" cy="{cy-0.6*s}" r="{0.55*s}" fill="#fff" stroke="none"/>'
            f'<ellipse cx="{cx-e-2.2*s}" cy="{cy+2.6*s}" rx="{1.6*s}" ry="{1.0*s}" fill="{R}" stroke="none"/><ellipse cx="{cx+e+2.2*s}" cy="{cy+2.6*s}" rx="{1.6*s}" ry="{1.0*s}" fill="{R}" stroke="none"/>'
            f'<path d="M{cx-1.8*s} {cy+2.4*s} Q{cx} {cy+4.2*s} {cx+1.8*s} {cy+2.4*s}" fill="none" stroke="{P}" stroke-width="{1.6*s}"/>')
G={
'centro': f'''<path d="M32 30 L32 13 M32 30 L49 23 M32 30 L45 47 M32 30 L19 47 M32 30 L15 23"/>
<circle cx="32" cy="13" r="4.5" fill="{L2}"/><circle cx="49" cy="23" r="4.5" fill="{R}"/><circle cx="45" cy="47" r="4.5" fill="#7FF0F7"/><circle cx="19" cy="47" r="4.5" fill="#8EE6B0"/><circle cx="15" cy="23" r="4.5" fill="{L1}"/>
<circle cx="32" cy="31" r="10" fill="{B}"/>'''+face(32,31,0.95),
'nuv:platform-core': f'''<path d="M16 39 L32 47 L48 39 L32 31 Z" fill="{L1}"/><path d="M16 32 L32 40 L48 32 L32 24 Z" fill="{L2}"/><path d="M16 24.5 L32 32.5 L48 24.5 L32 16.5 Z" fill="{B}"/>'''+face(32,24,0.75),
'nuv:sales-cloud': f'''<path d="M22 16 H42 V24 A10 10 0 0 1 22 24 Z" fill="{B}"/><path d="M22 18 H17 A5 5 0 0 0 22 26 M42 18 H47 A5 5 0 0 1 42 26" fill="none"/><path d="M32 34 V40"/><rect x="24" y="40" width="16" height="7" rx="3" fill="{L2}"/>'''+face(32,22,0.8),
'nuv:service-cloud': f'''<circle cx="32" cy="33" r="11" fill="{B}"/><path d="M18 33 V30 A14 14 0 0 1 46 30 V33" fill="none"/><rect x="14.5" y="29" width="7" height="11" rx="3.5" fill="{L2}"/><rect x="42.5" y="29" width="7" height="11" rx="3.5" fill="{L2}"/><path d="M46 40 Q46 47 38 47"/><circle cx="37" cy="47" r="2" fill="{R}"/>'''+face(32,33,0.85),
'nuv:data-360': f'''<path d="M19 19 V44 A13 5 0 0 0 45 44 V19" fill="{B}"/><ellipse cx="32" cy="19" rx="13" ry="5" fill="{L2}"/><path d="M19 27 A13 5 0 0 0 45 27" fill="none"/>'''+face(32,36,0.9),
'nuv:experience-cloud': f'''<rect x="14" y="16" width="36" height="30" rx="6" fill="{B}"/><path d="M14 23.5 H50" fill="none"/><circle cx="19.5" cy="20" r="1.3" fill="{R}" stroke="none"/><circle cx="24" cy="20" r="1.3" fill="{L2}" stroke="none"/>'''+face(32,33,0.95),
'nuv:field-service': f'''<path d="M32 50 C32 50 18 38 18 28 A14 14 0 0 1 46 28 C46 38 32 50 32 50 Z" fill="{B}"/>'''+face(32,28,0.9),
'nuv:revenue': f'''<path d="M19 14 H45 V49 L40.7 46 L36.3 49 L32 46 L27.7 49 L23.3 46 L19 49 Z" fill="{B}"/><path d="M25 35 H39 M25 40 H34" fill="none"/>'''+face(32,24,0.85),
'nuv:industries': f'''<circle cx="45" cy="13" r="3" fill="{L1}"/><circle cx="49.5" cy="9.5" r="2.2" fill="{L1}"/><path d="M14 48 V30 L23 35 V30 L32 35 V30 L41 35 V18 H48 V48 Z" fill="{B}"/>'''+face(28,41,0.8),
'nuv:marketing': f'''<path d="M15 27 H23 L42 16 V48 L23 37 H15 Z" fill="{B}"/><path d="M23 37 L26 47 H31 L29.5 38" fill="{L2}"/><path d="M47 25 Q51 32 47 39" fill="none"/>'''+face(31,31,0.8),
'nuv:commerce': f'''<path d="M24 25 V21 A8 8 0 0 1 40 21 V25" fill="none"/><path d="M16 25 H48 L45.5 49 H18.5 Z" fill="{B}"/>'''+face(32,36,0.95),
'nuv:tableau': f'''<circle cx="32" cy="32" r="16" fill="{B}"/><path d="M32 32 L32 16 A16 16 0 0 1 47.2 27.1 Z" fill="{R}"/><path d="M32 32 L47.2 27.1 A16 16 0 0 1 43.3 43.3 Z" fill="{L2}"/>'''+face(27,35,0.8),
'nuv:mulesoft': f'''<path d="M24 32 H40" fill="none"/><circle cx="21" cy="32" r="9.5" fill="{B}"/><circle cx="43" cy="32" r="9.5" fill="{L2}"/>'''+face(21,31,0.7)+face(43,31,0.7),
'nuv:slack': f'''<path d="M33 29 H48 A4 4 0 0 1 52 33 V42 A4 4 0 0 1 48 46 H47 V50 L42 46 H37 A4 4 0 0 1 33 42 Z" fill="{L2}"/><circle cx="40" cy="40" r="1.5" fill="{P}" stroke="none"/><circle cx="44.5" cy="40" r="1.5" fill="{P}" stroke="none"/><circle cx="49" cy="40" r="1.5" fill="{P}" stroke="none"/><path d="M13 19 A4 4 0 0 1 17 15 H37 A4 4 0 0 1 41 19 V30 A4 4 0 0 1 37 34 H25 L18 40 V34 H17 A4 4 0 0 1 13 30 Z" fill="{B}"/>'''+face(27,24,0.85),
'nuv:add-ons': f'''<path d="M17 23 H25 A4.5 4.5 0 1 1 34 23 H43 V31 A4.5 4.5 0 1 1 43 40 V48 H17 Z" fill="{B}"/>'''+face(30,36,0.9),
}
def svg(i, cor, titulo, tamanho=64):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="{tamanho}" height="{tamanho}" role="img" aria-label="{titulo}"><title>{titulo}</title>'
            f'<circle cx="32" cy="32" r="30" fill="{cor}" stroke="{P}" stroke-width="2.5"/>'
            f'<g fill="none" stroke="{P}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">{G[i]}</g></svg>')

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "icones", "nuvens")
os.makedirs(SAIDA, exist_ok=True)
for i, cor in [("centro", "#0B0F2A")] + [(n, PAL[k]) for k, n in enumerate(ORDEM)]:
    with open(os.path.join(SAIDA, i.replace("nuv:", "") + ".svg"), "w", encoding="utf-8") as h:
        h.write(svg(i, cor, NOMES[i]) + "\n")
print("ícones gerados em public/icones/nuvens/")
