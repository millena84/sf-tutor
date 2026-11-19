"""Lote 8b (Fase 2, classificação Acesso, identidade e segurança): os 31 campos de User que só tinham nome.

Resultado da leitura (ver a nota): a Object Reference descreve 2 deles (Country, UserPreferencesShowCountryToExternalUsers), que ganham
explicação. Para os outros, a Field Reference dá só tipo e rótulo: o tipo é gravado e o rótulo oficial vai para as notas; a explicação
continua pendente, porque não há descrição oficial. Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ld, sv               # noqa: E402
from carga import catalogo as C             # noqa: E402

DATA = "2026-11-19"
EXTR = "fontes/extracoes/lote8b-fase2-acesso.txt"
OR, FR = "src:objref-user-264", "src:fieldref-user-264"
C.registrar_fontes([
    C.fonte(OR, "User (Object Reference 264.0)",
            "https://developer.salesforce.com/docs/get_document_content/object_reference/sforce_api_objects_user.htm/en-us/264.0",
            "Descrição de Country e UserPreferencesShowCountryToExternalUsers; confirma que os outros 29 não constam da tabela.", EXTR, DATA),
    C.fonte(FR, "User (Field Reference, 264.0)",
            "https://developer.salesforce.com/docs/get_document_content/sfFieldRef/salesforce_field_reference_User.htm/en-us/264.0",
            "Tipo e rótulo dos campos de User; a página não traz descrições.", EXTR, DATA),
])

EXPLICA = {
    "Country": ("string", None, "País associado ao usuário, com até 80 caracteres."),
    "UserPreferencesShowCountryToExternalUsers": ("boolean", "26.0",
        "Controla se o país do usuário aparece para membros externos num site do Experience Cloud. Com false, o país ainda pode aparecer "
        "se UserPreferencesShowCountryToGuestUsers for true. O padrão é false."),
}
notas_fonte = open(EXTR, encoding="utf-8").read()
ROTULOS = {m.group(1): (m.group(2), m.group(3)) for m in re.finditer(r"^  (\w+) \| (\w+) \| (.+)$", notas_fonte, re.M)
           if m.group(1) not in EXPLICA}

o = ld("objetos-api/User.json")
velha = "Nome listado na Object Reference; tipo e propriedades não extraídos nesta rodada."
exp_n = tipo_n = 0
for c in o["campos"]:
    if c.get("explicacao") != "pendente":
        continue
    n = c["nome"]
    if n in EXPLICA:
        tipo, v, txt = EXPLICA[n]
        c["tipo_tecnico"] = tipo
        c["o_que_e"], c["explicacao"] = txt, "explicada"
        for s in (OR,):
            if s not in [e["fonte"] for e in c["evidencias"]]:
                c["evidencias"].append({"fonte": s})
        if v and c["disponibilidade"].get("estado") == "desconhecido":
            c["disponibilidade"] = {"desde_versao": v, "ate_versao": None, "estado": "verificado"}
        exp_n += 1
    elif n in ROTULOS:
        tipo, rotulo = ROTULOS[n]
        if c.get("tipo_tecnico") in (None, "(a extrair)"):
            c["tipo_tecnico"] = tipo
            tipo_n += 1
        if FR not in [e["fonte"] for e in c["evidencias"]]:
            c["evidencias"].append({"fonte": FR})
        nota = (f"Rótulo oficial: \"{rotulo}\". Sem descrição na Object Reference 264.0 nem na Field Reference (lote 8b); "
                "explicação fica pendente até haver fonte.")
        c["notas"] = [x for x in c.get("notas", []) if x != velha and not x.startswith("Rótulo oficial:")] + [nota]
o["cobertura"]["explicativa"]["presente"] = sum(1 for c in o["campos"] if c.get("explicacao") == "explicada")
sv("objetos-api/User.json", o)
print(f"lote 8b: {exp_n} campos explicados; {tipo_n} com tipo novo; {len(ROTULOS)} rótulos registrados")
