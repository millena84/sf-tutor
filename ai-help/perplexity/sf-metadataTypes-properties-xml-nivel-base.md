**Grupo 1 — Organização e metadados-base do CORE**, com o nível de detalhe adequado para material de consulta: para cada metadata type, você terá **finalidade, local do arquivo, propriedades, blocos complexos, exemplo XML, valores possíveis e cuidados de arquitetura/CTA**.

Uma premissa importante: `Settings` é o nome usado no `package.xml` para acessar a família de configurações da org, mas cada configuração tem seu próprio metadata type, como `MyDomainSettings`, `CompanySettings`, `BusinessHoursSettings` e `CustomerDataPlatformSettings`. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_settings.htm)

***

# Grupo 1 — Organização e metadados-base do CORE

## 1.1 Visão geral

Este grupo responde à pergunta:

> “Como a organização Salesforce está configurada antes mesmo de falarmos de Sales Cloud, Service Cloud, integrações ou automações?”

Ele inclui:

- Identidade da organização.
- Domínio e URLs.
- Idiomas e traduções.
- Moedas e calendário fiscal.
- Horários comerciais e feriados.
- Busca.
- Knowledge e conteúdo.
- Branding e Lightning.
- Mobile.
- Dev Hub e configurações de desenvolvimento.

Um **metadata component** é uma instância de um metadata type; os fields e valores desse componente também são metadata. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_intro.htm)

***

## 1.2 `Organization`

### Finalidade

Representa a organização Salesforce em si: dados cadastrais da empresa, localização, moeda padrão, idioma padrão e configurações globais de identidade.

### Local típico

```text
force-app/main/default/organizations/
```

### Estrutura XML

```xml
<Organization xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>00DXXXXXXXXXXXXXXX</fullName>
    <name>Minha Empresa</name>
    <country>Brasil</country>
    <languageLocaleKey>pt_BR</languageLocaleKey>
    <localeSidKey>pt_BR</localeSidKey>
    <currency>USD</currency>
    <timeZoneSidKey>America/Sao_Paulo</timeZoneSidKey>
</Organization>
```

### Propriedades principais

| Propriedade | Tipo | Obrigatória | Função |
|---|---|---|---|
| `fullName` | string | Sim | ID da organização, geralmente iniciado por `00D` |
| `name` | string | Sim | Nome da organização |
| `organizationType` | string | Não | Tipo de organização |
| `country` | string | Não | País |
| `street` | string | Não | Endereço |
| `city` | string | Não | Cidade |
| `state` | string | Não | Estado |
| `postalCode` | string | Não | CEP |
| `phone` | string | Não | Telefone |
| `fax` | string | Não | Fax |
| `languageLocaleKey` | string | Não | Idioma padrão |
| `localeSidKey` | string | Não | Locale regional |
| `timeZoneSidKey` | string | Não | Fuso horário |
| `currency` | string | Não | Moeda corporativa |
| `defaultLocaleSidKey` | string | Não | Locale padrão |
| `division` | string | Não | Divisão |
| `fiscalYearStartMonth` | int | Não | Mês de início do ano fiscal |
| `usesStartDateAsFiscalYearName` | boolean | Não | Nome do ano fiscal baseado no início |
| `correlationId` | string | Não | ID de correlação |
| `instanceName` | string | Não | Instância/pod |
| `isReadOnly` | boolean | Não | Indica se a org é somente leitura |

### Cuidados de CTA

- `timeZoneSidKey` afeta agendamentos, SLA, business hours e relatórios.
- `currency` e `localeSidKey` afetam formatação, arredondamento e integrações financeiras.
- `fiscalYearStartMonth` impacta forecasting, relatórios e Revenue Cloud.
- Não é comum versionar `Organization` como componente de deploy normal; ele é mais usado para leitura, auditoria e documentação.

***

## 1.3 `Settings`

### Finalidade

`Settings` é o agrupador usado no `package.xml` para recuperar ou implantar configurações da organização. Cada configuração específica tem seu próprio metadata type e arquivo `.settings`. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_settings.htm)

### Estrutura no `package.xml`

```xml
<types>
    <members>*</members>
    <name>Settings</name>
</types>
```

### Estrutura de arquivo

```text
force-app/main/default/settings/
├── Flow.settings
├── Case.settings
├── Knowledge.settings
├── MyDomain.settings
├── CustomerDataPlatform.settings
└── Security.settings
```

### Exemplo XML

```xml
<FlowSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableFlowTriggerRollback>true</enableFlowTriggerRollback>
</FlowSettings>
```

### Regra importante

Diferente de `CustomObject`, `Flow` ou `Profile`, os arquivos `.settings` normalmente representam **uma configuração única por org**, não uma coleção de componentes. 

### Cuidados de CTA

- `Settings` pode conter configurações sensíveis de segurança, integração e produto.
- Nem todo setting é deployável entre orgs.
- Alguns settings dependem de licença, feature enablement ou provisionamento.
- Sempre valide o **Metadata Coverage Report** antes de incluir um setting em pipeline.

***

## 1.4 `MyDomainSettings`

### Finalidade

Define o My Domain da organização: subdomínio, URLs de login, redirecionamentos e comportamento de acesso por URL. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_settings.htm)

### Local típico

```text
force-app/main/default/settings/MyDomain.settings
```

### Exemplo XML

```xml
<MyDomainSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <myDomainName>minhaempresa</myDomainName>
    <canOnlyLoginWithMyDomainUrl>true</canOnlyLoginWithMyDomainUrl>
    <doesApiLoginRequireOrgDomain>true</doesApiLoginRequireOrgDomain>
    <doesWarnOnForceComRedirect>true</doesWarnOnForceComRedirect>
    <redirectForceComSitesUrls>true</redirectForceComSitesUrls>
    <useStabilizedMyDomainHostnames>true</useStabilizedMyDomainHostnames>
</MyDomainSettings>
```

### Propriedades principais

