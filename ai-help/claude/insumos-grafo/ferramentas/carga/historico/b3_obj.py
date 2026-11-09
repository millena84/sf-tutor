# REGISTRO HISTÓRICO (issue #11). Script de carga como foi usado na sessão original, com caminhos absolutos daquela sessão.
# Não reexecute sobre o catálogo atual: o catálogo em JSON é a fonte da verdade. Para lotes novos, use ferramentas/carga/.
# Bootstrap: objetos API, relacionamentos, funcionalidades, nuvens e nó central.
from b1_base import save, ev, af, CLS, SUB_FUNCS

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

def build_objects():
    # ---------------- User ----------------
    S = "src:objref-user"
    rows = [("AboutMe","textarea","CFNSU"),("AccountId","reference","FGNS"),("Address","address","FN"),("Alias","string","CFGSU"),("BadgeText","string","FGNS"),("BannerPhotoUrl","url","FNS"),
            ("CallCenterId","reference","CFGNSU"),("City","string","CFGNSU"),("CommunityNickname","string","CFGSU"),("CompanyName","string","CFGNSU"),("ContactId","reference","CFGNSU"),("Country","string","CFGNSU"),
            ("CountryCode","picklist","CFGNSU"),("CurrentStatus","textarea","CFNSU"),("DefaultCurrencyIsoCode","picklist","CDFGNRSU"),("DefaultDivision","picklist","CDFGRSU"),("DefaultGroupNotificationFrequency","picklist","CDFGRSU"),
            ("DelegatedApproverId","reference","CFGNSU"),("Department","string","CFGNSU"),("DigestFrequency","picklist","CDFGRSU"),("Division","string","CFGNSU"),("Email","email","CFGISU"),("EmailEncodingKey","picklist","CFGRSU"),
            ("EmailPreferencesAutoBcc","boolean","CFU"),("EmployeeNumber","string","CFGNSU"),("EndDay","picklist","CFGNRSU"),("Extension","phone","CFGNSU"),("Fax","phone","CFGNSU"),("FederationIdentifier","string","CFINSU"),
            ("FirstName","string","CFGNSU"),("ForecastEnabled","boolean","CDFGSU"),("FullPhotoUrl","url","FNS"),("GeocodeAccuracy","picklist","CFGNRSU"),("HasUserVerifiedEmail","boolean","DFGS"),("HasUserVerifiedPhone","boolean","DFGS"),
            ("IndividualId","reference","CFGNSU"),("IsPartner","boolean","DF"),("IsPortalEnabled","boolean","DFGSU"),("IsPortalSelfRegistered","boolean","CDFGS")]
    desc = {"Email": "Endereço de e-mail do usuário.", "FirstName": "Nome do usuário.", "Department": "Departamento do usuário.", "FederationIdentifier": "Identificador usado no login único (SSO) federado.",
            "Alias": "Apelido curto do usuário.", "CommunityNickname": "Apelido exibido em comunidades.", "ContactId": "Contato associado, para usuários externos."}
    campos = [field("obj:User", n, t, p, None, desc.get(n), S) for n, t, p in rows]
    campos.append(field("obj:User", "IsActive", "boolean", "CDFGSU", None, "Informa se o usuário pode entrar na org; desativar não exclui o usuário.", S, rotulo="Ativo"))
    campos.append(field("obj:User", "ProfileId", "reference", None, None, "Perfil do usuário, que define suas permissões base e sua licença.", S, ref=["obj:Profile"], rel="Profile",
                        notas=["Propriedades de API não extraídas com segurança (a página nova exibia a linha sem o nome do campo)."]))
    campos.append(field("obj:User", "UserRoleId", "reference", None, None, "Papel do usuário na hierarquia de papéis.", S, ref=["UserRole"], rel="UserRole"))
    campos.append(field("obj:User", "ManagerId", "reference", None, None, "Usuário que é gestor deste usuário.", S, ref=["obj:User"], rel="Manager"))
    campos.append(field("obj:User", "Username", "string", None, None, "Nome de login no formato de e-mail, único entre todas as orgs.", S, req=("sim", None)))
    campos.append(field("obj:User", "UserType", "picklist", None, None, "Categoria de licença do usuário (lista restrita).", S))
    campos.sort(key=lambda c: c["nome"])
    obj("User", "Representa cada usuário da org: pessoas e integrações que fazem login.", "Representação principal da funcionalidade Usuários. Não existe metadata type correspondente.",
        [expo("padrao", "verificado", S, ["create()", "describeLayout()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "search()", "update()", "upsert()"],
              acesso="Criar ou atualizar exige Manage Internal Users; usuários de portal exigem também Manage Customer Users ou Manage External Users."),
         expo("tooling", "desconhecido", nota="Exposição pela Tooling API não investigada.")],
        campos, [{"api": "padrao", "soql": "SELECT Id, Username, IsActive, Profile.Name FROM User WHERE IsActive = true ORDER BY Username LIMIT 20", "contexto": "API padrão (REST /query ou SOAP query()).", "validacao": "documental"}],
        APEX_OK(S), cob("parcial", None, len(campos), cnt(campos), "BLOQUEIO: a extração alcançou 40 linhas da tabela (até IsPortalSelfRegistered) mais 5 campos citados; a lista completa da página não foi obtida."), S,
        alertas=["delete() não consta entre as chamadas suportadas: usuários são desativados (IsActive), não excluídos.", "A consulta só retorna o que o usuário da integração pode ver."])

    # ---------------- Profile ----------------
    S = "src:objref-profile"
    campos = [field("obj:Profile", "Description", "string", "CFGNSU", None, "Descrição do perfil.", S),
              field("obj:Profile", "IsSsoEnabled", "boolean", "DFGSU", None, "Se usuários do perfil podem delegar a verificação de login a um sistema corporativo.", S),
              field("obj:Profile", "LastReferencedDate", "dateTime", "FNS", "29.0", "Quando o usuário atual viu pela última vez um registro relacionado ao perfil.", S),
              field("obj:Profile", "LastViewedDate", "dateTime", "FNS", "29.0", "Quando o usuário atual viu o perfil pela última vez.", S),
              field("obj:Profile", "Name", "string", "CFGISU", None, "Nome do perfil.", S),
              field("obj:Profile", "UserLicenseId", "reference", "CFGS", None, "Licença de usuário associada ao perfil.", S, ref=["UserLicense"]),
              field("obj:Profile", "UserType", "picklist", "FGNRS", "10.0", "Categoria de licença do perfil.", S, vals=["Standard", "PowerPartner", "CspLitePortal", "CustomerSuccess", "PowerCustomerSuccess", "CsnOnly", "Guest"])]
    obj("Profile", "Representa cada perfil da org como registro consultável.", "Permite consultar perfis e suas permissões; o XML Profile é a forma implantável.",
        [expo("padrao", "verificado", S, ["create()", "delete()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "search()", "update()", "upsert()"],
              acesso="Ver configurações de perfil exige View Setup and Configuration; usuários de portal não acessam."),
         expo("tooling", "desconhecido", nota="Não investigado.")],
        campos, [{"api": "padrao", "soql": "SELECT Id, Name, UserType FROM Profile ORDER BY Name", "contexto": "API padrão.", "validacao": "documental"}],
        APEX_OK(S), cob("parcial", None, len(campos), cnt(campos), "Campos não-Permissions listados; Id e campos de sistema não constam da extração; Permissions* são dinâmicos."), S,
        din={"padrao_nome": "Permissions*", "descricao": "Um campo booleano por permissão (Create, Filter, Update). O conjunto depende da org e do tipo de licença; obter com describeSObjects().", "estado": "verificado", "evidencias": [ev(S)]})

    # ---------------- PermissionSet ----------------
    S = "src:objref-permissionset"
    campos = [field("obj:PermissionSet", "Description", "string", "CFNGSU", None, "Descrição do permission set.", S, restr="Até 255 caracteres."),
              field("obj:PermissionSet", "HasActivationRequired", "boolean", "CDFGSU", None, "Se o permission set exige sessão ativa.", S),
              field("obj:PermissionSet", "IsCustom", "boolean", "DFGS", None, "Verdadeiro se criado por um administrador; falso se padrão e ligado a uma licença.", S),
              field("obj:PermissionSet", "IsOwnedByProfile", "boolean", "DFGS", "25.0", "Informa se o permission set pertence a um perfil.", S),
              field("obj:PermissionSet", "Label", "string", "CFGSU", None, "Rótulo do permission set na interface.", S, restr="Até 80 caracteres."),
              field("obj:PermissionSet", "LicenseId", "reference", "CFGNS", "38.0", "Licença de permission set ou de usuário associada; substitui UserLicenseId.", S, ref=["PermissionSetLicense", "UserLicense"]),
              field("obj:PermissionSet", "Name", "string", "CFGSU", None, "Nome API único do permission set.", S, restr="Até 80 caracteres."),
              field("obj:PermissionSet", "NamespacePrefix", "string", "FGNS", "23.0", "Namespace do pacote, quando o permission set vem de um pacote.", S),
              field("obj:PermissionSet", "PermissionSetGroupId", "reference", "FGNS", "45.0", "Grupo de permission sets dono deste registro, ou nulo.", S, ref=["obj:PermissionSetGroup"]),
              field("obj:PermissionSet", "ProfileId", "reference", "FGNS", "25.0", "Perfil dono deste registro, ou nulo.", S, ref=["obj:Profile"]),
              field("obj:PermissionSet", "Type", "reference", "FGNS", "46.0", None, S, notas=["A página não descreve o campo além da versão; tipo transcrito como reference, conferir."]),
              field("obj:PermissionSet", "UserLicenseId", "reference", "CFGNS", "26.0", "Licença de usuário (obsoleto após a 37.0; usar LicenseId).", S, ref=["UserLicense"], ate="37.0")]
    obj("PermissionSet", "Representa cada permission set como registro consultável, inclusive os permission sets internos de perfis.", "Permite consultar quais permission sets existem e seus atributos; o XML PermissionSet é a forma implantável.",
        [expo("padrao", "verificado", S, ["create()", "delete()", "describeSObjects()", "query()", "retrieve()", "search()", "update()", "upsert()"],
              acesso="Desde Summer '20: View Setup and Configuration, Manage Session Permission Set Activations, Assign Permission Sets ou Manage Profiles and Permission Sets."),
         expo("tooling", "desconhecido", nota="Não investigado.")],
        campos, [{"api": "padrao", "soql": "SELECT Id, Name, Label, IsOwnedByProfile FROM PermissionSet WHERE IsOwnedByProfile = false", "contexto": "API padrão; o filtro exclui permission sets internos de perfis.", "validacao": "documental"}],
        APEX_OK(S), cob("parcial", None, len(campos), cnt(campos), "Campos não-Permissions listados; Id e campos de sistema não constam da extração; Permissions* são dinâmicos."), S,
        din={"padrao_nome": "Permissions*", "descricao": "Um campo booleano por permissão (Create, Filter, Update); conjunto varia por org e licença; obter com describeSObjects().", "estado": "verificado", "evidencias": [ev(S)]})

    # ---------------- PermissionSetGroup ----------------
    S = "src:objref-permissionsetgroup"
    campos = [field("obj:PermissionSetGroup", "Description", "textarea", "CFGNSU", None, "Descrição do grupo.", S),
              field("obj:PermissionSetGroup", "DeveloperName", "string", "CFGSU", None, "Nome do grupo usado na API.", S),
              field("obj:PermissionSetGroup", "HasActivationRequired", "boolean", "CDFGSU", "53.0", "Se o grupo exige sessão ativa.", S, default=("false", False, "A página declara default false.")),
              field("obj:PermissionSetGroup", "Language", "picklist", "CDFGNRSU", None, "Idioma do grupo.", S, vals=["da","de","en_US","es","es_MX","fi","fr","it","ja","ko","nl_NL","no","pt_BR","ru","sv","th","zh_CN","zh_TW"]),
              field("obj:PermissionSetGroup", "MasterLabel", "string", "CFGSU", None, "Rótulo do grupo.", S),
              field("obj:PermissionSetGroup", "NamespacePrefix", "string", "FGNS", None, "Namespace do grupo.", S),
              field("obj:PermissionSetGroup", "Status", "picklist", "DFGRS", None, "Estado de recálculo do grupo.", S, vals=["Updated", "Outdated", "Updating", "Failed"], completa="desconhecido")]
    obj("PermissionSetGroup", "Representa cada grupo de permission sets como registro consultável.", "Consulta de grupos; o XML PermissionSetGroup é a forma implantável.",
        [expo("padrao", "verificado", S, ["create()", "delete()", "describeSObjects() (transcrito como describeObject(); conferir)", "query()", "retrieve()", "update()", "upsert()"], desde="45.0",
              acesso="Ver: View Setup and Configuration, Manage Session Permission Set Activations ou Assign Permission Sets. Editar: Manage Profiles and Permission Sets."),
         expo("tooling", "desconhecido", nota="Não investigado.")],
        campos, [{"api": "padrao", "soql": "SELECT Id, DeveloperName, MasterLabel, Status FROM PermissionSetGroup", "contexto": "API padrão.", "validacao": "documental"}],
        APEX_OK(S), cob("parcial", None, len(campos), cnt(campos), "Tabela da página extraída; Id e campos de sistema não constam."), S)

    # ---------------- PermissionSetAssignment (junção) ----------------
    S = "src:objref-permissionsetassignment"
    campos = [field("obj:PermissionSetAssignment", "AssigneeId", "reference", "CFGS", None, "Informa qual usuário recebeu a atribuição.", S, ref=["obj:User"], rel="Assignee", rotulo="Quem recebe"),
              field("obj:PermissionSetAssignment", "ExpirationDate", "datetime", "CFNSU", "52.0", "Data em que a atribuição deixa de valer para o usuário.", S),
              field("obj:PermissionSetAssignment", "IsActive", "boolean", "DFGS", "52.0", "Informa se a atribuição está ativa.", S, default=("false", False, "A página declara default false.")),
              field("obj:PermissionSetAssignment", "IsRevoked", "boolean", "DFGSU", "57.0", "Informa se a atribuição foi revogada por uma política de acesso; o registro é mantido.", S, default=("false", False, "A página declara default false."), notas=["Disponível só com user access policies habilitadas."]),
              field("obj:PermissionSetAssignment", "LastCreatedByChangeId", "reference", "FGNS", "57.0", "Registro de mudança de acesso que criou a atribuição.", S, ref=["UserAccessChange"], rel="LastCreatedByChange", notas=["Nome do campo inferido do nome de relacionamento; confirmar no describe."], estado="desconhecido"),
              field("obj:PermissionSetAssignment", "LastDeletedByChangeId", "reference", "FGNS", "57.0", "Registro de mudança de acesso ligado à revogação.", S, ref=["UserAccessChange"], rel="LastDeletedByChange", notas=["Nome do campo inferido do nome de relacionamento; confirmar no describe."], estado="desconhecido"),
              field("obj:PermissionSetAssignment", "PermissionSetGroupId", "reference", "CFGNS", "41.0", "Informa o grupo de permission sets atribuído, quando a atribuição é de um grupo.", S, ref=["obj:PermissionSetGroup"], rel="PermissionSetGroup"),
              field("obj:PermissionSetAssignment", "PermissionSetId", "reference", "CFGNS", None, "Informa qual permission set foi atribuído.", S, ref=["obj:PermissionSet"], rel="PermissionSet")]
    obj("PermissionSetAssignment", "Objeto de junção: cada registro liga um usuário a um permission set ou a um grupo de permission sets.", "É onde a atribuição de permission sets e grupos fica gravada.",
        [expo("padrao", "verificado", S, ["create()", "delete()", "describeSObjects()", "query()", "retrieve()", "update()"], desde="22.0",
              acesso="Desde Summer '20: View Setup and Configuration, Assign Permission Sets ou Manage User."),
         expo("tooling", "desconhecido", nota="Não investigado.")],
        campos, [{"api": "padrao", "soql": "SELECT Id, Assignee.Username, PermissionSet.Name, PermissionSetGroupId FROM PermissionSetAssignment WHERE AssigneeId = '<Id do usuário>'", "contexto": "API padrão; substitua o marcador por um Id de usuário.", "validacao": "documental"}],
        APEX_OK(S), cob("parcial", None, len(campos), cnt(campos), "Campos da tabela extraída; Id e campos de sistema não constam."), S, juncao=True,
        alertas=["Para alterar uma atribuição, a página orienta excluir o registro antigo e inserir outro.", "A licença do permission set precisa ser compatível com a licença do perfil do usuário.",
                 "Não supor que PermissionSetId e PermissionSetGroupId estejam preenchidos em toda atribuição (ambos anuláveis)."])

    # ---------------- UserLogin ----------------
    S = "src:objref-userlogin"
    campos = [field("obj:UserLogin", "IsFrozen", "boolean", "DFGSU", "29.0", "Informa se a conta está congelada: login bloqueado sem desativar o usuário.", S),
              field("obj:UserLogin", "IsPasswordLocked", "boolean", "DFGSU", "29.0", "Informa bloqueio por excesso de tentativas; a API pode limpar, mas não definir.", S),
              field("obj:UserLogin", "UserId", "reference", "FGNS", "29.0", "Usuário a que este estado pertence; não pode ser alterado.", S, ref=["obj:User"])]
    obj("UserLogin", "Representa o estado atual de login de um usuário, como congelado ou bloqueado.", "Estado atual; não é histórico.",
        [expo("padrao", "verificado", S, ["describeSObjects()", "query()", "retrieve()", "update()"], desde="29.0", acesso="Manage Users."), expo("tooling", "desconhecido", nota="Não investigado.")],
        campos, [{"api": "padrao", "soql": "SELECT UserId, IsFrozen, IsPasswordLocked FROM UserLogin WHERE IsFrozen = true", "contexto": "API padrão.", "validacao": "documental"}],
        APEX_OK(S), cob("parcial", None, len(campos), cnt(campos), "Campos da tabela extraída; Id e campos de sistema não constam."), S)

    # ---------------- LoginHistory ----------------
    S = "src:objref-loginhistory"
    rows = [("ApiType","string","GNS",None,"Tipo de API usado pelo cliente."),("ApiVersion","string","GNS",None,"Versão de API usada."),("Application","string","GNS",None,"Aplicação usada no acesso."),
            ("AuthContextClassRef","string","FGNS","67.0","Método de autenticação informado pelo provedor externo (claim ACR)."),("AuthMethodReference","string","FGNS","51.0","Método de autenticação de provedor OIDC."),
            ("AuthenticationServiceId","reference","FGNS","34.0","Configuração de SAML ou provedor de autenticação usada."),("Browser","string","GNS",None,"Navegador usado."),
            ("CipherSuite","picklist","FGNRS","37.0","Conjunto de cifras TLS do login."),("ClientVersion","string","GNS",None,"Versão do cliente da API."),("CountryIso","string","FGNS","37.0","País do IP, em código ISO 3166."),
            ("ForwardedForIp","string","FGNS","61.0","Valor X-Forwarded-For enviado pelo cliente."),("LoginGeoId","reference","FGNS","34.0","Registro de geolocalização do login."),
            ("LoginSubType","picklist","FGNRS",None,"Subtipo do fluxo de login."),("LoginTime","dateTime","FS",None,"Data e hora do login (GMT)."),("LoginType","picklist","FGRS",None,"Método de login."),
            ("LoginUrl","string","FGNS",None,"URL de onde veio o pedido de login."),("NetworkId","reference","FGNS","31.0","Site do Experience Cloud acessado."),("OptionsIsGet","boolean","F",None,"Se o login usou HTTP GET."),
            ("OptionsIsPost","boolean","F",None,"Se o login usou HTTP POST."),("Platform","string","GNS",None,"Sistema operacional usado."),("SourceIp","string","FGNS",None,"IP da primeira requisição que chegou à Salesforce."),
            ("Status","string","GNS",None,"Resultado do login: sucesso ou motivo da falha."),("TlsProtocol","picklist","FGNRS","37.0","Versão de TLS usada."),("UserId","reference","FGNS",None,"Usuário que tentou entrar.")]
    refs = {"AuthenticationServiceId": ["AuthProvider", "SamlSsoConfig"], "LoginGeoId": ["LoginGeo"], "NetworkId": ["Network"], "UserId": ["obj:User"]}
    campos = [field("obj:LoginHistory", n, t, p, v, d, S, ref=refs.get(n), rotulo=("IP de origem" if n == "SourceIp" else None),
                    notas=(["Não aceita o operador LIKE."] if n == "SourceIp" else None)) for n, t, p, v, d in rows]
    obj("LoginHistory", "Representa cada tentativa de login, bem-sucedida ou não, na org e em portais habilitados.", "Histórico de tentativas; complementa o estado atual de UserLogin.",
        [expo("padrao", "verificado", S, ["describeSObjects()", "query()", "retrieve()", "delete() (habilitável a partir da 42.0)"], desde="21.0",
              acesso="Manage Users ou Monitor Login History; desde a 37.0 cada usuário lê os próprios registros."), expo("tooling", "desconhecido", nota="Não investigado.")],
        campos, [{"api": "padrao", "soql": "SELECT UserId, LoginTime, SourceIp, Status FROM LoginHistory ORDER BY LoginTime DESC LIMIT 20", "contexto": "API padrão.", "validacao": "documental"}],
        APEX_OK(S), cob("parcial", None, len(campos), cnt(campos), "Campos da tabela extraída; Id não consta. Retenção não declarada na página."), S,
        alertas=["Somente campos marcados como filtráveis (e Id) podem ser usados em filtros."])

    # ---------------- RecordType ----------------
    S = "src:objref-recordtype"
    campos = [field("obj:RecordType", "BusinessProcessId", "reference", "CFGNSU", "17.0", "Processo de negócio associado; exigido para tipos de Opportunity e Lead.", S, ref=["BusinessProcess"]),
              field("obj:RecordType", "Description", "string", "CFGNSU", None, "Descrição.", S, restr="Até 255 caracteres."),
              field("obj:RecordType", "DeveloperName", "string", "CFGSU", None, "Nome API único do tipo de registro.", S),
              field("obj:RecordType", "IsActive", "boolean", "DFGSU", None, "Se o tipo está ativo; só tipos ativos se aplicam a registros.", S),
              field("obj:RecordType", "IsPersonType", "boolean", "DFGS", None, "Marca tipo de conta pessoal (com contas pessoais habilitadas).", S),
              field("obj:RecordType", "Name", "string", "CFGSU", None, "Rótulo do tipo de registro.", S, restr="Até 80 caracteres."),
              field("obj:RecordType", "NamespacePrefix", "string", "FGNS", None, "Namespace do pacote gerenciado.", S),
              field("obj:RecordType", "SobjectType", "picklist", "CFGRS", None, "Objeto ao qual o tipo de registro se aplica.", S, dominio={"natureza": "lista_dinamica", "estado": "verificado", "evidencias": [ev(S)], "contexto": "Objetos da org que suportam tipos de registro, inclusive customizados."})]
    obj("RecordType", "Representa cada tipo de registro como registro consultável.", "Consulta dos tipos de registro e de seus Ids, usados em RecordTypeId dos registros.",
        [expo("padrao", "verificado", S, ["create()", "describeSObjects()", "getDeleted()", "getUpdated()", "query()", "retrieve()", "update()", "upsert()"],
              acesso="Tipos de registro não são controle de acesso; quem acessa o objeto lê as informações de tipo."), expo("tooling", "desconhecido", nota="Não investigado.")],
        campos, [{"api": "padrao", "soql": "SELECT Id, DeveloperName, SobjectType, IsActive FROM RecordType WHERE SobjectType = 'Account'", "contexto": "API padrão.", "validacao": "documental"}],
        APEX_OK(S), cob("parcial", None, len(campos), cnt(campos), "Campos da tabela extraída; Id e campos de sistema não constam."), S)

    # ---------------- ValidationRule (Tooling) ----------------
    S = "src:tooling-validationrule"
    T = ("tooling",)
    campos = [field("obj:ValidationRule", "Active", "boolean", "DFGS", None, "Se a regra está ativa.", S, T),
              field("obj:ValidationRule", "Description", "string", "FNS", None, "Descrição da regra.", S, T),
              field("obj:ValidationRule", "EntityDefinitionId", "string", "FGS", None, "Id do objeto (EntityDefinition) ao qual a regra pertence.", S, T, ref=["obj:EntityDefinition"], rel="EntityDefinition"),
              field("obj:ValidationRule", "ErrorDisplayField", "string", "FGNS", None, "Campo onde a mensagem aparece.", S, T),
              field("obj:ValidationRule", "ErrorMessage", "string", "FGNS", None, "Mensagem exibida quando a regra bloqueia.", S, T, restr="Até 255 caracteres."),
              field("obj:ValidationRule", "FullName", "string", "CGN", None, "Nome completo da regra.", S, T),
              field("obj:ValidationRule", "Id", "id", "DFGIS", None, "Id do registro da regra.", S, T),
              field("obj:ValidationRule", "ManageableState", "ManageableState", "FGNRS", None, "Estado do componente em pacotes.", S, T),
              field("obj:ValidationRule", "Metadata", "ValidationRule (Metadata API)", "CNU", None, "Conteúdo da regra no formato do tipo ValidationRule da Metadata API.", S, T, dominio={"natureza": "tipo_composto", "estado": "verificado", "evidencias": [ev(S)]}),
              field("obj:ValidationRule", "NamespacePrefix", "string", "FGNS", None, "Namespace.", S, T),
              field("obj:ValidationRule", "ValidationName", "string", "FGS", None, "Nome da regra.", S, T)]
    obj("ValidationRule", "Expõe as regras de validação pela Tooling API.", "Consultar e alterar regras de validação programaticamente; o campo Metadata traz o conteúdo no formato da Metadata API.",
        [expo("tooling", "verificado", S, ["create()", "delete()", "query()", "retrieve()", "update()", "upsert()"], ["Query", "GET", "POST", "PATCH"], "34.0"),
         expo("padrao", "nao_exposto", nota="Documentado como objeto da Tooling API; não aparece na Object Reference consultada. Confirmar ausência em describeGlobal se houver org.")],
        campos, [{"api": "tooling", "soql": "SELECT Id, ValidationName, Active, ErrorMessage FROM ValidationRule", "endpoint": "/services/data/v68.0/tooling/query?q=...", "contexto": "Tooling API.", "validacao": "documental"}],
        APEX_TOOLING, cob("completa", 11, len(campos), cnt(campos), "11 campos da tabela; o campo de relacionamento EntityDefinition é representado pela referência de EntityDefinitionId."), S,
        alertas=["A exposição na API padrão foi marcada como não exposta com base na documentação consultada; não testado em org."], estado="verificado")

    # ---------------- CustomField / CustomObject (Tooling) ----------------
    S = "src:tooling-customfield"
    campos = [field("obj:CustomField", n, t, p, v, d, S, T, **kw) for n, t, p, v, d, kw in [
        ("DeveloperName", "string", "FGS", None, "Nome de desenvolvedor do campo, sem o sufixo __c.", {}),
        ("ManageableState", "ManageableState", "FGNRS", None, "Estado do componente em pacotes.", {}),
        ("Metadata", "CustomFieldMetadata", "CNU", None, "Propriedades do campo no formato do tipo CustomField da Metadata API.", {"dominio": {"natureza": "tipo_composto", "estado": "verificado", "evidencias": [ev(S)]}}),
        ("NamespacePrefix", "string", "FGNS", None, "Namespace do campo.", {}),
        ("TableEnumOrId", "picklist", "FGRS", None, "Objeto pai, como nome (ex.: Account) ou Id.", {"dominio": {"natureza": "lista_dinamica", "estado": "verificado", "evidencias": [ev(S)], "contexto": "Objetos da org."}}),
        ("creationType", "DefinitionCreationType", "FGNS", "67.0", "Se o campo foi criado por usuário ou por taxonomia padrão.", {})]]
    obj("CustomField", "Expõe campos customizados pela Tooling API.", "Consultar e alterar campos customizados; o campo Metadata traz o conteúdo no formato da Metadata API.",
        [expo("tooling", "verificado", S, ["create()", "query()", "retrieve()", "search()", "update()", "upsert()"], ["Query", "GET", "POST", "PATCH"], "28.0", restr=["Metadata só pode ser consultado quando o resultado tem no máximo um registro."]),
         expo("padrao", "desconhecido", nota="Não investigado.")],
        campos, [{"api": "tooling", "soql": "SELECT DeveloperName, NamespacePrefix, TableEnumOrId FROM CustomField", "endpoint": "/services/data/v68.0/tooling/query?q=...", "contexto": "Tooling API.", "validacao": "documental"}],
        APEX_TOOLING, cob("parcial", None, len(campos), cnt(campos), "A extração pode ter omitido campos como Id e FullName; conferir."), S)
    S = "src:tooling-customobject"
    campos = [field("obj:CustomObject", n, t, p, v, d, S, T) for n, t, p, v, d in [
        ("CustomHelpId", "id", "FGNS", None, "Recurso de ajuda personalizada do objeto."), ("Description", "string", "FNS", None, "Descrição do objeto."),
        ("DeveloperName", "string", "FGS", None, "Nome de desenvolvedor sem o sufixo __c."), ("ExternalName", "string", "FGNS", None, "Tabela correspondente na fonte externa."),
        ("ExternalRepository", "string", "FGNS", None, "Nome da tabela externa definido pelo Validate and Sync."), ("Language", "string", "FGRS", None, "Código de idioma."),
        ("ManageableState", "ManageableState", "FGNRS", None, "Estado do componente em pacotes."), ("NamespacePrefix", "string", "FGNS", None, "Namespace do pacote."),
        ("SharingModel", "picklist", "FGNRS", None, "Modelo de compartilhamento."), ("creationType", "DefinitionCreationType", "FGNS", "67.0", "Se foi criado por usuário ou por taxonomia padrão.")]]
    obj("CustomObject", "Expõe objetos customizados pela Tooling API.", "Consulta de objetos customizados. Diferente de EntityDefinition, que cobre objetos padrão e customizados.",
        [expo("tooling", "verificado", S, ["query()", "retrieve()", "search()"], ["Query", "GET"], "31.0"), expo("padrao", "desconhecido", nota="Não investigado.")],
        campos, [{"api": "tooling", "soql": "SELECT DeveloperName, NamespacePrefix, SharingModel FROM CustomObject", "endpoint": "/services/data/v68.0/tooling/query?q=...", "contexto": "Tooling API.", "validacao": "documental"}],
        APEX_TOOLING, cob("parcial", None, len(campos), cnt(campos), "Campo Metadata/FullName não apareceu na extração; não presumir."), S)

    # ---------------- EntityDefinition / FieldDefinition (Tooling; parciais) ----------------
    S = "src:tooling-entitydefinition"
    names = ["DeploymentStatus", "Description", "DeveloperName", "DurableId", "FullName", "IsCustomSetting", "IsCustomizable", "IsQueryable", "KeyPrefix", "Label", "MasterLabel", "Metadata", "NamespacePrefix"]
    tipos = {"DeploymentStatus": ("picklist", "FGNRS"), "Description": ("string", "FNS"), "DeveloperName": ("string", "FGNS"), "DurableId": ("string", "FGNS"), "FullName": ("string", "CGN"),
             "IsCustomSetting": ("boolean", "DFGS"), "IsCustomizable": ("boolean", "DFGS"), "IsQueryable": ("boolean", "DFGS"), "KeyPrefix": ("string", "FGNS"), "Label": ("string", "FGNS"),
             "MasterLabel": ("string", "FGS"), "Metadata": ("CustomObject (Metadata API)", "CNU"), "NamespacePrefix": ("string", "FGNS"), "QualifiedApiName": ("string", None)}
    descs = {"DeploymentStatus": "Visibilidade de objetos customizados para não administradores.", "DurableId": "Identificador do objeto; recuperar antes de usar, pois pode mudar entre releases.",
             "FullName": "Nome completo; só em consultas com no máximo um registro.", "Metadata": "Metadados do objeto no formato CustomObject da Metadata API; só com no máximo um registro.",
             "QualifiedApiName": "Nome API qualificado do objeto.", "KeyPrefix": "Prefixo dos Ids dos registros do objeto.", "Label": "Rótulo do objeto."}
    campos = []
    for n in names:
        t, p = tipos[n]
        kw = {}
        if n == "DeploymentStatus": kw["vals"] = ["InDevelopment", "Deployed"]
        if n == "Metadata": kw["dominio"] = {"natureza": "tipo_composto", "estado": "verificado", "evidencias": [ev(S)]}
        campos.append(field("obj:EntityDefinition", n, t, p, None, descs.get(n), S, T, **kw))
    obj("EntityDefinition", "Expõe a definição de objetos padrão e customizados para consulta.", "Ponto de entrada para metadados de qualquer objeto; não é o único mapeamento de CustomObject (ver Tooling CustomObject).",
        [expo("tooling", "verificado", S, ["query()", "search()"], ["GET"], "32.0", restr=["Campos de relacionamento (Fields, Layouts etc.) só em subconsultas.", "Metadata e FullName só quando o resultado tem no máximo um registro."]),
         expo("padrao", "desconhecido", S, nota="A página da Tooling API cita uso via SOAP API (45.0+, modo guest); exposição e campos na API padrão a confirmar na Object Reference.")],
        campos, [{"api": "tooling", "soql": "SELECT DeveloperName, KeyPrefix, Label FROM EntityDefinition WHERE IsCustomizable = true", "endpoint": "/services/data/v68.0/tooling/query?q=...", "contexto": "Tooling API.", "validacao": "documental"}],
        APEX_TOOLING, cob("parcial", None, len(campos), cnt(campos), "Recorte de 13 campos entre os 64 extraídos (página com 137k caracteres lida até 100k; campos após NamespacePrefix, como QualifiedApiName, não foram lidos). Inventário completo pendente."), S,
        alertas=["A disponibilidade na API padrão não foi confirmada; o bloco Apex segue a exposição verificada (Tooling)."])
    S = "src:tooling-fielddefinition"
    fd = [("DataType", "string", "FGS", "Tipo exibido na interface, como Text(40)."), ("Description", "string", "FNS", "Descrição."), ("DeveloperName", "string", "FGS", "Nome de desenvolvedor."),
          ("DurableId", "string", "FGS", "Identificador do campo; recuperar antes de usar."), ("EntityDefinitionId", "string", "FGS", "Identificador do objeto que contém o campo."),
          ("FullName", "string", "CGN", "Nome completo; só em consultas com no máximo um registro."), ("IsNillable", "boolean", "DFGS", "Se o campo aceita nulo."), ("Label", "string", "FGS", "Rótulo."),
          ("Length", "int", "FGS", "Tamanho."), ("Metadata", "CustomField (Metadata API)", "CNU", None), ("QualifiedApiName", "string", "FGS", "Nome API qualificado do campo."),
          ("RelationshipName", "string", "FGS", "Nome do relacionamento, quando o campo é de referência.")]
    campos = []
    for n, t, p, d in fd:
        kw = {}
        if n == "EntityDefinitionId": kw.update(ref=["obj:EntityDefinition"], rel="EntityDefinition")
        if n == "Metadata": kw.update(dominio={"natureza": "tipo_composto", "estado": "desconhecido"}, notas=["A extração descreveu o campo de forma incoerente (layout compacto); tipo CustomField a confirmar."], estado="desconhecido")
        campos.append(field("obj:FieldDefinition", n, t, p, None, d, S, T, **kw))
    obj("FieldDefinition", "Expõe a definição de campos de objetos para consulta.", "Metadados de campos; não é o único mapeamento de CustomField (ver Tooling CustomField).",
        [expo("tooling", "verificado", S, ["query()", "describeSObject()"], ["GET"], "32.0", restr=["FullName e Metadata só quando o resultado tem no máximo um registro."]),
         expo("padrao", "desconhecido", nota="Não declarado na página lida.")],
        campos, [{"api": "tooling", "soql": "SELECT QualifiedApiName, DataType, Label FROM FieldDefinition WHERE EntityDefinition.QualifiedApiName = 'Account'", "endpoint": "/services/data/v68.0/tooling/query?q=...", "contexto": "Tooling API; os exemplos oficiais filtram pelo objeto.", "validacao": "documental"}],
        APEX_TOOLING, cob("parcial", None, len(campos), cnt(campos), "Recorte de 12 dos 56 campos extraídos (página com 126k caracteres lida até 100k)."), S)

# ---------------- Relacionamentos ----------------
def rel(rid, tipo, o, d, expl, estado, srcs, card=None, nat=None, cond=None):
    r = {"id": "rel:" + rid, "tipo": tipo, "origem": o, "destino": d, "explicacao": expl, "estado": estado, "evidencias": [ev(s) for s in srcs]}
    if card: r["cardinalidade_registros"] = card
    if nat: r["natureza_correspondencia"] = nat
    if cond: r["condicao"] = cond
    save("relacionamentos", rid, r)

def build_rels():
    PSA = "src:objref-permissionsetassignment"
    N1 = lambda src, nota: af("verificado", "N:1", nota, [ev(src)])
    rel("psa-assignee-user", "referencia_campo", {"entidade": "obj:PermissionSetAssignment", "campo": "AssigneeId"}, {"entidade": "obj:User"},
        "A atribuição precisa dizer quem recebe o acesso; AssigneeId guarda o Id do usuário.", "verificado", [PSA],
        N1(PSA, "Cada atribuição referencia um usuário; um usuário pode ter várias atribuições (a página orienta consultar por usuário)."))
    rel("psa-permissionset", "referencia_campo", {"entidade": "obj:PermissionSetAssignment", "campo": "PermissionSetId"}, {"entidade": "obj:PermissionSet"},
        "Indica qual permission set foi concedido.", "verificado", [PSA], N1(PSA, "Campo anulável: nem toda atribuição precisa preenchê-lo."), cond="Preenchido quando a atribuição é de um permission set.")
    rel("psa-permissionsetgroup", "referencia_campo", {"entidade": "obj:PermissionSetAssignment", "campo": "PermissionSetGroupId"}, {"entidade": "obj:PermissionSetGroup"},
        "Quando a atribuição é de um grupo, indica qual grupo.", "verificado", [PSA], N1(PSA, "Campo anulável."), cond="Preenchido quando a atribuição é de um grupo de permission sets.")
    rel("user-profile", "referencia_campo", {"entidade": "obj:User", "campo": "ProfileId"}, {"entidade": "obj:Profile"},
        "Todo usuário tem um perfil, gravado no próprio User (ProfileId). Não passa por PermissionSetAssignment.", "verificado", ["src:objref-user"],
        af("desconhecido", "N:1", "Estrutura de lookup indica N:1; obrigatoriedade do campo não extraída com segurança."))
    rel("user-manager", "referencia_campo", {"entidade": "obj:User", "campo": "ManagerId"}, {"entidade": "obj:User"},
        "O gestor de um usuário também é um usuário (auto-relacionamento).", "verificado", ["src:objref-user"], af("desconhecido", "N:1"))
    rel("permissionset-profile", "referencia_campo", {"entidade": "obj:PermissionSet", "campo": "ProfileId"}, {"entidade": "obj:Profile"},
        "Permission sets internos de perfil apontam para o perfil dono (IsOwnedByProfile = true).", "verificado", ["src:objref-permissionset"], af("desconhecido", None, "Relação 1:1 entre perfil e seu permission set interno não comprovada nesta sessão."))
    rel("permissionset-permissionsetgroup", "referencia_campo", {"entidade": "obj:PermissionSet", "campo": "PermissionSetGroupId"}, {"entidade": "obj:PermissionSetGroup"},
        "Registro de permission set pertencente a um grupo (dono), quando houver.", "verificado", ["src:objref-permissionset"], af("desconhecido"))
    rel("userlogin-user", "referencia_campo", {"entidade": "obj:UserLogin", "campo": "UserId"}, {"entidade": "obj:User"}, "O estado de login pertence a um usuário.", "verificado", ["src:objref-userlogin"], af("desconhecido"))
    rel("loginhistory-user", "referencia_campo", {"entidade": "obj:LoginHistory", "campo": "UserId"}, {"entidade": "obj:User"}, "Cada tentativa de login é de um usuário.", "verificado", ["src:objref-loginhistory"], af("desconhecido", "N:1"))
    rel("validationrule-entitydefinition", "referencia_campo", {"entidade": "obj:ValidationRule", "campo": "EntityDefinitionId"}, {"entidade": "obj:EntityDefinition"},
        "Cada regra pertence a um objeto, identificado em EntityDefinition.", "verificado", ["src:tooling-validationrule"], af("desconhecido"))
    rel("fielddefinition-entitydefinition", "referencia_campo", {"entidade": "obj:FieldDefinition", "campo": "EntityDefinitionId"}, {"entidade": "obj:EntityDefinition"},
        "Cada campo pertence a um objeto.", "verificado", ["src:tooling-fielddefinition"], af("desconhecido"))
    # Correspondências XML <-> API
    rel("cor-validationrule-tooling", "correspondencia_xml_api", {"entidade": "mdt:ValidationRule"}, {"entidade": "obj:ValidationRule", "campo": "Metadata"},
        "O campo Metadata do objeto Tooling ValidationRule traz o conteúdo no formato do tipo ValidationRule; os demais campos do objeto têm nomes próprios (ex.: ValidationName).", "verificado", ["src:tooling-validationrule"], nat="transformada")
    rel("cor-customfield-tooling", "correspondencia_xml_api", {"entidade": "mdt:CustomField"}, {"entidade": "obj:CustomField", "campo": "Metadata"},
        "O campo Metadata do objeto Tooling CustomField traz propriedades do tipo CustomField.", "verificado", ["src:tooling-customfield"], nat="transformada")
    rel("cor-customobject-entitydefinition", "correspondencia_xml_api", {"entidade": "mdt:CustomObject"}, {"entidade": "obj:EntityDefinition", "campo": "Metadata"},
        "EntityDefinition.Metadata é tipado como CustomObject e cobre objetos padrão e customizados.", "verificado", ["src:tooling-entitydefinition"], nat="transformada")
    rel("cor-customfield-fielddefinition", "correspondencia_xml_api", {"entidade": "mdt:CustomField"}, {"entidade": "obj:FieldDefinition", "campo": "Metadata"},
        "FieldDefinition.Metadata parece trazer o tipo CustomField, mas a descrição extraída é incoerente.", "desconhecido", ["src:tooling-fielddefinition"], nat="desconhecida")
    rel("cor-customobject-tooling", "correspondencia_xml_api", {"entidade": "mdt:CustomObject"}, {"entidade": "obj:CustomObject"},
        "O objeto Tooling CustomObject representa objetos customizados; a presença de um campo Metadata não foi confirmada na extração.", "desconhecido", ["src:tooling-customobject"], nat="desconhecida")
    rel("cor-permissionset-label", "correspondencia_xml_api", {"entidade": "mdt:PermissionSet", "campo": "label"}, {"entidade": "obj:PermissionSet", "campo": "Label"},
        "Candidata: ambos descrevem o rótulo do permission set com limite de 80 caracteres. Semelhança de nome e descrição não comprova equivalência.", "desconhecido",
        ["src:mdapi-permissionset", "src:objref-permissionset"], nat="desconhecida")
    for a, b, srcs, t in [("permissionset", "PermissionSet", ["src:mdapi-permissionset", "src:objref-permissionset"], "permission sets"),
                          ("profile", "Profile", ["src:mdapi-profile", "src:objref-profile"], "perfis"),
                          ("permissionsetgroup", "PermissionSetGroup", ["src:mdapi-permissionsetgroup", "src:objref-permissionsetgroup"], "grupos de permission sets"),
                          ("recordtype", "RecordType", ["src:mdapi-recordtype", "src:objref-recordtype"], "tipos de registro")]:
        rel(f"rep-{a}", "representacao_comum", {"entidade": f"mdt:{b}"}, {"entidade": f"obj:{b}"},
            f"Metadata type e objeto API descrevem {t} por caminhos diferentes: definição implantável versus registro consultável. A correspondência campo a campo não foi comprovada.", "verificado", srcs)

# ---------------- Funcionalidades ----------------
def func(fid, nome, tec, aliases, oq, fin, ex, principal, secundarias, mdts, objs, ausencias, setup, recs=None, alertas=None, limit=None, srcs=(), estado="verificado", pre=None):
    cp, sp = principal
    f = {"id": "func:" + fid, "nome": nome, "nome_tecnico": tec, "aliases": aliases, "termos_busca": sorted(set([nome.lower(), tec.lower()] + [a.lower() for a in aliases])),
         "o_que_e": oq, "finalidade": fin, "exemplo": ex,
         "classificacao_principal": {"classificacao": "cls:" + cp, "subclassificacao": "sub:" + sp},
         "classificacoes_secundarias": [{"classificacao": "cls:" + c, "subclassificacao": "sub:" + s, "motivo": m} for c, s, m in secundarias],
         "representacoes": {"metadata_types": [{"ref": "mdt:" + r, "papel": p} for r, p in mdts], "objetos_api": [{"ref": "obj:" + r, "papel": p} for r, p in objs], "ausencias": ausencias},
         "setup": setup, "recomendacoes": recs or [], "alertas": alertas or [], "limitacoes": limit or [], "estado": estado, "evidencias": [ev(s) for s in srcs]}
    if pre: f["pre_requisitos"] = pre
    SUB_FUNCS.setdefault("sub:" + sp, []).append(f["id"])
    for c, s, m in secundarias: SUB_FUNCS.setdefault("sub:" + s, []).append(f["id"])
    save("funcionalidades", fid, f)

NAO_INV = lambda tipo: {"tipo": tipo, "estado": "desconhecido", "motivo": "Não investigado nesta sessão; a lista vazia não comprova inexistência."}
SETUP_PEND = lambda v: af("desconhecido", v, "Caminho proposto, ainda não validado na interface (pt-BR).")

def build_funcs():
    A, D, Q, AU, UI, O, DV = ("acesso-identidade-e-seguranca", "dados-e-modelagem", "qualidade-governanca-e-ciclo-de-vida-dos-dados", "automacao-de-processos-e-regras-de-negocio",
                              "interface-e-experiencia-do-usuario", "observabilidade-auditoria-e-operacao", "desenvolvimento-testes-e-entrega")
    func("usuarios", "Usuários", "Users", ["user", "usuário", "provisionamento"],
         "Cada pessoa ou integração que acessa a org é um usuário, registrado no objeto User.", "Criar, desativar e ajustar quem acessa a org, com qual perfil, idioma e fuso.",
         "Uma nova analista entra na empresa: o administrador cria o usuário com o perfil adequado e depois atribui permission sets extras.",
         (A, "usuarios-e-provisionamento"), [], [], [("User", "Registro de cada usuário.")],
         [{"tipo": "metadata_type", "estado": "verificado", "motivo": "User não está entre os 993 metadata types da v68; usuários são registros do objeto User, não componentes implantáveis.", "evidencias": [ev("src:sdr-metadata-support"), ev("src:objref-user")]}],
         SETUP_PEND("Setup > Usuários > Usuários"),
         recs=[{"texto": "Manter perfis enxutos e conceder acessos adicionais por permission sets.", "natureza": "preferencia_projeto"}],
         alertas=["Usuários não são excluídos pela API (delete() não é suportado em User); desativa-se pelo campo IsActive."], srcs=["src:objref-user"])
    func("perfis", "Perfis", "Profiles", ["profile", "perfil"], "Conjunto base de permissões e configurações atribuído a cada usuário.",
         "Definir o acesso mínimo de um grupo de usuários e configurações que só existem no perfil, como horários e faixas de IP de login.",
         "Todo usuário tem exatamente um perfil, como 'Vendedor padrão'.", (A, "permissoes-perfis-e-grupos"),
         [(A, "sessoes-e-politicas-de-login", "O XML de perfil define loginHours e loginIpRanges.")],
         [("Profile", "Definição implantável do perfil.")], [("Profile", "Registro consultável do perfil.")], [], SETUP_PEND("Setup > Usuários > Perfis"),
         srcs=["src:mdapi-profile", "src:objref-profile"])
    func("permission-sets", "Permission sets", "Permission Sets", ["conjunto de permissões", "permissionset"], "Pacote de permissões que se soma ao perfil de um usuário.",
         "Conceder acesso extra sem criar um perfil novo para cada combinação.", "O permission set 'Gestão de Contratos' dá leitura e edição de contratos só para quem precisa.",
         (A, "permissoes-perfis-e-grupos"), [],
         [("PermissionSet", "Definição implantável das permissões.")], [("PermissionSet", "Registro consultável do permission set."), ("PermissionSetAssignment", "Atribuição a usuários (objeto de junção).")], [],
         SETUP_PEND("Setup > Usuários > Permission Sets"),
         recs=[{"texto": "Nomear pela capacidade concedida, não pela pessoa.", "natureza": "preferencia_projeto"}],
         alertas=["A atribuição a usuários é um registro de PermissionSetAssignment, não parte do XML."], srcs=["src:mdapi-permissionset", "src:objref-permissionset", "src:objref-permissionsetassignment"])
    func("permission-set-groups", "Grupos de permission sets", "Permission Set Groups", ["psg", "permission set group"], "Agrupa vários permission sets para atribuí-los de uma vez.",
         "Modelar perfis de trabalho combinando permission sets, com opção de silenciar permissões.", "O grupo 'Analista de Crédito' reúne três permission sets e é atribuído em um passo.",
         (A, "permissoes-perfis-e-grupos"), [],
         [("PermissionSetGroup", "Definição implantável do grupo.")], [("PermissionSetGroup", "Registro consultável do grupo."), ("PermissionSetAssignment", "Atribuição do grupo a usuários (mesmo objeto de junção dos permission sets).")], [],
         SETUP_PEND("Setup > Usuários > Permission Set Groups"), srcs=["src:mdapi-permissionsetgroup", "src:objref-permissionsetgroup", "src:objref-permissionsetassignment"])
    func("estado-e-historico-de-login", "Estado e histórico de login", "User login state and history", ["login history", "histórico de login", "iplogin", "ip de login", "usuário congelado"],
         "Mostra o estado atual de login de cada usuário (congelado, bloqueado) e o histórico de tentativas.", "Investigar acessos, bloqueios e a origem das tentativas de login.",
         "Verificar de qual IP veio uma tentativa de login que falhou ontem.", (A, "sessoes-e-politicas-de-login"),
         [(O, "historico-de-login", "O histórico de tentativas é usado em auditoria e operação.")], [],
         [("UserLogin", "Estado atual de login."), ("LoginHistory", "Histórico de tentativas.")],
         [{"tipo": "metadata_type", "estado": "verificado", "motivo": "UserLogin e LoginHistory não estão entre os metadata types da v68; são objetos de dados.", "evidencias": [ev("src:sdr-metadata-support")]}],
         SETUP_PEND("Setup > Usuários > Histórico de login"),
         alertas=["Não existe um item 'IpLogin': restrições de IP por perfil estão em Profile.loginIpRanges; o IP de cada tentativa está em LoginHistory.SourceIp."],
         srcs=["src:objref-userlogin", "src:objref-loginhistory"])
    func("objetos-customizados", "Objetos customizados", "Custom Objects", ["objeto", "custom object", "entidade"], "Estruturas criadas para guardar dados próprios do negócio.",
         "Modelar entidades que não existem entre os objetos padrão.", "Um objeto Contrato_Servico__c para contratos de manutenção.", (D, "objetos-e-entidades"), [],
         [("CustomObject", "Definição implantável do objeto e de seus filhos.")], [("EntityDefinition", "Definição consultável de objetos padrão e customizados."), ("CustomObject", "Objeto Tooling com dados de objetos customizados.")], [],
         SETUP_PEND("Setup > Gerenciador de objetos"), srcs=["src:mdapi-customobject", "src:tooling-entitydefinition", "src:tooling-customobject"])
    func("campos-customizados", "Campos customizados", "Custom Fields", ["campo", "custom field"], "Colunas adicionais em objetos padrão ou customizados.",
         "Guardar informações específicas com tipo, tamanho e regras próprios.", "Um campo Valor_Mensal__c do tipo moeda em Contrato_Servico__c.", (D, "campos-e-tipos"),
         [(D, "relacionamentos-e-juncoes", "Campos de lookup e master-detail criam relacionamentos e objetos de junção.")],
         [("CustomField", "Definição implantável do campo.")], [("FieldDefinition", "Definição consultável de campos."), ("CustomField", "Objeto Tooling com dados de campos customizados.")], [],
         SETUP_PEND("Setup > Gerenciador de objetos > [objeto] > Campos e relacionamentos"), srcs=["src:mdapi-customfield", "src:tooling-customfield", "src:tooling-fielddefinition"])
    func("tipos-de-registro", "Tipos de registro", "Record Types", ["record type", "tipo de registro"], "Variações de um mesmo objeto com valores de picklist, processos e páginas diferentes.",
         "Separar processos dentro do mesmo objeto.", "Contratos 'Manutenção' e 'Licenciamento' com listas de status diferentes.", (D, "tipos-de-registro-e-processos-de-negocio"),
         [(UI, "layouts-e-paginas-de-registro", "Tipos de registro determinam quais valores e layouts o usuário vê."), (D, "listas-de-valores", "O XML define os valores de picklist por tipo (picklistValues).")],
         [("RecordType", "Definição implantável do tipo de registro.")], [("RecordType", "Registro consultável do tipo de registro.")], [], SETUP_PEND("Setup > Gerenciador de objetos > [objeto] > Tipos de registro"),
         srcs=["src:mdapi-recordtype", "src:objref-recordtype"])
    func("regras-de-validacao", "Regras de validação", "Validation Rules", ["validation rule", "validação"], "Fórmulas que impedem salvar um registro quando uma condição de erro é verdadeira.",
         "Garantir a qualidade dos dados no momento da gravação.", "Impedir salvar um contrato com valor negativo.", (Q, "validacao"),
         [(AU, "acoes-e-regras", "Expressa uma regra de negócio aplicada automaticamente na gravação."), (D, "campos-e-tipos", "A regra é definida no objeto e avalia seus campos.")],
         [("ValidationRule", "Definição implantável da regra (filha de CustomObject).")], [("ValidationRule", "Objeto Tooling com a regra e seu conteúdo em Metadata.")], [],
         SETUP_PEND("Setup > Gerenciador de objetos > [objeto] > Regras de validação"), srcs=["src:mdapi-validationrule", "src:tooling-validationrule"])
    func("flow", "Flow", "Flow", ["fluxo", "flow builder", "automação declarativa"], "Automação declarativa construída no Flow Builder, com elementos, variáveis e decisões.",
         "Automatizar processos sem código, disparados por tela, registro, agendamento ou outros gatilhos.", "Atualizar o status do contrato quando a assinatura é registrada.",
         (AU, "flow-e-orquestracao"), [(DV, "versionamento-deploy-e-recuperacao", "Cada flow tem versões com status (Active, Draft, Obsolete...).")],
         [("Flow", "Definição implantável de uma versão de flow.")], [], [NAO_INV("objeto_api")], SETUP_PEND("Setup > Flows"), srcs=["src:mdapi-flow"])
    func("path", "Path", "Path (PathAssistant)", ["caminho", "pathassistant", "etapas"], "Barra visual de etapas baseada em um campo picklist, com campos e orientação por etapa.",
         "Orientar o usuário pelas etapas de um processo.", "Etapas de um contrato: Rascunho, Em análise, Assinado.", (UI, "orientacao-visual-e-path"),
         [(D, "listas-de-valores", "As etapas vêm dos valores de uma picklist (fieldName).")],
         [("PathAssistant", "Definição implantável do Path.")], [], [NAO_INV("objeto_api")], SETUP_PEND("Setup > Path Settings"), srcs=["src:mdapi-pathassistant"])
    func("lightning-pages", "Lightning pages", "Lightning Pages", ["flexipage", "página lightning", "app builder"], "Páginas montadas com componentes no Lightning App Builder.",
         "Organizar o que aparece em páginas de registro, de app e inicial.", "Uma página de registro de Contrato com abas e um componente de histórico.", (UI, "lightning-pages-e-componentes"),
         [(UI, "layouts-e-paginas-de-registro", "Páginas do tipo RecordPage definem a página de um registro.")],
         [("FlexiPage", "Definição implantável da página.")], [], [NAO_INV("objeto_api")], SETUP_PEND("Setup > Lightning App Builder"), srcs=["src:mdapi-flexipage"])
    func("acoes-rapidas", "Ações rápidas", "Quick Actions", ["quick action", "ação"], "Botões que abrem um formulário curto ou executam uma ação em contexto.",
         "Agilizar tarefas frequentes a partir de um registro ou da navegação global.", "'Registrar renovação' a partir de um contrato, abrindo um flow.", (UI, "acoes-rapidas"),
         [(AU, "acoes-e-regras", "Uma ação do tipo Flow invoca um flow (flowDefinition).")],
         [("QuickAction", "Definição implantável da ação.")], [], [NAO_INV("objeto_api")], SETUP_PEND("Setup > Gerenciador de objetos > [objeto] > Botões, links e ações"), srcs=["src:mdapi-quickaction"])
    func("tabs", "Tabs", "Custom Tabs", ["guia", "aba", "tab"], "Entradas de navegação para objetos, páginas, componentes ou URLs.",
         "Dar acesso a um objeto ou página pela navegação do app.", "A tab 'Contratos de Serviço' no app de Operações.", (UI, "tabs"),
         [(UI, "aplicativos-e-navegacao", "Tabs compõem a navegação dos apps.")],
         [("CustomTab", "Definição implantável da tab.")], [], [NAO_INV("objeto_api")], SETUP_PEND("Setup > Tabs"), srcs=["src:mdapi-customtab"])

def build_clouds():
    core_tree = {}
    import json, glob, os
    for p in sorted(glob.glob("/home/claude/sf-tutor/ai-help/claude/insumos-grafo/catalogo/funcionalidades/*.json")):
        f = json.load(open(p))
        c, s = f["classificacao_principal"]["classificacao"], f["classificacao_principal"]["subclassificacao"]
        core_tree.setdefault(c, {}).setdefault(s, []).append(f["id"])
    order = ["cls:" + c[0] for c in CLS]
    ca = [{"classificacao": c, "subclassificacoes": [{"subclassificacao": s, "funcionalidades": sorted(v)} for s, v in sorted(core_tree[c].items())]} for c in order if c in core_tree]
    save("nuvens", "platform-core", {
        "id": "nuv:platform-core", "nome_oficial": "Salesforce Platform", "aliases": ["Core", "Platform/Core (recorte do projeto)"], "sigla": "CORE",
        "resumo": "Camada compartilhada da org onde vivem modelagem de dados, segurança, automação, interface e desenvolvimento usados por várias nuvens.",
        "o_que_e": "No sf-tutor, Platform/Core é o recorte do primeiro inventário completo (ver config/escopo.json). Não é tratado como 'mãe' de todos os produtos.",
        "casos_de_uso": ["Modelar dados próprios do negócio.", "Controlar acesso de usuários.", "Automatizar processos declarativamente."],
        "contexto_tecnico": af("verificado", "Mesma org e mesmas APIs (Metadata API, API padrão, Tooling API) documentadas para os itens do piloto.", None, [ev("src:mdapi-intro"), ev("src:tooling-validationrule")]),
        "licencas": {"estado": "desconhecido", "nota": "Licenças e edições ainda não registradas. Diferenciar licença de usuário, licença de permission set, edição e add-on; a presença de um metadata type não indica licença."},
        "classificacoes_aplicaveis": ca, "dependencias": [], "limites": ["Nome comercial 'Salesforce Platform' não verificado em fonte nesta sessão."],
        "cobertura_inventario": "parcial", "estado": "desconhecido", "evidencias": [ev("src:mdapi-intro")]})
    for nid, nome, sig, res in [("sales-cloud", "Sales Cloud", "SALES", "Produto voltado a vendas. Usa capacidades da plataforma e tem capacidades próprias."),
                                ("service-cloud", "Service Cloud", "SERVICE", "Produto voltado a atendimento. Usa capacidades da plataforma e tem capacidades próprias.")]:
        save("nuvens", nid, {"id": "nuv:" + nid, "nome_oficial": nome, "aliases": [], "sigla": sig, "resumo": res,
             "contexto_tecnico": af("desconhecido", None, "Execução na mesma org da plataforma não verificada com fonte nesta sessão."),
             "licencas": {"estado": "desconhecido", "nota": "Não registradas."}, "classificacoes_aplicaveis": [],
             "limites": ["Funcionalidades compartilhadas e próprias ainda não associadas com evidência; a lista vazia não comprova ausência."],
             "cobertura_inventario": "nao_iniciada", "estado": "desconhecido", "evidencias": []})
    save("nuvens", "data-360", {"id": "nuv:data-360", "nome_oficial": "Data 360", "aliases": ["Data Cloud"], "sigla": "D360",
         "resumo": "Plataforma de dados da Salesforce, antes chamada Data Cloud. Entrada solicitada para o mapa.",
         "contexto_tecnico": af("bloqueado", None, "Org, runtime e APIs próprios ainda não investigados; não presumir que usa o mesmo contexto do Core. A página de CustomObject cita atributos de DMO/DLO (Data 360), o que indica tipos de metadados relacionados, mas não define o contexto completo."),
         "licencas": {"estado": "desconhecido", "nota": "A página de CustomObject menciona exigência de licença Data Cloud para atributos de data lake; demais licenças não registradas."},
         "classificacoes_aplicaveis": [], "limites": ["Sem inventário próprio; não declarar completo."], "cobertura_inventario": "nao_iniciada", "estado": "verificado",
         "evidencias": [ev("src:data360-nome", "Nome oficial atual e nome anterior (Data Cloud)."), ev("src:mdapi-customobject", "Subtipos MktDataModelAttributes/MktDataLakeAttributes.")]})

def build_root():
    save(None, "salesforce", {
        "id": "salesforce", "nome": "Salesforce",
        "nota_logo": "Posição do logotipo oficial; o asset, sua origem e os termos de uso precisam ser registrados antes do uso, com aviso de que o projeto não é afiliado à Salesforce.",
        "o_que_e": "Ecossistema de produtos e plataforma da Salesforce. Este mapa organiza o conteúdo por funcionalidades e, a partir delas, chega aos metadata types (XML), aos objetos consultáveis via API e a cada propriedade e campo.",
        "conceitos": [
            {"termo": "Org", "definicao": "Uma instância da Salesforce com seus dados, configurações e usuários."},
            {"termo": "Produto/nuvem", "definicao": "Oferta comercial, como Sales Cloud. Nem todo produto roda na mesma org nem usa as mesmas APIs."},
            {"termo": "Plataforma", "definicao": "Camada compartilhada (Platform/Core) usada por várias nuvens na mesma org."},
            {"termo": "Funcionalidade", "definicao": "Capacidade que alguém usa ou configura. É a unidade didática deste mapa e pode ter zero, um ou vários metadata types e objetos API."},
            {"termo": "Metadado", "definicao": "Configuração ou estrutura, como a definição de um permission set. Quando há metadata type, pode ser implantada pela Metadata API.",
             "analogia": "Metadado é a planta da casa; registro é quem mora nela.", "limite_analogia": "Algumas configurações vivem como registros, como usuários e atribuições de permissão."},
            {"termo": "Registro", "definicao": "Um dado guardado em um objeto, como um usuário específico."},
            {"termo": "API", "definicao": "Interface programática. API padrão, Tooling API e Metadata API expõem coisas diferentes; não são equivalentes."},
            {"termo": "Objeto consultável via API", "definicao": "Objeto exposto publicamente por uma API. O catálogo não documenta tabelas físicas internas da Salesforce."}],
        "organizacao_do_mapa": "Duas visões sobre o mesmo catálogo: por classificação funcional (inicial) e por nuvem/produto. Cada funcionalidade tem um único cadastro, mesmo aparecendo em vários caminhos.",
        "relacoes_entre_produtos": "Produtos como Marketing Cloud Engagement, B2C Commerce, MuleSoft, Tableau e Slack têm contextos técnicos próprios e ficam fora do recorte Core.",
        "como_navegar": ["Escolha uma classificação ou uma nuvem.", "Abra uma funcionalidade para ver suas representações técnicas.", "Abra um metadata type para ver propriedades XML, ou um objeto API para ver campos.",
                         "Relações técnicas ligam campos a objetos (referências) e metadata types a objetos (correspondências)."],
        "nuvens": ["nuv:platform-core", "nuv:sales-cloud", "nuv:service-cloud", "nuv:data-360"],
        "classificacoes": ["cls:" + c[0] for c in CLS],
        "versao_base": {"api_version": "68.0", "release": "Winter '27", "data_referencia": "2026-11-07", "escopo": "config/escopo.json"},
        "estado": "verificado", "evidencias": [ev("src:mdapi-intro"), ev("src:mdapi-components")]})
