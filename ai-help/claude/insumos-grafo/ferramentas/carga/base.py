"""Helpers básicos de carga do catálogo sf-tutor.

Caminho da base: variável de ambiente SFTUTOR_BASE (usada pelos testes, que trabalham numa cópia temporária)
ou, por padrão, a pasta ai-help/claude/insumos-grafo/ que contém esta ferramenta.
"""
import json, os, re, unicodedata

BASE = os.environ.get("SFTUTOR_BASE") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = os.path.join(BASE, "catalogo")


def caminho(*partes):
    return os.path.join(BASE, *partes)

def slug(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def save(sub, name, obj):
    """Grava catalogo/<sub>/<name>.json (UTF-8, indentado, com quebra final)."""
    p = os.path.join(ROOT, sub, name + ".json") if sub else os.path.join(ROOT, name + ".json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")

def ev(src, nota=None, secao=None):
    e = {"fonte": src}
    if secao: e["secao"] = secao
    if nota: e["nota"] = nota
    return e

def af(estado, valor=None, nota=None, evs=None):
    a = {"estado": estado}
    if valor is not None: a["valor"] = valor
    if nota: a["nota"] = nota
    if evs: a["evidencias"] = evs
    return a



def ld(rel):
    """Lê catalogo/<rel> (ex.: 'funcionalidades/cors.json')."""
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def sv(rel, obj):
    """Grava catalogo/<rel> com a mesma formatação de save()."""
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")