| Propriedade | Tipo | Obrigatória | Função |
|---|---|---|---|
| `fullName` | string | Sim | Nome do componente |
| `myDomainName` | string | Sim | Subdomínio, como `minhaempresa` |
| `myDomainSuffix` | picklist | Não | Sufixo do domínio |
| `canOnlyLoginWithMyDomainUrl` | boolean | Não | Exige login pelo My Domain |
| `doesApiLoginRequireOrgDomain` | boolean | Não | Exige My Domain para API |
| `doesWarnOnForceComRedirect` | boolean | Não | Avisa ao redirecionar URLs `.force.com` |
| `redirectForceComSitesUrls` | boolean | Não | Redireciona URLs antigas de Sites/Experience Cloud |
| `useStabilizedMyDomainHostnames` | boolean | Não | Oculta o nome da instância em URLs |
| `areLegacyRedirectsMaintained` | boolean | Não | Mantém redirecionamentos legados |
| `areLgcyRdirMaintainedWntr26` | boolean | Não | Controle de redirecionamento legado para Winter ’26 |
| `onboardCustomerSpecificSuffix` | boolean | Não | Campo reservado |
| `enableLegacyRedirections` | boolean | Não | Habilita redirecionamentos legados |

A documentação oficial detalha que `myDomainName` define o subdomínio usado em URLs como `MyDomainName.my.salesforce.com` e `MyDomainName.lightning.force.com`, e que `canOnlyLoginWithMyDomainUrl` restringe o login ao URL do My Domain. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_flowsettings.htm)

### Valores possíveis de `myDomainSuffix`

| Valor | Significado |
|---|---|
| `MySalesforce` | `my.salesforce.com` com enhanced domains |
| `MySalesforceLimited` | `my.salesforce.com` sem enhanced domains |
| `CloudforceLimited` | `cloudforce.com` |
| `DatabaseLimited` | `database.com` |
| `OrgLevelCertificate` | `my-salesforce.com` |
| `OrgLevelCertificateLimited` | Versão legada de `my-salesforce.com` |
| `Restricted1` | Reservado |
| `Restricted2` | Reservado |

### Cuidados de CTA

- My Domain é pré-requisito prático para SSO, OAuth, Connected Apps e integrações modernas.
- Alterar My Domain em produção exige plano de comunicação, DNS, cookies, bookmarks e integrações.
- `doesApiLoginRequireOrgDomain` deve ser tratado como decisão de segurança, não apenas configuração técnica.
- Redirecionamentos de `.force.com` impactam Experience Cloud, Sites, Visualforce e integrações antigas.

***

## 1.5 `CompanySettings`

### Finalidade

Define informações corporativas, moeda, idioma, fuso horário, endereço e calendário fiscal. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_mydomainsettings.htm)

### Local típico

```text
force-app/main/default/settings/Company.settings
```

### Exemplo XML

```xml
<CompanySettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <name>Minha Empresa</name>
    <country>Brasil</country>
    <languageLocaleKey>pt_BR</languageLocaleKey>
    <localeSidKey>pt_BR</localeSidKey>
    <timeZoneSidKey>America/Sao_Paulo</timeZoneSidKey>
    <currency>USD</currency>
    <fiscalYearStartMonth>1</fiscalYearStartMonth>
    <fiscalYearNameBasedOn>startingMonth</fiscalYearNameBasedOn>
</CompanySettings>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `name` | string | Nome da empresa |
| `organizationName` | string | Nome da organização |
| `country` | string | País |
| `street` | string | Endereço |
| `city` | string | Cidade |
| `state` | string | Estado |
| `postalCode` | string | CEP |
| `phone` | string | Telefone |
| `fax` | string | Fax |
| `primaryContact` | string | Contato principal |
| `languageLocaleKey` | string | Idioma |
| `localeSidKey` | string | Locale |
| `timeZoneSidKey` | string | Fuso horário |
| `currency` | string | Moeda corporativa |
| `defaultLocaleSidKey` | string | Locale padrão |
| `fiscalYearStartMonth` | int | Mês inicial do ano fiscal |
| `fiscalYearNameBasedOn` | picklist | Base do nome do ano fiscal |
| `usesStartDateAsFiscalYearName` | boolean | Nome baseado no início |
| `division` | string | Divisão |
| `taxEffectiveDate` | date | Data efetiva de imposto |

A documentação oficial mostra `fiscalYearNameBasedOn` com valores `endingMonth` ou `startingMonth`. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_mydomainsettings.htm)

### Cuidados de CTA

- Em grupos multinacionais, moeda, fuso e fiscal year são decisões de arquitetura corporativa.
- Alterar fiscal year depois de usar Forecasting, Revenue Cloud ou relatórios pode gerar retrabalho analítico.
- Para Brasil, valide locale, moeda, fuso e regras fiscais antes de definir integrações com ERP.

***

## 1.6 `LanguageSettings`

### Finalidade

Define quais idiomas estão habilitados na organização e qual é o idioma padrão.

### Local típico

```text
force-app/main/default/settings/Language.settings
```

### Exemplo XML

```xml
<LanguageSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableEndUserLanguageSelection>true</enableEndUserLanguageSelection>
    <enablePlatformActionOverrideLanguageFallback>true</enablePlatformActionOverrideLanguageFallback>
    <userLocalizationEnabled>true</userLocalizationEnabled>
</LanguageSettings>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableEndUserLanguageSelection` | boolean | Usuário escolhe idioma |
| `enablePlatformActionOverrideLanguageFallback` | boolean | Fallback de idioma |
| `userLocalizationEnabled` | boolean | Localização por usuário |
| `userTimeZoneSwitchingEnabled` | boolean | Fuso por usuário |
| `userTerritoryAssignmentEnabled` | boolean | Território por usuário |

### Cuidados de CTA

- Idioma afeta rótulos, traduções, layouts, templates, relatórios e Experience Cloud.
- Para material multilíngue, `LanguageSettings` deve ser planejado junto com `Translations`, `CustomLabels` e `CustomObjectTranslation`.
- Não confunda idioma da org com tradução de metadados: são camadas diferentes.

***

## 1.7 `TranslationSettings`

### Finalidade

Controla o comportamento global de traduções na organização.

### Local típico

```text
force-app/main/default/settings/Translation.settings
```

### Exemplo XML

```xml
<TranslationSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableTranslationWorkbench>true</enableTranslationWorkbench>
</TranslationSettings>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableTranslationWorkbench` | boolean | Habilita Translation Workbench |
| `overridePersonalLocaleSettings` | boolean | Sobrescreve locale pessoal |
| `translateIncomingEmails` | boolean | Traduz e-mails recebidos |

### Cuidados de CTA

- Tradução deve ser tratada como requisito funcional, não como ajuste final.
- Em Experience Cloud, traduções afetam navegação, componentes, labels e conteúdo.
- Em integrações, prefira códigos estáveis no backend e traduza apenas na camada de apresentação.

***

## 1.8 `Translations`

### Finalidade

Armazena traduções de metadados em um idioma específico.

### Local típico

```text
force-app/main/default/translations/pt_BR.translation-meta.xml
force-app/main/default/translations/en_US.translation-meta.xml
```

### Estrutura XML

```xml
<Translations xmlns="http://soap.sforce.com/2006/04/metadata">
    <customApplications>
        <label>Meu App</label>
        <name>Meu_App</name>
    </customApplications>
    <customLabels>
        <label>Erro de validação</label>
        <name>Erro_Validacao</name>
    </customLabels>
