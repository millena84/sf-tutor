"""Testes da base sf-tutor. Executar a partir de ai-help/claude/insumos-grafo/:
    python3 -m unittest discover -s testes -v
Os testes negativos copiam a base para uma pasta temporária e injetam defeitos; nada é alterado no catálogo real.
"""
import glob, json, os, shutil, sys, tempfile, unittest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "ferramentas"))
import sftutor as T  # noqa: E402


def ler(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def gravar(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


class BaseTemp(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        for d in ("catalogo", "schemas", "config", "fontes", "inventarios"):
            shutil.copytree(os.path.join(BASE, d), os.path.join(self.tmp, d))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def erros(self):
        return T.validar(self.tmp, checar_gerado=False).erros

    def cat(self, *p):
        return os.path.join(self.tmp, "catalogo", *p)

    def assertErro(self, trecho):
        e = self.erros()
        self.assertTrue(any(trecho in x for x in e), f"esperava erro contendo {trecho!r}; erros: {e[:8]}")


class TestCatalogoReal(unittest.TestCase):
    def test_valida_sem_erros(self):
        R = T.validar(BASE, checar_gerado=False)
        self.assertEqual(R.erros, [])

    def test_geracao_deterministica_e_atualizada(self):
        R = T.Erros()
        T.validar_gerado(R, BASE)
        self.assertEqual(R.erros, [])

    def test_user_nao_e_metadata_type(self):
        self.assertFalse(os.path.exists(os.path.join(BASE, "catalogo", "metadata-types", "User.json")))
        f = ler(os.path.join(BASE, "catalogo", "funcionalidades", "usuarios.json"))
        self.assertEqual(f["representacoes"]["metadata_types"], [])
        aus = [a for a in f["representacoes"]["ausencias"] if a["tipo"] == "metadata_type"]
        self.assertTrue(aus and aus[0]["evidencias"])

    def test_psa_e_user_profile(self):
        C = T.carregar(BASE)
        refs = {(r["origem"]["entidade"], r["origem"].get("campo"), r["destino"]["entidade"]) for r in C["relacionamentos"].values() if r["tipo"] == "referencia_campo"}
        for campo, alvo in (("AssigneeId", "obj:User"), ("PermissionSetId", "obj:PermissionSet"), ("PermissionSetGroupId", "obj:PermissionSetGroup")):
            self.assertIn(("obj:PermissionSetAssignment", campo, alvo), refs)
        self.assertIn(("obj:User", "ProfileId", "obj:Profile"), refs)
        self.assertTrue(C["objetos-api"]["obj:PermissionSetAssignment"]["juncao"])

    def test_funcionalidade_compartilhada_sem_duplicacao(self):
        C = T.carregar(BASE)
        usam = [f["id"] for f in C["funcionalidades"].values() if any(r["ref"] == "obj:PermissionSetAssignment" for r in f["representacoes"]["objetos_api"])]
        self.assertGreaterEqual(len(usam), 2)
        self.assertEqual(len(glob.glob(os.path.join(BASE, "catalogo", "objetos-api", "PermissionSetAssignment*.json"))), 1)
        # mesma funcionalidade em mais de uma subclassificação, um único arquivo
        f = C["funcionalidades"]["func:regras-de-validacao"]
        subs = [s["id"] for s in C["subclassificacoes"].values() if f["id"] in s["funcionalidades"]]
        self.assertGreaterEqual(len(subs), 2)

    def test_tooling_only_sem_apex_direto(self):
        C = T.carregar(BASE)
        vr = C["objetos-api"]["obj:ValidationRule"]
        self.assertEqual(vr["apex"]["consulta_soql_direta"]["estado"], "nao_exposto")

    def test_dominios_dinamicos(self):
        C = T.carregar(BASE)
        ps = C["objetos-api"]["obj:PermissionSet"]
        self.assertEqual(ps["dominio_dinamico_de_campos"]["padrao_nome"], "Permissions*")
        self.assertFalse(any(c["nome"].startswith("Permissions") for c in ps["campos"]))


class TestNegativos(BaseTemp):
    def test_user_como_metadata_type(self):
        d = ler(self.cat("metadata-types", "PermissionSet.json"))
        d["id"], d["nome"] = "mdt:User", "User"
        for p in d["propriedades"]:
            p["id"] = p["id"].replace("mdt:PermissionSet.", "mdt:User.")
        gravar(self.cat("metadata-types", "User.json"), d)
        self.assertErro("mdt:User: nome fora da lista oficial")

    def test_correspondencia_direta_sem_evidencia(self):
        p = self.cat("relacionamentos", "cor-permissionset-label.json")
        d = ler(p); d["natureza_correspondencia"] = "direta"; gravar(p, d)
        self.assertErro("correspondência direta sem evidência")

    def test_tag_xml_inventada(self):
        p = self.cat("metadata-types", "CustomObject.json")
        d = ler(p)
        d["exemplo_xml"]["xml"] = d["exemplo_xml"]["xml"].replace("<label>Contrato", "<fields><CustomField>x</CustomField></fields>\n    <label>Contrato")
        gravar(p, d)
        self.assertErro("<fields><CustomField>")

    def test_apex_direto_em_objeto_tooling(self):
        p = self.cat("objetos-api", "ValidationRule.json")
        d = ler(p)
        d["apex"]["consulta_soql_direta"] = {"estado": "verificado", "valor": True, "evidencias": [{"fonte": "src:tooling-validationrule"}]}
        gravar(p, d)
        self.assertErro("consulta Apex direta")

    def test_enum_completo_sem_valores(self):
        p = self.cat("metadata-types", "PermissionSetGroup.json")
        d = ler(p)
        for x in d["propriedades"]:
            if x["nome"] == "status":
                x["dominio"] = {"natureza": "enum_fechado", "lista_completa": "sim", "estado": "desconhecido"}
        gravar(p, d)
        self.assertErro("lista declarada completa sem valores")

    def test_obrigatoriedade_sem_evidencia(self):
        p = self.cat("objetos-api", "User.json")
        d = ler(p)
        for c in d["campos"]:
            if c["nome"] == "Email":
                c["obrigatoriedade"] = {"valor": "sim", "estado": "desconhecido"}
        gravar(p, d)
        self.assertErro("User.Email: obrigatoriedade 'sim' sem evidência")

    def test_default_inferido(self):
        p = self.cat("objetos-api", "UserLogin.json")
        d = ler(p)
        d["campos"][0]["default"] = {"forma": "false", "valor": False, "estado": "desconhecido"}
        gravar(p, d)
        self.assertErro("default 'false' sem evidência")

    def test_referencia_inexistente(self):
        p = self.cat("subclassificacoes", "validacao.json")
        d = ler(p); d["funcionalidades"].append("func:nao-existe"); gravar(p, d)
        self.assertErro("func:nao-existe inexistente")

    def test_id_duplicado(self):
        shutil.copy(self.cat("funcionalidades", "flow.json"), self.cat("funcionalidades", "flow-copia.json"))
        self.assertErro("id duplicado: func:flow")

    def test_soql_com_campo_invalido(self):
        p = self.cat("objetos-api", "UserLogin.json")
        d = ler(p); d["consultas"][0]["soql"] = "SELECT UserId, CampoInventado FROM UserLogin"; gravar(p, d)
        self.assertErro("'CampoInventado'")

    def test_campo_em_api_que_nao_expoe(self):
        p = self.cat("objetos-api", "ValidationRule.json")
        d = ler(p); d["campos"][0]["apis"] = ["padrao"]; gravar(p, d)
        self.assertErro("que não expõe o objeto")

    def test_nome_sem_rastro_na_extracao(self):
        p = self.cat("objetos-api", "UserLogin.json")
        d = ler(p); d["campos"][0]["nome"] = "CampoSemFonte"; d["campos"][0]["id"] = "obj:UserLogin.CampoSemFonte"; gravar(p, d)
        self.assertErro("CampoSemFonte: nome não encontrado nas notas de extração")

    def test_profile_via_psa_proibido(self):
        gravar(self.cat("relacionamentos", "psa-profile.json"), {
            "id": "rel:psa-profile", "tipo": "representacao_comum", "origem": {"entidade": "obj:PermissionSetAssignment"}, "destino": {"entidade": "obj:Profile"},
            "explicacao": "teste", "estado": "desconhecido", "evidencias": []})
        self.assertErro("Profile não deve ser ligado via PermissionSetAssignment")


    def test_schema_campo_obrigatorio_ausente(self):
        p = self.cat("funcionalidades", "path.json")
        d = ler(p); del d["exemplo"]; gravar(p, d)
        self.assertErro("schema[func:path]")

    def test_estado_invalido(self):
        p = self.cat("relacionamentos", "user-manager.json")
        d = ler(p); d["estado"] = "talvez"; gravar(p, d)
        self.assertErro("schema[rel:user-manager]")


class TestCiclos(BaseTemp):
    def test_expansao_de_estruturas_com_ciclo(self):
        a = ler(self.cat("estruturas", "PathAssistantStep.json"))
        a["propriedades"].append(dict(a["propriedades"][0], id="mdx:PathAssistantStep.filho", nome="filho", tipo_tecnico="PathAssistantStep", estrutura_ref="mdx:PathAssistantStep"))
        gravar(self.cat("estruturas", "PathAssistantStep.json"), a)
        C = T.carregar(self.tmp)
        prop = next(p for p in C["metadata-types"]["mdt:PathAssistant"]["propriedades"] if p["nome"] == "pathAssistantSteps")
        exp = T.expandir(C, prop, frozenset())
        filho = next(p for p in exp["estrutura_expandida"]["propriedades"] if p["nome"] == "filho")
        self.assertTrue(filho["estrutura_expandida"]["ciclo"])


class TestWsdl(unittest.TestCase):
    def test_heranca_e_ciclo(self):
        fx = os.path.join(BASE, "testes", "fixtures", "wsdl-sintetico.xml")
        tmp = tempfile.mkdtemp()
        try:
            r = T.importar_wsdl(fx, os.path.join(tmp, "out.json"))
            por = {t["nome"]: t for t in r["tipos"]}
            self.assertEqual(por["TipoA"]["categoria"], "metadata_type_candidato")
            self.assertEqual(por["EstruturaB"]["categoria"], "estrutura_auxiliar")
            self.assertIn("fullName", [e["nome"] for e in por["TipoA"]["elementos_herdados"]])
            self.assertTrue(por["CicloX"]["ciclo_heranca"])
            self.assertEqual(r["enumeracoes"][0]["valores"], ["Um", "Dois"])
        finally:
            shutil.rmtree(tmp)


class TestContratoSite(unittest.TestCase):
    """Contrato de gerado/site/ (issue #6): manifesto válido e arquivos coerentes com o catálogo."""
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        for d in ("catalogo", "schemas", "config", "fontes", "inventarios"):
            shutil.copytree(os.path.join(BASE, d), os.path.join(cls.tmp, d))
        cls.site = os.path.join(T.gerar(cls.tmp), "site")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def test_manifesto_valida_no_schema(self):
        import jsonschema
        schema = ler(os.path.join(BASE, "schemas", "site-manifest.schema.json"))
        jsonschema.validate(ler(os.path.join(self.site, "manifest.json")), schema)

    def test_arquivos_e_entidades(self):
        man = ler(os.path.join(self.site, "manifest.json"))
        for k in ("grafo_base", "visoes", "busca", "cobertura", "fontes"):
            self.assertTrue(os.path.exists(os.path.join(self.site, man["arquivos"][k])), k)
        base = ler(os.path.join(self.site, "grafo-base.json"))
        ids = {n["id"] for n in base["nos"]}
        self.assertFalse(any(n["tipo"] in ("campo_api", "propriedade_xml") for n in base["nos"]))
        for i in ids:
            self.assertTrue(os.path.exists(os.path.join(self.site, T.caminho_entidade(i))), i)
        busca = ler(os.path.join(self.site, "busca.json"))
        self.assertEqual(len(busca), sum(man["contagens"]["nos_por_tipo"].values()))
        for b in busca:
            if b["tipo"] in ("campo_api", "propriedade_xml"):
                self.assertIn(b.get("pai"), ids, b["id"])

    def test_estruturas_aninhadas_alcancaveis(self):
        base = ler(os.path.join(self.site, "grafo-base.json"))
        alvos = {a["destino"] for a in base["arestas"] if a["tipo"] == "tipo_composto"}
        for n in base["nos"]:
            if n["tipo"] == "estrutura_auxiliar":
                self.assertIn(n["id"], alvos, n["id"])


if __name__ == "__main__":
    unittest.main()


class TestMarcas(BaseTemp):
    """config/marcas.json: logos exibidos por referência ao endereço oficial."""
    def marcas(self):
        return os.path.join(self.tmp, "config", "marcas.json")

    def test_dominio_nao_permitido(self):
        d = ler(self.marcas()); d["itens"][0]["url"] = "https://exemplo.invalid/logo.svg"; gravar(self.marcas(), d)
        self.assertErro("marcas: domínio não permitido")

    def test_alvo_inexistente(self):
        d = ler(self.marcas()); d["itens"][1]["alvo"] = "nuv:nao-existe"; gravar(self.marcas(), d)
        self.assertErro("marcas: alvo nuv:nao-existe não existe")

    def test_dois_logos_no_mesmo_alvo(self):
        d = ler(self.marcas()); d["itens"][1]["alvo"] = "salesforce"; gravar(self.marcas(), d)
        self.assertErro("marcas: mais de um logo para salesforce")

    def test_projecao_leva_logo_ao_centro_e_nuvens(self):
        site = os.path.join(T.gerar(self.tmp), "site")
        g = ler(os.path.join(site, "grafo-base.json"))
        com_logo = {n["id"] for n in g["nos"] if "logo" in n}
        self.assertIn("salesforce", com_logo)
        self.assertTrue(all(i == "salesforce" or i.startswith("nuv:") for i in com_logo))
        self.assertEqual(ler(os.path.join(site, "entidades", "salesforce.json"))["logo_marca"]["formato"], "svg")


class TestConvencaoCorrespondencia(unittest.TestCase):
    """Correspondência XML↔API 'direta' ou 'transformada' exige evidência de campo (ex.: o campo Metadata tipado);
    'mesma coisa por caminhos diferentes' sem prova campo a campo é representacao_comum."""

    def test_correspondencia_forte_aponta_campo(self):
        for p in glob.glob(os.path.join(BASE, "catalogo", "relacionamentos", "*.json")):
            r = ler(p)
            if r["tipo"] == "correspondencia_xml_api" and r.get("natureza_correspondencia") in ("direta", "transformada"):
                self.assertTrue(r["destino"].get("campo") or r["origem"].get("campo"), f"{r['id']} sem campo comprovado")
