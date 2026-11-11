# ideia de Roteiro: Salesforce para um desenvolvedor back-end

São 10 blocos de no máximo 10 minutos. Cada bloco tem o objetivo, os pontos principais, uma analogia com o mundo back-end e um desenho para a lousa. O último bloco liga tudo à documentação gerada pelos utilitários.

---

## 0. Abertura: o mapa geral (3 min)

**Objetivo:** dar uma visão do todo antes dos detalhes.

**Frase de abertura:** *"A Salesforce é uma plataforma multi-tenant guiada por metadados. Quase tudo que você vê numa org é configuração armazenada como metadado, e o código é só uma parte disso."*

**Desenho (deixe no canto da lousa a conversa toda):**
```
┌──────────────────────── ORG (tenant) ────────────────────────┐
│  [Front-end]   LWC · Aura · Visualforce · Lightning Pages    │
│  [Lógica]      Apex · Triggers · Flows · Validation Rules    │
│  [Dados]       Objetos · Campos · Relacionamentos            │
│  [Segurança]   Profiles · Permission Sets · Sharing          │
│  [Integração]  APIs · Named Credentials · Platform Events    │
└──────────────────────────────────────────────────────────────┘
        ▲ tudo isso = METADADO (XML)     ▲ registros = DADOS
```
Volte a esse mapa em cada bloco: "agora estamos nesta camada".

---

## 1. Multi-tenancy: o que é uma "Org" (8 min)

**Pontos principais:**
- **Org = tenant.** Cada cliente tem uma ou mais orgs, identificadas por um **Org ID** (começa com `00D`).
- Várias orgs rodam na mesma infraestrutura (instâncias/pods, ex.: `NA123`, hoje na Hyperforce). O banco é compartilhado e separado logicamente pelo OrgId.
- **Consequência prática: os Governor Limits.** Como os recursos são compartilhados, a plataforma impõe limites por transação (ex.: 100 queries SOQL e 150 operações DML síncronas). Isso molda todo o jeito de programar.
- Atualizações são automáticas, 3 releases por ano (Spring, Summer, Winter). Ninguém "atualiza a versão".

**Analogia:** um SaaS com banco compartilhado e coluna `tenant_id` em todas as tabelas, com rate limiting rígido por request.

**Desenho, um prédio de apartamentos:**
```
        ┌───────────── Pod / Instância ─────────────┐
        │  🏢  Infra compartilhada (CPU, DB, app)   │
        │ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐   │
        │ │Org A  │ │Org B  │ │Org C  │ │Org D  │   │
        │ │00D...1│ │00D...2│ │00D...3│ │00D...4│   │
        │ └───────┘ └───────┘ └───────┘ └───────┘   │
        └───────────────────────────────────────────┘
          "o condomínio impõe regras" = Governor Limits
```

---

## 2. Metadados vs dados: o conceito central (10 min)

**Pontos principais:**
- **Dados** são os registros (uma Conta, um Caso). **Metadados** são a definição de tudo: objetos, campos, layouts, regras, permissões, código.
- A plataforma não gera tabelas físicas por cliente. Um **runtime engine** interpreta os metadados e monta o comportamento. Criar um campo é inserir metadado, não rodar `ALTER TABLE`.
- Os metadados são acessados pela **Metadata API** e representados como **XML**. Exemplo de campo:
  ```xml
  <!-- force-app/main/default/objects/Pedido__c/fields/Valor__c.field-meta.xml -->
  <CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
      <fullName>Valor__c</fullName>
      <label>Valor</label>
      <type>Currency</type>
      <precision>16</precision>
      <scale>2</scale>
  </CustomField>
  ```
- O código Apex também é metadado: um `.cls` acompanhado de um `.cls-meta.xml` com a versão da API.
- O `package.xml` (manifest) diz quais tipos e membros entram num retrieve ou deploy.

**Analogia:** é como se o schema do banco, os arquivos de config, o RBAC e o código fossem todos versionados como arquivos declarativos, num estilo "infra as code", só que para a aplicação inteira.

**Desenho, duas camadas:**
```
   METADADO (o "molde")              DADOS (o "conteúdo")
  ┌──────────────────────┐          ┌──────────────────────┐
  │ Objeto: Pedido__c    │          │ Pedido #001  R$ 500  │
  │  - Valor__c Currency │ ───────► │ Pedido #002  R$ 900  │
  │  - Status__c Picklist│  define  │ Pedido #003  R$ 120  │
  └──────────┬───────────┘          └──────────────────────┘
             │ Metadata API                ▲ REST/SOAP/Bulk API
             ▼                             │ SOQL / DML
      XML no Git (SFDX)
```

---

## 3. Modelo de dados (8 min)

**Pontos principais:**
- **Objetos standard** (Account, Contact, Opportunity, Case) e **objetos custom** (sufixo `__c`). Campos custom também usam `__c`, e relacionamentos usam `__r` nas queries.
- Todo registro tem um **ID de 15/18 caracteres**. Os 3 primeiros indicam o objeto (`001` = Account, `003` = Contact).
- Os relacionamentos:
  - **Lookup:** fraco, como uma FK opcional.
  - **Master-Detail:** forte, com delete em cascata, segurança herdada do pai e campos *roll-up summary*.