</Translations>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Idioma, como `pt_BR` |
| `customApplications` | complexo | Traduções de apps |
| `customLabels` | complexo | Traduções de labels |
| `customPageWebLinks` | complexo | Traduções de links |
| `customTabs` | complexo | Traduções de tabs |
| `flows` | complexo | Traduções de Flow |
| `globalValueSets` | complexo | Traduções de picklist global |
| `quickActions` | complexo | Traduções de quick actions |
| `reportTypes` | complexo | Traduções de report types |
| `scontrols` | complexo | Traduções de S-controls |
| `standardFields` | complexo | Traduções de campos padrão |
| `webLinks` | complexo | Traduções de web links |

### Cuidados de CTA

- Um arquivo de tradução por idioma.
- `CustomLabels` são preferíveis a textos fixos em Apex, LWC e Flow.
- Em LWC, combine `CustomLabels` com `import` para internacionalização.
- Em integrações, não traduza códigos de sistema; traduza apenas rótulos de UI.

***

## 1.9 `CustomLabels` e `CustomLabel`

### Finalidade

`CustomLabels` é o arquivo que agrupa labels; `CustomLabel` representa um label individual reutilizável e traduzível.

### Local típico

```text
force-app/main/default/labels/CustomLabels.labels-meta.xml
```

### Estrutura XML

```xml
<CustomLabels xmlns="http://soap.sforce.com/2006/04/metadata">
    <labels>
        <fullName>Risco_Alto</fullName>
        <categories>Antifraude</categories>
        <language>en_US</language>
        <protected>false</protected>
        <shortDescription>Score de risco alto</shortDescription>
        <value>High risk</value>
    </labels>
</CustomLabels>
```

### Propriedades de `CustomLabel`

| Propriedade | Tipo | Obrigatória | Função |
|---|---|---|---|
| `fullName` | string | Sim | API Name |
| `categories` | string | Não | Categoria |
| `language` | string | Sim | Idioma base |
| `protected` | boolean | Não | Protegido em pacote |
| `shortDescription` | string | Não | Descrição curta |
| `value` | string | Sim | Texto do label |
| `translations` | complexo | Não | Traduções |

### Uso em Apex

```apex
String mensagem = System.Label.Risco_Alto;
```

### Uso em LWC

```javascript
import RiscoAlto from '@salesforce/label/c.Risco_Alto';
```

### Cuidados de CTA

- Use `CustomLabels` para mensagens de erro, regras de negócio visíveis ao usuário e textos de UI.
- Evite textos fixos em Apex, LWC, Flow e OmniScript.
- Para produtos multilíngues, labels devem entrar no pipeline desde o início.

***

## 1.10 `CurrencyType`

### Finalidade

Representa uma moeda habilitada na organização.

### Local típico

```text
force-app/main/default/currencies/
```

### Estrutura XML

```xml
<CurrencyType xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>BRL</fullName>
    <isActive>true</isActive>
    <isCorporate>false</isCorporate>
    <decimalPlaces>2</decimalPlaces>
    <conversionRate>1.0</conversionRate>
</CurrencyType>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Código ISO da moeda |
| `isActive` | boolean | Moeda ativa |
| `isCorporate` | boolean | Moeda corporativa |
| `decimalPlaces` | int | Casas decimais |
| `conversionRate` | decimal | Taxa de conversão |
| `locale` | string | Locale |
| `symbol` | string | Símbolo |

### Cuidados de CTA

- Para operações financeiras, defina a moeda corporativa antes de criar registros.
- Advanced Currency Management altera o comportamento de taxas por data.
- Integrações bancárias devem definir explicitamente a moeda e a precisão esperada.

***

## 1.11 `AdvancedCurrencyManagementSettings`

### Finalidade

Habilita e configura o Advanced Currency Management, usado para taxas de câmbio por data.

### Local típico

```text
force-app/main/default/settings/AdvancedCurrencyManagement.settings
```

### Exemplo XML

```xml
<AdvancedCurrencyManagementSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableCurrencyEffectiveDates>true</enableCurrencyEffectiveDates>
</AdvancedCurrencyManagementSettings>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableCurrencyEffectiveDates` | boolean | Habilita datas efetivas |
| `enableCorrespondingCurrencyField` | boolean | Campo de moeda correspondente |

### Cuidados de CTA

- Ideal para forecasting histórico e relatórios multimoeda.
- Não é solução completa para câmbio em tempo real; para isso, use integração com serviço financeiro.
- Documente se a taxa é fixa, diária, mensal ou proveniente de ERP.

***

## 1.12 `DatedConversionRate`

### Finalidade

Representa uma taxa de conversão de moeda válida a partir de uma data.

### Estrutura XML

```xml
<DatedConversionRate xmlns="http://soap.sforce.com/2006/04/metadata">
    <isoCode>BRL</isoCode>
    <startDate>2026-01-01</startDate>
    <conversionRate>5.20</conversionRate>
</DatedConversionRate>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Identificador |
| `isoCode` | string | Moeda |
| `startDate` | date | Data inicial |
| `conversionRate` | decimal | Taxa |
| `nextStartDate` | date | Próxima data |
| `isCorporate` | boolean | Moeda corporativa |

### Cuidados de CTA

- Exige Advanced Currency Management.
- Não use para conversão em tempo real em transações bancárias.
- Para prevenção a fraude, registre a taxa usada no momento da transação, não apenas a taxa atual.

***

## 1.13 `FiscalYearSettings`

