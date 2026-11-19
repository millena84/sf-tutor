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
  - Concluído (2026-11-15): Automação, texto e funcionalidades (lote 6c, `ferramentas/carga/lotes/lote6c_automacao.py`).
    - Texto: roteiro pelas 6 seções; avançado do tema de 4 para 9 itens. Flow e orquestração de 2 para 7 itens; Decisões e aprovações ganhou nível avançado (6 itens); Ações e regras, Automação Apex, Notificações e Mecanismos legados ganharam itens. 32 fontes novas (`temas-detalhe-automacao.txt`, leitura por resultado de busca).
    - Funcionalidades: 6 novas (processos de aprovação, Flow Orchestration, regras de resposta automática, Apex triggers, notificações customizadas, Workflow Rules e Process Builder).
    - Tipos (lote 6d, `lote6d_automacao_tipos.py`, no mesmo dia, depois que a autora aprovou a leitura): 5 metadata types (ApprovalProcess, CustomNotificationType, AutoResponseRules, FlowSettings, ApexTrigger) e 13 estruturas, ligados às funcionalidades do lote 6c e a Flow. Nota: `mdapi-lote6d-automacao.txt`. A primeira passada tinha ficado sem tipos porque o WebFetch pediu aprovação e o pedido não foi respondido.
    - Pendências de Automação: (1) **Workflow** e filhos (WorkflowRule, WorkflowFieldUpdate, WorkflowAlert, WorkflowTask, WorkflowOutboundMessage) não foram cadastrados: a leitura devolveu tipo e descrição, mas não o nome de boa parte dos elementos. É o terceiro tipo com esse problema (Translations, CaseSettings, Workflow); vale tentar outro caminho de leitura (WSDL da Metadata API, PDF versionado ou a página aberta no navegador). (2) WorkflowActionReference (usado em ApprovalAction.action) e PackageVersion (ApexTrigger) não detalhados; por isso ApprovalProcess e ApexTrigger têm cobertura estrutural parcial. (3) Três enumerações de RuleEntry em AutoResponseRules sem valores no texto lido. (4) FlowDefinition, CustomNotificationType de Slack e ApexClass não lidos. (5) Caminho de Setup de processos de aprovação, Flow Orchestration e Workflow Rules não confirmado; o das regras de resposta automática de leads também não. (6) Representação de orquestrações na Metadata API não lida.
  - Correção de processo (2026-11-15): o Playwright serve `apps/sf-tutor/dist`. A ordem de validação do site é **build → lint → vitest → e2e → perf → build final** (ou `npm run verificar` seguido de `npm run build`). Nas rodadas de Org (#65) e Processos de produto (#66), os e2e rodaram antes do build, contra dados da rodada anterior. Refeito na ordem certa: a `main` com Org passou sem mudança; Processos tinha 1 teste e2e desatualizado e Automação outro, ambos por expectativa do teste (tema interno que deixou de estar "sem funcionalidade" ou "sem referências"), corrigidos nos próprios ramos.
  - Rodada B1 (2026-11-16): tipos destravados (lote 7a, `ferramentas/carga/lotes/lote7a_tipos_destravados.py`).
    - **Caminho de leitura:** o guia versionado 264.0 (endpoint `get_document_content`, o mesmo do prompt de retomada abaixo) devolve o nome dos campos que a referência nova (`docs/platform/api-metadata/references/meta-types/`) omitia. Os lotes 6a, 6b e 6d tinham usado a referência nova; a partir daqui, a leitura padrão volta a ser o guia versionado. Nota: `fontes/extracoes/mdapi-lote7a-versionado.txt`.
    - **Cadastrados:** CaseSettings (53 propriedades, 4 estruturas), Workflow (8) com 7 tipos filhos (WorkflowAlert, WorkflowFieldUpdate, WorkflowFlowAction, WorkflowKnowledgePublish, WorkflowOutboundMessage, WorkflowRule, WorkflowTask) e 4 estruturas, e Translations (33 propriedades, 58 estruturas). ApprovalProcess passou a cobertura estrutural completa, porque WorkflowActionReference agora existe.
    - **Ligações:** casos ← CaseSettings; workflow-rules-e-process-builder ← Workflow e os 7 filhos; translation-workbench e custom-labels ← Translations.
    - **Arquivos dos filhos de Workflow:** o registro do CLI não declara estratégia de decomposição para Workflow; os filhos foram cadastrados como elementos do arquivo `.workflow` do objeto. O registro também traz pasta e sufixo próprios de cada filho; quando são usados não foi verificado.
    - **Achado sobre os lotes 6a, 6b e 6d:** os campos que a referência nova lista sem descrição não constam do guia versionado 264.0. São 40 campos em 7 tipos (FieldServiceSettings 14, MyDomainSettings 3, ContractSettings 4, CommunitiesSettings 3, FlowSettings 5, ApprovalProcess 1, RuleEntry de AutoResponseRules 10). Foram mantidos, cada um com nota, disponibilidade `desconhecido` e divergência registrada no tipo. **Decisão pendente da autora:** manter com aviso ou remover do catálogo v68. A conferência comparou só a lista de nomes; tipo, obrigatoriedade e default dos demais campos desses tipos não foram reconferidos (exceção: allowedSubmitters de ApprovalProcess, que o guia versionado marca como Required).
    - **Não conferidos contra o guia versionado:** os outros tipos dos lotes 6a, 6b e 6d (CompanySettings, CurrencySettings, LanguageSettings, CustomMetadata, CustomLabels, LeadConfigSettings, ProductSettings, OrderSettings, CustomNotificationType, ApexTrigger).
    - **Pendências de B1:** (1) WorkflowSend consta do inventário como filho de Workflow, mas a página do guia versionado não o descreve; não cadastrado. (2) PicklistValueTranslation não é descrito na página de Translations; por isso Translations tem cobertura estrutural parcial. (3) FlowTextTemplateTranslation é descrito, mas nenhum campo da página o usa; ficou só na nota de extração. (4) A referência nova lista 69 campos em CaseSettings e 10 em Workflow; os campos a mais (17 e 2) não foram cadastrados. (5) AutoResponseRules: o guia versionado grafa `autoresponseRule` e `fullname`; a grafia não foi conferida no WSDL. (6) Caminho de Setup de CaseSettings, Workflow e Translations não levantado. (7) CustomObjectTranslation, GlobalValueSetTranslation e StandardValueSetTranslation não lidos. (8) Versão de entrada de cinco filhos de Workflow não informada na página.
  - Rodada A1 (2026-11-16): Desenvolvimento, testes e entrega (lote 7b, `ferramentas/carga/lotes/lote7b_desenvolvimento.py`).
    - **Tipos (guia versionado 264.0):** ApexClass, ApexPage, ApexComponent, StaticResource, LightningComponentBundle, AuraDefinitionBundle, ApexTestSuite, InstalledPackage, ApexSettings, DevHubSettings, SourceTrackingSettings e DeploymentSettings, com 5 estruturas (PackageVersion, Capabilities, LwcResource, LwcResources, Targets). ApexTrigger passou a cobertura estrutural completa (PackageVersion agora existe). Nota: `fontes/extracoes/mdapi-lote7b-desenvolvimento.txt`.
    - **Funcionalidades (14):** classes-apex, lightning-web-components, aura-components, visualforce, static-resources, testes-apex, testes-jest-de-lwc, pacotes-desbloqueados, pacotes-gerenciados, projeto-salesforce-dx, sandboxes, scratch-orgs-e-dev-hub, change-sets e devops-center. Ampliadas: metadata-api (DeploymentSettings) e apex-triggers (ApexSettings).
    - **Texto:** roteiro pelas 6 seções no tema principal, com 11 itens de nível avançado (eram 4); os 6 temas internos foram reescritos, com 5 a 8 itens cada, descrição própria e referências oficiais. 47 fontes novas, lidas pelo resultado de busca (`fontes/extracoes/temas-detalhe-desenvolvimento.txt`).
    - **Pendências de A1:** (1) Caminho de Setup não confirmado para classes Apex, LWC, Aura, Visualforce, static resources, sandboxes, pacotes gerenciados e DevOps Center. (2) LWC, Aura e Visualforce não foram ligados como tema secundário a Interface; fica para a rodada A3. (3) Valores de `target` de LWC, `AuraDefinitions` e a versão de entrada de LightningComponentBundle não constam do artigo versionado. (4) Limites de scratch orgs por edição do Dev Hub, quick deploy, pacotes gerenciados de primeira geração e AppExchange não lidos. (5) Objetos API do tema (por exemplo ApexClass e ApexTestResult na Tooling API, SandboxInfo) não investigados. (6) SandboxSettings consta do inventário e não foi lido. (7) Não foi lido se change sets têm metadata type. (8) Funcionalidades novas não ligadas a nuvens.
  - Rodada A2 (2026-11-16): Execução assíncrona, lotes e agendamento (lote 7c, `ferramentas/carga/lotes/lote7c_assincrono.py`).
    - **Objetos API (Object Reference versionada 264.0):** AsyncApexJob (13 campos), CronTrigger (10) e CronJobDetail (2), com dois relacionamentos. Nota: `fontes/extracoes/objref-lote7c-assincrono.txt`.
    - **Funcionalidades (5):** batch-apex, queueable-apex, future-methods, apex-agendado e monitoramento-de-jobs-apex. Flow ganhou os temas secundários agendamento e caminhos-assincronos; classes-apex ganhou AsyncApexJob.
    - **Texto:** roteiro pelas 7 seções no tema principal (8 itens avançados) e os 7 temas internos com descrição e referências. 15 fontes novas, lidas pelo resultado de busca (`fontes/extracoes/temas-detalhe-assincrono.txt`).
    - **Pendências de A2:** (1) Processamento orientado a eventos ficou só com o que já havia; triggers de platform event e a configuração do assinante não foram lidos de novo. (2) Caminho assíncrono e entrevistas pausadas de flow sem página própria lida. (3) Tabela completa de governor limits, Finalizers e Apex Cursors não lidos. (4) Exposição dos três objetos na Tooling API não verificada. (5) Objetos referenciados por AsyncApexJob.ParentJobId e CronTrigger.OwnerId não informados na página. (6) Caminho de Setup do atraso padrão de Queueable não confirmado.
  - Rodadas A3 e A4 (2026-11-16), num só PR: Interface e Observabilidade (lotes 7d e 7e), mais a correção da busca pedida pela autora.
    - **Busca por pasta e inventário inteiro (pedido da autora):** a busca do site não achava um metadata type pela pasta do projeto (por exemplo `applications`), e 871 dos 993 tipos do inventário v68 não apareciam de forma alguma. Agora: (a) todo metadata type com ficha leva a pasta, o sufixo e o nome de arquivo para a busca, e o resultado mostra "pasta X, sufixo .y"; (b) os tipos do inventário ainda sem ficha aparecem na busca, marcados como "ainda sem ficha", com pasta, sufixo e suporte no CLI, e não abrem nada. A origem é o registro do Salesforce CLI, via `inventarios/`. Código: `ferramentas/sftutor.py` (projeção do site), `apps/sf-tutor/src/model/busca.ts`, `src/ui/extras.ts`. Testes: `test_busca_cobre_o_inventario_inteiro_e_acha_por_pasta`, 5 testes de unidade e 1 e2e. Limite: 174 tipos do inventário não têm registro no CLI e, por isso, só são achados pelo nome.
    - **A3, tipos (guia versionado 264.0):** CustomApplication (23 propriedades, 15 estruturas), Layout (24, 25 estruturas; parcial por três enumerações não transcritas), CompactLayout, LightningExperienceTheme e BrandingSet. **Funcionalidades:** lightning-apps, page-layouts, compact-layouts, dynamic-forms e temas-e-branding; LWC, Aura e Visualforce passam a aparecer em Lightning pages e componentes.
    - **A4, objetos API:** SetupAuditTrail (6 campos) e EventLogFile (8). **Funcionalidades:** debug-logs, setup-audit-trail e event-monitoring; monitoramento-de-jobs-apex aparece também em Jobs, incidentes e diagnóstico.
    - **Texto:** novo mecanismo `ferramentas/carga/lotes/conteudo_extras.py`, que acrescenta itens ao conteúdo que o tema já tem, em vez de substituir. 40 itens avançados novos em 13 temas; 7 temas internos ganharam descrição e referências. 28 fontes novas, lidas pelo resultado de busca.
    - **Pendências:** (1) Interface: Tabs, Ações rápidas, Path e Experiências web sem texto novo nem referências; LightningExperienceSettings (que ativa o tema), AppMenu, HomePageLayout, CustomPageWebLink e ListView não lidos; caminho de Setup de page layouts não confirmado. (2) Observabilidade: Histórico de login e Limites e consumo sem referências novas; TraceFlag, DebugLevel e ApexLog (Tooling API), Field History Tracking, Transaction Security, Background Jobs e a lista de tipos de evento não lidos. (3) EventLogFile: Interval e Sequence são citados na página, mas não constam da tabela.
  - Rodadas A5 e A6 (2026-11-16), num só PR: Conteúdo, conhecimento e colaboração e IA, agentes e decisões assistidas (lote 7f, `ferramentas/carga/lotes/lote7f_conteudo_ia.py`).
    - **Tipos (guia versionado 264.0):** EmailTemplate (17 propriedades, 1 estrutura), Letterhead (11, 2 estruturas), Document (7), ContentAsset (9, 4 estruturas), ChatterSettings (17), GenAiPromptTemplate (11, 5 estruturas), GenAiFunction (10, 1 estrutura), GenAiPlugin (12, 1 estrutura; parcial) e EinsteinGptSettings (11). Nota: `fontes/extracoes/mdapi-lote7f-conteudo-ia.txt`. Dois relacionamentos por nome: EmailTemplate → Letterhead e GenAiPlugin → GenAiFunction.
    - **Funcionalidades (9):** email-templates, salesforce-files, asset-files, chatter, prompt-builder, agentes-agentforce, subagents-e-agent-actions, einstein-trust-layer e agentforce-data-library. static-resources aparece também em Bibliotecas e assets; lightning-knowledge, em Recuperação de conhecimento.
    - **Texto:** 28 itens avançados novos em 11 temas (`conteudo_extras.py`); os 11 temas internos das duas áreas ganharam descrição e referências. 33 fontes novas, lidas pelo resultado de busca (`fontes/extracoes/temas-detalhe-conteudo-ia.txt`).
    - **Achados:** (a) a Ajuda atual chama de subagent o que GenAiPlugin, na API 68.0, chama de topic; (b) as páginas de GenAiFunction e GenAiPlugin mandam usar GenAiPlannerBundle para o que é criado dentro de um agente, e esse tipo não consta do inventário v68 do projeto; (c) a página de Letterhead tem dois tipos de campo que parecem errados (registrados como divergência).
    - **Pendências:** (1) Conteúdo: ContentDocument, ContentVersion e ContentDocumentLink não cadastrados como objetos API (páginas não lidas por inteiro); bibliotecas (ContentWorkspace), Topics do Chatter, data categories, ContentSettings e as pastas DocumentFolder/EmailFolder não lidos; caminho de Setup de Files e de asset files não confirmado. (2) IA: nenhum metadata type do agente em si (Bot, BotVersion e os tipos Ai* do inventário não lidos); subtipos AiPluginUtteranceDef e GenAiPluginInstructionDef sem campos na página; modelos (AI Models, Models API), Testing Center e avaliação de agentes não lidos; caminho de Setup do Trust Layer, das data libraries e dos agentes não confirmado; nome do arquivo de GenAiFunction no source format não confirmado. (3) Lidos e não cadastrados: Group (public groups; fica para B4) e EinsteinAgentSettings (Einstein Case Classification; tema de atendimento).
  - Com A6, a fila A (texto por tema) terminou.
  - Rodadas B2 e B3 (2026-11-16), num só PR: catálogo de Relatórios e de Qualidade (lote 7g, `ferramentas/carga/lotes/lote7g_relatorios_qualidade.py`).
    - **Tipos (guia versionado 264.0):** Report (41 propriedades; parcial) e Dashboard (26; parcial), só no primeiro nível; ReportType (9, 3 estruturas); ReportFolder e DashboardFolder (5 cada; parcial, falta SharedTo), pela página Folder; DuplicateRule (13, 5 estruturas; parcial) e MatchingRules (2 estruturas). Nota: `fontes/extracoes/mdapi-lote7g-relatorios-qualidade.txt`.
    - **Funcionalidades (5):** relatorios, dashboards, custom-report-types, pastas-de-relatorios-e-dashboards e duplicate-management. Usam as fontes de Ajuda já registradas nas rodadas de texto.
    - **Texto:** os três itens "Como metadado" que diziam "ainda não detalhado" foram reescritos; "por onde começar" em 8 temas; 2 itens avançados novos.
    - **Pendências:** (1) Report e Dashboard: as páginas têm 238 mil e 173 mil caracteres e só os primeiros 100 mil foram lidos; nenhum subtipo cadastrado (colunas, filtros, agrupamentos, gráfico, componentes, grade); valores de ReportFormat não transcritos. (2) DuplicateRule: versão inicial não confirmada (a leitura devolveu 68.0 e o exemplo da página usa 38.0); campos herdados de FilterItem por DuplicateRuleFilterItem não listados na página. (3) SharedTo e FolderShare não lidos. (4) Caminho de Setup de duplicate rules, matching rules e report types não confirmado. (5) Temas de Qualidade ainda sem funcionalidade: classificação e sensibilidade, consentimento e privacidade, rastreabilidade e histórico, retenção e exclusão; em Relatórios, recursos analíticos de produto. (6) Objetos API de relatórios, dashboards e duplicidade (Report, Dashboard, DuplicateRecordSet e outros) não investigados.
  - Filas e public groups (2026-11-16), pedido da autora, antecipado de B4 (lote 7h, `ferramentas/carga/lotes/lote7h_filas_grupos.py`).
    - **Metadata types:** Queue (8 propriedades, 7 estruturas) e Group (4). **Objetos API:** Group (11 campos, com os 17 valores de Type), GroupMember (2) e QueueSobject (2). 8 relacionamentos. Nota: `fontes/extracoes/lote7h-filas-grupos.txt`.
    - **Funcionalidades:** filas e public-groups, com caminho de Setup confirmado. Omni-Channel, Chatter e pastas de relatórios foram ligados a elas. 7 itens avançados novos em dois temas de Acesso. 12 fontes de Ajuda novas, lidas pelo resultado de busca.
    - A exportação `exportacoes/acesso/` (Groups.json, Queue.json, fontes.json) foi regerada por `exportacoes/acesso/gerar.py`, porque o teste exige que ela reproduza o catálogo.
    - **Pendências:** CollaborationGroup e CollaborationGroupMember (grupos do Chatter) não lidos; UserRole e Organization não cadastrados (alvos de Group.RelatedId e OwnerId); SharingRules (metadata type) não lido; versão de entrada dos três objetos não informada nas páginas; exposição na Tooling API não verificada; valores de QueueSobject.SobjectType não listados na página do objeto; regras de atribuição não foram religadas a filas (página não relida).
  - Fecho da rodada A3 (2026-11-16), pedido da autora (lote 7i, `ferramentas/carga/lotes/lote7i_interface_fecho.py`).
    - **Tipos:** Network (71 propriedades, só o primeiro nível; parcial), CustomSite (51, 3 estruturas), NavigationMenu (3 estruturas), LightningExperienceSettings (42), ListView (10; parcial, falta SharedTo), WebLink (22) e PathAssistantSettings. Nota: `fontes/extracoes/lote7i-interface-fecho.txt`.
    - **Funcionalidades novas:** experience-cloud-sites, list-views e botoes-e-links-customizados. **Ampliadas:** path, tabs, acoes-rapidas, temas-e-branding, digital-experiences, filas e page-layouts (caminho de Setup agora confirmado).
    - **Texto:** os 8 temas internos de Interface têm agora descrição, referências e funcionalidade; 19 itens avançados novos. 25 fontes de Ajuda novas, lidas pelo resultado de busca.
    - **O que ainda falta em Interface:** subtipos de Network depois do corte da leitura (NetworkMemberGroups, NetworkTabSet, reputação e outros); SharedTo; CustomPageWebLink, HomePageLayout e HomePageComponent (Classic); ExperienceBundle e DigitalExperienceBundle (conteúdo das páginas do site); MobileSettings e a navegação do app móvel; AppMenu foi lido e não cadastrado (a página só diz "Reserved for future use", sem campos); criação de list views no Lightning Experience não lida.
  - Fecho da rodada A4 (2026-11-16), pedido da autora (lote 7j, `ferramentas/carga/lotes/lote7j_observabilidade_fecho.py`).
    - **Objetos (Tooling API, guia versionado 264.0):** TraceFlag (14 campos), DebugLevel (14) e ApexLog (10), com 3 relacionamentos; ligados à funcionalidade debug-logs. Nota: `fontes/extracoes/lote7j-observabilidade-fecho.txt`.
    - **Funcionalidades novas:** system-overview e armazenamento-de-dados-e-arquivos (tema Limites e consumo, que não tinha nenhuma) e transaction-security. limites-de-api-e-alocacoes aparece também em Limites e consumo.
    - **Texto:** Limites e consumo e Histórico de login ganharam descrição e referências; 11 itens avançados novos em quatro temas. 16 fontes de Ajuda novas, lidas pelo resultado de busca. Os 6 temas internos de Observabilidade têm agora descrição, referências e funcionalidade.
    - **O que ainda falta em Observabilidade:** TransactionSecurityPolicy (a página do guia versionado devolveu conteúdo ilegível; registrado como bloqueado); objetos de eventos em tempo real (LoginEvent, ReportEvent, ApiEvent); lista de tipos de evento de EventLogFile; exposição de TraceFlag, DebugLevel e ApexLog na API padrão não verificada; caminho de Setup de Transaction Security não lido; Background Jobs e Identity Verification History não lidos.
  - Fecho da rodada B2 (2026-11-16), pedido da autora (lote 7g ampliado).
    - **Subtipos:** as páginas de Report (237.873 caracteres) e Dashboard (173.302) foram lidas inteiras, em partes, com o parâmetro offset. Entraram 21 estruturas de Report (agregações, buckets, agrupamentos, filtros, cross filters, fórmulas, gráfico, período) e 15 de Dashboard (filtros, grade, colunas, componentes, tabelas); ChartSummary é compartilhada. Report e Dashboard passam a ter cobertura estrutural completa. ReportFormat ganhou os valores (Matrix, Summary, Tabular, Joined).
    - **Funcionalidade nova:** crm-analytics, no tema Recursos analíticos de produto, que não tinha nenhuma. Com isso, os 6 temas internos de Relatórios têm funcionalidade. 8 fontes de Ajuda novas, lidas pelo resultado de busca (`fontes/extracoes/temas-detalhe-crm-analytics.txt`).
    - **Texto:** 6 itens avançados novos (reports, métricas e agregações, dashboards e recursos analíticos de produto).
    - **Divergências registradas:** campos tipados como enumeração que o exemplo usa como elementos (cadastrados como estruturas); ReportBucketFieldType, ReportBucketFieldNullTreatment e Language sem lista de valores; autoselectColumnsFromReport e isAutoSelectFromReport fora das tabelas; DashboardTableColumn.sortBy tipado como DashboardComponentSection.
    - **O que ainda falta em Relatórios:** metadata types Wave* (CRM Analytics) e AnalyticSnapshot não lidos; objetos API de relatórios e dashboards não investigados; caminho de Setup para habilitar o CRM Analytics não lido; Tableau Next não tratado.
  - Fecho da rodada B3 (2026-11-17), pedido da autora (lote 7k, `ferramentas/carga/lotes/lote7k_qualidade_fecho.py`).
    - **Metadata type:** PrivacySettings (13 propriedades). **Objetos API:** Individual (28 campos), ContactPointTypeConsent (17), DataUsePurpose (8) e FieldHistoryArchive (10, big object), com 3 relacionamentos. Nota: `fontes/extracoes/lote7k-qualidade-fecho.txt`.
    - **Funcionalidades:** field-history-tracking, field-audit-trail, recycle-bin, data-classification e consent-management. Os 4 temas de Qualidade que não tinham funcionalidade agora têm; caminhos de Setup confirmados para histórico de campos, Data Classification e Data Protection and Privacy. 10 fontes de Ajuda novas, lidas pelo resultado de busca.
    - **Texto:** 7 itens avançados novos nos quatro temas.
    - **O que ainda falta em Qualidade:** objetos de histórico (AccountHistory e afins), ContactPointConsent, ContactPointEmail e AuthorizationForm*; FieldDefinition e FieldSecurityClassification; caminho de Setup do Field Audit Trail e de acesso à Recycle Bin; Privacy Center e Salesforce Archive; valores dos picklists de Individual (a página não lista).
  - Temas internos ainda sem funcionalidade: 7, todos do escopo de B4.
  - Rodada B4, parte A (2026-11-17), issues #8 e #9 (lote 7l, `ferramentas/carga/lotes/lote7l_b4_estruturas.py`).
    - **#9:** KnowledgeSettings (12 estruturas) e ForecastingSettings (11) agora têm cobertura estrutural completa. ForecastingGroup e ForecastingGroupItem não foram cadastrados, porque nenhuma propriedade os usa.
    - **#8:** Profile (ProfileUserPermission, ProfileServicePresenceStatusAccess); CustomObject (SearchLayouts, ProfileSearchLayouts e HistoryRetentionPolicy como estruturas; BusinessProcess, FieldSet e Index como metadata types filhos); CustomField (Picklist, descontinuado; summaryFilterItems → FilterItem); ValueSet (ValueSettings, CustomValue). Tooling API: chamadas, REST e campos de Profile, PermissionSet, PermissionSetGroup, PermissionSetAssignment, User e RecordType.
    - **Continua parcial:** Profile (LoginFlow, ProfileAgentAccess, ProfileActionOverride e ProfileLoginHours não têm seção na página); CustomObject (ActionOverride, SharingReason, SharingRecalculation e NamedFilter ilegíveis); PicklistValue (ilegível), que deixa CustomField, RecordType e BusinessProcess parciais. Nota: `fontes/extracoes/lote7l-b4-estruturas.txt`.
  - Rodada B4, parte B (2026-11-17), issues #8 e #34 (lote 7m, `ferramentas/carga/lotes/lote7m_b4_acesso_temas.py`).
    - **Metadata types:** Role, SharingRules, SharingCriteriaRule, SharingOwnerRule, SharingGuestRule, SharingTerritoryRule, IndustriesSettings (190 opções, página de 150 mil caracteres lida por partes) e RevenueManagementSettings (19, guia de Revenue Management). **Estruturas:** SharedTo (23) e AccountSharingRuleSettings (3). **Objeto API:** UserRole (13 campos; a página clássica estava ilegível, então foram usadas a nova referência de objetos e a Field Reference).
    - **Funcionalidades:** hierarquia-de-papeis, regras-de-compartilhamento, licencas-de-usuario, configuracoes-de-nuvens-de-setor e revenue-management. Os 6 temas internos que estavam vazios agora têm funcionalidades; outras-areas fica sem nenhuma por desenho, o que está explicado no texto do tema.
    - **Caminhos de Setup (#8):** verificados os de perfis, tipos de registro, contas, contatos, oportunidades, casos, campanhas, produtos e catálogos de preço, previsões colaborativas e equipes de conta e de oportunidade (leads já estava verificado). Nota: `fontes/extracoes/lote7m-b4-acesso-temas.txt`.
  - Rodada B5, parte A (2026-11-17), pedido da autora: "deixar a estrutura completa" (lote 7n, `ferramentas/carga/lotes/lote7n_b5_estruturas.py`; funções comuns em `ferramentas/carga/ligacao.py`).
    - **Resultado:** todos os metadata types e estruturas têm cobertura estrutural completa, menos Flow (parte B). Saíram de parcial: Profile, CustomObject, CustomField, RecordType, BusinessProcess, CustomTab, QuickAction, FlexiPage, GenAiPlugin, Network, Layout, AutoResponseRules, DuplicateRule, EntitlementProcess, Translations, PresenceUserConfig, ListView, ReportFolder e DashboardFolder.
    - **Novos:** os metadata types PicklistValue (tabela lida na página FieldDefinition da Tooling API) e SharingReason; 54 estruturas (ActionOverride, NamedFilter, SharingRecalculation, LoginFlow, ProfileActionOverride, ProfileAgentAccess, ProfileLoginHours, subtipos de FlexiPage, QuickAction, GenAiPlugin e Network, PicklistValueTranslation). Enumerações completadas: FilterOperation, FeedItemType, SummaryLayoutStyle, PlatformActionListContext, RuleEntry, TabVisibility, QuickActionLabel, FlexiPageType e motif.
    - **Fontes:** páginas que vinham ilegíveis abriram por outro endereço (`customfield.htm`, `namedfilter.htm`). O novo site da referência (`docs/platform/api-metadata/...`) mostra API 68.0, mas a extração perde nomes de propriedade; só foi usado onde os nomes vieram legíveis. Correção: a nota do lote 7l dizia que quatro subtipos de Profile não tinham seção; eles estão na primeira parte da página.
  - Rodada B5, parte B (2026-11-17): os subtipos de Flow (lote 7o, `ferramentas/carga/lotes/lote7o_b5_flow.py`). A página de Flow (825 mil caracteres) foi lida por partes, com leituras extras nas junções: 94 seções, 89 estruturas. Os campos herdados (FlowBaseElement → FlowElement → FlowNode) entram em cada estrutura marcados com herdada_de. collectionFilterCriteria é reservado e não tem seção. **Com isso, todos os 161 metadata types e as 470 estruturas têm cobertura estrutural completa.**
  - Rodada B5, parte C (2026-11-17): objetos API (lote 7p, `ferramentas/carga/lotes/lote7p_b5_objetos.py`). As páginas que as notas antigas diziam "servidas truncadas" eram cortadas pelo leitor em 100 mil caracteres; lidas com offset, as tabelas foram até o fim. 300 campos novos (Contact, Campaign, Quote, AgentWork, KnowledgeArticleVersion, Case, Opportunity, Account com os campos de conta pessoal, User, EntityDefinition e FieldDefinition). Linhas vazias da tabela e Id e campos de sistema não listados seguem a convenção do catálogo. **Os 84 objetos API passam a ter cobertura estrutural completa.**
  - Rodada B5, parte D (2026-11-17): caminhos de Setup de 16 funcionalidades, verificados na Ajuda (lote 7q, `ferramentas/carga/lotes/lote7q_b5_setup.py`). Por decisão da autora, aura-components, lightning-web-components e queueable-apex ficam com Setup "não aplicável" (recursos de código). Continuam sem caminho 10: agentforce-data-library, configuracoes-de-nuvens-de-setor, crm-analytics, dynamic-forms, einstein-trust-layer, field-audit-trail, flow-orchestration, recycle-bin, revenue-management e servicos-externos-registrados-commerce. A issue #39 não foi trabalhada nesta rodada.
  - Rodada B5, parte E (2026-11-17): caminhos das funcionalidades restantes (lote 7r, `ferramentas/carga/lotes/lote7r_b5_setup_restantes.py`). Nove ficam verificadas. Recycle Bin (App Launcher) e serviços externos do Commerce (app Commerce > Settings > Store > Extensions) não são telas de Setup, e a nota de cada uma diz isso. A política de retenção do Field Audit Trail continua sendo feita pela Metadata API; a tela registrada é a de Field History Tracking. **configuracoes-de-nuvens-de-setor segue 'desconhecido'**: cada nuvem de setor tem páginas próprias, e nenhuma fonte lida mostra um caminho único para as opções de IndustriesSettings.
  - Rodada B5, parte F (2026-11-17): itens da #39 que tinham fonte nova (lote 7s, `ferramentas/carga/lotes/lote7s_b5_issue39.py`): limites do Composite (25 subrequisições; 500 em composite graphs; allOrNone) e da Metadata API (10.000 arquivos; .zip de 39 MB compactado e 600 MB descompactado); caminhos de Token Exchange Handlers e da conexão de entrada do Private Connect. Continuam bloqueadas as páginas de ExtlClntAppAttestSettings, ExtlClntAppAttestConfigurablePolicies, ExtlClntAppOauthSecuritySettings, McpServerDefinition e ApiNamedQuery (o endpoint versionado devolve binário), mobileAppConfig e o caminho para criar escopo OAuth customizado.
  - Decisões da autora na #39 (2026-11-17): (1) os conectores de dados (DataConnector*, DataStream*, ExternalDataConnector etc.) ficam para quando a nuvem Data 360 for trabalhada, não entram na visão Platform/Core; (2) a ligação estrutural entre funcionalidade e propriedade (por exemplo, Versões de API ↔ `apiVersion`) fica para a v2. Na #39 restam só itens sem fonte disponível.
  - B5 encerrada, exceto pelo que depende de fonte que hoje não abre. Seguem: D1, C2, C3, D2 e D3.
  - Rodada D1, parte A (2026-11-17): auditoria de conteúdo (`ferramentas/auditoria_conteudo.py`, relatório em `relatorios/auditoria-conteudo.md`). Corrigido: 32 estruturas de Profile/PermissionSet com o mesmo texto genérico (lote 7t); `o_que_e` vazio do Data 360 e licenças do Platform/Core, que deixa o estado 'desconhecido' (lote 7u). Achado principal: **887 propriedades e campos (29 nós; quase todos campos de objetos API, como User, Account, Lead e QuoteLineItem) seguem com a explicação marcada como pendente** e aparecem no site com o texto padrão da carga. 79 campos explicativos curtos ficam como revisão didática. Revisão visual do build local em desktop e mobile: sem erro de JavaScript; as imagens externas (logos) não carregam no ambiente de teste.
  - Rodada D1, parte B (2026-11-17), por decisão da autora (principais agora, resto na v2): 378 campos de User, Account, Contact, Lead, Opportunity e Case ganharam explicação lida na Object Reference 264.0 (lote 7v). Nesses seis objetos restam 34 pendentes (31 de User, que vêm da Field Reference e não aparecem na página do objeto). **Na v2:** os demais objetos e propriedades com explicação pendente (cerca de 510 itens; a lista por nó está em `relatorios/auditoria-conteudo.md`).
  - **D1 encerrada (2026-11-17).** O relatório de fechamento do MVP está em `relatorios/mvp-fechamento.md`. Issues: #16 (CI) e #8 fechadas, porque tudo foi feito; #15 só depende do secret `TUTORIAL_SF_GRAFO_TOKEN`; #12 atualizada (as páginas "truncadas" foram resolvidas com offset; falta a org de teste).
  - Seguem: C2 (paleta e rótulos; #23, #17), C3 (acessibilidade; #19), D2 (certificações) e D3 (nuvens × funcionalidades).
  - C2 concluída (PR #97). Auditoria de acessibilidade da C3 feita sem alterar código; a regressão de contraste da busca foi corrigida antes (PR #98).
  - Rodada de nuvens (2026-11-17, decisão da autora; lote 7w): 9 nuvens/produtos novos como nó, ligados às funcionalidades já cadastradas e sem inventário de metadata types. Campo didático `categoria` (na_org, plataforma_propria, misto). Platform/Core passa a se chamar Agentforce 360 Platform. Agentforce não virou nó separado, porque os agentes ficam na plataforma. `config/escopo.json` registra que os produtos fora do recorte aparecem no mapa, enquanto o critério X1 segue valendo para o inventário.
  - C3 (acessibilidade, 2026-11-18): itens 3 a 10 da auditoria feitos (migalhas com 24px, títulos h2>h3>h4 na ficha, rótulos esmaecidos a 3:1 ou mais, tipo como descrição dos links, botão "Reduzir animações" com estado só em aria-pressed). axe nos testes E2E, em 10 estados mais as janelas, desktop e 360px. Roteiro com leitor de tela em `apps/sf-tutor/ACESSIBILIDADE.md`, a ser executado pela autora.
  - **Plano de evolução combinado com a autora (2026-11-18):**
    - Fase 0: secret `TUTORIAL_SF_GRAFO_TOKEN` (#15), para publicar automaticamente (autora).
    - Fase 1: acabamento (acessibilidade feita; logos de Experience Cloud e Industries se houver endereço; slogan #102).
    - **Fase 2 (prioridade):** explicações pendentes, uma classificação por sessão e um PR por lote. Lista viva em `relatorios/fase2-pendencias-por-classificacao.md` (gerada por `ferramentas/pendencias_explicacao.py`): 509 itens em 26 nós, sendo 377 em "Processos de negócio específicos de produto".
    - Fase 3: inventário por nuvem (Experience Cloud → Field Service → Revenue → Industries → Data 360, com conectores).
    - Fase 4: classificação Core dos 981 metadata types (#10), em lotes pequenos e em paralelo.
    - Fase 5: ligação funcionalidade ↔ propriedade e mapeamento XML ↔ campo de API (mudam o esquema).
    - Fase 6: certificações (#96).
    - Contínuo: validação em org e fontes bloqueadas (#12).
    - Para poupar créditos: lotes pequenos e fechados por sessão; validação completa só no fim de cada lote.
  - #10, etapa 1 (2026-11-18, opção B da autora; lote 7x): os 161 metadata types catalogados ganharam decisão de recorte com critério e motivo (`classificacao_core_por_item.justificativas`). Resultado: 123 no Core; 30 fora por serem específicos de uma nuvem (Sales, Service, Experience), mas que continuam no mapa; 4 fora por licença (Field Service, Industries, Revenue, Commerce); 4 pendentes de licença (tipos de IA generativa). O C2 foi reescrito conforme a decisão. Também foram ligadas 74 funcionalidades que não tinham nuvem: a visão "Por nuvem" passa a mostrar todas as 137.
  - Seguem: #10 etapa 2 (os 832 tipos não catalogados, por família e com uma fonte por família), alternada com lotes da Fase 2; depois a etapa 3 (cadastrar os incluídos).
  - #10, etapa 2, lote 1 (2026-11-18; lote 7y, `ferramentas/carga/lotes/lote7y_core_familias_1.py`): 35 tipos decididos, todos fora do Core por X2 (produto de setor), sem cadastro no catálogo.
    - Famílias: Health Cloud (12), Net Zero Cloud (11) e Omnistudio (12). Fonte de lista por família nos guias de desenvolvedor de cada produto; nota em `fontes/extracoes/lote7y-core-familias-1.txt`.
    - Cada decisão traz `familia`, `evidencias` (fonte de "lista" e fonte de "licenca") e `alcance_da_licenca`: "proprio_tipo" quando a frase de licença está na página do tipo (só OmniIntegrationProcedure) e "familia" quando vale pelo produto. As exigências vêm de frases de edição ("com Health Cloud", "com Net Zero Cloud habilitado") e da regra de acesso de OmniIntegrationProcedure (licença Omnistudio).
    - Validador: as fontes citadas no recorte contam como usadas; todo tipo com decisão precisa estar no inventário; todo tipo com evidência de "lista" precisa aparecer na nota da fonte. Três testes novos (`TestRecorteCoreFamilias`).
    - Ficaram pendentes de propósito: OmniUiCard (fora da lista Omnistudio lida); DecisionMatrixDefinition, DecisionTable e DecisionTableDatasetLink (lista de Lookup Tables sem frase de licença); Ins* (a lista de Insurance Claims só traz InsPlcyLimitConsumptionRule).
    - Restam 797 dos 832 tipos não catalogados (801 pendentes no inventário, contando os 4 de IA da etapa 1).
    - Próximas famílias sugeridas, com fonte já localizada ou provável: Insurance e Financial Services (guias próprios), Public Sector (Reglt*, Assessment*), Data 360 (precisa de lista legível; o endereço `meta_data_cloud_types.htm` devolveu só índice), CRM Analytics (Wave*, Analytics*; falta frase de licença na página do tipo), Experience Cloud (Community*, DigitalExperience*, Network*), Agentforce IT Service (Cnfg*, ServiceItsm*). Depois, os tipos de plataforma (*Settings genéricos), que tendem a entrar no Core e pedem fonte por tipo.
  - #10, etapa 2, lote 2 (2026-11-18; lote 7y2, `ferramentas/carga/lotes/lote7y2_core_familias_2.py`): 25 tipos com decisão e motivo, mesmo padrão do lote 1.
    - Excluídos por X2 (11): Discovery Framework (5; vem incluído só em nuvens de setor), Salesforce Pricing (4; edições de Revenue Management) e Public Sector (2).
    - Pendentes por C2, com motivo (14): Agentforce IT Service. A frase de edição lida não esclarece a licença.
    - Nota: `fontes/extracoes/lote7y2-core-familias-2.txt`. Dos 27 nomes da lista de IT Service, 13 não constam do inventário v68 e ficaram de fora.
    - Achado: a nota de `src:help-revenue-settings` não registra a frase "exige licença de Revenue Management" que o catálogo atribui a ela (funcionalidade revenue-management, Setup). Conferir numa rodada de qualidade.
    - Ainda sem frase de licença: Field Service (TimeSheetTemplate; Skill também serve ao roteamento de chats), Lookup Tables, Insurance.
    - Tipos não catalogados sem nenhuma decisão: 772 de 832.
  - #10, etapa 2, lote 3 (2026-11-19; lote 7y3, `ferramentas/carga/lotes/lote7y3_core_familias_3.py`): 14 tipos com decisão e motivo.
    - CRM Analytics (9 Wave*): excluídos por X2 (licenças por usuário, `src:help-crm-analytics-licenses`). Sem página de lista única: cada tipo tem a própria fonte (página do tipo, lida pelo resultado de busca).
    - Experience Cloud (4): ExperienceBundle, DigitalExperienceConfig, CommunityTemplateDefinition e CommunityThemeDefinition, excluídos por C3, como Network e CustomSite na etapa 1. O validador aceita `alcance_da_licenca = "nao_se_aplica"` para essas decisões.
    - Pendente com motivo (1): DigitalExperienceBundle, que serve a workspaces de site, marketing e general.
    - Sem decisão de propósito: SiteDotCom (serve a Experience Cloud e a Site.com), WaveAnalyticAssetCollection (página não lida) e os Analytics* (não lidos; podem ser de outro produto).
    - Nota: `fontes/extracoes/lote7y3-core-familias-3.txt`. Tipos não catalogados sem nenhuma decisão: 758 de 832.
  - #10, etapa 2, lote 4 (2026-11-19; lote 7y4, `ferramentas/carga/lotes/lote7y4_core_settings_plataforma.py`): Settings de plataforma, pela página geral de Settings da Metadata API 264.0 (`src:mdapi-settings-264`).
    - 30 incluídos no Core pelo C2 ajustado (configuram a plataforma e não há registro de licença): OrgSettings, SharingSettings, SecuritySettings, PicklistSettings, SearchSettings, SandboxSettings, UserInterfaceSettings, RecordPageSettings, DynamicFormsSettings etc.
    - 5 pendentes com motivo: EventSettings e RealTimeEventSettings (indício de add-on de monitoramento), EmailIntegrationSettings (inclui Salesforce Inbox), ObjectLinkingSettings (parece de canais de atendimento) e NotificationsSettings (a página repete a frase de MobileSettings).
    - 15 nomes não aparecem na página lida e ficam sem decisão (ver a nota).
    - Regra nova C4 (decisão da autora em 2026-11-19): Agentforce e IA generativa ficam como "condicional", ligados ao Core e às nuvens que os usam, com a condição registrada. Diverge do C2, que deixaria esses tipos fora por licença. O inventário passa a contar "condicional"; nenhum tipo foi reclassificado ainda (fica para o lote da família de IA, com fonte).
    - Tipos não catalogados sem nenhuma decisão: 723 de 832.
  - #10, etapa 2, lote 5 (2026-11-19; lote 7y5, `ferramentas/carga/lotes/lote7y5_core_ia_c4.py`): primeira aplicação do C4. 8 tipos ficam "condicional".
    - Orientação da autora (2026-11-19), registrada em cada decisão (`orientacao_autora`): GenAiFunction e relacionados são diretamente de Agentforce, seja o agente de Sales, Service ou Core; prompt templates seguem a mesma linha (Sales e Service trazem prompts standard; o Core tende a usar customizados). Por isso os 8 ligam a nuv:platform-core, nuv:sales-cloud e nuv:service-cloud.
    - Agentes (condição "Agentforce habilitado na org"): AiAuthoringBundle, GenAiFunction, GenAiPlugin, AiEvaluationDefinition (frase na página do próprio tipo). Bot e BotVersion: "Agentforce habilitado, ou Einstein Bots (Service Cloud)".
    - Prompt templates (condição "IA generativa habilitada, com add-on Einstein for Platform, Einstein ou Agentforce for Sales ou Service, ou Agentforce Foundations"): GenAiPromptTemplate e EinsteinGptSettings. A Ajuda confirma as categorias pilot, custom e standard.
    - GenAiFunction, GenAiPlugin, GenAiPromptTemplate e EinsteinGptSettings estavam pendentes desde a etapa 1; o campo `historico` registra a mudança. Com isso, não sobra pendente da etapa 1.
    - Validador: decisão "condicional" precisa de `condicao` e de estar na lista `condicionais`; dois testes novos.
    - Cuidado registrado: `registrar_fontes` não sobrescreve um id que já existe. Uma fonte nova com o id de outra (aqui, src:help-prompt-builder) fica com a nota antiga; o validador acusou e a fonte nova virou src:help-prompt-builder-edicoes.
    - Ficam para o próximo lote de IA (sem fonte lida): AiAgent*, AiBundle*, AiSurface*, AiPlanner*, Einstein*Settings, Agentforce*Settings, BotBlock*, BotTemplate, BotSettings. GenAiPlannerBundle não consta do inventário v68.
    - Inventário: 153 incluídos, 8 condicionais, 93 excluídos, 739 pendentes. O site ainda não usa a decisão de Core; mostrar "condicional" no grafo é tarefa da etapa 3.
  - #10, etapa 2, lote 6 (2026-11-19; lote 7y6, `ferramentas/carga/lotes/lote7y6_core_ia_c4_2.py`): segunda rodada da família de IA pelo C4. 9 tipos condicionais.
    - Condicional, Core + Sales + Service (6): AiAgentDefinition e AiAgentDefinitionVersion (o agente na API 68), AiSurface e AiResponseFormat (conexões personalizadas com agentes), GenAiPromptTemplateActv (ativação de prompt standard; condição de prompt templates) e BotTemplate (guarda variáveis de agentes; condição "Agentforce ou Einstein Bots").
    - Condicional INFERIDO (3): BotBlock, BotBlockVersion e BotSettings. As fontes só falam de Einstein Bots; por orientação da autora (2026-11-19), "o que for bot" fica associado ao Agentforce com `"inferido": true` e `nota_inferencia`. O validador exige a nota quando há `inferido`; um teste novo.
    - Ainda sem decisão na família: AiAgentDefinitionPlanner, AiBundle*, AiPlanner*, AiResponseFormatIstr, AiSurfaceInput, AiSurfaceInstruction, Einstein*Settings, Agentforce*Settings e outros.
    - Inventário: 153 incluídos, 17 condicionais, 93 excluídos, 730 pendentes. Tipos não catalogados sem decisão: 708 de 832.
  - Fase 2, lote Acesso (2026-11-19; lote 8b, `ferramentas/carga/lotes/lote8b_fase2_acesso.py`): os 31 campos de User que só tinham nome.
    - Achado: a Object Reference 264.0 (lida inteira, até WirelessEmail) só descreve 2 deles: Country e UserPreferencesShowCountryToExternalUsers, que ganharam explicação. A Field Reference não traz descrições, só tipo e rótulo.
    - Os outros 29 ganharam tipo (27) e o rótulo oficial nas notas. A Field Reference não traz descrições, e o rótulo, na maioria, só repete o nome técnico (ex.: HasSentWarningEmail238).
    - Estado novo `nao_encontrada` (decisão da autora em 2026-11-19), para 27 deles: texto padrão "Não encontrada descrição oficial na última versão da documentação (264.0, API 68.0); verificado também nas notas da release Winter '27 (por busca)". Versão e release vêm de `config/versoes.json`. A conferência da release foi por busca: a página "New and Changed Objects" não abre na leitura direta. Também conferida a Object Reference nova (sem descrição para eles).
    - UserPermissionsMobileUser e UserPreferencesSetupAssistantPrefDisabled não apareceram na leitura e seguem `pendente`.
    - O site mostra o novo estado como "descrição oficial não encontrada" (`apps/sf-tutor/src/ui/painel.ts`). Fase 2: 409 itens.
    - A cobertura explicativa de User foi recontada: 177 de 206 (o número anterior, 46, estava desatualizado).
  - Fase 2, lote Conteúdo (2026-11-18; lote 8a, `ferramentas/carga/lotes/lote8a_fase2_conteudo.py`): os 35 campos pendentes de KnowledgeArticleVersion ganharam tipo e explicação; 5 também a versão em que entraram. A cobertura explicativa do objeto fica completa (42 de 42). Fonte: Object Reference 264.0 pelo endpoint versionado (`src:objref-knowledgearticleversion-264`); as letras de propriedade de API não foram lidas e seguem 'desconhecido'. A classificação Conteúdo sai da lista da Fase 2 (438 itens restantes).
  - Fase 2, lote Automação (2026-11-18; lote 7z, `ferramentas/carga/lotes/lote7z_fase2_automacao.py`): 36 campos de primeiro nível de Flow ganharam explicação, e 25 deles também a versão em que entraram.
    - Fonte: página de Flow na referência atual da Metadata API (`src:mdapi-flow-ref-atual`); nota em `fontes/extracoes/lote7z-fase2-automacao.txt`. A página não mostra o nome ao lado de cada linha: a correspondência foi feita pelo tipo da linha, que coincide com o tipo já catalogado.
    - Textos só com o que a fonte diz (sem rótulos de interface nem exemplos que ela não traz).
    - Seguem pendentes, sem texto na fonte: Flow.segment (a página só o mostra dentro de FlowStart), cinco campos de FlowSettings (a página atual só dá o tipo; a versionada 264.0 não os lista) e ApprovalProcess.processOrder (a página versionada não lista o campo).
    - Fase 2 passa de 509 para 473 itens. Próximo lote sugerido: Conteúdo (35) ou Acesso (32); "Processos de negócio" (377) fica dividido por subtema (Vendas, Atendimento, Serviço de campo, Experiências externas).
  - Plano de rodadas combinado com a autora (2026-11-16), na ordem: C1 (CI e publicação automática; PRs #68 e #69), B1 (esta), A1 Desenvolvimento, A2 Assíncrono e lotes, A3 Interface, A4 Observabilidade, A5 Conteúdo, A6 IA e agentes, B2 catálogo de Relatórios, B3 Qualidade, B4 remanescentes de Dados/Acesso/Org/Processos (inclui #8 e #9), B5 qualidade do já cadastrado (caminhos de Setup, objetos API, #39), D1 fechamento do MVP, C2 paleta e rótulos (#23, #17), C3 acessibilidade e ajustes (#19), D2 camada de certificações, D3 nuvens × funcionalidades.
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