- **SOQL** é parecido com SQL, mas sem `JOIN` explícito: você navega pelos relacionamentos.
  ```sql
  SELECT Name, Account.Name, (SELECT Id FROM Contacts) FROM Account
  ```
- Outros recursos do modelo: Record Types (variações de um mesmo objeto), Picklists, Formula Fields e Validation Rules.

**Analogia:** um ORM em que o schema é editado por uma UI ou por XML, e a "query" é SOQL.

**Desenho, ER simplificado:**
```
   Account ──1:N (lookup)──► Contact
      │
      └──1:N (master-detail)──► Pedido__c ──► ItemPedido__c
                                  ▲ Σ roll-up do valor dos itens
```

---

## 4. Segurança e acesso (8 min)

**Pontos principais.** Há três perguntas, em camadas:
1. **Pode entrar e usar o objeto?** É respondida por **Profile** e **Permission Sets** (CRUD no objeto e FLS, a segurança por campo).
2. **Quais registros vê?** É respondida pelo **Sharing**: OWD (padrão da org: Private ou Public), **Role Hierarchy**, Sharing Rules e Manual Sharing.
3. **Como o código respeita isso?** Pelas palavras-chave `with sharing` / `without sharing` e por `WITH USER_MODE` nas queries.
- A tendência atual é deixar o Profile mínimo e conceder acesso por Permission Sets e Permission Set Groups.

**Analogia:** RBAC (o que pode fazer) combinado com row-level security (quais linhas vê).

**Desenho, um funil:**
```
   Todos os registros da org
   ▼  OWD (baseline: Private / Read / Read-Write)
   ▼  + Role Hierarchy (chefe vê dos subordinados)
   ▼  + Sharing Rules / Teams / Manual
   ▼  ∩ Object + Field permissions (Profile / Permission Set)
   = O que o usuário enxerga
```

---

## 5. Ambientes, projeto SFDX e deploy (10 min)

**Pontos principais:**
- Tipos de org: **Production**, **Sandboxes** (Developer, Developer Pro, Partial Copy, Full) e **Scratch Orgs** (efêmeras, criadas a partir de um arquivo de definição).
- **Salesforce CLI (`sf`)** e **estrutura de projeto SFDX**:
  ```
  sfdx-project.json
  manifest/package.xml
  force-app/main/default/
     classes/        → Apex (.cls + .cls-meta.xml)
     triggers/
     lwc/            → componentes front-end
     objects/        → objetos, campos, record types (XML)
     permissionsets/
     flows/
     layouts/
  ```
- O "build" não gera binário: o deploy envia metadado para a org. Em produção, **os testes Apex rodam no deploy** e a cobertura mínima é de **75%**.
- Formas de deploy: `sf project deploy start`, Change Sets (legado, via UI), pipelines CI/CD ou DevOps Center. Também existem packages (unlocked e managed).

**Analogia:** a org é o "servidor" e o deploy é aplicar um diff declarativo. Lembra um `kubectl apply`, mas com testes obrigatórios.

**Desenho, um pipeline:**
```
  Dev (scratch/sandbox) ─► Git (PR) ─► CI: validate + testes ─► QA/UAT sandbox ─► PROD
        ▲ sf retrieve                       sf deploy --dry-run         sf deploy
```

---

## 6. Back-end: Apex e padrões de projeto (10 min)

**Pontos principais:**
- **Apex** é uma linguagem parecida com Java, fortemente tipada, compilada e executada na plataforma. DML (`insert`, `update`) e SOQL fazem parte da própria linguagem.
- **Triggers** disparam em eventos de registro (before/after insert/update/delete).
- **Order of Execution:** validações, before triggers, after triggers, flows, commit. Conhecer essa ordem evita muito bug.
- **Bulkification:** um trigger recebe até 200 registros de uma vez. Nunca coloque query ou DML dentro de loop.
- Padrões comuns:
  - **Trigger Handler:** um trigger por objeto, com a lógica numa classe.
  - **Separation of Concerns (fflib / Apex Enterprise Patterns):** *Service* (regras de negócio), *Domain* (lógica do objeto), *Selector* (queries), *Unit of Work* (DML agrupado).
- Processamento assíncrono: `@future`, **Queueable**, **Batch Apex** (grandes volumes) e **Schedulable** (cron).
- Testes: classes `@isTest`, `Test.startTest()` e mocks com `HttpCalloutMock`/`Stub API`.

**Analogia:** uma arquitetura em camadas (Controller → Service → Repository), só que o "Repository" é o Selector com SOQL, e cada request tem quotas de recursos.

