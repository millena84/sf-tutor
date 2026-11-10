# Order of Execution no Salesforce

## Objetivo

Este documento consolida o **Order of Execution** do Salesforce, incluindo a sequência de execução das automações, os **Governor Limits** e as boas práticas de arquitetura para uma organização Salesforce moderna.

O **Order of Execution** define *quando* cada regra, Flow, Trigger, Workflow e processo roda durante uma operação de gravação. Os **Governor Limits** definem *quanto* cada transação pode consumir de recursos como SOQL, DML, CPU, heap, chamadas externas e e-mails.

> Analogia: o Order of Execution é a **fila de produção** da fábrica. Os Governor Limits são os **limites de matéria-prima, energia e tempo** disponíveis para produzir tudo dentro da mesma ordem.

## Quando o Order of Execution é aplicado

A sequência é aplicada a operações de gravação como:

- `insert`
- `update`
- `upsert`
- `delete`
- `undelete`

Ela vale para gravações feitas por:

- Interface de usuário
- API
- Apex DML
- Importações
- Ferramentas de migração
- Automações que executam DML

## Visão geral

```text
Usuário / API / Apex envia dados
                |
                v
Validações iniciais
                |
                v
Before-save Flow
                |
                v
Before Trigger
                |
                v
Validation Rules
                |
                v
Duplicate Rules
                |
                v
Gravação temporária no banco
                |
                v
After Trigger
                |
                v
Assignment / Auto-Response / Workflow
                |
                v
Process Builder / Flows acionados por Workflow
                |
                v
After-save Flow
                |
                v
Entitlement Rules
                |
                v
Roll-up Summary no pai
                |
                v
Roll-up Summary no avô
                |
                v
Criteria-Based Sharing
                |
                v
Commit
                |
                v
Pós-commit assíncrono
```

## Sequência completa

A sequência abaixo segue a documentação atual do **Apex Developer Guide** da Salesforce para `insert`, `update` e `upsert`.

