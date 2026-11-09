"""Objetos API e seus campos (obj:)."""
from .base import save, ev, af

L = {"C": "create", "D": "defaulted_on_create", "F": "filter", "G": "group", "N": "nillable", "R": "restricted_picklist", "S": "sort", "U": "update", "I": "id_lookup"}

def field(obj, nome, tipo, props, ver, desc, src, apis=("padrao",), **kw):
    e = [ev(src)]
    pa = {"estado": "verificado" if props is not None else "desconhecido"}
    if props is not None:
        for k, v in L.items():
            pa[v] = k in props
        pa["evidencias"] = e
    ro = None if props is None else not ("C" in props or "U" in props)
    t = tipo.lower()
    if kw.get("vals"):
        dom = {"natureza": "enum_fechado", "valores": [{"valor": v} for v in kw["vals"]], "lista_completa": kw.get("completa", "desconhecido"), "estado": "verificado", "evidencias": e,
               "contexto": kw.get("contexto", "Valores conforme a página; listas de picklist podem variar por org, idioma ou recurso habilitado.")}
    elif t == "boolean":
        dom = {"natureza": "booleano", "valores": [{"valor": "true"}, {"valor": "false"}], "lista_completa": "sim", "estado": "verificado", "evidencias": e}
    elif t == "reference":
        dom = {"natureza": "referencia", "estado": "verificado" if kw.get("ref") else "desconhecido", **({"evidencias": e} if kw.get("ref") else {}),
               "contexto": "Id de registro do(s) objeto(s) referenciado(s)."}
    elif t in ("datetime", "date"):
        dom = {"natureza": "data_hora", "estado": "verificado", "evidencias": e}
    elif t in ("int", "double", "currency"):
        dom = {"natureza": "numerico", "estado": "verificado", "evidencias": e}
    elif t == "id":
        dom = {"natureza": "identificador", "estado": "verificado", "evidencias": e}
    elif t in ("picklist", "multipicklist"):
        dom = {"natureza": "lista_dinamica", "estado": "desconhecido", "contexto": "Valores não extraídos; podem depender de org, idioma ou recurso."}
    elif t in ("string", "textarea", "email", "phone", "url"):
        dom = {"natureza": "texto_livre", "estado": "verificado", "evidencias": e}
    else:
        dom = {"natureza": "desconhecida", "estado": "desconhecido"}
    if kw.get("dominio"): dom = kw["dominio"]
    if kw.get("req"):
        ob = {"valor": kw["req"][0], "estado": "verificado", "evidencias": e}
        if kw["req"][1]: ob["condicao"] = kw["req"][1]
    else:
        ob = {"valor": "desconhecida", "estado": "desconhecido"}
    if kw.get("default"):
        forma, valor, nota = kw["default"]
        dflt = {"forma": forma, "estado": "verificado", "evidencias": e, **({"valor": valor} if valor is not None else {}), **({"nota": nota} if nota else {})}
    elif props and "D" in props:
        dflt = {"forma": "desconhecido", "estado": "desconhecido", "nota": "A API marca o campo como 'defaulted on create', mas o valor não foi declarado na extração."}
    else:
        dflt = {"forma": "nao_declarado_na_fonte", "estado": "desconhecido"}
    f = {"id": f"{obj}.{nome}", "nome": nome, "tipo_tecnico": tipo,
         "o_que_e": desc or "Explicação pendente: campo listado a partir da fonte, ainda sem texto didático.",
         "apis": list(apis), "propriedades_api": pa, "somente_leitura": ro,
         "origem": af("verificado", "padrao_plataforma", "Campo padrão do objeto documentado.", e),
         "obrigatoriedade": ob, "default": dflt, "dominio": dom,
         "disponibilidade": {"desde_versao": ver, "ate_versao": kw.get("ate"), "estado": "verificado" if ver else "desconhecido"},
         "explicacao": "explicada" if desc else "pendente", "estado": kw.get("estado", "verificado"), "evidencias": e}
    if kw.get("ref") is not None:
        f["referencia"] = {"alvos": kw["ref"], "nome_relacionamento": kw.get("rel")}
    if kw.get("rotulo"): f["rotulo_didatico"] = kw["rotulo"]
    if kw.get("notas"): f["notas"] = kw["notas"]
    if kw.get("restr"): f["restricoes"] = af("verificado", kw["restr"], None, e)
    return f

def obj(nome, o_que_e, papel, exposicoes, campos, consultas, apex, cobertura, src, juncao=False, alertas=None, label=None, din=None, estado="verificado"):
    o = {"id": "obj:" + nome, "nome": nome, "o_que_e": o_que_e, "papel": papel, "exposicoes": exposicoes, "campos": campos,
         "consultas": consultas, "apex": apex, "juncao": juncao,
         "setup": af("nao_aplicavel", None, "Objeto consultável via API; não é tela do Setup."),
         "cobertura": cobertura, "alertas": alertas or [], "estado": estado, "evidencias": [ev(src)]}
    if label: o["label_oficial"] = af("desconhecido", label, "Rótulo didático; label oficial não extraído.")
    if din: o["dominio_dinamico_de_campos"] = din
    save("objetos-api", nome, o)

def cob(est, esp, pres, expl, nota):
    return {"estrutural": {"estado": est, "esperado": esp, "presente": pres, "nota": nota},
            "explicativa": {"estado": "completa" if expl == pres else "parcial", "esperado": pres, "presente": expl},
            "mapeamento": {"estado": "parcial", "nota": "Ver relacionamentos registrados."}}

def expo(api, estado, src=None, chamadas=None, rest=None, desde=None, acesso=None, restr=None, nota=None):
    x = {"api": api, "estado": estado}
    for k, v in (("chamadas", chamadas), ("metodos_rest", rest), ("acesso_especial", acesso), ("restricoes_consulta", restr), ("nota", nota)):
        if v: x[k] = v
    x["desde_versao"] = desde
    if src: x["evidencias"] = [ev(src)]
    return x

APEX_OK = lambda src: {"consulta_soql_direta": af("verificado", True, "Objeto da API padrão: consultável por SOQL em Apex, sujeito a permissões.", [ev(src)]), "nota": "Exemplo Apex não fornecido nesta fase."}
APEX_TOOLING = {"consulta_soql_direta": af("nao_exposto", False, "Objeto exposto apenas pela Tooling API: não é consultável por SOQL comum em Apex. Em Apex, o acesso seria um callout HTTP para a Tooling API, com autenticação e permissões próprias; não implementado nesta fase."), "nota": "Usar a Tooling API (REST/SOAP)."}

def cnt(campos): return sum(1 for c in campos if c["explicacao"] == "explicada")