**Desenho, as camadas e o fluxo de um trigger:**
```
  Trigger (fino) ──► Handler ──► Service ──► Domain
                                   │            │
                                   ▼            ▼
                                Selector     Unit of Work
                                 (SOQL)       (DML único)
  ─────────────────────────────────────────────────────
  ⚠ por transação: 100 SOQL · 150 DML · 10s CPU · heap 6MB
```

---

## 7. Automação declarativa vs código (5 min)

**Pontos principais:**
- **Flow** é a ferramenta low-code principal (Record-Triggered, Screen, Scheduled e Autolaunched Flows). Workflow Rules e Process Builder estão descontinuados.
- Regra prática: **"clicks before code"**. Use Apex quando houver complexidade, volume ou integração.
- Ponto de atenção: Flow e Apex no mesmo objeto podem conflitar, por isso a order of execution importa.
- Flows também são metadado: arquivos XML `.flow-meta.xml`.

**Desenho, uma escada de decisão:**
```
 Validation Rule / Formula  →  Flow  →  Apex
   (mais simples)                     (mais poder/controle)
```

---

## 8. Front-end: LWC e afins (8 min)

**Pontos principais:**
- **Lightning Web Components (LWC)** é o padrão atual, baseado em Web Components (HTML, JS ES6+ e CSS). Cada componente é uma pasta com `.html`, `.js` e `.js-meta.xml` (onde ele pode ser usado).
- **Aura** é o framework anterior. **Visualforce** é o legado, renderizado no servidor e parecido com JSP.
- Acesso a dados a partir do front-end:
  - **Lightning Data Service / `@wire` adapters:** CRUD sem escrever back-end, com cache e segurança automáticos.
  - **Métodos Apex `@AuraEnabled`:** chamados via `@wire` ou de forma imperativa. Fazem papel de endpoint.
- Montagem das telas: os componentes são encaixados em **Lightning Pages** pelo **Lightning App Builder**, sem código.
- Comunicação entre componentes: `@api` (de pai para filho), eventos (de filho para pai) e **Lightning Message Service** (entre componentes sem relação direta).

**Analogia:** uma SPA modular em que o "BFF" são as classes Apex `@AuraEnabled`.

**Desenho, a stack:**
```
  ┌───────── Lightning Page (App Builder) ─────────┐
  │  [LWC A] ◄─LMS─► [LWC B]                       │
  │     │ @wire / LDS          │ imperativo        │
  └─────┼──────────────────────┼───────────────────┘
        ▼                      ▼
   UI API (sem código)     Apex @AuraEnabled ──► SOQL/DML
```

---

## 9. Integração (10 min)

**Pontos principais.** Há duas direções:

**Entrando (sistemas externos chamando a Salesforce):**
- APIs nativas: **REST**, **SOAP**, **Bulk API 2.0** (grandes volumes), **Composite** (várias operações numa chamada) e **GraphQL**.
- **Apex REST customizado:** `@RestResource(urlMapping='/pedidos/*')`.
- Autenticação **OAuth 2.0** via **Connected App / External Client App** (fluxos JWT Bearer, Client Credentials e outros).

**Saindo (a Salesforce chamando sistemas externos):**
- **Apex Callouts** (`HttpRequest`) usando **Named Credentials + External Credentials**, que guardam endpoint e segredos fora do código.
- Eventos: **Platform Events** (pub/sub), **Change Data Capture** (stream de alterações nos registros) e **Pub/Sub API** (gRPC).
- Middleware: MuleSoft ou outro ESB/iPaaS.

**Pontos de arquitetura:** limites de callouts (100 por transação, timeout de 120s), callouts não podem ocorrer depois de DML pendente na mesma transação, e operações pesadas devem ser assíncronas (Queueable com callout).

**Analogia:** a Salesforce funciona como um serviço com API gateway próprio, message broker interno (Platform Events/CDC) e um cofre de segredos (Named Credentials).

**Desenho, um hub:**
```
                    OAuth (Connected App)
   ERP ──REST/Bulk──►┌────────────┐◄──Pub/Sub API── Consumidores
                     │  SALESFORCE│──Platform Events / CDC──►
   App  ◄──Callout───│    ORG     │
   (via Named Cred.) └─────┬──────┘
                           ▼
                   MuleSoft / Middleware
```

---

## 10. Fechamento: como ler a documentação gerada (5 min)

**Objetivo:** ligar tudo que foi visto à estrutura de documentação que vocês criaram a partir dos utilitários.

**Sugestão de fala:** *"A documentação espelha os tipos de metadado. Cada seção corresponde a uma pasta do `force-app` e a uma camada do mapa do bloco 0."*

**Desenho, retomando o mapa:** desenhe setas de cada camada do mapa inicial para a seção correspondente da documentação:
```
  Dados        → objects/ (campos, relacionamentos)
  Segurança    → permissionsets/, profiles/
  Lógica       → classes/, triggers/, flows/
  Front-end    → lwc/, flexipages/
  Integração   → namedCredentials/, externalCredentials/, platformEvents (objects/*__e)
```
Peça ao desenvolvedor que abra um objeto na documentação e siga os rastros: campos, triggers do objeto, classes chamadas e componentes que exibem o objeto. Isso fixa o conteúdo na prática.

