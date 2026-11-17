#!/usr/bin/env python3
"""Gera svg/order-of-execution-completo.svg de forma reproduzível.

Fonte técnica: Apex Developer Guide, "Triggers and Order of Execution"
(numeração oficial 1-20). Esquema didático; classificações de fase e de
mecanismo são próprias do projeto, não nomenclatura oficial.
"""

from pathlib import Path
from xml.sax.saxutils import escape

BASE = Path(__file__).resolve().parent
SAIDA = BASE / "svg" / "order-of-execution-completo.svg"
FONTE = ("https://developer.salesforce.com/docs/platform/apex-dev/references/"
         "apex-dev/apex-triggers-order-of-execution.html")

# Paleta Desbugando (a mesma dos diagramas bloco-*)
NAVY, INK, BG = "#0B0F2A", "#1C1440", "#F5F7FF"
ROXO, CIANO, ROSA, VERDE = "#9B6BFF", "#3EE6F2", "#FF4FB8", "#2BBE6A"
FONT = "Arial, DejaVu Sans, sans-serif"

W = 1080
COL_X, COL_W = 250, 470          # coluna principal
ANOT_X, ANOT_W = 760, 300        # anotações à direita

MEC = {  # mecanismo -> (cor, rótulo da pílula)
    "sis": (INK, "Sistema"),
    "apex": (ROXO, "Apex"),
    "flow": (CIANO, "Flow"),
    "regra": (ROSA, "Regra declarativa"),
    "commit": (VERDE, "Commit"),
    "async": (ROXO, "Assíncrono"),
}

# (número, título, linhas de detalhe, mecanismos, legado?)
ETAPAS = [
    (1, "Carrega o registro", ["Original do banco ou inicializado para upsert"], ["sis"], False),
    (2, "Aplica os novos valores e valida conforme a origem",
     ["UI padrão: regras do layout, obrigatórios, formato, tamanho máximo",
      "Apex / API: só chaves estrangeiras e picklists restritas",
      "Criação multilinha (ex.: quote/opportunity line items): validation rules"],
     ["sis"], False),
    (3, "Record-triggered Flows before-save", ["Alteram o próprio registro sem DML adicional"], ["flow"], False),
    (4, "Before triggers", ["before insert / before update"], ["apex"], False),
    (5, "Validações de sistema de novo + validation rules",
     ["Obrigatórios e não nulos; regras do layout não são repetidas"], ["sis", "regra"], False),
    (6, "Duplicate rules", ["Ação “bloquear” interrompe o salvamento aqui"], ["regra"], False),
    (7, "Salva no banco, SEM commit", ["No insert, o ID já existe; ainda pode ser desfeito"], ["sis"], False),
    (8, "After triggers", ["after insert / after update"], ["apex"], False),
    (9, "Assignment rules", ["A primeira regra que casar define o proprietário"], ["regra"], False),
    (10, "Auto-response rules", ["A primeira regra que casar prepara o e-mail"], ["regra"], False),
    (11, "Workflow rules", ["Field update dispara uma reexecução (ver ao lado)"], ["regra"], True),
    (12, "Escalation rules", ["Aplicável a objetos com escalonamento (ex.: Case)"], ["regra"], False),
    (13, "Processes + flows lançados por process ou workflow",
     ["Sem ordem garantida entre eles"], ["regra", "flow"], True),
    (14, "Record-triggered Flows after-save", ["Caminho imediato: ainda antes do commit"], ["flow"], False),
    (15, "Entitlement rules", ["Aplicável a objetos com entitlements"], ["regra"], False),
    (16, "Roll-up summary / cross-object workflow no PAI",
     ["Recalcula o pai, que passa pelo procedimento de save"], ["sis"], False),
    (17, "Roll-up summary / cross-object workflow no AVÔ",
     ["Se o pai mudou: recalcula o avô, que passa pelo save"], ["sis"], False),
    (18, "Criteria-based sharing", ["Avalia compartilhamento por critério (acesso a registro, não FLS)"], ["sis"], False),
    (19, "COMMIT de todas as operações DML", ["A partir daqui, o salvamento está confirmado"], ["commit"], False),
    (20, "Lógica pós-commit (sem ordem garantida)",
     ["Envio de e-mail · Apex assíncrono enfileirado (Queueable, future)",
      "Caminhos assíncronos de record-triggered Flow"], ["async"], False),
]

