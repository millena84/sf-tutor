"""Issue #34, item 3 (detalhamento dos temas principais): fontes novas e conteúdo que substitui o de temas internos
que estavam rasos (sem nível avançado ou sem fonte própria), um tema principal por vez.

Fontes lidas pelos resultados de busca restritos aos domínios oficiais; uma nota de extração por tema principal
(fontes/extracoes/temas-detalhe-<tema>.txt). Usado por conteudo_temas.py, aplicado por último (prevalece sobre
conteudo_sub.py).
"""
from carga.catalogo import fonte
from conteudo_cls import E, ini, enc, av

AJ = dict(tipo="oficial_ajuda", versao="sem versão (Ajuda Salesforce)", metodo="leitura_resultado_busca")
DOC = dict(versao="sem versão na página", metodo="leitura_resultado_busca")

FONTES_DETALHE = []
D = {}

# ====================================================================== Qualidade, governança e ciclo de vida dos dados
_EXT = "fontes/extracoes/temas-detalhe-qualidade.txt"
_DATA = "2026-11-14"


def _f(i, t, u, p, **k):
    FONTES_DETALHE.append(fonte(i, t, u, p, _EXT, _DATA, **k))


_H = "https://help.salesforce.com/s/articleView?id="
_f("src:help-duplicate-management-customize", "Customize Duplicate Management", _H + "sales.duplicate_prevention_map_of_tasks.htm&type=5",
   "Papel das matching rules e das duplicate rules; permissões e edições.", **AJ)
_f("src:help-duplicate-detection-process", "Duplicate Detection and Handling Process", _H + "sf.duplicate_detection_and_handling.htm&type=5",
   "Comparação entre objetos e match keys.", **AJ)
_f("src:help-duplicate-rules-things-to-know", "Things to Know About Duplicate Rules", _H + "sales.duplicate_rules_overview.htm&type=5",
   "Limites de regras ativas, duplicate record sets e global picklists.", **AJ)
_f("src:help-duplicate-rules-customize", "Customize Duplicate Rules", _H + "sales.duplicate_rules_create.htm&type=5",
   "Ações padrão, acesso necessário e ativação.", **AJ)
_f("src:help-duplicate-prevention", "Stop Users from Creating Duplicate Records", _H + "sf.duplicate_prevention.htm&type=5",
   "Regras padrão ativas, person accounts e alerta ou bloqueio.", **AJ)
_f("src:help-matching-rules", "Matching Rules", _H + "sales.matching_rule_map_of_reference.htm&type=5",
   "Matching rules padrão não editáveis.", **AJ)
_f("src:help-matching-rules-considerations", "Things to Know Before You Customize Matching Rules", _H + "sf.matching_rules_considerations.htm&type=5",
   "Limites de matching rules.", **AJ)
_f("src:help-duplicate-jobs-considerations", "Things to Know About Duplicate Jobs", _H + "sf.duplicate_jobs_considerations.htm&type=5",
   "Limites e sobrescrita de duplicate jobs.", **AJ)
_f("src:help-duplicate-rules-classic-view", "Show Duplicate Records in Salesforce Classic", _H + "sf.duplicate_rules_what_my_users_see_classic.htm&type=5",
   "O que o usuário vê; opção Bypass sharing rule.", **AJ)
_f("src:help-duplicate-web-to-lead", "Salesforce Duplicate Matching Rules Blocking Web-to-Lead Submissions (KB)", _H + "000336839&type=1",
   "Web-to-Lead sempre bloqueia o duplicado.", **AJ)
_f("src:help-matching-rule-ineffective", "Unable to Activate Matching Rule to Identify Duplicate Records in a Salesforce Organization (KB)",
   _H + "000383122&type=1", "Matching rule ineficaz não ativa (limiar de 2%).", **AJ)
_f("src:soap-findduplicates", "findDuplicates() (SOAP API Developer Guide)",
   "https://developer.salesforce.com/docs/platform/api/guide/sforce-api-calls-findduplicates.html", "Aplicar duplicate rules pela API; limite de 50 elementos.", **DOC)