---

## Sugestões de uso

- **Conversa rápida (cerca de 30 min):** blocos 0, 1, 2, 6 e 9. É o núcleo que um dev back-end mais precisa.
- **Série completa:** são aproximadamente 85 minutos, que podem ser divididos em 3 sessões:
  - **Sessão 1, Fundamentos:** blocos 0 a 4.
  - **Sessão 2, Desenvolvimento:** blocos 5 a 8.
  - **Sessão 3, Integração e documentação:** blocos 9 e 10.
- **Fio condutor:** use um exemplo único do começo ao fim (ex.: o objeto `Pedido__c`, com campo, permissão, trigger, LWC e integração com ERP). Assim cada bloco acrescenta uma peça ao mesmo desenho.

Posso transformar este roteiro num documento compartilhável, ou num deck de slides com os desenhos já prontos.


---

# OBS: sobre xms internos

Em parte, sim. A ideia de "interpretar em tempo de execução" está certa, mas há dois detalhes que mudam o quadro: **o XML não é o que roda**, e **quem interpreta é o servidor, não o browser**. O texto do roteiro dá margem para essa leitura, então vale ajustar.

## 1. O XML é só o formato de transporte

O XML aparece quando os metadados **saem ou entram** na org: no retrieve, no deploy, nos arquivos do projeto SFDX e no Git. É uma serialização, como um JSON de exportação.

Dentro da org, os metadados ficam **em tabelas de banco**. Segundo o whitepaper de arquitetura multi-tenant que a Salesforce publicou, a estrutura é mais ou menos assim:

- **Tabelas de metadados** (o "dicionário"): uma tabela registra os objetos de cada org, outra os campos de cada objeto, sempre com o OrgId.
- **Uma grande tabela de dados genérica**: todos os registros de todos os objetos custom de todas as orgs ficam nela. Cada linha tem OrgId, ID do objeto e dezenas de colunas genéricas ("slots", tipo `Value0`, `Value1`...). O metadado diz que, na org X, o campo `Valor__c` do objeto `Pedido__c` está guardado no slot `Value7`.
- **Tabelas auxiliares de índice e de relacionamento**, porque as colunas genéricas sozinhas não seriam eficientes para buscar.

Por isso criar um campo não precisa de `ALTER TABLE`: a plataforma só insere uma linha no dicionário dizendo qual slot passa a ser `Valor__c`. O schema físico nunca muda.

## 2. Quem interpreta é o servidor, e com cache

Quando você abre uma página, o fluxo é este:

1. O **browser** carrega o framework Lightning (JavaScript) e pede ao servidor os dados e a descrição da tela.
2. O **servidor** consulta os metadados da sua org (objeto, campos, layout, permissões do seu usuário). Isso fica **em cache**, então não se relê tudo a cada clique.
3. Com essas informações, o servidor **gera a query** nas tabelas genéricas (traduz `Valor__c` para `Value7`, aplica sharing e FLS) e devolve **JSON**, com dados e a descrição da tela.
4. O **browser** só renderiza os componentes com o que recebeu.

O código Apex segue a mesma lógica: é compilado no deploy e fica guardado e em cache já compilado. Ele não é reinterpretado do texto a cada execução.

Então a resposta para a sua pergunta é: sim, a org é montada dinamicamente a cada acesso, a partir dos metadados. Mas isso acontece **no servidor**, a partir de **tabelas e cache**, e não por leitura de XML no browser.

## Desenho para a lousa

```
 Seu projeto (Git)            ORG (servidor Salesforce)                 Browser
┌──────────────┐  deploy  ┌───────────────────────────────┐  JSON   ┌───────────┐
│ arquivos XML │ ───────► │ Tabelas de metadados (+cache) │ ──────► │ Lightning │
│ (.field-meta │ ◄─────── │          │ "Valor__c = slot 7"│         │ renderiza │
│  .xml etc.)  │ retrieve │          ▼                    │         └───────────┘
└──────────────┘          │ Runtime engine monta a query  │
                          │          ▼                    │
                          │ Tabela de dados genérica      │
                          │ (OrgId | Obj | Value0..ValueN)│
                          └───────────────────────────────┘
```

## Sugestão de fala, conforme o público

- **Para uma conversa mais executiva:** *"Tudo na org é configuração guardada como metadado, e a plataforma monta a aplicação a partir disso. O XML é como exportamos e versionamos esses metadados."*
- **Para um público técnico, como o seu dev back-end:** use o desenho acima e a ideia dos "slots" na tabela genérica. É isso que explica de verdade por que não existe `ALTER TABLE` e por que a plataforma impõe tantos limites.

Um cuidado: esse modelo de tabelas genéricas vem de material público da própria Salesforce e é muito citado. Mas é uma descrição simplificada, e a implementação interna atual (com a Hyperforce, por exemplo) não é documentada em detalhe. Na conversa, apresente como "o modelo conceitual", não como a arquitetura exata de hoje.

