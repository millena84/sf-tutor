# Exportação de acesso e compartilhamento

Os JSONs apresentam o catálogo de referência existente para `User`, `Profile`,
`PermissionSet`, `PermissionSetGroup`, `Role`, `Group` (Groups), `Queue` e OWD,
na versão de referência 68.0. Não são uma extração de uma organização.

**A exportação é parcial:** não atende ainda ao pedido de todas as propriedades
XML e todos os campos com explicações. Ela preserva os estados, evidências e
contagens do catálogo original; `null` significa que o levantamento ainda não
foi realizado, não que o tipo ou objeto não tenha propriedades ou campos.
O registro de fontes está em `fontes.json`, com caminhos relativos à raiz de
`insumos-grafo/`. A documentação oficial não pôde ser consultada novamente
nesta exportação.

- `User` é um objeto de API, não um metadata type XML.
- `Role`, `Group` e `Queue` têm pasta e sufixo obtidos do snapshot do registro
  da CLI; suas propriedades XML e os campos dos objetos relacionados ainda não
  foram levantados aqui.
- `Profile` e `CustomObject` têm estruturas XML aninhadas ainda não detalhadas;
  os campos dos objetos exportados têm cobertura parcial. Em particular, `User`
  tem 183 campos registrados, dos quais 23 têm explicação, e a lista não é completa.
- `PermissionSet` e `PermissionSetGroup` têm propriedades de primeiro nível
  documentadas no catálogo; os objetos relacionados e as correspondências
  XML/API continuam parciais. Campos `Permissions*` são um domínio dinâmico,
  não uma lista completa neste catálogo.
- OWD é uma configuração, não um tipo XML independente. O arquivo `OWD.json`
  inclui o `CustomObject` completo conforme o levantamento existente, inclusive
  `sharingModel` e `externalSharingModel`; não implica que todos os cenários
  de compartilhamento de todos os objetos estejam cobertos.
- “Objeto relacionado” é um objeto exposto por API, não uma afirmação sobre
  tabelas físicas privadas nem uma correspondência direta de todos os campos.

As pastas são relativas ao diretório de metadados do pacote, normalmente
`force-app/main/default/`; em `CustomObject` o source format é decomposto por
objeto e por tipo filho. Consulte `arquivos` para os formatos de fonte e da
Metadata API e as notas de cobertura antes de usar os dados.

Para atualizar os arquivos depois de alterar o catálogo:

```bash
python3 exportacoes/acesso/gerar.py
```

O comando é executado a partir de `insumos-grafo/` e não altera o catálogo.
Para completar o levantamento, é necessário consultar as referências oficiais
da versão escolhida e, para uma organização concreta, conferir seu Metadata WSDL
e `describe` dos objetos acessíveis, incluindo campos condicionais e customizados.
