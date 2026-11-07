# Relatório de cobertura

Base: API 68.0 (Winter '27), referência 2026-11-07.
Gerado por `ferramentas/sftutor.py cobertura`. Cobertura estrutural, explicativa e de relacionamentos são medidas separadas.

## Metadata types

- Universo v68 (METADATA_SUPPORT.md): **993** tipos.
- Classificados como incluídos no recorte Core: 12; pendentes de classificação: 981.
- Cadastrados: **12** de 993. Estruturalmente completos (contra a página oficial): 4. Completos nas três dimensões: 0.
- Porcentagem do recorte Core: não calculada, porque o denominador do recorte ainda não está definido (classificação item a item pendente).

| Tipo | Estrutural | Esperadas | Presentes | Explicadas | Estruturas | Mapeamento | Completo |
|---|---|---|---|---|---|---|---|
| mdt:CustomField | parcial | 60 | 60 | 60 | 2 | parcial | não |
| mdt:CustomObject | parcial | 55 | 55 | 55 | 0 | parcial | não |
| mdt:CustomTab | parcial | 17 | 17 | 17 | 0 | parcial | não |
| mdt:FlexiPage | parcial | 12 | 12 | 12 | 0 | parcial | não |
| mdt:Flow | parcial | 50 | 50 | 13 | 0 | parcial | não |
| mdt:PathAssistant | completa | 7 | 7 | 7 | 1 | parcial | não |
| mdt:PermissionSet | completa | 24 | 24 | 24 | 18 | parcial | não |
| mdt:PermissionSetGroup | completa | 7 | 7 | 7 | 0 | parcial | não |
| mdt:Profile | parcial | 27 | 27 | 27 | 16 | parcial | não |
| mdt:QuickAction | parcial | 22 | 22 | 22 | 0 | parcial | não |
| mdt:RecordType | parcial | 7 | 7 | 7 | 1 | parcial | não |
| mdt:ValidationRule | completa | 6 | 6 | 6 | 0 | parcial | não |

## Propriedades XML

- Em metadata types: 294 listadas, 257 explicadas.
- Em estruturas auxiliares: 115 listadas, 115 explicadas.
- Universo total: Sem WSDL não há denominador confiável do total de propriedades do recorte.

## Objetos consultáveis via API

- Catalogados: 22. Campos listados: 577; explicados: 257.
- Universo: Universo de objetos da plataforma não enumerado.

| Objeto | Estrutural | Esperados | Presentes | Explicados | APIs verificadas |
|---|---|---|---|---|---|
| obj:Case | parcial | n/d | 56 | 12 | padrao |
| obj:CustomField | parcial | n/d | 6 | 6 | tooling |
| obj:CustomObject | parcial | n/d | 10 | 10 | tooling |
| obj:CustomTab | completa | 13 | 13 | 13 | tooling |
| obj:EntityDefinition | parcial | n/d | 13 | 6 | tooling |
| obj:FieldDefinition | parcial | n/d | 12 | 11 | tooling |
| obj:FlexiPage | completa | 11 | 11 | 11 | tooling |
| obj:Flow | completa | 15 | 15 | 15 | tooling |
| obj:FlowDefinition | completa | 11 | 11 | 11 | tooling |
| obj:Lead | parcial | n/d | 74 | 14 | padrao |
| obj:LoginHistory | parcial | n/d | 24 | 24 | padrao |
| obj:Opportunity | parcial | n/d | 58 | 11 | padrao |
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

- Total: 37; verificados: 34.
- Por tipo: correspondencia_xml_api: 11, referencia_campo: 22, representacao_comum: 4

## Taxonomia e funcionalidades

- Classificações: 14; subclassificações: 92 (com funcionalidades: 21).
- Funcionalidades cadastradas: 17 (universo de funcionalidades não definido).