# Fases (classificação didática própria): (primeira, última, nome, linhas, cor)
FASES = [
    (1, 6, "1 · Antes de salvar", ["Prepara e valida", "o registro"], CIANO),
    (7, 15, "2 · Salvo, sem commit", ["Automações no", "próprio registro"], ROXO),
    (16, 18, "3 · Propagação", ["Efeitos em outros", "registros"], ROSA),
    (19, 19, "4 · Confirmação", [], VERDE),
    (20, 20, "5 · Depois do commit", ["Outra(s) transação(ões)"], ROXO),
]

out = []
add = out.append


def t(x, y, s, size=13, anchor="start", weight=None, fill=INK, italic=False):
    extra = f' font-weight="{weight}"' if weight else ""
    extra += ' font-style="italic"' if italic else ""
    add(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
        f'fill="{fill}"{extra}>{escape(s)}</text>')


def rect(x, y, w, h, fill, op=1.0, stroke=None, sw=1, rx=6, dash=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    s += f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
        f'fill-opacity="{op}"{s}/>')


def seta(d, dash=None, cor=INK, marker="arrow"):
    s = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="1.6"{s} '
        f'marker-end="url(#{marker})"/>')


def caixa_nota(x, y, w, linhas, cor, titulo=None, dash=None):
    h = 14 + (22 if titulo else 0) + 17 * len(linhas)
    rect(x, y, w, h, cor, 0.10, cor, 1.2, 6, dash)
    yy = y + 22
    if titulo:
        t(x + 12, yy, titulo, 13, weight="700", fill=NAVY)
        yy += 21
    for ln in linhas:
        t(x + 12, yy, ln, 12)
        yy += 17
    return h


# ---------- layout vertical ----------
y = 30
corpo = []
add('<g font-family="%s">' % FONT)
t(30, y + 8, "Order of Execution no Salesforce · salvamento completo", 22, weight="700", fill=NAVY)
t(30, y + 32, "insert, update e upsert de um registro · numeração oficial do Apex Developer Guide (1–20)", 13)
y += 62

# Cliente
rect(COL_X, y, COL_W, 44, INK, 0.05, INK, 1, 6, "4 3")
t(COL_X + 14, y + 19, "No navegador (só UI, se houver picklist dependente)", 13, weight="700", fill=NAVY)
t(COL_X + 14, y + 36, "Validação JavaScript dos valores da picklist dependente", 12)
t(COL_X - 18, y + 27, "Cliente", 13, anchor="end", weight="700", fill=NAVY)
y += 44
seta(f"M{COL_X + COL_W/2} {y} V{y + 22}")
y += 24
t(COL_X - 18, y + 4, "Servidor", 13, anchor="end", weight="700", fill=NAVY)
y += 14

pos = {}  # número -> (y_topo, altura)
GAP = 14
for i, (n, tit, det, mecs, legado) in enumerate(ETAPAS):
    if n == 19:
        y += 8
    h = 30 + 16 * len(det) + 6
    cor = MEC[mecs[0]][0]
    if n == 19:
        rect(COL_X, y, COL_W, h, VERDE, 0.20, NAVY, 2)
    else:
        rect(COL_X, y, COL_W, h, "#FFFFFF", 1, cor, 1.3, 6, "6 4" if legado else None)
    # faixa lateral do mecanismo
    for j, m in enumerate(mecs):
        c = MEC[m][0]
        add(f'<rect x="{COL_X + 1 + j*6}" y="{y + 1}" width="6" height="{h - 2}" fill="{c}" fill-opacity="0.85"/>')
    # número
    cx = COL_X + 32
    add(f'<circle cx="{cx}" cy="{y + 20}" r="13" fill="{cor}" fill-opacity="0.22" stroke="{cor}"/>')
    t(cx, y + 24.5, str(n), 13, anchor="middle", weight="700", fill=NAVY)
    t(COL_X + 54, y + 25, tit, 14, weight="700", fill=NAVY)
    yy = y + 43
    for d in det:
        t(COL_X + 54, yy, d, 12)
        yy += 16
    # pílulas de mecanismo (texto, não só cor)
    px = COL_X + COL_W - 8
    rotulos = [MEC[m] for m in mecs] + ([(INK, "legado")] if legado else [])
    for c, r in reversed(rotulos):
        pw = 8 + 6.6 * len(r)
        px -= pw
        rect(px, y - 9, pw, 18, c if r != "legado" else "#FFFFFF", 0.95 if r != "legado" else 1,
             c if r != "legado" else INK, 1, 9, "3 2" if r == "legado" else None)
        if r != "legado":
            rect(px, y - 9, pw, 18, "#FFFFFF", 0.55, None, 1, 9)
        t(px + pw/2, y + 4, r, 11, anchor="middle", weight="700", fill=NAVY)
        px -= 4
    pos[n] = (y, h)
    y += h
    if n != 20:
        espaco = GAP + (18 if n == 19 else 0)
        seta(f"M{COL_X + COL_W/2} {y} V{y + espaco - 2}")
        y += espaco
