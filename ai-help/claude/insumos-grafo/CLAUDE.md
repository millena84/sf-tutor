# Instruções locais: ai-help/claude/insumos-grafo

- Edite somente `catalogo/`, `config/`, `fontes/`, `schemas/`, `ferramentas/`, `testes/` e `relatorios/` (exceto `relatorios/cobertura.md`, que é gerado).
- Nunca edite `gerado/` ou `inventarios/` à mão. Rode `python3 ferramentas/sftutor.py tudo` após qualquer mudança e deixe a validação com 0 erros.
- Não invente metadata types, propriedades, campos, valores, defaults, caminhos de Setup ou relacionamentos. Sem fonte, use estado `desconhecido`; nunca preencha com suposição.
- Todo novo fato precisa de uma fonte em `fontes/registro.json` e de uma nota de extração em `fontes/extracoes/` (URL versionada, data, método e o que foi lido).
- Um metadata type só pode ser cadastrado se constar de `inventarios/metadata-types-v68.json`. Objetos de dados (User, Organization, PermissionSetAssignment etc.) vão para `objetos-api/`.
- Não escreva "completo" em cobertura sem esperado == presente, tipos compostos detalhados e estruturas usadas completas; o validador recusa.
- Use pt-BR nas explicações e preserve os nomes técnicos originais. Paráfrases, nunca cópia de trechos da documentação.
- Não salve credenciais, IDs reais, dados pessoais ou registros de org. Não faça commit, push ou publicação sem autorização.
- Para continuar o catálogo, siga `relatorios/retomada.md`.
