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

## "Sobre este tema" (issue #34, fase 1, 2026-11-09)
- **Divergência registrada (tradução didática):** a especificação (`tarefas/00-especificacao-grafo.md`) chama os dois níveis de classificação e subclassificação. O site mostra os dois como **"Tema"**, por decisão da autora (opção B). Os nomes nos dados, no schema e no validador não mudam.
- A seção "Estado do agrupamento" foi substituída por "Sobre este tema", com três camadas fixas:
  1. Para quem está começando;
  2. Para quem já conhece Salesforce (contagens derivadas do grafo);
  3. Nível avançado, recolhido (estado do recorte e referências oficiais).
- O estado do recorte é derivado de `estado` e `referencias_oficiais`. Hoje todos os temas estão como **curadoria do projeto**: estado `desconhecido`, sem referência oficial.
- Pendentes:
  - **Fase 2:** `criterio_inclusao` por tema, exigido pelo validador.
  - **Fase 3:** cruzar com referências oficiais; a fonte ainda não foi escolhida.
  - **Fase 4:** seletor de nível de leitura no site (opcional).

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