| Ordem | Etapa | O que acontece | Governor Limits relevantes |
|---:|---|---|---|
| 1 | Carrega o registro original | O Salesforce lê a versão atual do registro no banco. Em `insert`, inicializa o novo registro. Em `upsert`, inicializa o registro se ele não existir. | SOQL executado antes pode consumir o limite de 100 queries em Apex síncrono ou 200 em assíncrono. |
| 2 | Aplica os novos valores | Os valores enviados pela UI, API ou Apex substituem os valores antigos nos campos. | O tamanho do payload pode impactar consumo de heap e chamadas externas. |
| 3 | Executa validações iniciais do sistema | Verifica layout, campos obrigatórios, formatos, tamanho máximo e regras específicas conforme a origem da requisição. Em API/Apex, valida chaves estrangeiras, formatos e picklists restritas. | Não é um Governor Limit Apex, mas falhas aqui impedem o avanço da transação. |
| 4 | Executa Record-Triggered Flows **Before Save** | Flows rápidos executados antes da gravação. Servem para calcular ou corrigir campos no próprio registro, sem executar DML. | O Apex invocado pelo Flow consome SOQL, DML, CPU, heap e callouts da mesma transação. |
| 5 | Executa todos os **Before Triggers** | Executam `before insert`, `before update`, `before delete` e `before undelete`. É o local para alterar campos do próprio registro antes da gravação. | SOQL: 100 síncrono / 200 assíncrono. DML: 150 statements. CPU: 10.000 ms síncrono. Heap: 10 MB síncrono. |
| 6 | Executa validações novamente | O Salesforce roda novamente a maior parte das validações de sistema e as Validation Rules customizadas. | A Validation Rule enxerga o registro já alterado por Before-save Flow e Before Trigger. |
| 7 | Executa Duplicate Rules | Se a regra de duplicidade estiver configurada para bloquear, o registro não é salvo e as etapas seguintes não acontecem. | Pode acionar Apex ou Flow, que compartilham os limites da transação. |
| 8 | Salva o registro no banco, sem commit | O registro recebe um ID, mas a transação ainda não está confirmada. Se algo falhar depois, a operação pode ser revertida. | O DML já consome o limite de 150 statements e até 10.000 registros processados por transação. |
| 9 | Executa todos os **After Triggers** | Executam `after insert`, `after update`, `after delete` e `after undelete`. É o local para lógica que precisa do ID ou para criar/atualizar outros registros. | É o ponto crítico de SOQL em loop, DML em loop, CPU e heap. |
| 10 | Executa Assignment Rules | Distribuem Lead ou Case para usuário ou fila conforme critérios. | Pode disparar automações que consomem limites da transação. |
| 11 | Executa Auto-Response Rules | Envia respostas automáticas para Lead ou Case conforme critérios. | E-mails podem consumir o limite de 10 chamadas `sendEmail` por transação. |
| 12 | Executa Workflow Rules | Regras legadas que podem disparar ações imediatas, incluindo Field Updates. | Um Field Update reexecuta `before update` e `after update` triggers uma vez adicional. |
| 13 | Executa Process Builder e Flows acionados por Workflow | Executam automações sem ordem garantida entre si. | Cada DML disparado pode iniciar outro ciclo de save e consumir novamente SOQL, DML, CPU e heap. |
| 14 | Executa Record-Triggered Flows **After Save** | Executam após o registro ter sido gravado, mas antes do commit final. | É um ponto comum de estouro de SOQL e DML quando o Flow consulta ou atualiza registros em loop. |
| 15 | Executa Entitlement Rules | Aplicam regras de entitlement, relevantes em cenários de serviço e SLA. | Pode disparar lógica que consome limites da transação. |
| 16 | Recalcula Roll-up Summary no pai | Se o registro tem roll-up summary ou participa de cross-object workflow, o Salesforce recalcula e atualiza o campo no registro pai. | O pai passa por outro processo de gravação, podendo consumir DML e disparar triggers. |
| 17 | Recalcula Roll-up Summary no avô | Se a atualização do pai impactar um avô com roll-up summary ou cross-object workflow, o Salesforce recalcula e atualiza também o registro do avô. | Pode amplificar o consumo de DML e CPU em cadeias de relacionamento. |
| 18 | Executa Criteria-Based Sharing | Avalia regras de compartilhamento baseadas em critérios. | Pode gerar operações de compartilhamento, mas não é um Governor Limit Apex. |
| 19 | Executa o commit | Confirma todas as operações DML da transação. | Se algum limite for estourado antes, a transação falha e o DML é revertido. |
| 20 | Executa lógica pós-commit | Executa e-mails, Apex assíncrono, `Queueable`, `@future` e asynchronous paths de Record-Triggered Flows. | Aqui começam limites assíncronos e diários por organização. |

## Onde cada automação entra

| Automação | Quando roda | Uso recomendado |
|---|---|---|
| Before-save Flow | Antes dos Before Triggers e das Validation Rules customizadas. | Calcular ou preencher campos do próprio registro. |
| Before Trigger | Depois do Before-save Flow e antes das Validation Rules. | Normalizar dados, aplicar regras de negócio e modificar campos do próprio registro. |
| Validation Rule | Depois de Before-save Flow e Before Trigger. | Bloquear o salvamento quando uma regra de negócio não for atendida. |
| Duplicate Rule | Depois das validações customizadas. | Impedir duplicidade ou alertar o usuário. |
| After Trigger | Após a gravação temporária, antes do commit. | Criar registros relacionados, usar o ID do registro e executar lógica dependente do ID. |
| Assignment Rule | Depois de After Trigger. | Distribuir Lead ou Case para usuário ou fila. |
| Auto-Response Rule | Depois de After Trigger. | Enviar resposta automática para Lead ou Case. |
| Workflow Rule | Depois de After Trigger. | Tecnologia legada; Field Updates podem reexecutar triggers uma vez. |
| Process Builder | Depois de Workflow Rules. | Tecnologia legada; migrar para Record-Triggered Flow. |
| After-save Flow | Depois de Workflow Rules e Process Builder. | Automação moderna pós-gravação, criação de tarefas, atualizações relacionadas e integrações. |
| Entitlement Rule | Depois de After-save Flow. | Aplicar regras de serviço e SLA. |
| Roll-up Summary | Após After-save Flow. | Atualizar totais no pai, como soma de oportunidades em uma Account. |
| Criteria-Based Sharing | Após roll-ups. | Avaliar regras de compartilhamento baseadas em critérios. |
| Commit | Após todas as etapas anteriores. | Confirmar definitivamente a transação. |
| Post-commit | Após o commit. | E-mails, Queueable, `@future`, Platform Events e asynchronous paths. |

