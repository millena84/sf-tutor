"""Lote 7u (rodada D1, fechamento do MVP): nós de nuvem com lacunas apontadas na auditoria.

- Data 360: o_que_e vazio. O texto novo resume o contexto técnico já verificado no próprio nó.
- Platform/Core: licenças passam a ter fonte (licenças de usuário Salesforce Platform e Salesforce Platform Login)
  e o nó deixa o estado 'desconhecido'. O limite sobre o nome é reescrito: a Ajuda usa 'Salesforce Platform'
  como nome de licença; usar o nome para a camada compartilhada continua sendo escolha do projeto.

Ordem: lote7t_d1_descricoes.py, este script, conteudo_temas.py e temas_internos.py. Reexecutável.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga.base import ld, sv, ev           # noqa: E402
from carga import catalogo as C             # noqa: E402

DATA = "2026-11-17"
EXTR = "fontes/extracoes/lote7u-d1-nuvens.txt"
C.registrar_fontes([
    C.fonte("src:help-user-licenses-overview", "User Licenses (Salesforce Help)",
            "https://help.salesforce.com/s/articleView?language=en_US&id=platform.users_understanding_license_types.htm&type=5",
            "Licença Lightning Platform: apps e objetos customizados e recursos da plataforma, sem objetos de CRM como oportunidades e casos.",
            EXTR, DATA, tipo="oficial_ajuda", versao="sem versão (Ajuda Salesforce)", metodo="leitura_resultado_busca"),
])

d = ld("nuvens/data-360.json")
d["o_que_e"] = ("Plataforma de dados da Salesforce, antes chamada Data Cloud. Pode ser habilitada numa org existente ou numa org nova "
                "dedicada (home org), à qual outras orgs se ligam como companion orgs. Guarda os dados num lakehouse e os mapeia "
                "para o modelo de dados C360; tem API, armazenamento e empacotamento próprios. No sf-tutor ainda não tem inventário "
                "de funcionalidades.")
sv("nuvens/data-360.json", d)

p = ld("nuvens/platform-core.json")
p["licencas"] = {
    "estado": "verificado",
    "nota": ("A licença de usuário Salesforce Platform dá acesso a apps e objetos customizados e a recursos da plataforma, mas não aos "
             "objetos padrão de CRM (leads, oportunidades, campanhas, previsões, casos). Salesforce Platform Login oferece o mesmo acesso, "
             "cobrado por login. Usuários com a licença Salesforce (CRM completo) também usam a plataforma. Edições e add-ons não registrados."),
    "itens": [
        {"nome": "Salesforce Platform (licença de usuário)", "tipo": "licenca_usuario",
         "evidencias": [ev("src:help-user-licenses"), ev("src:help-user-licenses-overview")]},
        {"nome": "Salesforce Platform Login (licença de usuário)", "tipo": "licenca_usuario",
         "evidencias": [ev("src:help-user-licenses")]},
    ],
}
p["limites"] = [x for x in p["limites"] if not x.startswith("Nome comercial 'Salesforce Platform'")] + [
    "'Salesforce Platform' é o nome de uma licença de usuário na Ajuda; usá-lo para a camada compartilhada é escolha didática do projeto."]
p["estado"] = "verificado"
for s in ("src:help-user-licenses", "src:help-user-licenses-overview"):
    if not any(e["fonte"] == s for e in p["evidencias"]):
        p["evidencias"].append(ev(s))
sv("nuvens/platform-core.json", p)
print("lote 7u: Data 360 com o_que_e; Platform/Core com licenças e estado verificado")
