"""Exemplos XML escritos à mão (issue #20): AssignmentRules, EscalationRules e BusinessHoursSettings.
Usam só elementos catalogados. Rodar a partir de ai-help/claude/insumos-grafo/."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from carga.base import ld, sv

NOTA = ("Exemplo escrito pelo projeto apenas com elementos documentados. Textos entre colchetes indicam o que preencher; "
        "valores sem colchetes são ilustrativos e seguem a lista ou o formato documentado.")
NS = 'xmlns="http://soap.sforce.com/2006/04/metadata"'
FILTRO = """            <criteriaItems>
                <field>[campo avaliado]</field>
                <operation>[operador de comparação (FilterOperation)]</operation>
                <value>[valor comparado]</value>
            </criteriaItems>"""
EX = {
 "AssignmentRules": f"""<?xml version="1.0" encoding="UTF-8"?>
<AssignmentRules {NS}>
    <!-- Um arquivo por objeto (por exemplo, Case.assignmentRules); cada assignmentRule é uma regra -->
    <assignmentRule>
        <fullName>[nome da regra]</fullName>
        <active>true</active>
        <ruleEntry>
            <!-- Para quem vai o registro quando o critério bate -->
            <assignedTo>[nome do usuário ou da fila]</assignedTo>
            <assignedToType>Queue</assignedToType>
            <!-- Critério: use criteriaItems (com booleanFilter opcional) ou formula -->
{FILTRO}
        </ruleEntry>
    </assignmentRule>
</AssignmentRules>""",
 "EscalationRules": f"""<?xml version="1.0" encoding="UTF-8"?>
<EscalationRules {NS}>
    <escalationRule>
        <fullName>[nome da regra]</fullName>
        <active>true</active>
        <ruleEntry>
            <!-- Origem do horário comercial: None, Case ou Static (com Static, informe businessHours) -->
            <businessHoursSource>None</businessHoursSource>
{FILTRO}
            <!-- Início da contagem: CaseCreation ou CaseLastModified -->
            <escalationStartTime>CaseCreation</escalationStartTime>
            <escalationAction>
                <!-- Minutos até escalonar (valor ilustrativo) -->
                <minutesToEscalation>60</minutesToEscalation>
                <assignedTo>[nome do usuário ou da fila]</assignedTo>
                <assignedToType>Queue</assignedToType>
                <notifyCaseOwner>true</notifyCaseOwner>
            </escalationAction>
        </ruleEntry>
    </escalationRule>
</EscalationRules>""",
 "BusinessHoursSettings": f"""<?xml version="1.0" encoding="UTF-8"?>
<BusinessHoursSettings {NS}>
    <businessHours>
        <name>[nome único do horário]</name>
        <active>true</active>
        <default>false</default>
        <timeZoneId>[fuso horário]</timeZoneId>
        <!-- Horários no formato HH:mm:ss.SSSZ (valores ilustrativos); repita para os outros dias -->
        <mondayStartTime>08:00:00.000Z</mondayStartTime>
        <mondayEndTime>18:00:00.000Z</mondayEndTime>
    </businessHours>
</BusinessHoursSettings>""",
}
for nome, xml in EX.items():
    m = ld(f"metadata-types/{nome}.json")
    m["exemplo_xml"] = {"xml": xml, "natureza": "didatico_projeto", "nota": NOTA}
    sv(f"metadata-types/{nome}.json", m)
print("ok exemplos:", ", ".join(EX))