Quer que eu atualize o bloco 2 do Google Doc com essa explicação e o novo desenho? O link continua o mesmo.

---

# Sobre o banco interno

## É Oracle?

Seu ex tech lead não estava errado. Por muito tempo foi Oracle, e talvez ainda seja em parte. A migração é gradual e pouco divulgada.

**Linha do tempo aproximada** (confirmei as datas de memória, sem pesquisar):
- **1999 a meados da década de 2010:** core sobre Oracle. Era o que todo mundo da área sabia e repetia.
- **Por volta de 2016:** saíram as primeiras notícias de que a Salesforce desenvolvia um banco próprio para reduzir a dependência da Oracle.
- **Por volta de 2018 em diante:** engenheiros da Salesforce passaram a falar publicamente do SDB, baseado em PostgreSQL.
- **Final de 2020:** anúncio da Hyperforce (a plataforma rodando em nuvem pública), o que acelera essa transição.

Ou seja, se ele aprendeu isso antes de 2018, ou se não acompanhou esses detalhes internos, faz todo sentido ele dizer Oracle. E ninguém de fora sabe com certeza quanto do core ainda roda em Oracle hoje.

**Sobre a relação com o Java, há um cuidado:** a semelhança do Apex com Java não tem ligação com o banco ser Oracle.
- O Apex lembra Java porque a Salesforce quis uma sintaxe familiar para os desenvolvedores, e os servidores de aplicação dela rodam em Java (JVM). O Apex é executado nessa camada.
- A Oracle só comprou a Sun, dona do Java, em 2010. O Apex é de 2007, quando o Java ainda não era da Oracle.
- Linguagem de aplicação e banco de dados são camadas independentes. Dá para ter Java em cima de PostgreSQL, Oracle ou qualquer outro banco.

Então a conclusão "faz sentido ser Oracle porque o Apex é baseado em Java" não se sustenta. São duas coisas que aconteceram em paralelo.

Se quiser levar isso para a conversa com segurança, posso pesquisar fontes públicas com as datas exatas e o estado atual.

**Sobre o Oracle:** não, não era na nuvem da Oracle. A Salesforce comprava licenças do Oracle Database e rodava o banco nos **próprios data centers**. Eram espaços alugados em empresas de colocation (como a Equinix), com servidores e storage dela. A Oracle Cloud, como existe hoje, nem existia na maior parte desse período. Era o modelo clássico: software da Oracle em hardware da Salesforce.

**(Abrindo o parênteses: Hyperforce na AWS)**

Você entendeu certo: a Hyperforce é a migração das orgs dos data centers próprios para nuvem pública, com a **AWS como principal parceira**. A Salesforce chegou a anunciar outras nuvens, mas a AWS é a base na prática.

**Existe um paper?** Até onde sei, não existe um documento público detalhando a infraestrutura na AWS, muito menos como o banco roda lá. O que existe é material mais conceitual:
- **Blog de engenharia da Salesforce** (engineering.salesforce.com): posts sobre a Hyperforce e seu projeto interno (codinome **Falcon**), com conceitos como infraestrutura como código, **células** (unidades isoladas que agrupam orgs, a evolução dos antigos "pods"), Kubernetes e infraestrutura imutável.
- **Página de Trust/Compliance da Hyperforce:** fala de residência de dados por região, criptografia e zero trust, mas sem detalhes de arquitetura.

**Sobre o banco na AWS:** o serviço de servidor dedicado que você está tentando lembrar provavelmente é o **EC2 Dedicated Hosts** (ou Dedicated Instances, ou instâncias bare metal). Agora, onde o SDB roda exatamente eu **não sei**. Faz mais sentido que esteja sobre **EC2** (talvez dedicado ou bare metal, por desempenho e isolamento), gerenciado pela própria Salesforce, do que num serviço gerenciado como o **RDS**. Um banco próprio e customizado normalmente não cabe num serviço gerenciado. Lembro também de falas dos engenheiros de que o SDB separa computação de armazenamento, possivelmente usando storage da nuvem. Mas isso é inferência e memória vaga, não informação confirmada.

Se quiser, pesquiso os posts do blog de engenharia e o que foi apresentado sobre o SDB para te dar fontes concretas.

**(Lembrete: o parênteses continua aberto.)** Quando quiser fechar, voltamos para o que estava pendente: atualizar o bloco 2 do Google Doc com a explicação do runtime engine e o novo desenho.

## Então o que é? o SDB?

Encontrei uma fonte oficial, e ela confirma o que eu tinha lembrado de forma vaga, com bem mais detalhe. A fonte é o guia **"The Salesforce Platform – Transformed for Tomorrow"**, do site Salesforce Architects. A página não tem data de publicação, mas cita números "de outubro de 2025".

## O que o guia diz sobre o SalesforceDB (SDB)