### Finalidade

Define o calendário fiscal da organização.

### Estrutura XML

```xml
<FiscalYearSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>FY2026</fullName>
    <name>FY2026</name>
    <startDate>2026-01-01</startDate>
    <endDate>2026-12-31</endDate>
    <isStandardYear>true</isStandardYear>
</FiscalYearSettings>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | API Name |
| `name` | string | Nome |
| `startDate` | date | Início |
| `endDate` | date | Fim |
| `isStandardYear` | boolean | Ano padrão |
| `periodId` | string | Período |
| `quarterId` | string | Trimestre |
| `weekId` | string | Semana |

### Cuidados de CTA

- Impacta forecasting, quotas, relatórios e Revenue Cloud.
- Mudanças tardias podem invalidar comparações históricas.
- Em grupos com múltiplos calendários, documente qual calendário é master.

***

## 1.14 `BusinessHoursSettings`

### Finalidade

Define horários comerciais usados por SLA, Entitlements, Cases, Campaigns e escalonamentos. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_companyprofilesettings.htm)

### Local típico

```text
force-app/main/default/settings/BusinessHours.settings
```

### Estrutura XML

```xml
<BusinessHoursSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <businessHours>
        <fullName>Horario_Comercial_BR</fullName>
        <active>true</active>
        <default>true</default>
        <name>Horário Comercial BR</name>
        <timeZoneId>America/Sao_Paulo</timeZoneId>
        <mondayStartTime>08:00:00.000Z</mondayStartTime>
        <mondayEndTime>18:00:00.000Z</mondayEndTime>
        <tuesdayStartTime>08:00:00.000Z</tuesdayStartTime>
        <tuesdayEndTime>18:00:00.000Z</tuesdayEndTime>
    </businessHours>
</BusinessHoursSettings>
```

### Propriedades do bloco `businessHours`

| Propriedade | Tipo | Obrigatória | Função |
|---|---|---|---|
| `fullName` | string | Sim | API Name |
| `name` | string | Sim | Nome único |
| `active` | string | Não | Ativo |
| `default` | string | Não | Horário padrão |
| `timeZoneId` | string | Sim | Fuso horário |
| `mondayStartTime` | string | Não | Início segunda |
| `mondayEndTime` | string | Não | Fim segunda |
| `tuesdayStartTime` | string | Não | Início terça |
| `tuesdayEndTime` | string | Não | Fim terça |
| `wednesdayStartTime` | string | Não | Início quarta |
| `wednesdayEndTime` | string | Não | Fim quarta |
| `thursdayStartTime` | string | Não | Início quinta |
| `thursdayEndTime` | string | Não | Fim quinta |
| `fridayStartTime` | string | Não | Início sexta |
| `fridayEndTime` | string | Não | Fim sexta |
| `saturdayStartTime` | string | Não | Início sábado |
| `saturdayEndTime` | string | Não | Fim sábado |
| `sundayStartTime` | string | Não | Início domingo |
| `sundayEndTime` | string | Não | Fim domingo |

A documentação confirma `businessHours`, `holidays`, `timeZoneId`, `name`, `active`, `default` e os horários por dia da semana. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_companyprofilesettings.htm)

### Cuidados de CTA

- Business Hours afetam cálculo de SLA, escalonamento e tempos de resposta.
- Para antifraude, normalmente o monitoramento é 24x7; para atendimento, pode ser 8x5.
- Documente se o SLA considera feriados, fuso do cliente ou fuso da operação.

***

## 1.15 `HolidaySettings`

### Finalidade

Define feriados que podem ser considerados por business hours, SLA e escalonamento. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_companyprofilesettings.htm)

### Estrutura XML

```xml
<HolidaySettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <holidays>
        <fullName>Feriado_Nacional</fullName>
        <name>Feriado Nacional</name>
        <description>Feriado nacional</description>
        <isRecurring>false</isRecurring>
        <activityDate>2026-12-25</activityDate>
        <businessHours>Horario_Comercial_BR</businessHours>
    </holidays>
</HolidaySettings>
```

### Propriedades do bloco `holidays`

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | API Name |
| `name` | string | Nome |
| `description` | string | Descrição |
| `isRecurring` | string | Recorrente |
| `activityDate` | string | Data, para não recorrente |
| `recurrenceStartDate` | string | Início da recorrência |
| `recurrenceEndDate` | string | Fim da recorrência |
| `startTime` | string | Hora inicial |
| `endTime` | string | Hora final |
| `recurrenceType` | picklist | Tipo de recorrência |
| `recurrenceInterval` | string | Intervalo |
| `recurrenceDayOfWeek` | picklist | Dia da semana |
| `recurrenceDayOfMonth` | string | Dia do mês |
| `recurrenceMonthOfYear` | picklist | Mês |
| `recurrenceInstance` | string | Instância |
| `businessHours` | string | Business hours associado |

### Valores de `recurrenceType`

| Valor | Significado |
|---|---|
| `RecursDaily` | Diário |
| `RecursEveryWeekday` | Dias úteis |
| `RecursWeekly` | Semanal |
| `RecursMonthly` | Mensal |
| `RecursMonthlyNth` | Mensal por posição |
| `RecursYearly` | Anual |
| `RecursYealyNth` | Anual por posição |

A documentação confirma os valores de recorrência, horários e associação a business hours. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_companyprofilesettings.htm)

### Cuidados de CTA

- Feriados regionais exigem modelagem por território ou business hours separados.
- Não trate feriado apenas como calendário: ele pode alterar SLA, roteamento e expectativa do cliente.
- Para operação 24x7, crie business hours próprios em vez de reutilizar horário comercial.

***

## 1.16 `SearchSettings`

### Finalidade

Define comportamento global da busca, incluindo opções de busca, sinônimos e promoções.

### Local típico

```text
force-app/main/default/settings/Search.settings
```

### Exemplo XML

```xml
<SearchSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableInContextSearch>true</enableInContextSearch>
    <enableRecentlyViewedSearch>true</enableRecentlyViewedSearch>
    <enableSynonymSuggestions>true</enableSynonymSuggestions>
