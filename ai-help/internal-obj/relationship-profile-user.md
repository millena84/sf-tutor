A associação **User → Profile** não fica em uma tabela intermediária: o próprio objeto **`User`** possui o campo **`ProfileId`**, que aponta para o registro em **`Profile`**. Cada usuário tem **um único Profile**; um Profile pode estar associado a muitos usuários. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_profile.htm)

## Modelo interno

```text
User (005...)
 ├── ProfileId ───────────────► Profile (00e...)
 └── UserRole.Id ─────────────► UserRole (00E...) — opcional
```

- **`User.ProfileId`**: campo de relacionamento lookup para `Profile`.
- **`Profile`**: representa o conjunto base de permissões, layouts, apps e configurações atribuídas ao usuário. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_profile.htm)
- **`UserRole`**: é outra associação, separada, feita por `User.UserRoleId`; nem todo usuário possui Role. [salesforcefaqs](https://salesforcefaqs.com/get-current-user-info-using-apex-in-salesforce/)

## SOQL para consultar

```soql
SELECT Id, Name, ProfileId, Profile.Name
FROM User
WHERE IsActive = true
```

Para listar os usuários de um perfil específico:

```soql
SELECT Id, Name, Email
FROM User
WHERE Profile.Name = 'System Administrator'
```

Ou, de forma mais segura — evitando depender do nome:

```soql
SELECT Id, Name, Email
FROM User
WHERE ProfileId = '00eXXXXXXXXXXXXXXX'
```

## Em Apex

```apex
User u = [
    SELECT Id, Name, ProfileId, Profile.Name
    FROM User
    WHERE Id = :UserInfo.getUserId()
];

System.debug(u.ProfileId);
System.debug(u.Profile.Name);
```

Também é possível obter o ID do perfil do usuário em execução sem SOQL:

```apex
Id profileId = UserInfo.getProfileId();
```

`UserInfo.getProfileId()` retorna apenas o ID; para o nome, consulte `User.Profile.Name` ou o objeto `Profile`. [salesforcefaqs](https://salesforcefaqs.com/get-current-user-info-using-apex-in-salesforce/)

## Atenção: Profile não é Permission Set

| Relação | Onde fica | Cardinalidade |
|---|---|---|
| **User → Profile** | `User.ProfileId` | 1 usuário : 1 profile |
| **User → Permission Set** | `PermissionSetAssignment` | 1 usuário : N permission sets |
| **User → Permission Set Group** | `PermissionSetAssignment`, por meio dos permission sets do grupo | 1 usuário : N grupos |
| **User → Role** | `User.UserRoleId` | 1 usuário : 0 ou 1 role |

Ou seja: para o **Profile**, consulte diretamente `User.ProfileId`; para **Permission Sets**, a tabela de junção é `PermissionSetAssignment`. [developer.salesforce](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_profile.htm)
