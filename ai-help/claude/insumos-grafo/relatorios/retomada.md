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

Os JSONs de `catalogo/` são a fonte da verdade. Os lotes 1, 2 e 3a a 3d foram aplicados por scripts de carga mantidos fora do repositório; edições futuras devem ser feitas nos JSONs ou por ferramentas criadas em `ferramentas/`.

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
- **Falta (lote 5f em diante):**
  - Sub-estruturas pendentes de ConnectedApp e plugins de external client app: mobile, push, canvas, notificação, attest, SAML e ExtlClntAppOauthSecuritySettings.
  - Outros certificados: PublicKeyCertificate, PublicKeyCertificateSet, UserAuthCertificate e InboundCertificate.
  - McpServerDefinition e ApiNamedQuery, quando houver fonte.
  - Conectores de dados.
  - Os **objetos API** do tema.
  - As demais APIs como funcionalidades (REST, SOAP, Metadata, Tooling, Composite); só Bulk API e Pub/Sub API estão cadastradas.
  - A definição do evento (`__e`) e do objeto externo (`__x`), ambos via CustomObject.
  - Exemplos XML.
  - Caminhos de Setup, ainda `desconhecido`.

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