</SearchSettings>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableInContextSearch` | boolean | Busca contextual |
| `enableRecentlyViewedSearch` | boolean | Busca por recentes |
| `enableSynonymSuggestions` | boolean | Sugestões de sinônimo |
| `enableSearchResultCaching` | boolean | Cache de resultados |
| `enableSuggestedRecords` | boolean | Registros sugeridos |

### Cuidados de CTA

- Em bases grandes, busca é um ponto de performance.
- Sinônimos melhoram experiência, mas podem gerar falsos positivos em antifraude.
- Para busca avançada, avalie Search Index, Data Cloud e sistemas externos.

***

## 1.17 `SynonymDictionary`

### Finalidade

Define sinônimos usados pela busca.

### Estrutura XML

```xml
<SynonymDictionary xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Sinonimos_Fraude</fullName>
    <label>Sinônimos de Fraude</label>
    <terms>
        <term>fraude</term>
        <term>estelionato</term>
        <term>golpe</term>
    </terms>
</SynonymDictionary>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | API Name |
| `label` | string | Rótulo |
| `terms` | complexo | Grupo de termos equivalentes |
| `term` | string | Termo individual |

### Cuidados de CTA

- Use para melhorar busca de casos, artigos e knowledge.
- Evite sinônimos ambíguos em processos regulatórios.
- Documente a origem do vocabulário: negócio, jurídico ou analytics.

***

## 1.18 `KnowledgeSettings`

### Finalidade

Configura o Salesforce Knowledge: idiomas, categorias, artigos, tradução e configurações de publicação.

### Local típico

```text
force-app/main/default/settings/Knowledge.settings
```

### Exemplo XML

```xml
<KnowledgeSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableKnowledge>true</enableKnowledge>
    <enableLightningKnowledge>true</enableLightningKnowledge>
    <languages>
        <language>en_US</language>
        <language>pt_BR</language>
    </languages>
</KnowledgeSettings>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableKnowledge` | boolean | Habilita Knowledge |
| `enableLightningKnowledge` | boolean | Lightning Knowledge |
| `languages` | complexo | Idiomas |
| `defaultLanguage` | string | Idioma padrão |
| `enableArticleManagement` | boolean | Gestão de artigos |
| `enableArticleSubscriptions` | boolean | Assinaturas |
| `enableExternalArticleContent` | boolean | Conteúdo externo |

### Cuidados de CTA

- Lightning Knowledge usa objetos e modelo diferente do Knowledge clássico.
- Para Agentforce, Knowledge é insumo direto para respostas.
- Defina governança de revisão, aprovação, expiração e tradução.

***

## 1.19 `DataCategoryGroup`

### Finalidade

Define categorias de dados usadas principalmente por Knowledge, Articles e conteúdo classificado.

### Estrutura XML

```xml
<DataCategoryGroup xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Categorias_Fraude</fullName>
    <label>Categorias de Fraude</label>
    <objectUsage>
        <entity>Knowledge__kav</entity>
    </objectUsage>
    <dataCategory>
        <name>Fraude_Cartao</name>
        <label>Fraude em Cartão</label>
    </dataCategory>
</DataCategoryGroup>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | API Name |
| `label` | string | Rótulo |
| `description` | string | Descrição |
| `objectUsage` | complexo | Objetos que usam a categoria |
| `entity` | string | Objeto |
| `dataCategory` | complexo | Categoria |
| `name` | string | Nome da categoria |
| `label` | string | Rótulo |
| `dataCategory` | complexo | Subcategoria |

### Cuidados de CTA

- Categorias são hierárquicas.
- Use taxonomia estável antes de publicar artigos.
- Para IA, categorias ajudam retrieval, mas não substituem governança de conteúdo.

***

## 1.20 `ContentSettings`

### Finalidade

Configura Files, Content, bibliotecas, versões e comportamento de conteúdo. 

### Local típico

```text
force-app/main/default/settings/Content.settings
```

### Exemplo XML

```xml
<ContentSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableContent>true</enableContent>
    <enableContentNotes>true</enableContentNotes>
    <enableFileUploadAndSync>true</enableFileUploadAndSync>
</ContentSettings>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableContent` | boolean | Habilita Content |
| `enableContentNotes` | boolean | Notas |
| `enableFileUploadAndSync` | boolean | Upload e sync |
| `enableFileSharing` | boolean | Compartilhamento |
| `enableFollowContent` | boolean | Seguir conteúdo |
| `enableContentTagging` | boolean | Tags |

### Cuidados de CTA

- Arquivos podem conter dados pessoais e sensíveis.
- Defina retenção, classificação, criptografia e acesso antes de habilitar upload amplo.
- Para antifraude, documentos de identidade exigem controle reforçado de acesso e auditoria.

***

## 1.21 `ContentAsset`

### Finalidade

Representa um asset reutilizável, geralmente imagem ou arquivo visual usado em Lightning, Experience Cloud e branding.

### Local típico

```text
force-app/main/default/contentassets/
```

### Estrutura XML

```xml
<ContentAsset xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Logo_Empresa</fullName>
    <language>en_US</language>
    <masterLabel>Logo Empresa</masterLabel>
    <originNetwork>Network</originNetwork>
    <versions>
        <version>
            <number>1</number>
            <pathOnClient>logo.png</pathOnClient>
            <zipEntryContent>...</zipEntryContent>
        </version>
    </versions>
</ContentAsset>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | API Name |
| `masterLabel` | string | Rótulo |
| `language` | string | Idioma |
| `originNetwork` | string | Rede de origem |
| `versions` | complexo | Versões |
| `version` | complexo | Versão individual |
| `number` | int | Número da versão |
| `pathOnClient` | string | Arquivo original |
| `zipEntryContent` | base64 | Conteúdo |
| `reasonForChange` | string | Motivo da alteração |

### Cuidados de CTA

- Assets são versionáveis e deployáveis.
- Evite colocar dados sensíveis em assets públicos.
- Para Experience Cloud, valide cache, CDN e acessibilidade.

***

## 1.22 `Document`

### Finalidade

Representa um documento armazenado em pasta, geralmente usado em cenários legados, templates e anexos.

### Estrutura XML