## Governor Limits essenciais

Governor Limits existem porque o Apex roda em um ambiente multitenant. Eles impedem que uma transação consuma recursos excessivos e prejudique outras organizações na plataforma.

| Recurso | Limite síncrono | Limite assíncrono | Impacto prático |
|---|---:|---:|---|
| SOQL queries | 100 | 200 | Consultas dentro de loops estouram rapidamente. |
| Registros retornados por SOQL | 50.000 | 50.000 | Consultas amplas podem retornar muitas linhas. |
| Registros por `Database.getQueryLocator` | 10.000 | 10.000 | Relevante em Batch Apex. |
| SOSL queries | 20 | 20 | Buscas textuais consomem limite próprio. |
| Registros retornados por SOSL | 2.000 | 2.000 | Limite por consulta. |
| DML statements | 150 | 150 | `insert`, `update`, `delete`, `merge`, `undelete` e `Approval.process` contam. |
| Registros processados por DML | 10.000 | 10.000 | Inserir 10.001 registros em uma transação falha. |
| Profundidade de recursão de triggers | 16 | 16 | Evita loops infinitos entre triggers. |
| Callouts HTTP/web service | 100 | 100 | Integrações em massa exigem Queueable ou Batch. |
| Tempo total de callouts | 120 segundos | 120 segundos | Cada chamada tem timeout padrão de 10 segundos. |
| `@future` methods | 50 | 0 em Batch/Future; 50 em Queueable | Não é possível chamar `@future` a partir de Batch ou de outro `@future`. |
| `System.enqueueJob` | 50 | 1 | Limite de Queueable enfileirados. |
| `sendEmail` | 10 | 10 | Limite de chamadas de e-mail por transação. |
| Heap size | 10 MB | 25 MB | Listas, maps e strings grandes podem estourar. |
| CPU time | 10.000 ms | 60.000 ms | Inclui Apex, código de pacotes e workflows; não inclui tempo de espera de banco ou callout. |
| Tempo máximo de transação | 10 minutos | 10 minutos | Limite total de execução. |

## Pontos que costumam confundir

### Validation Rule roda depois de Flows e Triggers

Validation Rules customizadas rodam depois do **Before-save Flow** e do **Before Trigger**. Portanto, um campo corrigido ou calculado antes pode evitar ou disparar um erro de validação.

```text
Before-save Flow
        |
        v
Before Trigger
        |
        v
Validation Rule
```

### O registro já tem ID no After Trigger

No **After Trigger**, o registro já recebeu ID, mas a transação ainda não foi confirmada. Por isso, ele é adequado para criar registros relacionados, mas não garante que a transação será commitada.

### Workflow Field Update reexecuta Triggers

Quando um Workflow Rule atualiza um campo, o Salesforce roda novamente os `before update` e `after update` triggers, **apenas uma vez adicional**.

Nessa reexecução, não rodam novamente:

- Validation Rules customizadas
- Flows
- Duplicate Rules
- Process Builder
- Escalation Rules

### Vários Triggers não têm ordem garantida

Dois `before insert` triggers do mesmo objeto podem executar em qualquer ordem. A boa prática é ter **um Trigger por objeto e evento**, delegando a lógica para um Trigger Handler.

### Recursão limita reexecuções

Em um save recursivo, os passos 9 a 17 são ignorados. Isso limita reexecuções de assignment, auto-response, workflow, escalation, after-save flow, entitlement e roll-ups durante a recursão.

### `Trigger.old` não representa o valor imediatamente anterior

`Trigger.old` mantém o valor original antes da primeira atualização do registro. Ele não representa necessariamente o valor imediatamente anterior ao Field Update de um Workflow.

## Exemplo prático: Opportunity

Suponha uma `Opportunity` com:

- `Amount`
- `Probability`
- `StageName`
- Before-save Flow que calcula `Expected_Revenue__c`
- Before Trigger que normaliza o estágio
- Validation Rule que impede valor negativo
- After-save Flow que cria uma Task quando a oportunidade é fechada

A sequência seria:

```text
1. Salesforce carrega a Opportunity atual
2. Aplica os valores enviados
3. Validações iniciais
4. Before-save Flow calcula Expected_Revenue__c
5. Before Trigger normaliza StageName
6. Validation Rule valida Amount e os campos já alterados
7. Duplicate Rule, se configurada
8. Registro é gravado temporariamente e recebe ID
9. After Trigger, se existir
10. Assignment / Auto-response / Workflow, se existirem
11. After-save Flow cria a Task
12. Roll-up na Account é recalculado, se aplicável
13. Sharing é avaliado
14. Commit
15. E-mails, Queueable e async paths rodam depois
```

## Exemplo de código: Before Trigger

Cenário: normalizar o estágio de uma Opportunity antes da gravação.

```apex
trigger OpportunityTrigger on Opportunity (before insert, before update) {
    for (Opportunity opp : Trigger.new) {
        if (opp.StageName == 'Closed Won') {
            opp.Probability = 100;
        }
    }
}
```

Neste exemplo:

- O Trigger roda antes da gravação.
- Ele altera apenas campos do próprio registro.
- Não há DML, portanto não consome o limite de DML.
- Se houver SOQL dentro do Trigger, ela consome o limite de SOQL da transação.

## Exemplo de código: After Trigger

Cenário: criar uma Task quando uma Opportunity é fechada.

```apex
trigger OpportunityTrigger on Opportunity (after update) {
    List<Task> tasks = new List<Task>();

    for (Opportunity opp : Trigger.new) {
        Opportunity oldOpp = Trigger.oldMap.get(opp.Id);

        Boolean wasClosed = oldOpp.IsClosed;
        Boolean isClosed = opp.IsClosed;

        if (!wasClosed && isClosed) {
            tasks.add(new Task(
                Subject = 'Follow-up da oportunidade',
                WhatId = opp.Id,
                Status = 'Not Started'
            ));
        }
    }

    if (!tasks.isEmpty()) {
        insert tasks;
    }
}
```

Neste exemplo:

- O Trigger roda depois da gravação temporária.
- O registro já possui ID.
- O DML é executado uma única vez, fora do loop.
- Se houver 200 oportunidades, apenas 1 DML statement é usado.

## Exemplo de código: Queueable

Cenário: enviar dados de oportunidades fechadas para um data lake após o commit.

```apex
public class OpportunityDataLakeJob implements Queueable {
    private List<Id> opportunityIds;

    public OpportunityDataLakeJob(List<Id> opportunityIds) {
        this.opportunityIds = opportunityIds;
    }

    public void execute(QueueableExecutionContext context) {
        List<Opportunity> opportunities = [
            SELECT Id, Name, Amount, StageName
            FROM Opportunity
            WHERE Id IN :opportunityIds
        ];

        // Integração ou processamento
    }
}
```

Chamada após o commit:

```apex
System.enqueueJob(new OpportunityDataLakeJob(opportunityIds));
```

Neste exemplo:

- O Queueable roda após o commit.
- Ele consome limites assíncronos, não os limites da transação original.
- É adequado para integrações e processamentos pesados.
- O limite de `System.enqueueJob` é 50 em contexto síncrono e 1 em contexto assíncrono.

## Boas práticas de arquitetura

| Necessidade | Melhor local |
|---|---|
| Calcular ou preencher campo do próprio registro | Before-save Flow |
| Validar regra de negócio e bloquear save | Validation Rule |
| Normalizar, derivar ou corrigir campos do próprio registro com Apex | Before Trigger |
| Criar registros relacionados ou usar o ID | After Trigger ou After-save Flow |
| Atualizar registros relacionados | After-save Flow |
| Enviar e-mail, chamar integração assíncrona ou processar volume | Queueable, `@future`, Platform Event ou async path |
| Automatizar processo novo | Record-Triggered Flow |
| Evitar Workflow Rules e Process Builder | Migrar para Record-Triggered Flow |

## Padrão bulk-first

O padrão **bulk-first** significa escrever código que funciona corretamente mesmo quando muitos registros são processados em uma única transação.

### Errado: SOQL dentro do loop

```apex
for (Opportunity opp : Trigger.new) {
    Account acc = [
        SELECT Id, Region__c
        FROM Account
        WHERE Id = :opp.AccountId
    ];
}
```

### Correto: SOQL fora do loop

```apex
Set<Id> accountIds = new Set<Id>();

for (Opportunity opp : Trigger.new) {
    accountIds.add(opp.AccountId);
}

Map<Id, Account> accounts = new Map<Id, Account>(
    [
        SELECT Id, Region__c
        FROM Account
        WHERE Id IN :accountIds
    ]
);
```