y_fim_etapas = y

# ---------- fases (gutter esquerdo) ----------
for a, b, nome, linhas, cor in FASES:
    y0 = pos[a][0] - 6
    y1 = pos[b][0] + pos[b][1] + 6
    rect(18, y0, 196, y1 - y0, cor, 0.12, cor, 1, 6)
    t(30, y0 + 22, nome, 14, weight="700", fill=NAVY)
    for k, ln in enumerate(linhas):
        t(30, y0 + 41 + 16 * k, ln, 12)

# Transação: chave 1–19
yt0, yt1 = pos[1][0], pos[19][0] + pos[19][1]
add(f'<path d="M232 {yt0} H226 V{yt1} H232" fill="none" stroke="{NAVY}" stroke-width="2"/>')

# Save recursivo: chave 9–17 (à direita da coluna)
yr0, yr1 = pos[9][0] + 4, pos[17][0] + pos[17][1] - 4
xr = 200
add(f'<path d="M{xr - 6} {yr0} H{xr} V{yr1} H{xr - 6}" fill="none" stroke="{ROSA}" stroke-width="2"/>')
add(f'<text x="{xr - 14}" y="{(yr0 + yr1)/2}" font-size="12" fill="{INK}" font-weight="700" '
    f'text-anchor="middle" transform="rotate(-90 {xr - 14} {(yr0 + yr1)/2})">'
    f'Save recursivo: etapas 9 a 17 são puladas</text>')

# ---------- anotações ----------
# Transação (topo da coluna direita)
y_tr = pos[1][0] - 6
caixa_nota(ANOT_X, y_tr, ANOT_W,
           ["Etapas 1 a 19 são a MESMA transação:",
            "orçamento de governor limits compartilhado.",
            "Exceção não tratada antes do commit",
            "→ nada do salvamento é confirmado.",
            "“After” = depois de gravar, não de confirmar."],
           NAVY, "Fronteira transacional")

# Dependent: bloqueio por duplicate rule
y6 = pos[6][0]
hb = caixa_nota(ANOT_X, y6 - 8, ANOT_W,
                ["Registro NÃO é salvo; nenhuma etapa",
                 "seguinte roda (nem after triggers,",
                 "nem workflow rules)."],
                ROSA, "Duplicate rule com bloqueio")
seta(f"M{COL_X + COL_W} {y6 + pos[6][1]/2} H{ANOT_X - 4}", cor=ROSA, marker="arrowRosa")

# Workflow field update
y11 = pos[11][0]
hw = caixa_nota(ANOT_X + 20, pos[8][0] - 10, ANOT_W - 20,
                ["1. Atualiza o registro de novo",
                 "2. Repete validações de sistema",
                 "3. Before e after UPDATE triggers",
                 "\u00a0\u00a0\u00a0rodam mais 1 vez (só 1), mesmo",
                 "\u00a0\u00a0\u00a0que a operação seja insert",
                 "Não repete: validation rules, flows,",
                 "duplicate, processes, escalation.",
                 "Trigger.old = valor antes do update",
                 "inicial, não antes do field update."],
                ROXO, "Workflow field update ↺", dash="5 3")
seta(f"M{COL_X + COL_W} {y11 + pos[11][1]/2} C {ANOT_X - 10} {y11 + 20}, {ANOT_X - 10} {y11 - 40}, "
     f"{ANOT_X + 16} {pos[8][0] + hw/2}", dash="5 3", cor=ROXO, marker="arrowRoxo")

# Process / flow DML
y13 = pos[13][0]
caixa_nota(ANOT_X + 20, y13 - 4, ANOT_W - 20,
           ["DML feito por process ou flow:",
            "o registro afetado passa pelo",
            "procedimento de save de novo."],
           ROXO, "Nova entrada no save")
seta(f"M{COL_X + COL_W} {y13 + pos[13][1]/2} H{ANOT_X + 16}", dash="5 3", cor=ROXO, marker="arrowRoxo")

# Pai/avô
y16 = pos[16][0]
caixa_nota(ANOT_X + 20, y16, ANOT_W - 20,
           ["Pai e avô executam o próprio",
            "order of execution dentro da",
            "mesma transação: mais consumo",
            "de limites e mais automações."],
           ROSA, "Cascata para cima")
seta(f"M{COL_X + COL_W} {y16 + pos[16][1]/2} H{ANOT_X + 16}", cor=ROSA, marker="arrowRosa")

