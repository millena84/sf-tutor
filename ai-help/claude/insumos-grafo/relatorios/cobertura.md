# Relatório de cobertura

Base: API 68.0 (Winter '27), referência 2026-11-07.
Gerado por `ferramentas/sftutor.py cobertura`. Cobertura estrutural, explicativa e de relacionamentos são medidas separadas.

## Metadata types

- Universo v68 (METADATA_SUPPORT.md): **993** tipos.
- Classificados como incluídos no recorte Core: 12; pendentes de classificação: 981.
- Cadastrados: **15** de 993. Estruturalmente completos (contra a página oficial): 5. Completos nas três dimensões: 0.
- Porcentagem do recorte Core: não calculada, porque o denominador do recorte ainda não está definido (classificação item a item pendente).

| Tipo | Estrutural | Esperadas | Presentes | Explicadas | Estruturas | Mapeamento | Completo |
|---|---|---|---|---|---|---|---|
| mdt:CustomField | parcial | 60 | 60 | 60 | 2 | parcial | não |
| mdt:CustomObject | parcial | 55 | 55 | 55 | 0 | parcial | não |
| mdt:CustomTab | parcial | 17 | 17 | 17 | 0 | parcial | não |
| mdt:EntitlementProcess | parcial | 14 | 14 | 14 | 2 | parcial | não |
| mdt:FlexiPage | parcial | 12 | 12 | 12 | 0 | parcial | não |
| mdt:Flow | parcial | 50 | 50 | 13 | 0 | parcial | não |
| mdt:PathAssistant | completa | 7 | 7 | 7 | 1 | parcial | não |
| mdt:PermissionSet | completa | 24 | 24 | 24 | 18 | parcial | não |
| mdt:PermissionSetGroup | completa | 7 | 7 | 7 | 0 | parcial | não |
| mdt:Profile | parcial | 27 | 27 | 27 | 16 | parcial | não |
| mdt:QuickAction | parcial | 22 | 22 | 22 | 0 | parcial | não |
| mdt:RecordType | parcial | 7 | 7 | 7 | 1 | parcial | não |
| mdt:ServicePresenceStatus | completa | 3 | 3 | 3 | 1 | parcial | não |
| mdt:Territory2Model | parcial | 3 | 3 | 3 | 0 | parcial | não |
| mdt:ValidationRule | completa | 6 | 6 | 6 | 0 | parcial | não |

## Propriedades XML

- Em metadata types: 314 listadas, 277 explicadas.
- Em estruturas auxiliares: 130 listadas, 130 explicadas.
- Universo total: Sem WSDL não há denominador confiável do total de propriedades do recorte.

## Objetos consultáveis via API

- Catalogados: 29. Campos listados: 754; explicados: 332.
- Universo: Universo de objetos da plataforma não enumerado.

| Objeto | Estrutural | Esperados | Presentes | Explicados | APIs verificadas |
|---|---|---|---|---|---|
| obj:Account | parcial | n/d | 76 | 9 | padrao |
| obj:AccountTeamMember | completa | 11 | 11 | 11 | padrao |
| obj:BusinessHours | completa | 20 | 20 | 19 | padrao |
| obj:Case | parcial | n/d | 56 | 12 | padrao |
| obj:CaseMilestone | completa | 20 | 20 | 20 | padrao |
| obj:Contact | parcial | n/d | 37 | 3 | padrao |
| obj:CustomField | parcial | n/d | 6 | 6 | tooling |
| obj:CustomObject | parcial | n/d | 10 | 10 | tooling |
| obj:CustomTab | completa | 13 | 13 | 13 | tooling |
| obj:EntityDefinition | parcial | n/d | 13 | 6 | tooling |
| obj:FieldDefinition | parcial | n/d | 12 | 11 | tooling |
| obj:FlexiPage | completa | 11 | 11 | 11 | tooling |
| obj:Flow | completa | 15 | 15 | 15 | tooling |
| obj:FlowDefinition | completa | 11 | 11 | 11 | tooling |
| obj:Lead | parcial | n/d | 74 | 14 | padrao |
| obj:LeadStatus | completa | 5 | 5 | 5 | padrao |
| obj:LoginHistory | parcial | n/d | 24 | 24 | padrao |
| obj:Opportunity | parcial | n/d | 58 | 11 | padrao |
| obj:OpportunityTeamMember | completa | 8 | 8 | 8 | padrao |
| obj:PathAssistant | completa | 13 | 13 | 13 | tooling |
| obj:PermissionSet | parcial | n/d | 12 | 11 | padrao, tooling |
| obj:PermissionSetAssignment | parcial | n/d | 8 | 8 | padrao, tooling |
| obj:PermissionSetGroup | parcial | n/d | 7 | 7 | padrao, tooling |
| obj:Profile | parcial | n/d | 7 | 7 | padrao, tooling |
| obj:QuickActionDefinition | completa | 22 | 22 | 22 | tooling |
| obj:RecordType | parcial | n/d | 8 | 8 | padrao, tooling |
| obj:User | parcial | n/d | 183 | 23 | padrao, tooling |
| obj:UserLogin | parcial | n/d | 3 | 3 | padrao |
| obj:ValidationRule | completa | 11 | 11 | 11 | tooling |

## Relacionamentos

- Total: 51; verificados: 48.
- Por tipo: correspondencia_xml_api: 11, referencia_campo: 36, representacao_comum: 4

## Taxonomia e funcionalidades

- Classificações: 14; subclassificações: 92 (com funcionalidades: 24).
- Funcionalidades cadastradas: 31 (universo de funcionalidades não definido).