```xml
<Document xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Template_Contestacao</fullName>
    <contentType>application/pdf</contentType>
    <description>Template de contestação</description>
    <keywords>contestacao, fraude</keywords>
    <name>Template Contestação</name>
</Document>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | API Name |
| `contentType` | string | MIME type |
| `description` | string | Descrição |
| `keywords` | string | Palavras-chave |
| `name` | string | Nome |
| `folderId` | string | Pasta |
| `isPublic` | boolean | Público |
| `body` | base64 | Conteúdo |

### Cuidados de CTA

- Prefira `ContentVersion`, `ContentAsset` ou `StaticResource` em arquiteturas modernas.
- `Document` é mais comum em integrações legadas.
- Documente retenção e ciclo de vida.

***

## 1.23 `Folder`, `ReportFolder`, `DashboardFolder` e `EmailFolder`

### Finalidade

Organizam relatórios, dashboards, templates de e-mail e documentos.

### Estrutura XML de `ReportFolder`

```xml
<ReportFolder xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Fraude_Relatorios</fullName>
    <accessType>Shared</accessType>
    <name>Fraude Relatórios</name>
    <publicFolderAccess>ReadWrite</publicFolderAccess>
    <sharedTo>
        <roleAndSubordinates>Fraude_Analista</roleAndSubordinates>
    </sharedTo>
</ReportFolder>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | API Name |
| `name` | string | Nome |
| `accessType` | picklist | Acesso |
| `publicFolderAccess` | picklist | Acesso público |
| `sharedTo` | complexo | Compartilhamento |
| `folderShares` | complexo | Compartilhamentos |
| `folderAccess` | complexo | Acesso |

### Cuidados de CTA

- Pastas são parte da governança de BI.
- Compartilhamento de pasta não substitui segurança de dados.
- Em orgs grandes, padronize nomenclatura e ownership.

***

## 1.24 `BrandingSet`

### Finalidade

Define conjunto de propriedades visuais de branding.

### Estrutura XML

```xml
<BrandingSet xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Branding_Antifraude</fullName>
    <masterLabel>Branding Antifraude</masterLabel>
    <brandingSetProperty>
        <propertyName>NAV_BACKGROUND_COLOR</propertyName>
        <propertyValue>#0B5CAB</propertyValue>
    </brandingSetProperty>
</BrandingSet>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | API Name |
| `masterLabel` | string | Rótulo |
| `brandingSetProperty` | complexo | Propriedades |
| `propertyName` | string | Nome da propriedade |
| `propertyValue` | string | Valor |

### Cuidados de CTA

- Branding é deployável, mas deve ser versionado com cuidado.
- Cores e logos afetam Experience Cloud, Lightning e mobile.
- Para acessibilidade, valide contraste e legibilidade.

***

## 1.25 `LightningExperienceSettings`

### Finalidade

Configura comportamento global do Lightning Experience.

### Local típico

```text
force-app/main/default/settings/LightningExperience.settings
```

### Exemplo XML

```xml
<LightningExperienceSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableLightningExperience>true</enableLightningExperience>
</LightningExperienceSettings>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableLightningExperience` | boolean | Habilita Lightning |
| `enableLightningOnboarding` | boolean | Onboarding |
| `enableLightningForAllUsers` | boolean | Lightning para todos |
| `enableLightningPreview` | boolean | Preview |

### Cuidados de CTA

- Lightning é o padrão atual; Visualforce e Classic devem ser tratados como legado.
- Migração de Classic para Lightning exige revisão de layouts, botões, JavaScript e páginas.
- Não habilite recursos experimentais em produção sem avaliação de risco.

***

## 1.26 `LightningExperienceTheme`

### Finalidade

Define tema visual do Lightning Experience.

### Estrutura XML

```xml
<LightningExperienceTheme xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Tema_Antifraude</fullName>
    <defaultBrandingSet>Branding_Antifraude</defaultBrandingSet>
    <description>Tema do app antifraude</description>
    <masterLabel>Tema Antifraude</masterLabel>
    <shouldOverrideLoadingImage>false</shouldOverrideLoadingImage>
</LightningExperienceTheme>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | API Name |
| `masterLabel` | string | Rótulo |
| `description` | string | Descrição |
| `defaultBrandingSet` | string | Branding padrão |
| `shouldOverrideLoadingImage` | boolean | Sobrescreve imagem de loading |
| `shouldOverrideLoadingImageBackgroundColor` | boolean | Cor de fundo |
| `loadingImage` | string | Imagem |
| `pageColor` | string | Cor da página |

### Cuidados de CTA

- Tema deve ser consistente entre apps e Experience Cloud.
- Evite temas diferentes por time sem governança de design system.
- Versione assets junto com o tema.

***

## 1.27 `LightningOnboardingConfig`

### Finalidade

Configura onboarding e assistência no Lightning Experience.

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | API Name |
| `masterLabel` | string | Rótulo |
| `description` | string | Descrição |
| `enabled` | boolean | Habilitado |
| `context` | string | Contexto |
| `content` | complexo | Conteúdo |

### Cuidados de CTA

- Útil para adoção, mas não deve substituir treinamento estruturado.
- Em operações críticas, onboarding deve reforçar regras de compliance.

***

## 1.28 `MobileSettings`

### Finalidade

Define configurações gerais de mobile.

### Local típico

```text
force-app/main/default/settings/Mobile.settings
```

### Exemplo XML

```xml
<MobileSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableMobileAdmin>false</enableMobileAdmin>
</MobileSettings>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableMobileAdmin` | boolean | Administração mobile |
| `enableMobilePush` | boolean | Push |
| `enableMobileSecurity` | boolean | Segurança mobile |

### Cuidados de CTA

- Mobile amplia superfície de ataque.
- Combine MFA, device policy, session timeout e restrição de dados sensíveis.
- Para field service, valide offline e sincronização.

***

## 1.29 `MobileApplicationDetail`

### Finalidade

Define detalhes de aplicativo mobile associado à org.

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | API Name |
| `applicationLabel` | string | Rótulo |
| `applicationBundleId` | string | Bundle ID |
| `applicationVersion` | string | Versão |
| `platform` | picklist | Plataforma |
| `version` | string | Versão |
| `description` | string | Descrição |

### Cuidados de CTA

- Versionamento de app mobile deve estar alinhado ao release da org.
- Mudanças de API podem quebrar versões antigas do app.
- Defina política de backward compatibility.

***

## 1.30 `ConnectedAppSettings`

### Finalidade

Configurações globais de Connected Apps.

### Local típico

```text
force-app/main/default/settings/ConnectedApp.settings
```