_f("src:help-validation-rules", "Validation Rules", _H + "fields_about_field_validation.htm&type=5",
   "Como a validação atua ao salvar; aviso sobre Einstein Prediction Builder.", **AJ)
_f("src:help-validation-considerations", "Validation Rule Considerations", _H + "sf.fields_validation_considerations.htm&type=5",
   "Ordem de processamento das regras.", **AJ)
_f("src:help-validation-tips", "Tips for Writing Validation Rules", _H + "platform.fields_validation_rules_tips.htm&type=5",
   "Boas práticas ao escrever regras de validação.", **AJ)

D["sub:validacao"] = {
    "para_iniciantes": ini("Regras de validação são fórmulas que impedem salvar um registro quando uma condição de erro é verdadeira. Ao "
                           "salvar, todas as regras são verificadas; se alguma acusa erro, a mensagem aparece e nada é gravado.",
                           "Impedir salvar um contrato com valor negativo.",
                           E("src:mdapi-validationrule", "src:help-validation-rules"), comece=["func:regras-de-validacao"]),
    "encadeamento": enc("É a primeira barreira de qualidade: atua no momento de salvar e vem antes das regras de atribuição, de resposta "
                        "automática, de workflow e de escalonamento. Duplicados são tratados em 'Duplicidade e correspondência'.",
                        E("src:mdapi-validationrule", "src:help-validation-considerations")),
    "avancado": [
        av("decisao", "Validação, automação ou segurança",
           "A validação bloqueia a gravação; não esconde o campo nem corrige o valor. Para restringir quem edita, use a segurança de "
           "campo; para preencher ou corrigir valores, use automação.", E("src:mdapi-validationrule", "src:security-fls", "src:mdapi-flow")),
        av("implantacao", "Onde a validação entra na gravação",
           "A ordem de processamento é: validation rules, assignment rules, auto-response rules, workflow rules com ações imediatas e "
           "escalation rules. Quando uma regra de validação falha, as demais continuam sendo verificadas. Record-triggered flows também "
           "executam as regras de validação customizadas.",
           E("src:help-validation-considerations", "src:help-rtf-considerations")),
        av("atencao", "Regra que trava dado válido",
           "Regras conflitantes no mesmo campo impedem salvar o registro; por isso a orientação é testar antes de ativar e acompanhar pelo "
           "debug log. Vale considerar tudo o que pode fazer o registro falhar: assignment rules, field updates, segurança de campo e "
           "campos ocultos. Não se recomenda validar um campo numérico gerenciado pelo Einstein Prediction Builder.",
           E("src:help-validation-tips", "src:help-validation-rules")),
        av("decisao", "Fórmulas mais seguras",
           "Em Opportunity, a orientação é evitar os merge fields IsClosed e IsWon e usar ISPICKVAL sobre o Stage. RecordType.Id permite "
           "aplicar a regra só a um tipo de registro.", E("src:help-validation-tips")),
    ],
}
D["sub:duplicidade-e-correspondencia"] = {
    "para_iniciantes": ini("Duas regras trabalham juntas contra registros repetidos. A matching rule define como reconhecer um duplicado "
                           "(quais campos comparar e com que rigor). A duplicate rule define o que fazer quando ele aparece: avisar, "
                           "bloquear ou só registrar para relatório.",
                           "Ao cadastrar um lead com o mesmo e-mail de um contato existente, a vendedora vê o alerta com o possível "
                           "duplicado antes de salvar.",
                           E("src:help-duplicate-management-customize", "src:help-duplicate-detection-process")),
    "encadeamento": enc("Atua quando um registro é criado ou editado; a validação, em 'Validação', olha o valor de cada campo. Para limpar "
                        "duplicados que já existem, duplicate jobs usam as mesmas matching rules.",
                        E("src:help-duplicate-management-customize", "src:mdapi-validationrule")),
    "avancado": [
        av("decisao", "Avisar, bloquear ou reportar",
           "As duplicate rules padrão vêm ativas para business accounts, contatos e leads; para person accounts, é preciso ativá-las. A "
           "ação padrão na criação é permitir com alerta e reportar. Com a opção Report, o registro e seus duplicados entram num "
           "duplicate record set, até 100 duplicados por matching rule executada.",
           E("src:help-duplicate-prevention", "src:help-duplicate-rules-customize", "src:help-duplicate-rules-things-to-know")),
        av("limite", "Quantas regras",
           "Até cinco duplicate rules ativas por objeto, cada uma com até três matching rules. Matching rules: até cinco ativas por objeto, "
           "25 ativas no total e 100 no total, com um único campo de lookup por regra. As matching rules padrão não podem ser editadas. "
           "Valores de global picklist não são suportados em duplicate rules.",
           E("src:help-duplicate-rules-things-to-know", "src:help-matching-rules-considerations", "src:help-matching-rules")),
        av("seguranca", "O que o usuário enxerga",
           "Para ver os duplicados detectados, o usuário precisa de Read no objeto da regra, e a contagem mostra só os registros a que "
           "ele tem acesso. Com Bypass sharing rule, a comparação inclui todos os registros, e a mensagem só indica que há duplicados.",
           E("src:help-duplicate-rules-customize", "src:help-duplicate-rules-classic-view")),
        av("atencao", "Comportamentos que surpreendem",
           "Em Web-to-Lead, um envio que bate com o critério é sempre bloqueado, mesmo com a regra em permitir com alerta. Uma matching "
           "rule considerada ineficaz não pode ser ativada: o limiar padrão é de 2% de match keys repetidas.",
           E("src:help-duplicate-web-to-lead", "src:help-matching-rule-ineffective")),
        av("escala", "Limpeza em massa e API",
           "Duplicate jobs rodam também em objetos customizados, mas sem comparar e mesclar. Rodar de novo com o mesmo objeto e a mesma "
           "matching rule sobrescreve o resultado anterior, e 1.000.000 de duplicados acumulados bloqueia novos jobs. Pela SOAP API, "
           "findDuplicates() aplica as duplicate rules a até 50 registros por chamada.",
           E("src:help-duplicate-jobs-considerations", "src:soap-findduplicates")),
        av("implantacao", "Como metadado",
           "DuplicateRule e MatchingRules constam da lista oficial de metadata types da versão 68; as propriedades deles ainda não estão "
           "detalhadas neste catálogo.", E("src:sdr-metadata-support")),
    ],
}
D["sub:rastreabilidade-e-historico"] = {
    "para_iniciantes": ini("Guarda o histórico de alterações de campos: quem mudou, o que mudou e quando. O rastreamento é ligado campo a "
                           "campo e só registra a partir do momento em que é ligado.",
                           "Um auditor confere quem alterou o valor de um contrato no mês passado.",
                           E("src:security-guide", "src:help-field-history-tracking")),
    "encadeamento": enc("Cruza com Observabilidade: o Security Guide trata o histórico de campos junto com auditoria e monitoramento. "
                        "Por quanto tempo o histórico fica guardado é assunto de 'Retenção, arquivamento e exclusão'.",
                        E("src:security-guide", "src:help-field-history-tracking")),
    "avancado": [
        av("limite", "O que o histórico guarda",
           "Sem Field Audit Trail, o histórico fica até 18 meses (24 pela API), em até 20 campos por objeto. Ele mora num objeto "
           "relacionado (AccountHistory, MyCustomObject__History) e não conta no armazenamento. Campos de texto longo registram só que "
           "houve mudança, não os valores.", E("src:help-field-history-tracking", "src:help-field-audit-trail")),
        av("implantacao", "Como metadado",
           "O rastreamento é ligado no objeto (enableHistory no CustomObject) e em cada campo (trackHistory no CustomField).",
           E("src:mdapi-customobject", "src:mdapi-customfield")),
        av("decisao", "Quando o padrão não basta",
           "O Field Audit Trail amplia para até 200 campos por objeto e guarda o histórico até ser excluído, no big object "
           "FieldHistoryArchive, acessível só por API.", E("src:help-field-audit-trail")),
    ],
}
