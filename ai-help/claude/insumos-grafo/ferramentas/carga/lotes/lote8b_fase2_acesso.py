"""Lote 8b (Fase 2, classificação Acesso, identidade e segurança): os 31 campos de User que só tinham nome.

Resultado da leitura (ver a nota): a Object Reference descreve 2 deles (Country, UserPreferencesShowCountryToExternalUsers), que ganham
explicação. Para os outros, a Field Reference dá só tipo e rótulo: o tipo é gravado e o rótulo oficial vai para as notas; a explicação
continua pendente, porque não há descrição oficial. Reexecutável. Rode a partir de ai-help/claude/insumos-grafo/.
"""
import json, os, re, sys

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

V = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "config", "versoes.json"), encoding="utf-8"))["plataforma_core"]
TEXTO_NAO_ENCONTRADA = (f"Não encontrada descrição oficial na última versão da documentação ({V['numero_interno_documentacao']}, "
                        f"API {V['api_version']}); verificado também nas notas da release {V['release']} (por busca).")
C.registrar_fontes([
    C.fonte("src:objref-user-atual", "User (Object Reference, referência nova)",
            "https://developer.salesforce.com/docs/platform/object-reference/references/standard-objects/object-user.html",
            "Conferência: nenhum dos 29 campos tem descrição ligada ao nome.", EXTR, DATA, versao="sem versão na página"),
    C.fonte("src:rn-winter27-busca", "Salesforce Winter '27 Release Notes: New and Changed Objects (por busca)",
            "https://help.salesforce.com/s/articleView?id=release-notes.rn_api_objects.htm&language=en_US&release=264&type=5",
            "Conferência por busca: os 29 campos não aparecem nas notas de versão.", EXTR, DATA, versao="Winter '27",
            metodo="leitura_resultado_busca"),
])

o = ld("objetos-api/User.json")
velha = "Nome listado na Object Reference; tipo e propriedades não extraídos nesta rodada."
exp_n = tipo_n = 0
for c in o["campos"]:
    if c.get("explicacao") not in ("pendente", "nao_encontrada"):
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
        nota = f"Rótulo oficial: \"{rotulo}\"."
        c["o_que_e"], c["explicacao"] = TEXTO_NAO_ENCONTRADA, "nao_encontrada"
        for s_ in ("src:objref-user-atual", "src:rn-winter27-busca"):
            if s_ not in [e["fonte"] for e in c["evidencias"]]:
                c["evidencias"].append({"fonte": s_})
        c["notas"] = [x for x in c.get("notas", []) if x != velha and not x.startswith("Rótulo oficial:")] + [nota]
o["cobertura"]["explicativa"]["presente"] = sum(1 for c in o["campos"] if c.get("explicacao") == "explicada")
sv("objetos-api/User.json", o)
print(f"lote 8b: {exp_n} campos explicados; {tipo_n} com tipo novo; "
      f"{sum(1 for c in o['campos'] if c.get('explicacao') == 'nao_encontrada')} sem descrição oficial encontrada")