### Exemplo XML

```xml
<ConnectedAppSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableAdminCanApproveConnectedApps>false</enableAdminCanApproveConnectedApps>
</ConnectedAppSettings>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableAdminCanApproveConnectedApps` | boolean | Admin aprova apps |
| `enableAdminCanManageConnectedApps` | boolean | Admin gerencia apps |
| `enableAdminCanCreateConnectedApps` | boolean | Admin cria apps |

### Cuidados de CTA

- Connected Apps são pontos críticos de identidade e acesso.
- Restrinja criação e aprovação a administradores especializados.
- Monitore scopes, callbacks e permissões concedidas.

***

## 1.31 `DevHubSettings`

### Finalidade

Habilita e configura o Dev Hub, usado para criar e gerenciar Scratch Orgs e pacotes.

### Local típico

```text
force-app/main/default/settings/DevHub.settings
```

### Exemplo XML

```xml
<DevHubSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableUnlockedPackages>true</enableUnlockedPackages>
    <enableSecondGenerationPackaging>true</enableSecondGenerationPackaging>
</DevHubSettings>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableUnlockedPackages` | boolean | Unlocked Packages |
| `enableSecondGenerationPackaging` | boolean | 2GP |
| `enableNamespaceRegistry` | boolean | Namespace registry |
| `enableSourceTracking` | boolean | Source tracking |

### Cuidados de CTA

- Dev Hub é base para DevOps Center, 2GP e modularização.
- Não habilite recursos de pacote em produção sem governança.
- Defina estratégia de namespace antes de publicar pacotes.

***

## 1.32 `ScratchOrgInfo`

### Finalidade

Representa informações de uma Scratch Org criada a partir do Dev Hub.

### Estrutura XML

```xml
<ScratchOrgInfo xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Scratch_Antifraude</fullName>
    <adminEmail>admin@empresa.com</adminEmail>
    <country>BR</country>
    <edition>Developer</edition>
    <expirationDate>2026-12-31</expirationDate>
    <hasSampleData>true</hasSampleData>
    <orgName>Antifraude Scratch</orgName>
</ScratchOrgInfo>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | API Name |
| `adminEmail` | string | E-mail do admin |
| `country` | string | País |
| `description` | string | Descrição |
| `edition` | string | Edição |
| `expirationDate` | date | Expiração |
| `features` | string | Features |
| `hasSampleData` | boolean | Dados de exemplo |
| `language` | string | Idioma |
| `orgName` | string | Nome |
| `settings` | complexo | Settings |
| `snapshot` | string | Snapshot |

### Cuidados de CTA

- Scratch Orgs são efêmeras.
- Use definição de Scratch Org versionada no repositório.
- Não trate Scratch Org como ambiente de longa duração.

***

## 1.33 `SourceTrackingSettings`

### Finalidade

Configura source tracking, usado para comparar mudanças entre Scratch Org e projeto SFDX.

### Exemplo XML

```xml
<SourceTrackingSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableSourceTracking>true</enableSourceTracking>
</SourceTrackingSettings>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableSourceTracking` | boolean | Habilita tracking |

### Cuidados de CTA

- Source tracking é excelente para desenvolvimento, não para auditoria de produção.
- Use Git como fonte de verdade definitiva.
- Combine com testes, code review e pipeline.

***

## 1.34 `ReleaseManagementSettings`

### Finalidade

Configura comportamento de release management.

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableReleaseManagement` | boolean | Habilita release management |
| `enableReleaseUpdate` | boolean | Release updates |
| `enableReleaseVersioning` | boolean | Versionamento |

### Cuidados de CTA

- Release management deve definir janelas, rollback, comunicação e critérios de go/no-go.
- Metadados não substituem plano de release.
- Para produtos separados, como Marketing Cloud e B2C Commerce, o ciclo de release é independente.

***

## 1.35 `DeploymentSettings`

### Finalidade

Configura comportamento de deploy.

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableDeployment` | boolean | Habilita deploy |
| `enableDeploymentValidation` | boolean | Validação |
| `enableRollback` | boolean | Rollback |
| `deploymentOptions` | complexo | Opções |

### Cuidados de CTA

- Deploy não é apenas “mover arquivo”: envolve dependências, testes, dados e ordem.
- Para objetos com Master-Detail, campos obrigatórios e sharing, a ordem importa.
- Em pipelines, valide em sandbox antes de produção.

***

## 1.36 `PackageSettings`

### Finalidade

Configura comportamento de pacotes na org.

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enablePackages` | boolean | Habilita pacotes |
| `enablePackageVersioning` | boolean | Versionamento |
| `enablePackageDependencies` | boolean | Dependências |

### Cuidados de CTA

- Pacotes reduzem acoplamento, mas exigem estratégia de versionamento.
- 1GP, 2GP, unlocked e managed packages têm regras diferentes.
- Para ISVs, namespace e compatibilidade são decisões críticas.

***

## 1.37 `UserInterfaceSettings`

### Finalidade

Configurações gerais de interface.

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableUserInterface` | boolean | Interface |
| `enableEnhancedProfileUserInterface` | boolean | UI de perfil |
| `enableEnhancedPageLayoutEditor` | boolean | Editor de layout |
| `enableInlineEditing` | boolean | Edição inline |

### Cuidados de CTA

- Configurações de UI afetam produtividade, mas também risco operacional.
- Edição inline pode facilitar mudanças acidentais em registros críticos.
- Alinhe com permissões, validações e auditoria.

***

## 1.38 `UserEngagementSettings`

### Finalidade

Configura recursos de engajamento e adoção do usuário.

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableUserEngagement` | boolean | Engajamento |
| `enableInAppGuidance` | boolean | Guidance |
| `enablePrompts` | boolean | Prompts |
| `enableWalkthroughs` | boolean | Walkthroughs |

### Cuidados de CTA

- Prompts e walkthroughs ajudam adoção.
- Evite poluir telas críticas de operação.
- Meça adoção com analytics antes de expandir.

***

## 1.39 `PathAssistantSettings`

### Finalidade