# Pós-commit
y20 = pos[20][0]
caixa_nota(ANOT_X, y20 - 6, ANOT_W,
           ["Roda depois do commit, com limites",
            "próprios. Falha aqui NÃO desfaz o",
            "registro já confirmado."],
           ROXO, "Fora da transação de origem")

# ---------- legenda e notas ----------
y = y_fim_etapas + 34
add(f'<line x1="30" y1="{y - 14}" x2="{W - 30}" y2="{y - 14}" stroke="{INK}" stroke-opacity="0.2"/>')
t(30, y + 6, "Legenda", 14, weight="700", fill=NAVY)
lx = 110
for chave in ["sis", "apex", "flow", "regra", "commit"]:
    c, r = MEC[chave]
    add(f'<rect x="{lx}" y="{y - 6}" width="14" height="14" rx="3" fill="{c}" fill-opacity="0.85"/>')
    t(lx + 20, y + 6, r, 12)
    lx += 34 + 6.8 * len(r)
rect(lx, y - 6, 26, 14, "#FFFFFF", 1, INK, 1.2, 3, "5 3")
t(lx + 32, y + 6, "borda tracejada = legado", 12)

notas = [
    "• Vários triggers (ou vários flows) no mesmo objeto e evento: a ordem entre eles não é garantida.",
    "• Workflow Rules e Process Builder: fim de suporte em 31/12/2025, mas automações já ativas continuam rodando.",
    "• API 53.0 e anteriores: o guia registra posição diferente para after-save Flow em relação a entitlement rules.",
    "• Etapas condicionais: dependem da operação, do objeto, da origem e do que está configurado na org.",
    "• Fases, cores e agrupamento de mecanismos são classificação didática do Desbugando, não nomenclatura oficial.",
    "Fonte: Apex Developer Guide, “Triggers and Order of Execution” · verificado em 17/11/2026 (Winter ’27).",
]
y += 30
for n in notas:
    t(30, y, n, 12, italic=n.startswith("Fonte"))
    y += 19
y += 12
add("</g>")

ALTURA_CORPO = y
H = ALTURA_CORPO + 52

# ---------- rodapé de marca ----------
logo = (BASE / "marca" / "desbugando-bug-lupa-escura.svg").read_text(encoding="utf-8")
logo_corpo = logo.split(">", 1)[1].rsplit("</svg>", 1)[0]
rodape = (
    f'<g data-brand-footer="true" aria-label="Desbugando - tecnologia sem mistério">'
    f'<rect x="0" y="{ALTURA_CORPO}" width="{W}" height="52" fill="{INK}"/>'
    f'<g opacity="0.92"><svg x="18" y="{ALTURA_CORPO + 8}" width="36" height="36" '
    f'viewBox="0 0 120 120" aria-hidden="true">{logo_corpo}</svg>'
    f'<text x="66" y="{ALTURA_CORPO + 32}" text-anchor="start" font-family="{FONT}" '
    f'font-size="15" font-weight="600" fill="{BG}">Desbugando - tecnologia sem mistério</text></g></g>'
)

titulo = "Order of Execution no Salesforce · salvamento completo"
desc = ("Sequência oficial de 20 etapas ao salvar um registro com insert, update ou upsert: "
        "carga, validações, before-save Flow, before triggers, duplicate rules, gravação sem commit, "
        "after triggers, assignment, auto-response, workflow, escalation, processes, after-save Flow, "
        "entitlement, roll-ups no pai e no avô, criteria-based sharing, commit e lógica pós-commit. "
        f"Inclui reentradas e interrupções. Referência técnica: {FONTE}. Esquema didático.")

marcadores = "".join(
    f'<marker id="{i}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
    f'orient="auto-start-reverse"><path d="M1 1 L8 5 L1 9" fill="none" stroke="{c}" stroke-width="1.5"/></marker>'
    for i, c in [("arrow", INK), ("arrowRosa", ROSA), ("arrowRoxo", ROXO)]
)

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'role="img" aria-labelledby="title desc">\n'
    f'<title id="title">{escape(titulo)}</title>\n<desc id="desc">{escape(desc)}</desc>\n'
    f'<defs>{marcadores}</defs>\n<rect width="{W}" height="{ALTURA_CORPO}" fill="{BG}"/>\n'
    + "\n".join(out) + "\n" + rodape + "</svg>\n"
)

if __name__ == "__main__":
    SAIDA.write_text(svg, encoding="utf-8")
    print(f"{SAIDA.relative_to(BASE)}: {W}x{H}")