- **Base:** é um banco relacional "cloud-native" feito para o multi-tenant da Salesforce. O texto diz que ele *"estende o PostgreSQL, separa computação e armazenamento e usa Kubernetes e storage em nuvem"*.
- **Escala:** o SDB cuida de *"todos os dados transacionais de CRM"*, mais de **1,1 trilhão de transações por mês**.
- **Armazenamento:** o registro definitivo dos dados é um **storage de objetos em nuvem, como o S3 da AWS**. Arquivamento e replicação entre regiões acontecem nessa camada.
- **Como grava (LSM tree):** cada alteração vai primeiro para um log de transações (só de acréscimo) e para a memória. Depois é gravada em arquivos ordenados por chave, que são **imutáveis** e passam por merge e compactação periódicos. É o mesmo princípio de bancos como RocksDB e Cassandra.
- **Cache:** como o S3 tem latência alta, o SDB usa **caches de storage distribuídos**, um para os logs de transação e outro para os arquivos de dados.
- **Computação:** tudo roda em **Kubernetes**. Há um cluster primário e dois standby, em **três zonas de disponibilidade**. Para escalar, basta adicionar nós, que leem o storage imutável compartilhado sem precisar de coordenação.
- **Schema:** são 3 grandes atualizações de schema por ano e atualizações menores toda semana, sem downtime.

## O que isso muda no que eu disse antes

- **A migração é mais avançada do que eu imaginava.** O guia diz que o SDB atende *todos* os dados transacionais de CRM. Também diz que mais de 95% dos clientes já passaram para a nova plataforma, embora essa porcentagem se refira à plataforma em geral, não especificamente ao banco.
- **Minha suposição de EC2 ou servidor dedicado estava incompleta.** O modelo é **Kubernetes para computação e S3 para armazenamento**, como no Aurora ou no Neon. Não é um banco instalado em servidores com disco local.
- **O guia não fala de Oracle**, nem para dizer que saíram dela. Então "a Salesforce saiu do Oracle" é uma conclusão nossa, não uma afirmação oficial. Uma análise de terceiros lembra que o Larry Ellison já disse publicamente que a Salesforce "nunca sairia do Oracle". Seu ex tech lead tinha uma base razoável.

## Sobre as células da Hyperforce

- Cada org fica numa **célula da Hyperforce**, que já inclui o serviço SDB. A célula é o equivalente moderno da antiga "instância" (como NA123).
- A plataforma é descrita como **multi-cloud**. A AWS aparece como exemplo (S3, EMR), não como a única nuvem.

## Desenho para a lousa

```
        Célula Hyperforce (1 região, 3 AZs)
┌────────────────────────────────────────────┐
│  Kubernetes                                │
│  [Primário] [Standby] [Standby]  ← compute │
│       │  AZ-a     AZ-b     AZ-c            │
│       ▼                                    │
│  Caches de storage (log | arquivos)        │
│       ▼                                    │
│  Storage em nuvem (ex.: S3)                │
│  arquivos imutáveis + log append-only      │
└────────────────────────────────────────────┘
```

