# Ponto de retomada

Situação em 2026-11-08, após o lote 3d (pendências de Agentforce Sales e Service fechadas) e a projeção do site (`gerado/site/`, contrato 1.0.0). Os números vivos estão em `relatorios/cobertura.md`; o detalhe do que foi resolvido está em `relatorios/resolucao-bloqueios.md`.

## O que está pronto

- **Pipeline executável e validado:** 0 erros e 24 testes passando. O validador também exige que todo nome de propriedade ou campo apareça na nota de extração da fonte citada.
- **Escopo e versão:** fixados em `config/` (API 68.0, Winter '27).
- **Universo de metadata types:** 993 tipos da v68, a partir de snapshots oficiais com hash.
- **Taxonomia proposta:** 14 classificações e 92 subclassificações, ainda sem cruzamento com a documentação oficial.
- **Catálogo do piloto:**
  - 31 funcionalidades (as sem objeto ou metadata type lido declaram a ausência como `desconhecido`);
  - 36 metadata types e 64 estruturas;
  - 60 objetos API;
  - 90 relacionamentos.
- **Caminhos de Setup:** verificados em 20 das 31 funcionalidades (lista das 11 restantes na tabela de lacunas).
- **Data 360:** contexto técnico verificado.
- **Agentforce Sales e Agentforce Service** (antes Sales Cloud e Service Cloud): nome, contexto técnico e licenças verificados. Vendas tem 10 funcionalidades próprias e atendimento, 3; Knowledge, regras de atribuição, horário comercial, apps de console e Path entram como capacidades compartilhadas. O relatório de pesquisa usado como mapa está em `fontes/pesquisas/`.

Os JSONs de `catalogo/` são a fonte da verdade. Os lotes 1 a 5k foram aplicados por scripts de carga, hoje guardados como registro em `ferramentas/carga/historico/`. Edições futuras devem ser feitas nos JSONs ou com a biblioteca `ferramentas/carga/`.

## Acompanhamento no GitHub

Os lotes e o site são acompanhados por issues em millena84/sf-tutor (milestones "MVP do site" e "v2"). Este arquivo continua sendo a fonte do detalhe técnico; cada issue aponta para a seção correspondente. O site é publicado em millena84/tutorial-sf-grafo (GitHub Pages), só com autorização.

## Projeção para o site

`gerado/site/` é gerada por `sftutor.py gerar` com contrato versionado (`manifest.json`, schema em `schemas/site-manifest.schema.json`, testes em `testes/test_insumos.py`). O app em `apps/sf-tutor/` copia essa pasta no build; a cópia é gerada, nunca editada.

**Estado do app (2026-11-08):** MVP local pronto para revisão, ainda sem commit e sem publicação.
- Comandos e arquitetura: `apps/sf-tutor/NOTA-ARQUITETURA.md`.
- `npm run verificar` passa: build com validação da base, lint, 28 testes unitários, 25 E2E (desktop e 360px) e performance (dados reais e fixture sintética).
- Pendências visuais: logo oficial (hoje placeholder identificado) e inspeção da referência flavinho.pages.dev (bloqueada para acesso automatizado).
- Publicação: PR #1 em millena84/tutorial-sf-grafo com o build em `docs/`. Depois do merge, ative o Pages manualmente (Settings → Pages → Deploy from a branch → `main` / `/docs`); a API de Pages não é acessível nas sessões do Claude.
- Evolução: issues #13 a #20 (logo, referência visual, publicação automática, CI, rótulos, arraste, acessibilidade, avisos do validador).

## Lacunas por item

| Item | Situação | Lacuna concreta |
|---|---|---|
| mdt:PermissionSet, PermissionSetGroup, ValidationRule, PathAssistant | estrutural completa | Mapeamento campo a campo XML↔API pendente; grafias a conferir no WSDL |
| mdt:Profile | parcial | 6 subtipos não servidos pela documentação (ProfileUserPermission, ProfileServicePresenceStatusAccess, LoginFlow, ProfileAgentAccess, ProfileActionOverride, ProfileLoginHours) |
| mdt:CustomObject | parcial | Subtipos (ActionOverride, BusinessProcess, ListView, SearchLayouts…), vários deles metadata types próprios |
| mdt:CustomField | parcial | CustomValue (parcial) e ValueSettings |
| mdt:RecordType | parcial | PicklistValue |
| mdt:Flow | parcial | Subtipos Flow*; 37 propriedades sem explicação |
| mdt:FlexiPage, QuickAction, CustomTab | parcial | Subtipos; falta exemplo XML de FlexiPage |
| obj:User | parcial | 25 nomes da Field Reference não capturados; tipos e propriedades de API dos campos vindos só da Field Reference |
| Exposições Tooling de Profile, PermissionSet, PSG, PSA, User, RecordType | exposição verificada | Campos e operações da exposição Tooling |
| obj:UserLogin (Tooling) | indeterminado | Fora do trecho servido do índice |
| obj:EntityDefinition, FieldDefinition | parcial | Recortes de 13 de 64 e de 12 de 56 campos |
| Setup de 11 funcionalidades | desconhecido | Perfis, tipos de registro, contas, contatos, leads, oportunidades, casos, campanhas, produtos e catálogos de preço, previsões colaborativas, equipes de conta e de oportunidade |
| Licenças de Core | desconhecido | Não registradas |
| Licenças de Sales e Service | parcial | Licença de usuário e feature license registradas; matriz completa de edições pendente |
| obj:Lead | parcial | 74 nomes lidos; tipos e propriedades só de 14 campos |
| obj:Opportunity, obj:Case | parcial | Object Reference truncada; propriedades de API faltam para campos vindos só da Field Reference |
| obj:Account, obj:Contact | parcial | Tabela de conta pessoal (Account) e tabela de Contact servidas truncadas |
| Objetos parciais de Sales e Service | parcial | Contact, Campaign, Product2, Quote, AgentWork, KnowledgeArticleVersion (páginas truncadas); QueueRoutingConfig e Entitlement (linha sem nome); Knowledge__kav sem página própria |
| mdt:KnowledgeSettings, ForecastingSettings | parcial | Subtipos lidos (nota de extração), ainda não cadastrados como estruturas |
| mdt:PresenceUserConfig | parcial | Tabela com uma linha vazia |
| mdt:EntitlementProcess | parcial | WorkflowActionReference sem estrutura detalhada |

## Bloqueios reais

1. **Teste em org.** Não há org disponível; nenhuma execução foi simulada.
2. **Limite de tamanho do endpoint de documentação** (cerca de 54 a 112 mil caracteres por página). Contornável por:
   - liberação de rede para baixar o HTML completo;
   - os PDFs versionados;
   - o `metadata.wsdl`, para as propriedades.

O WSDL **não** é bloqueio: a documentação de cada tipo é a fonte alternativa prevista no prompt.
3. **Logos da Salesforce e das nuvens:** os termos de uso exigem permissão escrita, e o ambiente não baixa do portal de marca. Detalhes e caminhos em `relatorios/logos-salesforce-2026-11-08.md`.

**Integração, APIs e eventos (issue #24), em andamento.** Ver `relatorios/auditoria-integracao-2026-11-08.md`.
- **Lote 5a (2026-11-09):** 9 funcionalidades, 11 metadata types e 7 estruturas, com 6 referências por nome entre componentes.
  - Funcionalidades: named credentials, sites remotos, CSP, CORS, eventos de plataforma, Change Data Capture, External Services, objetos externos e auth providers.
  - Metadata types: NamedCredential, ExternalCredential, RemoteSiteSetting, CspTrustedSite, CorsWhitelistOrigin, PlatformEventChannel, PlatformEventChannelMember, PlatformEventSubscriberConfig, ExternalServiceRegistration, ExternalDataSource e AuthProvider.
  - Extração: `fontes/extracoes/mdapi-lote5a.txt`.
  - Novo no schema: propriedade com `referencia.alvos` para referência pelo nome do componente no XML.
- **Lote 5b (2026-11-09):** 3 funcionalidades, 11 metadata types e 12 estruturas, com 9 referências por nome (inclusive ConnectedApp → PermissionSet e Profile).
  - Funcionalidades: connected apps, external client apps e OAuth (escopos customizados, troca de token e fluxos).
  - Metadata types: ConnectedApp, ConnectedAppSettings, ExternalClientApplication, ExtlClntAppOauthSettings, ExtlClntAppGlobalOauthSettings, ExtlClntAppOauthConfigurablePolicies, ExtlClntAppConfigurablePolicies, ExternalClientAppSettings, OauthCustomScope, OauthTokenExchangeHandler e OauthOidcSettings.
  - Extração: `fontes/extracoes/mdapi-lote5b.txt`.
  - **ConnectedApp está parcial:** ConnectedAppOauthIdToken, ConnectedAppOauthPolicy, ConnectedAppSamlConfig, ConnectedAppSessionPolicy e ConnectedAppMobileDetailConfig não foram extraídos. O conteúdo servido veio truncado e a página renderizada não mostra os nomes dos campos.
  - A página de ExtlClntAppOauthSecuritySettings não foi encontrada (meta_extlclntappoauthsecuritysettings.htm devolveu binário).
- **Lote 5c (2026-11-09):** 5 funcionalidades novas, 8 metadata types e 2 estruturas, com 4 referências por nome.
  - Funcionalidades novas: certificados e chaves, login único por SAML, conexões de rede privadas de saída, serviços externos registrados (Commerce) e Event Relay.
  - Funcionalidades ampliadas: named credentials (ExternalAuthIdentityProvider), eventos de plataforma e Change Data Capture (ManagedEventSubscription e PlatformEventSettings).
  - Metadata types: Certificate, SamlSsoConfig, ExternalAuthIdentityProvider, OutboundNetworkConnection, RegisteredExternalService, EventRelayConfig, ManagedEventSubscription e PlatformEventSettings.
  - Referências: ExternalCredentialParameter.externalAuthIdentityProvider, NamedCredentialParameter.outboundNetworkConnection, EventRelayConfig.destinationResourceName (→ NamedCredential) e EventRelayConfig.eventChannel (→ PlatformEventChannel).
  - Extração: `fontes/extracoes/mdapi-lote5c.txt`.
  - **Não ligados de propósito:** campos `certificate`/`decryptionCertificate` e o legado NamedCredential.outboundNetworkConnection. As notas extraídas não dizem que o valor é o nome de um componente Certificate; ficam para conferência.
  - **McpServerDefinition e ApiNamedQuery:** sem página de referência da Metadata API (as URLs devolveram binário). Não catalogados.
- **Lote 5d (2026-11-09): contratos, limites e tratamento de falhas (INT-07).** A sub-classificação estava vazia; agora tem 3 funcionalidades próprias e 3 secundárias.
  - Funcionalidades: limites de API e alocações, versões de API e ciclo de vida, reprocessamento e monitoramento de eventos.
  - Objetos API (completos): EventBusSubscriber (12 campos) e PlatformEventUsageMetric (10 campos).
  - Secundárias em INT-07: External Services, Event Relay e eventos de plataforma.
  - Limites e versões **não têm metadata type**: ficam com ausência registrada, recurso REST em `representacoes.codigo` e, no caso dos limites, caminho de Setup verificado.
  - O nome Private Connect foi confirmado no recurso /limits e entrou como alias de conexões de rede privadas.
  - O painel do site passou a mostrar `representacoes.codigo` e `representacoes.interface`.
  - Extração: `fontes/extracoes/lote5d-contratos-limites.txt`.
- **Lote 5e (2026-11-09): INT-07, segunda parte.** 3 funcionalidades novas.
  - Limites e falhas de callouts (principal INT-07): 100 por transação, timeouts e operações pendentes.
  - Bulk API 2.0 e Bulk API (principal APIs de dados e metadados; secundária INT-07): a primeira API catalogada como funcionalidade nessa sub-classificação.
  - Pub/Sub API (principal eventos e mensageria; secundária INT-07): ligada a ManagedEventSubscription e PlatformEventUsageMetric.
  - As páginas da Pub/Sub API não têm versão; o registro diz isso.
  - Extração: `fontes/extracoes/lote5e-int07.txt`.
  - Ainda fora: relação geral entre a versão de API e os componentes (`apiVersion`).
- **Lote 5f (2026-11-09): APIs de dados e metadados.** 4 funcionalidades: REST API (com Composite), SOAP API, Metadata API e Tooling API.
  - Nenhuma tem metadata type: a ausência está registrada como `nao_aplicavel`, com fonte.
  - Metadata API e Tooling API também aparecem em desenvolvimento, testes e entrega, como classificação secundária.
  - Não obtidos: os limites da Metadata API e a página geral de recursos compostos (as URLs devolveram binário).
  - Extração: `fontes/extracoes/lote5f-apis.txt`.
- **Lote 5g (2026-11-09):** 12 metadata types, 6 estruturas e 8 referências por nome.
  - Certificados: PublicKeyCertificate, PublicKeyCertificateSet, UserAuthCertificate e InboundCertificate.
  - Rede: InboundNetworkConnection; conexões de rede privadas passam a cobrir entrada e saída.
  - Plugins de external client app: mobile (configurações e políticas), push (configurações e políticas), canvas, notificação e políticas SAML.
  - Não obtidos (as URLs devolveram binário): ExtlClntAppAttestSettings, ExtlClntAppAttestConfigurablePolicies e ExtlClntAppOauthSecuritySettings.
  - Extração: `fontes/extracoes/mdapi-lote5g.txt`.
- **Lote 5h (2026-11-09): ConnectedApp completo e definição de __e/__x.**
  - Lendo a página de ConnectedApp em partes, saíram 4 estruturas: ConnectedAppOauthIdToken, ConnectedAppOauthPolicy, ConnectedAppSamlConfig e ConnectedAppSessionPolicy. Com isso, ConnectedApp e ConnectedAppOauthConfig ficaram com cobertura estrutural completa.
  - A atualização da extração foi anexada a `mdapi-lote5b.txt`. O `lote5b.py` foi atualizado e roda de novo antes do `lote5g.py`.
  - ConnectedAppMobileDetailConfig não tem tabela na página (só o elemento `mobileAppConfig` no exemplo XML): continua fora do catálogo.
  - Referências novas: ConnectedAppSamlConfig.encryptionCertificate → Certificate e CustomObject.externalDataSource → ExternalDataSource. A página diz "nome" nos dois casos.
  - Eventos de plataforma e objetos externos passam a apontar CustomObject como a definição do `__e` e do `__x`.
  - Attest de external client app e ExtlClntAppOauthSecuritySettings seguem sem página legível (o atlas também falhou).
- **Lote 5i (2026-11-09): caminhos de Setup da integração.** 19 das 20 funcionalidades que estavam `desconhecido` agora têm caminho verificado na Ajuda ou nos guias oficiais (21 fontes novas, extração em `help-setup-integracao.txt`).
  - Segue `desconhecido`: serviços externos registrados (Commerce). A fonte descreve o registro só por API.
  - Parciais, com nota: conexões privadas (só a saída), escopos OAuth (só a atribuição) e Bulk API (tela de acompanhamento, não de configuração).
- **Lote 5j (2026-11-09): objetos API de integração.** 6 objetos com tabela de campos completa (contagem conferida em segunda leitura): NamedCredential (16), ConnectedApplication (15), AuthProvider (30), OauthToken (9), ExternalDataSource (13) e CspTrustedSite (16).
  - Lookups: NamedCredential e ExternalDataSource → AuthProvider; ExternalDataSource → NamedCredential; OauthToken → User.
  - Representações comuns XML↔API: NamedCredential, ConnectedApp↔ConnectedApplication, AuthProvider, ExternalDataSource e CspTrustedSite. Entraram como "correspondência transformada" e foram corrigidas no lote 5k.
  - A exposição na Tooling API ficou `desconhecido`: a lista da Tooling lida na sessão de 2026-11-07 não chega a esses nomes.
  - Extração: `fontes/extracoes/lote5j-objetos-integracao.txt`.
- **Lote 5k (2026-11-09): versão de API e correção do 5j.**
  - Correção: os 5 pares XML↔API do lote 5j viraram `representacao_comum`. "Correspondência transformada" exige prova de campo (como o campo Metadata tipado), e ela não existia. Novo teste em `test_insumos.py` protege a convenção.
  - Versão de API: a única propriedade `apiVersion` do catálogo é mdt:Flow.apiVersion. Ganhou nota apontando o ciclo de vida das versões. O schema não tem relação entre funcionalidade e propriedade, então a ligação ficou só no texto, registrada como limitação.
- **Falta (depois da série 5):**
  - ConnectedAppMobileDetailConfig (sem tabela na página); attest de external client app e ExtlClntAppOauthSecuritySettings (sem página legível).
  - McpServerDefinition e ApiNamedQuery, quando houver fonte.
  - Conectores de dados (DataConnector*, DataStream*, ExternalDataConnector etc.). Pelos nomes, parecem ser do Data 360: antes de catalogar, decidir se entram na visão Platform/Core ou numa nuvem própria.
  - Outros objetos API do tema (por exemplo, external credentials, configuração SAML, event relay e assinantes), se houver página na Object Reference.
  - Limites da Metadata API (página não legível). Relação funcionalidade↔propriedade: exigiria estender o schema; está como decisão pendente.
  - Exemplos XML.
  - Caminhos de Setup restantes: criação de escopo OAuth customizado e de handler de troca de token; conexão de entrada do Private Connect.

## Ferramentas de carga (issue #11, 2026-11-09)
- Lotes novos usam a biblioteca `ferramentas/carga/` (uso em `ferramentas/README.md`). Ela não depende de nada fora do repositório.
- Os scripts originais dos lotes 1 a 5k estão em `ferramentas/carga/historico/`, só como registro: não reexecute sobre o catálogo atual.
- **Equivalência conferida:** os lotes 5c (metadata types e estruturas) e 5j (objetos API) foram rodados com a biblioteca numa cópia da base e geraram arquivos idênticos byte a byte aos do catálogo.
- O teste `TestCargaNova` carrega um lote de exemplo numa cópia temporária e valida.

## Avisos do validador (issue #20, 2026-11-09)
- De 69 para 3 avisos.
- **64 metadata types** ganharam esqueleto XML comentado, gerado por `ferramentas/exemplos_xml.py` só com propriedades catalogadas:
  - obrigatórios ativos;
  - condicionais comentados;
  - valores documentados, ou textos entre colchetes dizendo o que preencher.
  - Natureza `didatico_projeto`, com nota de que não é arquivo pronto para implantação.
- **Fontes sem uso removidas do registro:** `src:mdapi-types-list` (índice de tipos, sem afirmação que dependa dele) e `src:rest-sobject-describe` (nunca relida). As duas continuam citadas em `tarefas/00-especificacao-grafo.md`.
- **AssignmentRules, BusinessHoursSettings e EscalationRules:** as estruturas já estavam catalogadas; o gerador é que não tratava tipos sem propriedade obrigatória e só com estruturas. Os três ganharam exemplos escritos à mão (`ferramentas/carga/lotes/exemplos_regras_e_horarios.py`), com regra, entrada, critério e ação. **O validador termina com 0 avisos.**
- O gerador também foi corrigido: `fullName` dentro de estruturas é elemento real (o nome de cada regra), e, sem obrigatórios, a amostra mostra a primeira estrutura. A opção `--regerar` refaz só esqueletos gerados por ele.

## "Sobre este tema" (issue #34, 2026-11-09)
- **Divergência registrada (tradução didática):** a especificação (`tarefas/00-especificacao-grafo.md`) chama os dois níveis de classificação e subclassificação. O site mostra os dois como **"Tema"**, por decisão da autora (opção B). Os nomes nos dados, no schema e no validador não mudam.
- **Fase 1 (tela):** "Sobre este tema" em três camadas fixas:
  1. Para quem está começando;
  2. Para quem já conhece Salesforce (contagens derivadas do grafo);
  3. Nível avançado, recolhido.
- **Fase 2 (dados):** os 106 temas têm `escopo` (o que entra) e `fora_do_escopo` (o que fica fora e em qual tema procurar).
  - Os dois campos são obrigatórios nos schemas de classificação e subclassificação.
  - São redação do projeto: delimitam o recorte e não afirmam fatos técnicos. Script: `ferramentas/carga/lotes/escopo_temas.py`.
- **Fase 3 (referências oficiais):** os 14 temas de primeiro nível têm referências à documentação oficial, com 11 fontes novas. Nota de extração: `fontes/extracoes/temas-referencias-oficiais.txt`.
  - Cada referência começa dizendo como corresponde ao tema: "Cobre o tema", "Cobre parte do tema" ou "Mais ampla que o tema". O validador recusa referência sem isso.
  - O estado continua `desconhecido` e o site mostra "Parcialmente conferido". Tema `verificado` sem referência é erro.
  - Os temas internos (subclassificações) ainda não têm referência própria. O site aponta para as referências do tema de cima.
- **Camada de certificações (pedida pela autora): bloqueada.**
  - As páginas de credencial e as trilhas de preparação do Trailhead não trazem o roteiro da prova na leitura automática (conteúdo renderizado por JavaScript).
  - O guia oficial da prova e a Trailhead Academy precisam de aprovação de acesso.
  - Nada foi registrado a partir de sites de terceiros.
  - Para retomar: aprovar o acesso a trailhead.salesforce.com/help e trailheadacademy.salesforce.com, ou anexar os PDFs dos guias.
  - Ao incluir esses domínios na lista de fontes, ajustar `DOMINIOS_FONTE` em `ferramentas/sftutor.py`.
- **Fase 4:** seletor de nível de leitura no site, adiado pela autora.
- **Conteúdo específico por tema (piloto, 2026-11-09):** feito depois do retorno da autora de que as camadas estavam genéricas.
  - **Parte automática:** o gerador grava em cada tema o campo calculado `derivado`, com:
    - funcionalidades, metadata types e objetos API;
    - suporte no Salesforce CLI, exposição por API e dependências entre componentes;
    - pré-requisitos, alertas e exemplos das funcionalidades.
  - O cabeçalho dos temas mostra o estado do recorte (campo `recorte` no grafo), não "Desconhecido".
  - Contrato do site: 1.2.0.
  - **Curado, com fontes:** os campos opcionais `para_iniciantes`, `encadeamento` e `avancado` (decisão, segurança, implantação, testes, limite, escala, ponto de atenção). Cada bloco exige evidências.
    - O validador confere se `por_onde_comecar` cita funcionalidades do próprio tema.
    - Piloto: `cls:interface-e-experiencia-do-usuario` e `sub:lightning-pages-e-componentes` (`ferramentas/carga/lotes/conteudo_temas.py`).
    - Fontes novas: o guia Building Forms (architect.salesforce.com, domínio incluído na lista de fontes), Field-Level Security (lida na versão 58.0: a página atual não exibiu o artigo) e Lightning Pages (Ajuda).
  - **Não incluído por falta de fonte legível:** opções de ativação de Lightning record pages, limite de componentes por página e orientação de desempenho.
- **Conteúdo curado em todos os temas principais e na maior parte dos internos (2026-11-09):**
  - Cobertura: os 14 temas principais e 70 dos 92 internos têm conteúdo curado. Scripts: `conteudo_cls.py` e `conteudo_sub.py`, aplicados por `conteudo_temas.py`.
  - Os textos recombinam fatos já catalogados nas funcionalidades e as notas de extração do #34, com as fontes citadas em cada bloco.
  - Uma fonte nova: `src:apex-queueable`, lida pelo resultado de busca.
  - **22 temas internos ficaram sem conteúdo curado, por falta de fonte lida** (lista `PENDENTES` em `conteudo_sub.py`):
    - Organização: parâmetros reutilizáveis, domínios e URLs, habilitação de recursos.
    - Dados: metadados de configuração de dados.
    - Qualidade: classificação e sensibilidade, retenção, consentimento.
    - Automação: notificações, mecanismos legados.
    - Interface: experiências web, portais e mobile.
    - Execução assíncrona: caminhos assíncronos.
    - Relatórios: tipos de relatório, pastas, métricas.
    - Conteúdo: colaboração, templates.
    - Observabilidade: logs.
    - IA: recuperação de conhecimento.
    - Produto: serviço de campo, experiências externas, capacidades setoriais, outras áreas.
  - Esses temas continuam com o texto genérico e o resumo calculado. Próximo: pesquisar fontes para eles e depois detalhar cada tema por seção, como pediu a autora.
- **Pendentes, lote 1 (2026-11-09):**
  - 7 dos 22 temas pendentes ganharam conteúdo: tipos de relatório, mecanismos legados e migração, notificações, logs e rastreamento, domínios e URLs, parâmetros reutilizáveis e caminhos assíncronos.
  - Fontes: 17 novas, lidas pelos resultados de busca restritos a help.salesforce.com e developer.salesforce.com. Nota de extração: `fontes/extracoes/temas-pendentes-lote1.txt`. Script: `conteudo_pendentes.py`.
  - Continuam pendentes 15:
    - habilitação de recursos;
    - metadados de configuração de dados;
    - classificação e sensibilidade;
    - retenção;
    - consentimento;
    - experiências web, portais e mobile;
    - pastas e acesso;
    - métricas;
    - colaboração;
    - templates;
    - recuperação de conhecimento;
    - serviço de campo;
    - experiências externas;
    - capacidades setoriais;
    - outras áreas.
- **Pendentes, lotes 2 a 4 (2026-11-10):** os 15 restantes ganharam conteúdo; a lista `PENDENTES` ficou vazia e os 106 temas têm conteúdo curado.
  - Lote 2 (Qualidade e Relatórios, 5 temas): 21 fontes, `temas-pendentes-lote2.txt`, `conteudo_pendentes2.py` (PR #52).
  - Lote 3 (Conteúdo, IA, Interface, Organização e Dados, 6 temas): 28 fontes, `temas-pendentes-lote3.txt`, `conteudo_pendentes3.py` (PR #53).
  - Lote 4 (Produto, 4 temas): 16 fontes, `temas-pendentes-lote4.txt`, `conteudo_pendentes4.py`.
  - Todas as fontes foram lidas pelos resultados de busca restritos a help.salesforce.com e developer.salesforce.com (`leitura_resultado_busca`).
  - "Outras áreas" é um agrupamento do projeto: tem só as camadas para iniciantes e encadeamento, apoiadas em `src:sdr-metadata-support`, sem nível avançado.
  - Os temas seguem com `estado: desconhecido`; a fronteira do recorte não foi cruzada com a documentação oficial.
  - Próximo no #34: detalhar seção por seção os 13 temas principais (Relatórios, IA e Conteúdo primeiro). A camada de certificações continua bloqueada por acesso.
- **Detalhamento dos temas principais (item 3 do #34, a partir de 2026-11-10):**
  - Ordem definida pela autora: 1) Integração, 2) Acesso e segurança, 3) Dados e modelagem, 4) Qualidade e governança, 5) Relatórios, 6) Org e configurações, 7) Processos de produto, 8) Automação, 9) Desenvolvimento, 10) Assíncrono e lotes, 11) Interface, 12) Observabilidade, 13) Conteúdo, 14) IA e agentes.
  - Leitura adotada para "seção por seção": cada tema interno é uma seção. O encadeamento vira um roteiro numerado pelos temas internos, e o avançado ganha ao menos um item por seção, na mesma ordem. Só texto: sem cadastro novo no catálogo e sem preencher `prerequisitos` (pontos deixados em aberto com a autora).
  - Cada passada também limpa o dado genérico dos temas internos (`temas_internos.py`): descrição curta escrita pelo projeto, referências oficiais já registradas (o site passa de "Curadoria do projeto" para "Parcialmente conferido") e a mesma nota de estado dos temas principais. O estado continua `desconhecido`.
  - Concluído: Integração, texto (PR #55) e limpeza dos 7 temas internos.
  - Concluído: Acesso e segurança, texto e limpeza dos 7 temas internos (avançado de 5 para 12 itens, sem fonte nova).
  - Concluído: Dados e modelagem, texto e limpeza dos 7 temas internos (avançado de 4 para 11 itens, sem fonte nova).
  - Concluído: Qualidade e governança, texto e limpeza dos 6 temas internos (avançado de 2 para 10 itens). 15 fontes novas (`temas-detalhe-qualidade.txt`, `conteudo_detalhe.py`): Duplicidade ganhou conteúdo completo; Validação e Rastreabilidade ganharam nível avançado. DuplicateRule e MatchingRules constam do inventário mas não estão no catálogo.
  - Concluído: Relatórios, texto e limpeza dos 6 temas internos (avançado de 1 para 8 itens). 17 fontes novas (`temas-detalhe-relatorios.txt`): Reports, Dashboards e Recursos analíticos de produto ganharam conteúdo completo. Report, Dashboard, ReportType, ReportFolder, DashboardFolder, WaveDashboard e WaveDataset constam do inventário mas não estão no catálogo.
  - Decisão de 2026-11-14 (aprovada pela autora): a partir de Org e configurações, cada tema é detalhado **com o cadastro dos metadata types dele no catálogo**, na mesma rodada do texto.
  - Decisão de 2026-11-14 (site, PR #64): metadata type e objeto API passam a ser o último nó do mapa; propriedades XML, campos e estruturas abrem numa tabela em janela (parâmetros `t` e `f` na URL). Ver `apps/sf-tutor/NOTA-ARQUITETURA.md`, seção "Último nó do mapa".
  - Concluído: Org e configurações, texto, limpeza dos 8 temas internos e catálogo (lote 6a, `ferramentas/carga/lotes/lote6a_org.py`).
    - Texto: avançado do tema de 3 para 9 itens; 7 temas internos reescritos em `conteudo_detalhe.py` (Identificação, Localização e Moedas não tinham nível avançado). 30 fontes de Ajuda novas (`temas-detalhe-org.txt`, leitura por resultado de busca).
    - Catálogo: 6 metadata types (CompanySettings, CurrencySettings, LanguageSettings, MyDomainSettings, CustomMetadata, CustomLabels), 4 estruturas (FiscalYearSettings, Currency, CustomMetadataValue, CustomLabel) e 9 funcionalidades (informações da empresa, idiomas da org, Translation Workbench, custom labels, múltiplas moedas, ano fiscal, feriados, My Domain, custom metadata types). Nota: `mdapi-lote6a-org.txt`.
    - Endereço da documentação: as páginas `atlas.en-us.264.0.api_meta` hoje devolvem só um índice em PDF. O padrão que funciona é `https://developer.salesforce.com/docs/platform/api-metadata/references/meta-types/metadata-<tipo em minúsculas>.html` (sem versão na URL; o artigo fica nos primeiros 100 mil caracteres, o resto é índice de navegação, conferido em MyDomainSettings).
    - Pendências deste tema: (1) **Translations** não foi cadastrado, porque a leitura não devolveu com segurança o nome de cada elemento; CustomObjectTranslation, GlobalValueSetTranslation e StandardValueSetTranslation também constam do inventário e não foram lidos. (2) CustomLabel não consta do inventário v68 e ficou como estrutura, embora a página o trate como metadata type. (3) Objetos API do tema (por exemplo Organization, CurrencyType, DatedConversionRate, FiscalYearSettings, Holiday) não foram investigados. (4) O vínculo entre custom metadata types e CustomObject não foi lido. (5) Não se confirmou qual metadata type guarda os dados da página Company Information fora o ano fiscal. (6) As funcionalidades novas não foram ligadas a nuvens (nuvens × funcionalidades fica por último). (7) 'Settings' e 'Habilitação de recursos' seguem sem funcionalidade própria, por serem transversais.
    - Divergências documentais registradas: seções FiscalYearSetting/FiscalYearSettings em CompanySettings; obrigatoriedade de conversionRate em CurrencySettings; fullName em CustomLabels.
  - Concluído: Processos de produto, texto, limpeza dos 7 temas internos e catálogo (lote 6b, `ferramentas/carga/lotes/lote6b_processos.py`).
    - Texto: roteiro pelas 7 seções; avançado do tema de 5 para 12 itens. Receita e comércio ganhou conteúdo completo (não tinha nível avançado); Vendas, Atendimento, Serviço de campo e Experiências externas ganharam itens novos, editados no lugar (`conteudo_sub.py`, `conteudo_pendentes4.py`). 20 fontes de Ajuda novas (`temas-detalhe-processos.txt`).
    - Catálogo: 6 metadata types (LeadConfigSettings, ProductSettings, OrderSettings, ContractSettings, FieldServiceSettings, CommunitiesSettings), 1 estrutura (ObjectMappingItem) e 4 funcionalidades novas (pedidos, contratos, Field Service, Digital Experiences); Leads e Produtos e catálogos de preço ampliadas. Nota: `mdapi-lote6b-processos.txt`.
    - Texto genérico corrigido: os 9 Settings com "Configurações de X da org." (Account, Campaign, Entitlement, Forecasting, Knowledge, OmniChannel, Opportunity, Quote, Territory2) ganharam descrição do que guardam, escrita a partir das propriedades já catalogadas.
    - Pendências deste tema: (1) **CaseSettings** não foi cadastrado: em duas leituras, a página devolveu tipo e descrição de 69 campos, mas não os nomes dos elementos. Mesma causa provável de Translations; tentar outro caminho de leitura (WSDL, PDF versionado ou a página no navegador). (2) A página de RevenueManagementSettings devolveu erro do site. (3) FieldServiceSettings: nome-base do arquivo não informado na página; 14 de 54 campos sem descrição. ContractSettings: 4 de 6 campos sem descrição. (4) Objetos API de pedidos, contratos, Field Service e sites não investigados. (5) Capacidades setoriais e Outras áreas seguem sem funcionalidade; IndustriesSettings e Network não foram lidos. (6) Funcionalidades novas não ligadas a nuvens.
  - Faltam, na ordem: Automação, Desenvolvimento, Assíncrono e lotes, Interface, Observabilidade, Conteúdo, IA e agentes.
  - Achado para a camada de certificações: o guia de prova "Salesforce Certified Platform Administrator Exam Guide" apareceu como artigo em help.salesforce.com (id=005298966), domínio já aceito. Não foi lido nem usado; conferir se os demais guias também estão lá.

## Próximos lotes

1. **Lote 3 — fechar as lacunas da tabela acima** que dependem só de documentação:
   - páginas próprias de ActionOverride, BusinessProcess, ListView etc.;
   - campos Tooling das exposições já confirmadas;
   - Setup de Perfis e de Tipos de registro na Ajuda.
2. **Lote 4 — classificação Core** dos 981 tipos pendentes, em famílias, sempre com a página do tipo como evidência.
3. **Lotes 5+ — uma classificação por vez.** Ordem: Acesso, Dados, Automação, Interface, Desenvolvimento, Organização (família Settings).
4. **Revisões transversais:**
   - cruzar a taxonomia com a documentação oficial;
   - cadastrar as estruturas de KnowledgeSettings e ForecastingSettings (as linhas já estão em `fontes/extracoes/mdapi-lote3d.txt`);
   - matriz de licenças e edições.

## Prompt de retomada

```text
Você está no repositório sf-tutor, pasta ai-help/claude/insumos-grafo/.
Leia CLAUDE.md, README.md, relatorios/retomada.md, relatorios/resolucao-bloqueios.md e
relatorios/cobertura.md desta pasta, e ../tarefas/00-especificacao-grafo.md e
../tarefas/01-prompt-criar-insumos.md.
Rode `python3 ferramentas/sftutor.py tudo` e `python3 -m unittest discover -s testes`
e confirme 0 erros antes de mudar algo.
Execute o próximo lote pendente de relatorios/retomada.md (comece pelo Lote 3):
- leia as páginas oficiais pelo endpoint versionado
  https://developer.salesforce.com/docs/get_document_content/<livro>/<pagina>.htm/en-us/264.0
  (atenção ao corte de ~54 a 112 mil caracteres; use offset e registre o que não foi servido)
  e a Ajuda (help.salesforce.com) por busca restrita ao domínio;
- registre cada fonte em fontes/registro.json e a nota em fontes/extracoes/
  (o validador exige que os nomes apareçam na nota);
- edite os JSONs de catalogo/ (fonte da verdade); nunca marque completo sem
  esperado == presente e estruturas detalhadas;
- ao terminar, rode `tudo` e os testes, atualize esta retomada e informe o que foi
  feito, validado, pendente e o próximo passo.
Se o usuário fornecer metadata.wsdl ou PDFs versionados, use-os antes para fechar as
lacunas de páginas truncadas.
Publicação: só com autorização. Fluxo autorizado: branch nova a partir da main
atualizada (confira antes se o PR anterior já foi mergeado), PR com "Closes #n" da
issue correspondente. Nunca push direto na main.
```
