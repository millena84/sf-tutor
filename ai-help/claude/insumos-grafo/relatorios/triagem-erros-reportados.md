# Triagem dos erros reportados

Rotina para tratar o que chega pelo botão "Reportar erro" do Metadata Desbugado (#152). Versão de 2026-11-26.

## Resumo

1. Todo reporte vira uma issue no repositório público, com o label `erro-reportado`.
2. Na triagem, a issue recebe um label de decisão: `confirmado`, `sem-mudanca`, `aguardando-fonte` ou `duplicado`.
3. A correção entra no `sf-tutor` por PR, com fonte oficial, e é publicada.
4. A issue recebe uma resposta e é fechada. Se a pessoa pediu crédito, ganha `creditar`.
5. As notas de versão listam as issues fechadas com `creditar`.

## De onde vêm os reportes

| Canal | Como chega | O que fazer |
| --- | --- | --- |
| Issue no GitHub | Já vem com o label `erro-reportado` e o formulário preenchido | Seguir a rotina |
| E-mail para o suporte | Chega com o assunto `ERRO REPORTADO: Metadata Desbugado (<id>)` | Abrir uma issue no repositório público com o conteúdo, **sem** o e-mail nem dados pessoais de quem enviou; escrever "Reportado por e-mail". Responder o e-mail com o link da issue |

## Labels

Criados pelo workflow de publicação (passo "Garantir os labels da triagem"). Não precisa criar à mão.

| Label | Quando usar |
| --- | --- |
| `erro-reportado` | Entrada. Aplicado pelo formulário |
| `confirmado` | Conferido na fonte oficial: o site está errado e a correção está a caminho |
| `sem-mudanca` | Conferido: o site já está de acordo com a fonte, ou a mudança não faz sentido |
| `aguardando-fonte` | Não deu para confirmar; falta uma fonte oficial |
| `duplicado` | Já existe outra issue sobre o mesmo ponto |
| `creditar` | Quem reportou preencheu nome ou usuário do GitHub e pediu crédito |

## Passo a passo

### 1. Primeira leitura (meta: até 7 dias)

- **Dados sensíveis:** se a issue tiver dados de org, credenciais, IDs de registro ou dados pessoais de terceiros, edite a issue para remover e avise a pessoa na resposta.
- **Tipo do problema:** veja o que a ficha afirma e o que a pessoa diz. Classifique mentalmente:
  - erro factual (tipo, propriedade, campo, valor, versão);
  - informação desatualizada;
  - classificação didática (em que tema ou funcionalidade o item aparece; é escolha do projeto);
  - texto confuso;
  - problema do site (algo não abre, não funciona).
- **Duplicado:** se já existe issue igual, aplique `duplicado`, responda com o link e feche.

### 2. Conferir na fonte oficial

- Abra a página oficial da Salesforce na versão de referência do site (hoje API 68.0).
- Se a pessoa mandou uma fonte, confira essa também.
- **Confirmado:** aplique `confirmado`.
- **O site já está certo:** aplique `sem-mudanca` e responda explicando, com a fonte.
- **Sem fonte que decida:** aplique `aguardando-fonte` e peça uma fonte à pessoa. Se ninguém trouxer em 30 dias, feche explicando.
- **Classificação didática:** não existe fonte oficial que decida. Decida pelo escopo escrito no próprio catálogo (campos `escopo` e `fora_do_escopo` do tema) e registre o motivo na resposta.

### 3. Corrigir no `sf-tutor`

- Corrija em `catalogo/`, `config/` ou `fontes/`, nunca em `gerado/` ou `inventarios/`.
- Todo fato novo precisa da fonte em `fontes/registro.json` e de nota de extração.
- Rode `python3 ferramentas/sftutor.py tudo` (0 erros) e, se mexer no site, `npm run verificar`.
- Abra o PR citando o link da issue pública no corpo. Como a issue está em outro repositório, "Fixes #n" não fecha a issue sozinho.
- Para pedir ao Claude: "faça a triagem da issue <link>" com o texto da issue colado, porque a sessão não lê o repositório público.

### 4. Publicar

- Merge do PR no `sf-tutor`.
- O workflow abre o PR de publicação no repositório público; merge dele.

### 5. Responder e fechar

- Responda com um dos modelos abaixo e feche a issue.
- Se a pessoa preencheu nome ou usuário do GitHub, aplique `creditar`. Preencher esses campos é o pedido de crédito; o formulário diz que servem para isso.

### 6. Créditos nas notas de versão

- Ao preparar uma versão, liste as issues fechadas com `creditar` desde a versão anterior:

```bash
gh issue list --repo millena84/metadata-desbugando --label creditar --state closed --search "closed:>=AAAA-MM-DD" --json number,title,body,author
```

- Use o nome ou o usuário que a pessoa escreveu no formulário. Para reportes por e-mail, use o nome só se a pessoa o escreveu no campo "Nome".
- **Não guarde a lista de créditos nos insumos.** As instruções do projeto proíbem dados pessoais em `ai-help/claude/insumos-grafo/`. Os nomes ficam nas issues, escritas pelas próprias pessoas, e nas notas de versão publicadas.

## Modelos de resposta

**Corrigido**
> Obrigada pelo reporte! Conferimos na documentação oficial (<link>) e você tem razão: <o que mudou>. A correção já está publicada. <Se pediu crédito: Seu nome vai nas notas da próxima versão.>

**Sem mudança**
> Obrigada pelo reporte! Conferimos na documentação oficial (<link>) e a ficha está de acordo com ela: <explicação curta>. Se você tiver uma fonte que diga outra coisa, comente aqui que reabrimos.

**Aguardando fonte**
> Obrigada pelo reporte! Não encontramos na documentação oficial algo que confirme ou descarte isso. Você tem um link da Salesforce que mostre o correto? Sem uma fonte, fechamos esta issue em 30 dias.

**Classificação didática**
> Obrigada pelo reporte! Essa organização em temas é uma escolha didática do projeto, não da Salesforce. Pelo escopo do tema (<escopo>), <decisão e motivo>.

**Duplicado**
> Obrigada pelo reporte! Esse ponto já está sendo tratado em <link>; acompanhe por lá.

## Caso 1: public groups em "Permissões, perfis e grupos" (adiado para depois do MVP)

- **Origem:** teste do envio de erro feito pela autora no celular, em 2026-11-26, sobre a ficha do tema `sub:permissoes-perfis-e-grupos`.
- **Pergunta:** public groups não deveriam ficar em hierarquias?
- **O que o catálogo diz hoje:**
  - `func:public-groups` tem como classificação principal `sub:permissoes-perfis-e-grupos`.
  - Tem como secundárias `sub:acesso-a-registros-e-hierarquias` ("alvo de sharing rules") e `sub:pastas-e-acesso`.
  - O escopo de "Permissões, perfis e grupos" é "o que um usuário pode fazer: perfis, permission sets e grupos de permission sets" e manda "quais registros o usuário enxerga" para "Acesso a registros e hierarquias".
  - O próprio item avançado do tema, "Para que serve um public group", descreve o grupo como alvo de sharing rules, pastas de relatórios e dashboards e list views, todos ligados a acesso a registros.
- **Tipo:** classificação didática. Nenhuma fonte oficial decide; vale o escopo escrito no catálogo.
- **Avaliação:** o reporte procede. Pelo escopo do próprio projeto, public groups decidem quais registros alguém enxerga, não o que pode fazer. O "grupos" do nome do tema é de permission set groups.
- **Proposta:**
  1. A classificação principal passa a ser `sub:acesso-a-registros-e-hierarquias`.
  2. "Permissões, perfis e grupos" vira secundária, com o motivo "nome parecido: os 'grupos' deste tema são permission set groups".
  3. O item avançado "Para que serve um public group" e as considerações de grupos grandes e aninhados vão para "Acesso a registros e hierarquias".
  4. `func:public-groups` sai do "por onde começar" de "Permissões, perfis e grupos".
- **Status:** decisão da autora em 2026-11-26: não mexer no MVP (era um teste do envio). Reavaliar depois do lançamento.