**Fontes:**
- [The Salesforce Platform – Transformed for Tomorrow (Salesforce Architects)](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-transformation.html), a fonte principal.
- [Architectural Principles for High Availability on Hyperforce (Salesforce Engineering)](https://engineering.salesforce.com/architectural-principles-for-high-availability-on-hyperforce/)
- [Behind the Scenes of Hyperforce (Salesforce Engineering)](https://engineering.salesforce.com/behind-the-scenes-of-hyperforce-salesforces-infrastructure-for-the-public-cloud-429309542d8e/)
- [Hyperforce Migration (Salesforce Engineering)](https://engineering.salesforce.com/unlocking-hyperforce-migration-innovative-solutions-for-a-smooth-transition-to-the-cloud/)
- [Salesforce Database Architecture (cirra.ai)](https://cirra.ai/articles/salesforce-database-architecture-explained), uma análise de terceiros sobre a questão do Oracle.

**(O parênteses continua aberto.)** O que estava pendente é atualizar o bloco 2 do Google Doc com a explicação do runtime engine. Se quiser, também posso incluir essa parte do SDB como curiosidade opcional, para quando o público for mais técnico.

Quase. O SDB é o banco que guarda os metadados, mas eles **não ficam lá em XML**. Esse é o ponto que vale reforçar na conversa.

**Como funciona:**
- Dentro da org, os metadados são **linhas em tabelas**, no "dicionário" que comentei antes: uma tabela de objetos, uma de campos e assim por diante, todas com o OrgId. Essas tabelas ficam no mesmo banco que os dados, hoje o SDB.
- O **XML só existe na fronteira**: quando a Metadata API exporta (retrieve) ou importa (deploy). No deploy, a plataforma lê o XML, valida e grava como linhas nas tabelas. No retrieve, faz o caminho inverso e monta o XML a partir das tabelas.
- Na execução, os metadados mais usados ficam em **cache**. O guia cita o Vegacache, um serviço baseado em Redis com mais de 2 trilhões de requisições por dia. Por isso a plataforma não vai ao banco a cada clique.

**Desenho:**
```
 Seu projeto        Metadata API                ORG
┌──────────┐ deploy ┌──────────────┐  grava ┌───────────────────────┐
│ XML      │ ─────► │ lê, valida e │ ─────► │ SDB: tabelas de       │
│ (.xml)   │ ◄───── │ converte     │ ◄───── │ metadados + dados     │
└──────────┘retrieve└──────────────┘  lê    │        ▲              │
                                            │  cache (Vegacache)    │
                                            │        ▲              │
                                            │  runtime engine       │
                                            └───────────────────────┘
```

**Uma ressalva:** o guia da Salesforce diz explicitamente que o SDB guarda "todos os dados transacionais de CRM" e "metadados do Data 360". Ele **não diz com todas as letras** que os metadados das orgs ficam no SDB. Como esses metadados sempre ficaram no mesmo banco que os dados (no tempo do Oracle era assim), é a conclusão mais provável. Mas é inferência minha, não afirmação oficial.

**Para a conversa:** *"O XML é como o metadado viaja entre o projeto e a org. Dentro da org ele vira linhas em tabelas, no mesmo banco dos dados, com cache na frente."*

**(O parênteses continua aberto.)** Já podemos fechar e voltar para a atualização do bloco 2 do Google Doc, com a explicação do runtime engine e este desenho. Quer que eu inclua também o trecho do SDB como curiosidade opcional?

Quase. Há dois ajustes.

## 1. O XML serve para o CRUD de metadados, e só por um dos caminhos

| O que muda | Por onde | Formato |
|---|---|---|
| **Metadados** (criar campo, objeto, regra) | Metadata API (deploy/retrieve) | **XML** |
| | Setup, a tela de configuração no browser | sem arquivo nenhum, grava direto |
| | Tooling API | JSON |
| **Dados** (criar ou editar um Pedido) | Tela, SOQL/DML no Apex, REST API, Bulk API | **JSON/CSV, nunca XML de metadado** |

Então o XML **não** é o CRUD em geral. Ele é o formato do CRUD de metadados **quando passa pela Metadata API**, que é o caminho do SFDX, do Git e do deploy. Se alguém cria um campo clicando no Setup, nenhum XML é gerado. O XML só aparece se você fizer um retrieve depois.

(A SOAP API de dados usa envelope XML, mas isso é só o protocolo de transporte, como em qualquer web service SOAP. Não tem relação com os arquivos de metadado.)

## 2. As tabelas são relacionais, mas não do jeito tradicional

**É tradicional no sentido de banco relacional:** são tabelas, linhas, colunas e SQL por baixo, já que o SDB estende o PostgreSQL.

**Não é tradicional em dois pontos:**
- **Não há uma tabela por objeto.** No modelo conceitual, os registros de vários objetos e de várias orgs ficam numa **tabela genérica** com colunas "slot" (`Value0`, `Value1`...). O dicionário de metadados diz que, na sua org, `Valor__c` é o slot 7. O seu `Pedido__c` não vira uma tabela `pedido` com coluna `valor`.
- **Não usa o armazenamento tradicional do PostgreSQL.** O PostgreSQL normal grava em páginas que são alteradas no próprio lugar. O SDB grava em log e arquivos imutáveis (LSM) no storage em nuvem.

## Resumo para a lousa

```
METADADO:  XML (Metadata API) ou Setup ──► linhas nas tabelas de dicionário
DADOS:     JSON (APIs) / SOQL-DML      ──► linhas na tabela genérica (slots)
                                            └── tudo no SDB (Postgres modificado,
                                                arquivos imutáveis em storage nuvem)
```

**Frase para a conversa:** *"O XML é só um formato de troca para metadados. Dentro da org, metadados e dados são linhas em tabelas, mas num modelo genérico multi-tenant, e não uma tabela por objeto como num sistema tradicional."*

**(O parênteses continua aberto.)** Quando quiser fechar, atualizo o bloco 2 do Google Doc com tudo isso: o runtime engine, o XML como formato de troca, as tabelas genéricas e o SDB como curiosidade opcional.

### exercicio bobo:

>Mas vamos supor o cenario: 1 org bananinha. Dados e componentes da org bananinha ficarão armazenados no sdb. O servidor interpreta o projeto sf (xmls) no lado server (tennant da org) e renderiza o setup da org com seus componentes? e como é no caso, por exemplo, de um registro custom metadata? Ou im registro em account? Ou um flow trigger em Contact?

Quase, mas com uma correção importante: **o servidor não interpreta o projeto sf (os XMLs) quando a org é usada**. Os XMLs são processados **uma vez, no deploy**, e viram linhas no SDB. Depois disso, o servidor trabalha só com essas linhas e com o cache. O projeto pode até ser apagado do seu computador que a org continua funcionando igual.

Outro ajuste: o tenant não é um servidor. A org bananinha é **lógica**. Os servidores da célula são compartilhados com várias outras orgs, e o que separa a bananinha das outras é o **OrgId** em cada linha e em cada entrada de cache.

## O ciclo de vida da org bananinha

```
① DEPLOY (uma vez)          ② USO (toda requisição)
projeto sf (XML)            Usuário abre o Setup ou uma tela
     │ Metadata API              │
     ▼                           ▼
valida, compila Apex,       Servidor da célula (compartilhado)
grava linhas no SDB  ──►    lê metadados da bananinha (cache → SDB)
(OrgId = bananinha)         monta resposta JSON → browser renderiza
```

O **Setup** é só mais uma tela montada a partir dessas linhas: ele lista os objetos, campos e flows que estão gravados para a bananinha.

## Os seus três casos

### 1. Um registro de Custom Metadata (ex.: `Config_Frete__mdt`)
- É **metadado**, mesmo tendo "cara" de registro. Por isso vai no deploy como XML (`Config_Frete.SP.md-meta.xml`) e é gravado nas **tabelas de metadados**, não nas de dados.
- Na execução, fica **em cache** com os outros metadados. Consequências práticas:
  - Ler com SOQL **não conta** no limite de 100 queries.
  - **Não dá para alterar com DML comum** no Apex. Só por deploy (inclusive via Apex, com `Metadata.Operations`, de forma assíncrona).
- **Analogia:** é um arquivo de configuração versionado, não uma tabela de domínio.

### 2. Um registro de Account
- É **dado puro**. Nunca vira XML de metadado e não vai no deploy.
- Fluxo ao salvar pela tela:
  1. O browser envia JSON para o servidor.
  2. O servidor busca no cache os metadados da bananinha: campos da Account, permissões do usuário, validation rules, triggers e flows ativos.
  3. Ele executa a **order of execution** (validações, triggers, flows...).
  4. Grava a linha no SDB com o OrgId da bananinha.
- Detalhe: o modelo de "tabela genérica com slots" vale principalmente para **objetos custom**. Objetos standard como Account provavelmente têm estrutura física própria e otimizada, com os campos custom que você cria neles indo para slots. Isso não é documentado em detalhe, então trate como provável, não como certo.

### 3. Um Record-Triggered Flow em Contact
- A **definição** do flow é metadado. Vai como `.flow-meta.xml` no deploy, é gravada nas tabelas de metadados e fica em cache, já pronta para executar.
- A **execução** acontece quando alguém salva um Contact:
  1. O servidor começa a transação do Contact.
  2. Na order of execution, consulta o cache: *"quais flows ativos a bananinha tem para Contact, nesse evento?"*
  3. Executa o flow **na mesma transação**. Ele divide os governor limits com triggers e outras automações.
  4. Faz o commit de tudo junto, ou dá rollback de tudo se algo falhar.

## Resumo

| Caso | Tipo | Viaja como XML? | Onde fica | Como é usado |
|---|---|---|---|---|
| Custom Metadata | Metadado | Sim | Tabelas de metadados + cache | Leitura rápida, sem gastar limite |
| Account | Dado | Não | Tabelas de dados | CRUD via tela, APIs, SOQL/DML |
| Flow em Contact | Metadado (definição) | Sim | Tabelas de metadados + cache | Dispara ao salvar um Contact |

**Frase para a conversa:** *"O projeto é a planta da casa. O deploy constrói a casa. Depois disso, ninguém mais consulta a planta: a org vive dos metadados gravados no banco."*

**(O parênteses continua aberto.)** Esse cenário da bananinha daria um ótimo exemplo prático no bloco 2 do Google Doc. Quer que eu inclua junto na atualização quando fecharmos?

Fechado! Antes do parênteses, a conversa estava assim:

1. Você perguntou se o banco interno da Salesforce é **Oracle**, porque seu ex tech lead tinha dito isso. Falamos da linha do tempo e de por que o Apex parecido com Java não tem relação com o banco.
2. Na mesma mensagem em que abriu o parênteses, você perguntou se, **quando rodava em Oracle, era na nuvem da Oracle**. Essa já respondi: não, era Oracle licenciado rodando nos data centers próprios da Salesforce.

Esse assunto ficou encerrado. A pesquisa feita dentro do parênteses até completou a história: o core hoje roda no SalesforceDB, um banco baseado em PostgreSQL.

O que ficou **pendente** de antes é a **atualização do bloco 2 do Google Doc**, que você não chegou a confirmar. Pelo que conversamos, eu incluiria:
- **Correção do runtime engine:** a org é montada no servidor a partir de tabelas e cache, e o XML é só o formato de troca no deploy e no retrieve.
- **Metadados em tabelas:** o dicionário de metadados e a tabela genérica com slots, para explicar por que não existe `ALTER TABLE`.
- **CRUD de metadados vs CRUD de dados:** a tabela de quem usa XML e quem não usa.
- **O cenário da org bananinha:** Custom Metadata, Account e Flow em Contact, com a frase "a planta da casa".
- **Curiosidade opcional:** o SDB (PostgreSQL, storage em nuvem, células da Hyperforce), com as fontes.