### Errado: DML dentro do loop

```apex
for (Opportunity opp : Trigger.new) {
    insert new Task(
        Subject = 'Follow-up',
        WhatId = opp.Id
    );
}
```

### Correto: DML fora do loop

```apex
List<Task> tasks = new List<Task>();

for (Opportunity opp : Trigger.new) {
    tasks.add(new Task(
        Subject = 'Follow-up',
        WhatId = opp.Id
    ));
}

insert tasks;
```

## Monitoramento de limites

Use os métodos da classe `Limits` para diagnosticar consumo em tempo de execução:

```apex
System.debug('Queries: ' + Limits.getQueries());
System.debug('DML statements: ' + Limits.getDmlStatements());
System.debug('Heap size: ' + Limits.getHeapSize());
System.debug('CPU time: ' + Limits.getCpuTime());
```

Métodos úteis:

| Método | O que retorna |
|---|---|
| `Limits.getQueries()` | Quantidade de SOQL já executadas |
| `Limits.getLimitQueries()` | Limite máximo de SOQL |
| `Limits.getDmlStatements()` | Quantidade de DML statements já executados |
| `Limits.getLimitDmlStatements()` | Limite máximo de DML statements |
| `Limits.getHeapSize()` | Heap já consumido |
| `Limits.getLimitHeapSize()` | Limite máximo de heap |
| `Limits.getCpuTime()` | CPU já consumida |
| `Limits.getLimitCpuTime()` | Limite máximo de CPU |

## Recomendação moderna

Em uma organização Salesforce moderna, o padrão recomendado é:

1. **Before-save Flow** para cálculos e preenchimento de campos no próprio registro.
2. **Validation Rule** para bloquear gravações que violem regras de negócio.
3. **Before Trigger** para normalização e regras de negócio no próprio registro.
4. **After-save Flow** para automações relacionadas e integrações leves.
5. **After Trigger** para lógica Apex que precisa do ID ou de controle mais fino.
6. **Queueable, `@future` ou Platform Event** para integrações, e-mails e processamentos pesados após o commit.
7. **Trigger Handler** para manter um único ponto de entrada por objeto e evento.
8. **Bulk-first** para evitar SOQL e DML dentro de loops.

## Fontes consultadas

- Salesforce Developers. *Triggers and Order of Execution*. Apex Developer Guide. Disponível em: https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-triggers-order-of-execution.html
- Salesforce Developers. *Execution Governors and Limits*. Apex Developer Guide. Disponível em: https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm
- Salesforce Ben. *Order of Execution in Salesforce Simplified + Infographic*. Disponível em: https://www.salesforceben.com/learn-salesforce-order-of-execution/
- Salesforce Ben. *Salesforce Flow Builder vs. Apex*. Disponível em: https://www.salesforceben.com/salesforce-flow-builder-vs-apex/
- Salesforce Raman. *Salesforce Order of Execution*. YouTube. Disponível em: https://www.youtube.com/watch?v=-MDG_eWm4B8
- Salesforce Help. *Process Order for Salesforce Automation Rules and Apex*. Disponível em: https://help.salesforce.com/s/articleView?id=000005694&language=en_US&type=1
- Salesforce Help. *Workflow Considerations*. Disponível em: https://help.salesforce.com/s/articleView?id=platform.workflow_rules_considerations.htm&language=en_US&type=5
- Salesforce Help. *Define the Run Order of Record-Triggered Flows for an Object*. Disponível em: https://help.salesforce.com/s/articleView?id=platform.flow_task_trigger_run_order.htm&language=en_US&type=5

## Observação final

O Order of Execution não é apenas uma lista para decorar. Ele é uma ferramenta de **arquitetura de automação**: ajuda a decidir onde colocar cada regra, evitar loops, reduzir consumo de Governor Limits e garantir que a lógica execute no momento correto.

Para uma organização Salesforce moderna, a recomendação prática é:

```text
Before-save Flow
    para campos do próprio registro

Validation Rule
    para bloquear gravações inválidas

After-save Flow
    para automações modernas pós-gravação

Apex Trigger
    quando Flow não atende

Queueable / Platform Event
    para integrações e processamentos pesados
```

---

- Versões:
  - Criado em: 10/11/2026
  - Atualizado em: 10/11/2026
  - Versão: 1.0.0