Configura o Path Assistant globalmente.

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enablePathAssistant` | boolean | Habilita Path |
| `enablePathAssistantForAllUsers` | boolean | Para todos |

### Cuidados de CTA

- Path é guia visual, não regra de negócio.
- Não use Path para validação crítica.
- Combine com Flow, validation rules e approval process.

***

## 1.40 `ActivitiesSettings`

### Finalidade

Configura tarefas, eventos, calendário e atividades.

### Exemplo XML

```xml
<ActivitiesSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <allowUsersToRelateMultipleContactsToTasksAndEvents>true</allowUsersToRelateMultipleContactsToTasksAndEvents>
    <enableActivityReminders>true</enableActivityReminders>
    <enableClickCreateEvents>true</enableClickCreateEvents>
    <enableDragAndDropScheduling>true</enableDragAndDropScheduling>
    <enableGroupTasks>true</enableGroupTasks>
    <enableLogEmail>true</enableLogEmail>
    <enableRecurringEvents>true</enableRecurringEvents>
    <enableRecurringTasks>true</enableRecurringTasks>
    <enableSimpleTaskCreation>true</enableSimpleTaskCreation>
    <enableSidebarCalendarShortcut>false</enableSidebarCalendarShortcut>
    <enableUserManagement>0</enableUserManagement>
</ActivitiesSettings>
```

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `allowUsersToRelateMultipleContactsToTasksAndEvents` | boolean | Múltiplos contatos |
| `enableActivityReminders` | boolean | Lembretes |
| `enableClickCreateEvents` | boolean | Criar evento por clique |
| `enableDragAndDropScheduling` | boolean | Arrastar e soltar |
| `enableDatedConversionRates` | boolean | Taxas por data |
| `enableGroupTasks` | boolean | Tarefas em grupo |
| `enableLogEmail` | boolean | Log de e-mail |
| `enableRecurringEvents` | boolean | Eventos recorrentes |
| `enableRecurringTasks` | boolean | Tarefas recorrentes |
| `enableSimpleTaskCreation` | boolean | Criação simples |
| `enableSidebarCalendarShortcut` | boolean | Atalho de calendário |
| `enableUserManagement` | string | Gestão de usuário |
| `showEventDetailsMultiUserView` | boolean | Detalhes multiusuário |
| `showHomePageHoverLinksForEvents` | boolean | Hover links |

### Cuidados de CTA

- Atividades são base para cadência comercial, atendimento e auditoria.
- Em antifraude, tarefas podem registrar ações do analista.
- Evite usar Task como repositório de decisão crítica sem objeto próprio.

***

## 1.41 `ActivitySettings`

### Finalidade

Configurações adicionais de atividades.

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableActivityCapture` | boolean | Captura de atividade |
| `enableEmailTracking` | boolean | Tracking |
| `enableEventLogging` | boolean | Log |

### Cuidados de CTA

- Captura automática de atividade pode gerar volume alto de dados.
- Avalie privacidade, consentimento e retenção.
- Em setor financeiro, alinhe com política de comunicação com cliente.

***

## 1.42 `CalendarSettings`

### Finalidade

Configura calendários da organização.

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableCalendar` | boolean | Calendário |
| `enableCalendarSharing` | boolean | Compartilhamento |
| `defaultCalendarView` | picklist | Visualização padrão |

### Cuidados de CTA

- Calendário deve respeitar fuso horário e business hours.
- Em Field Service, calendário se conecta a agendamento e capacidade.
- Para auditoria, registre quem alterou agendamentos.

***

## 1.43 `EventSettings`

### Finalidade

Configurações de eventos.

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableEventLogging` | boolean | Log |
| `enableEventNotifications` | boolean | Notificações |
| `enableEventReminders` | boolean | Lembretes |

### Cuidados de CTA

- Eventos de calendário não são Platform Events.
- Não confunda `Event` de agenda com `PlatformEvent` de integração.
- Para integração orientada a eventos, use `PlatformEvent`, `ChangeDataCapture` ou `PushTopic`.

***

## 1.44 `TaskSettings`

### Finalidade

Configurações de tarefas.

### Propriedades principais

| Propriedade | Tipo | Função |
|---|---|---|
| `fullName` | string | Nome do componente |
| `enableTaskReminders` | boolean | Lembretes |
| `enableTaskNotifications` | boolean | Notificações |
| `defaultTaskStatus` | picklist | Status padrão |
| `defaultTaskPriority` | picklist | Prioridade padrão |

### Cuidados de CTA

- Tarefa é ferramenta operacional, não fonte de verdade de decisão.
- Para workflow regulatório, prefira objeto customizado com histórico.
- Use Queue e assignment rules para distribuição.

***

# 2. Padrão de documentação para os próximos grupos

Para manter consistência no material, cada metadata type deve ter esta ficha:

```markdown
## Metadata type: NomeDoTipo

### Finalidade
O que ele representa.

### Local do arquivo
Caminho padrão no projeto SFDX.

### Estrutura XML
Exemplo mínimo funcional.

### Propriedades principais
Tabela com propriedade, tipo, obrigatoriedade e função.

### Blocos complexos
Listas, filhos e relacionamentos.

### Valores possíveis
Enums e picklists relevantes.

### Exemplo completo
XML funcional.

### Impacto em CTA
Segurança, dados, integração, performance, deploy e governança.

### Erros comuns
Armadilhas práticas.

### Fonte oficial
Link ou referência do Metadata API Developer Guide.
```

***

# 3. Ordem sugerida dos próximos capítulos

Depois deste Grupo 1, a sequência mais didática é:

```text
Grupo 2 — Dados, objetos e modelo relacional
Grupo 3 — Segurança, identidade, acesso e sharing
Grupo 4 — Automação declarativa e programática
Grupo 5 — Interface, apps e experiência
Grupo 6 — Integração, APIs, eventos e mensageria
Grupo 7 — DevOps, pacotes, deploy e SDLC
Grupo 8 — Nuvens do CORE
Grupo 9 — Marketing Cloud
Grupo 10 — B2C Commerce
Grupo 11 — MuleSoft, Tableau, Slack, Data Cloud e Agentforce
```

A documentação oficial do Metadata API é a referência-base: ela explica que um metadata component é uma instância de um metadata type e que seus fields e valores também são metadata.  Para o grupo de configurações, a referência oficial confirma que `Settings` agrupa configurações como `MyDomainSettings`, e que esses arquivos `.settings` têm comportamento próprio de um componente por configuração. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_settings.htm)
