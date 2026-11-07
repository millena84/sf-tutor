A CTA **não é uma certificação de uma nuvem específica**: ela avalia sua capacidade de arquitetar soluções no **núcleo Salesforce Platform** e integrá-lo aos produtos do ecossistema. Na prática, o centro do exame é a plataforma compartilhada — Sales, Service, Experience, Platform, dados, segurança, integração, identidade e SDLC — enquanto produtos adquiridos ou mais especializados aparecem como **fronteiras de integração**. [trailhead.salesforce](https://trailhead.salesforce.com/en/credentials/technicalarchitect)

## O que a CTA cobre diretamente

| Área | Nuvens/capacidades normalmente no escopo | Papel na arquitetura |
|---|---|---|
| **Core Platform** | Salesforce Platform, Lightning Platform, Apex, LWC, Flow, Metadata, APIs, governor limits | Base técnica comum da solução |
| **CRM operacional** | Sales Cloud, Service Cloud, Field Service, Revenue/Life Sciences conforme cenário | Processos de vendas, atendimento, campo e receita |
| **Experiência digital** | Experience Cloud, sites/portais, Mobile, Slack como canal | Usuários externos, parceiros e colaboração |
| **Dados e analytics** | Data model, Data Cloud, CRM Analytics/Tableau, reporting | Modelo de dados, qualidade, governança e insights |
| **Segurança e identidade** | Users, Profiles, Permission Sets, Sharing, SSO, OAuth, MFA, Shield | Acesso, conformidade e proteção de dados |
| **Integração** | APIs, Platform Events, CDC, MuleSoft, Salesforce Connect, middleware | Comunicação entre Salesforce e sistemas externos |
| **DevOps** | Sandboxes, Scratch Orgs, Metadata API, SFDX, CI/CD, testes | Entrega segura e repetível |

As certificações que habilitam a CTA cobrem exatamente esses eixos: **Application Architect** concentra-se em plataforma, dados, sharing e desenvolvimento; **System Architect** concentra-se em integração, identidade e ciclo de vida/deployment. [trailhead.salesforce](https://trailhead.salesforce.com/en/credentials/architectreviewboard)

## O que costuma ficar “fora do core”

Não significa que a CTA ignore esses produtos: eles podem aparecer em um cenário de Review Board, mas normalmente são tratados como **sistemas integrados**, com decisões de contrato de API, sincronização, identidade, latência e resiliência.

| Produto | Relação com o core | Como normalmente se integra |
|---|---|---|
| **Marketing Cloud Engagement** | Produto separado, com conta, business units e dados próprios | Marketing Cloud Connect, APIs, SFTP, data extensions, eventos |
| **B2C Commerce** | Plataforma de e-commerce separada, com instâncias/realm próprios | APIs/OCAPI, conectores, Order Management, middleware |
| **B2B/D2C Commerce** | Mais próximo do core, mas com variações por produto | Objetos, APIs, Order Management e integrações |
| **MuleSoft** | Plataforma de integração separada | APIs gerenciadas, conectores, orquestração e governança |
| **Tableau** | Produto de analytics separado | Conectores, extração, embedded analytics, CRM Analytics |
| **Slack** | Produto colaborativo separado | Apps, workflows, APIs, notificações e ações no Slack |
| **Data Cloud** | Camada de dados/customer profile integrada, mas com arquitetura própria | Data streams, identity resolution, segmentos, ativação |
| **Agentforce/Einstein** | Capacidades de IA sobre dados e fluxos da plataforma | Prompts, agentes, ações, dados e governança |

O Slack, Tableau e MuleSoft funcionam como produtos autônomos que também são integrados ao Customer 360; o Flow e as APIs da plataforma são formas comuns de conectá-los aos processos do core. [trailhead.salesforce](https://trailhead.salesforce.com/en/credentials/technicalarchitect)

## Mesma instância x instâncias diferentes

**Analogia:** o core Salesforce é como um condomínio: Sales, Service, Experience e suas automações moram no mesmo “apartamento” — a sua **Salesforce Org**. Marketing Cloud, B2C Commerce, MuleSoft e Tableau são prédios vizinhos: podem pertencer ao mesmo ecossistema, mas possuem endereço, portaria, banco de dados e regras próprias.

| Grupo | Normalmente na mesma org/instância lógica | Observação |
|---|---|---|
| **Core Salesforce** | Sales Cloud, Service Cloud, Experience Cloud, Platform, Flow, Apex, LWC, Chatter, Reports/Dashboards | Compartilham objetos, permissões, metadados, APIs e a mesma org |
| **CRM Analytics** | Pode conviver no core, mas com datasets e assets próprios | Integra-se a objetos e dados do core |
| **Data Cloud** | Integra-se fortemente ao core, mas é uma camada de dados própria | Não deve ser tratada como “mais uma tabela” do core |
| **Marketing Cloud** | Instância/conta separada, organizada em business units | A integração com o CRM é explícita e pode ser multi-org.  [trailhead.salesforce](https://trailhead.salesforce.com/trailblazer-community/feed/0D54V00007T4MuPSAV) |
| **B2C Commerce** | Instâncias separadas dentro de um realm de Commerce | Usa APIs e conectores para trocar pedido, cliente e catálogo.  [help.salesforce](https://help.salesforce.com/s/articleView?id=000389453&language=no&type=1) |
| **MuleSoft** | Runtime/plataforma separada | Atua como camada de integração e governança de APIs |
| **Tableau** | Serviço separado | Consome dados via conectores, extrações ou integrações |
| **Slack** | Serviço separado | Integra-se por apps, workflows, eventos e APIs |

## Como isso aparece na CTA

Em um caso de CTA, a pergunta não é “qual nuvem eu uso?”, mas:

1. **Onde o dado é master?** Core, Marketing Cloud, Commerce, ERP ou Data Cloud?
2. **Qual é a latência exigida?** Tempo real, quase real, batch noturno ou evento.
3. **Como autenticamos?** SSO, OAuth, JWT, Connected App, Named Credential ou service account.
4. **O que acontece se um lado cair?** Retry, fila, dead-letter, reprocessamento e conciliação.
5. **Como governamos o deploy?** Cada produto tem ciclo de release, ambiente e ferramenta próprios.
6. **Como isolamos dados e permissões?** Especialmente entre usuários internos, parceiros, clientes e sistemas.

## Exemplo prático: antifraude

Imagine um caso de transação suspeita:

- A transação chega por **API/evento** no core Salesforce.
- Um **Flow ou Apex** cria um `Fraud Case__c`.
- O **Service Cloud** mostra o caso ao analista.
- O **Data Cloud** unifica cliente, dispositivo e histórico.
- O **MuleSoft** consulta o motor antifraude e o core bancário.
- O **Slack** notifica o time de risco.
- O **Tableau** analisa padrões e falsos positivos.

Aqui, o **core é a orquestração do caso**, mas a solução só é arquiteturalmente correta se você definir dono do dado, contrato de evento, autenticação, latência, fallback e ciclo de release de cada produto.

Em resumo: **CTA cobre profundamente o core Salesforce e, de forma arquitetural, a integração com as demais nuvens**. Sales, Service e Experience normalmente compartilham a mesma org; Marketing Cloud, B2C Commerce, MuleSoft, Tableau e Slack costumam ser instâncias/produtos separados, conectados por APIs, eventos e integrações controladas. [trailhead.salesforce](https://trailhead.salesforce.com/en/credentials/technicalarchitect)
