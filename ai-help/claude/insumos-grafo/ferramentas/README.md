# Ferramentas dos insumos

| Arquivo | Para quê |
|---|---|
| `sftutor.py` | Valida o catálogo e gera as projeções (`python3 ferramentas/sftutor.py tudo`). Rode depois de qualquer mudança; a validação precisa terminar com 0 erros. |
| `carga/` | Biblioteca para montar lotes novos de catálogo (metadata types, estruturas, objetos API, relacionamentos, funcionalidades). |
| `carga/historico/` | Scripts originais dos lotes 1 a 5k, guardados só como registro. **Não reexecute** sobre o catálogo atual. |

## Regras que valem para qualquer lote

- O catálogo em JSON (`catalogo/`) é a fonte da verdade. Um lote acrescenta ou corrige arquivos e não reconstrói o que já existe.
- Todo fato novo precisa de fonte em `fontes/registro.json` e de nota de extração em `fontes/extracoes/`. O validador confere que cada nome de propriedade aparece na nota da fonte citada.
- Sem fonte, o estado é `desconhecido`. Não preencha com suposição.
- Um metadata type só entra se estiver em `inventarios/metadata-types-v68.json`.
- Correspondência XML↔API "direta" ou "transformada" exige prova de campo (como o campo `Metadata` tipado no objeto Tooling). Sem essa prova, use `representacao_comum`. Há teste para isso.

## Como montar um lote novo

1. Leia a documentação e escreva a nota de extração em `fontes/extracoes/<lote>.txt`: URL versionada, data, método e o que foi lido.
2. Crie um script do lote, por exemplo `ferramentas/carga/lotes/lote6a.py`. Pode ficar fora do repositório enquanto está em rascunho, mas entra no PR.
3. Rode o script a partir de `ai-help/claude/insumos-grafo/`. Depois rode `python3 ferramentas/sftutor.py tudo` e `python3 -m unittest discover -s testes`.

Esqueleto:

```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # pasta ferramentas/
from carga import mdt as M
from carga.mdt import P
from carga.obj import field, expo, obj, cob, cnt, APEX_OK
from carga.base import af
from carga import catalogo as C

DATA = "2026-11-10"
EXTR = "fontes/extracoes/lote6a.txt"
C.registrar_fontes([C.fonte_mdapi("ExemploType", EXTR, DATA)])

M.struct("ExemploItem", "src:mdapi-exemplotype", ["mdt:ExemploType"], [
    P("nome", "string", None, "Nome do item.", "S"),
], "Item da lista de ExemploType.")
M.mdt("ExemploType", "src:mdapi-exemplotype", "O que o tipo representa.", "Para que serve.", "60.0", [
    P("label", "string", None, "Rótulo.", "S"),
    P("itens", "ExemploItem[]", None, "Itens.", estrutura="ExemploItem"),
    M.FULLNAME_HERDADO(None),
], curinga=True, setup=af("desconhecido", None, "Caminho no Setup não verificado."))
M.emit_structs()   # grava as estruturas registradas com struct()

C.marcar_referencia("estruturas", "ExemploItem", "nome", "mdt:OutroType")
C.rel_referencia("exemploitem-outrotype", "mdx:ExemploItem", "nome", "mdt:OutroType", "Explicação do vínculo.", "src:mdapi-exemplotype")
C.ampliar_funcionalidade("alguma-funcionalidade", mdts=[("ExemploType", "Papel do tipo na funcionalidade.")], srcs=["src:mdapi-exemplotype"])
```

### Peças principais

- **Propriedades e estruturas.** `P(nome, tipo, desde, descricao, req, **kw)` monta uma linha. `req` pode ser `S` (obrigatória), `N` (não marcada), `C:condição` ou `?` (desconhecida). Entre os `kw`:
  - `vals=[(valor, descricao)]`, com `completa="nao"` quando a lista é parcial;
  - `default=("valor", "x", nota)` e `estrutura="Nome"`;
  - `notas=[...]` e `herdada="Metadata"`.
- **Tipos `*Settings`.** Use `M.mdt(..., arquivos_prontos=M.arquivos_settings("Tipo", "Base", src))`, porque o registro do CLI só conhece o tipo genérico `Settings`.
- **Campos de objeto API.** `field(obj, nome, tipo, props, desde, descricao, src, **kw)`. `props` são as letras da Object Reference: C create, D defaulted, F filter, G group, I idLookup, N nillable, R restricted, S sort e U update.
- **Relacionamentos.**
  - `C.rel_lookup(...)`: lookups entre objetos.
  - `C.rel_referencia(...)` com `C.marcar_referencia(...)`: referência por nome no XML.
  - `C.rel_representacao_comum(...)`: o mesmo componente visto como XML e como objeto API.
- **Funcionalidades.** `C.funcionalidade(...)` cria uma nova. Para alterar uma existente, use `C.ampliar_funcionalidade(...)`, `C.secundaria(...)` e `C.definir_setup(...)`. `C.ligar_nuvem(...)` inclui a funcionalidade numa nuvem, só pela classificação principal.

### Testes e cópia temporária

A variável de ambiente `SFTUTOR_BASE` aponta a biblioteca para outra cópia da base. Os testes copiam `catalogo/`, `fontes/` etc. para uma pasta temporária e carregam um lote de exemplo ali, sem tocar no catálogo real (`testes/test_insumos.py`, classe `TestCargaNova`).

## Diferenças em relação aos scripts históricos

- Os caminhos são relativos à pasta `insumos-grafo/`; os históricos usavam caminhos absolutos da sessão.
- A lista de metadata types conhecidos (`MDT_NAMES`) acompanha o catálogo. Os históricos usavam uma lista fixa.
- As funções de construção inicial do lote 1 (taxonomia, nuvens e nó central) não foram levadas para a biblioteca, porque reconstruiriam o catálogo. Ficam só em `historico/`.
