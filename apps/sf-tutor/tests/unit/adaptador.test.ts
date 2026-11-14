import { describe, expect, it, beforeAll } from 'vitest';
import { Indice, montarCena, revelarCaminho, recolher, chaveDe, caminhoDe, TAMANHO_PAGINA, type EstadoExpansao, type Visao } from '../../src/model/adaptador';
import { caminhoEntidade } from '../../src/data/carregador';
import { dadosReais, entidadeReal } from './dados-reais';

let ind: Indice;
const exp0 = (): EstadoExpansao => ({ expandidos: new Set(['salesforce']), paginas: new Map() });
beforeAll(() => { ind = new Indice(dadosReais()); });

describe('índice e ids canônicos', () => {
  it('cada id da busca existe uma única vez no índice', () => {
    const d = dadosReais();
    const ids = d.busca.map((b) => b.id);
    expect(new Set(ids).size).toBe(ids.length);
    expect(ind.nos.size).toBe(ids.length);
  });
  it('toda folha (campo/propriedade) tem pai existente', () => {
    for (const n of ind.nos.values()) {
      if (n.tipo === 'campo_api' || n.tipo === 'propriedade_xml') expect(ind.no(n.pai!), n.id).toBeTruthy();
    }
  });
  it('caminho de arquivo de entidade segue o gerador', () => {
    expect(caminhoEntidade('salesforce')).toBe('entidades/salesforce.json');
    expect(caminhoEntidade('obj:User')).toBe('entidades/obj/User.json');
    expect(caminhoEntidade('mdx:AssignmentRules_RuleEntry')).toBe('entidades/mdx/AssignmentRules_RuleEntry.json');
    expect(entidadeReal('obj/User.json').id).toBe('obj:User');
  });
  it('chave de ocorrência é reversível', () => {
    const c = ['salesforce', 'cls:x', 'func:y'];
    expect(caminhoDe(chaveDe(c))).toEqual(c);
  });
});

describe('cena (ocorrências visíveis)', () => {
  for (const v of ['funcionalidade', 'nuvem'] as Visao[]) {
    it(`estado inicial da visão ${v}: centro e primeiro nível, sem folhas`, () => {
      const cena = montarCena(ind, v, exp0());
      expect(cena.ocorrencias[0].id).toBe('salesforce');
      const tipos = new Set(cena.ocorrencias.slice(1).map((o) => ind.no(o.id)!.tipo));
      expect([...tipos]).toEqual([v === 'funcionalidade' ? 'classificacao' : 'nuvem']);
    });
  }
  it('é determinística e não repete chaves', () => {
    const e = exp0();
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('obj:User', 'funcionalidade')!);
    e.expandidos.add(chaveDe(ind.caminhoPreferido('obj:User', 'funcionalidade')!));
    const a = montarCena(ind, 'funcionalidade', e);
    const b = montarCena(ind, 'funcionalidade', e);
    expect(a).toEqual(b);
    const chaves = a.ocorrencias.map((o) => o.chave);
    expect(new Set(chaves).size).toBe(chaves.length);
    const arestas = a.arestas.map((x) => x.id);
    expect(new Set(arestas).size).toBe(arestas.length);
  });
  it('metadata type e objeto são o último nó: campos e propriedades não entram no mapa', () => {
    for (const id of ['obj:User', 'mdt:PermissionSet', 'mdt:NamedCredential']) {
      const cam = ind.caminhoPreferido(id, 'funcionalidade')!;
      expect(cam[cam.length - 1]).toBe(id);
      expect(ind.quantidadeFilhos('funcionalidade', cam), id).toBe(0);
      expect(ind.itensDaTabela(id).length, id).toBeGreaterThan(0);
      const e = exp0();
      revelarCaminho(ind, 'funcionalidade', e, cam);
      e.expandidos.add(chaveDe(cam));
      const cena = montarCena(ind, 'funcionalidade', e);
      expect(cena.ocorrencias.some((o) => o.paiChave === chaveDe(cam)), id).toBe(false);
      for (const o of cena.ocorrencias) expect(['campo_api', 'propriedade_xml', 'estrutura_auxiliar']).not.toContain(ind.no(o.id)!.tipo);
    }
    expect(ind.itensDaTabela('obj:User').length).toBeGreaterThan(TAMANHO_PAGINA);
  });
  it('campo, propriedade e estrutura levam ao nó que os contém (âncora)', () => {
    expect(ind.ancoras('obj:User.ProfileId')).toEqual(['obj:User']);
    expect(ind.ancoras('obj:User')).toEqual(['obj:User']);
    expect(ind.ancoras('mdt:PermissionSet.applicationVisibilities')).toEqual(['mdt:PermissionSet']);
    // propriedade de estrutura auxiliar: sobe até o metadata type que usa a estrutura
    expect(ind.ancoras('mdx:NamedCredentialParameter.externalCredential')).toContain('mdt:NamedCredential');
    expect(ind.ancoras('mdx:NamedCredentialParameter')).toContain('mdt:NamedCredential');
    const cam = ind.caminhoPreferido('obj:User.ProfileId', 'funcionalidade')!;
    expect(cam[cam.length - 1]).toBe('obj:User');
    expect(ind.caminhoValido(cam, 'funcionalidade')).toBe(true);
  });
  it('recolher remove descendentes da expansão', () => {
    const cam = ind.caminhoPreferido('obj:User.ProfileId', 'funcionalidade')!;
    const e = exp0();
    revelarCaminho(ind, 'funcionalidade', e, cam);
    recolher(e, chaveDe(cam.slice(0, 2)));
    const cena = montarCena(ind, 'funcionalidade', e);
    expect(cena.ocorrencias.some((o) => o.id === 'obj:User')).toBe(false);
  });
  it('relação técnica de um campo é desenhada entre os donos (User → Profile, por User.ProfileId)', () => {
    const e = exp0();
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('obj:User.ProfileId', 'funcionalidade')!);
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('obj:Profile', 'funcionalidade')!);
    const cena = montarCena(ind, 'funcionalidade', e);
    const t = cena.arestas.find((a) => a.tecnica && a.aresta?.rel_id === 'rel:user-profile');
    expect(t).toBeTruthy();
    expect(t!.origem.endsWith('obj:User')).toBe(true);
    expect(t!.destino.endsWith('obj:Profile')).toBe(true);
    expect(cena.arestas.filter((a) => a.id === t!.id).length).toBe(1);
  });
});

describe('caminhos', () => {
  it('User não tem metadata type: só objeto API abaixo da funcionalidade', () => {
    const filhos = ind.filhos('funcionalidade', ind.caminhoPreferido('func:usuarios', 'funcionalidade')!).map((f) => ind.no(f.id)!.tipo);
    expect(filhos).not.toContain('metadata_type');
    expect(filhos).toContain('objeto_api');
  });
  it('funcionalidade compartilhada aparece em Sales e Service com o mesmo id', () => {
    const cams = ind.caminhosPara('func:apps-de-console', 'nuvem');
    const nuvens = new Set(cams.map((c) => c[1]));
    expect(nuvens.has('nuv:sales-cloud')).toBe(true);
    expect(nuvens.has('nuv:service-cloud')).toBe(true);
    expect(new Set(cams.map((c) => c[c.length - 1]))).toEqual(new Set(['func:apps-de-console']));
  });
  it('caminhoPreferido respeita o contexto quando há vários caminhos', () => {
    const cams = ind.caminhosPara('func:apps-de-console', 'nuvem');
    const service = cams.find((c) => c[1] === 'nuv:service-cloud')!;
    expect(ind.caminhoPreferido('func:apps-de-console', 'nuvem', service)![1]).toBe('nuv:service-cloud');
  });
  it('caminhoValido rejeita caminhos inventados', () => {
    expect(ind.caminhoValido(['salesforce', 'nuv:sales-cloud', 'obj:User'], 'nuvem')).toBe(false);
    expect(ind.caminhoValido(ind.caminhoPreferido('obj:User', 'funcionalidade')!, 'funcionalidade')).toBe(true);
  });
  it('FlexiPage, QuickAction e PathAssistant são alcançáveis nas duas visões', () => {
    for (const id of ['mdt:FlexiPage', 'mdt:QuickAction', 'mdt:PathAssistant']) {
      expect(ind.caminhoPreferido(id, 'funcionalidade'), id).toBeTruthy();
      expect(ind.caminhoPreferido(id, 'nuvem'), id).toBeTruthy();
    }
  });
  it('estruturas aninhadas são alcançáveis a partir da propriedade', () => {
    const estruturas = [...ind.nos.values()].filter((n) => n.tipo === 'estrutura_auxiliar');
    const sem = estruturas.filter((n) => !ind.caminhoPreferido(n.id, 'funcionalidade'));
    expect(sem.map((n) => n.id)).toEqual([]);
  });
});

describe('integração (lote 5a)', () => {
  it('as funcionalidades de integração são alcançáveis nas duas visões', () => {
    for (const id of ['func:named-credentials', 'func:platform-events', 'func:change-data-capture', 'func:external-objects', 'func:auth-providers', 'func:cors']) {
      const cam = ind.caminhoPreferido(id, 'funcionalidade')!;
      expect(cam, id).toBeTruthy();
      expect(cam[1], id).toBe('cls:integracao-apis-e-eventos');
      expect(ind.caminhoPreferido(id, 'nuvem'), id).toBeTruthy();
    }
  });
  it('referência por nome no XML vira aresta técnica (parâmetro da named credential → ExternalCredential)', () => {
    const e = exp0();
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('mdx:NamedCredentialParameter.externalCredential', 'funcionalidade')!);
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('mdt:ExternalCredential', 'funcionalidade')!);
    const cena = montarCena(ind, 'funcionalidade', e);
    const t = cena.arestas.find((a) => a.tecnica && a.aresta?.rel_id === 'rel:ncparam-externalcredential');
    expect(t).toBeTruthy();
    expect(t!.destino.endsWith('mdt:ExternalCredential')).toBe(true);
  });
});

describe('integração (lote 5b)', () => {
  it('connected apps e external client apps ficam em autenticação de integrações', () => {
    for (const id of ['func:connected-apps', 'func:external-client-apps', 'func:oauth-escopos-e-troca-de-token']) {
      expect(ind.caminhoPreferido(id, 'funcionalidade')![2], id).toBe('sub:autenticacao-de-integracoes');
    }
  });
  it('ConnectedApp.permissionSetName liga o app ao metadata type PermissionSet', () => {
    const e = exp0();
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('mdt:ConnectedApp.permissionSetName', 'funcionalidade')!);
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('mdt:PermissionSet', 'funcionalidade')!);
    const t = montarCena(ind, 'funcionalidade', e).arestas.find((a) => a.tecnica && a.aresta?.rel_id === 'rel:connectedapp-permissionset');
    expect(t?.destino.endsWith('mdt:PermissionSet')).toBe(true);
  });
});

describe('integração (lote 5c)', () => {
  it('certificados e SSO SAML ficam em acesso; Event Relay em eventos', () => {
    expect(ind.caminhoPreferido('func:certificados', 'funcionalidade')![2]).toBe('sub:credenciais-certificados-e-protecao-de-dados');
    expect(ind.caminhoPreferido('func:sso-saml', 'funcionalidade')![2]).toBe('sub:autenticacao-sso-e-mfa');
    expect(ind.caminhoPreferido('func:event-relay', 'funcionalidade')![2]).toBe('sub:eventos-e-mensageria');
  });
  it('EventRelayConfig.eventChannel liga o relay ao canal de eventos', () => {
    const e = exp0();
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('mdt:EventRelayConfig.eventChannel', 'funcionalidade')!);
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('mdt:PlatformEventChannel', 'funcionalidade')!);
    const t = montarCena(ind, 'funcionalidade', e).arestas.find((a) => a.tecnica && a.aresta?.rel_id === 'rel:eventrelay-channel');
    expect(t?.destino.endsWith('mdt:PlatformEventChannel')).toBe(true);
  });
});

describe('contratos, limites e falhas (lote 5d)', () => {
  it('limites, versões e reprocessamento ficam em INT-07', () => {
    for (const id of ['func:limites-de-api-e-alocacoes', 'func:versoes-de-api', 'func:reprocessamento-e-monitoramento-de-eventos']) {
      expect(ind.caminhoPreferido(id, 'funcionalidade')![2], id).toBe('sub:contratos-limites-e-tratamento-de-falhas');
    }
  });
  it('EventBusSubscriber.Retries é alcançável pela funcionalidade de reprocessamento', () => {
    const c = ind.caminhoPreferido('obj:EventBusSubscriber.Retries', 'funcionalidade')!;
    expect(c).toContain('func:reprocessamento-e-monitoramento-de-eventos');
    // o caminho termina no objeto; o campo abre na tabela dele
    expect(c[c.length - 1]).toBe('obj:EventBusSubscriber');
    expect(ind.itensDaTabela('obj:EventBusSubscriber')).toContain('obj:EventBusSubscriber.Retries');
  });
});

describe('INT-07, segunda parte (lote 5e)', () => {
  it('callouts em INT-07; Bulk API em APIs de dados; Pub/Sub API em eventos', () => {
    expect(ind.caminhoPreferido('func:limites-e-falhas-de-callouts', 'funcionalidade')![2]).toBe('sub:contratos-limites-e-tratamento-de-falhas');
    expect(ind.caminhoPreferido('func:bulk-api', 'funcionalidade')![2]).toBe('sub:apis-de-dados-e-metadados');
    expect(ind.caminhoPreferido('func:pub-sub-api', 'funcionalidade')![2]).toBe('sub:eventos-e-mensageria');
  });
});

describe('APIs de dados e metadados (lote 5f)', () => {
  it('REST, SOAP, Metadata e Tooling API ficam na sub-classificação de APIs', () => {
    for (const id of ['func:rest-api', 'func:soap-api', 'func:metadata-api', 'func:tooling-api']) {
      expect(ind.caminhoPreferido(id, 'funcionalidade')![2], id).toBe('sub:apis-de-dados-e-metadados');
    }
  });
});

describe('certificados e plugins de external client app (lote 5g)', () => {
  it('PublicKeyCertificateSetKey.publicKeyCertificate referencia PublicKeyCertificate', () => {
    const e = exp0();
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('mdx:PublicKeyCertificateSetKey.publicKeyCertificate', 'funcionalidade')!);
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('mdt:PublicKeyCertificate', 'funcionalidade')!);
    const t = montarCena(ind, 'funcionalidade', e).arestas.find((a) => a.tecnica && a.aresta?.rel_id === 'rel:pkcsetkey-pkc');
    expect(t?.destino.endsWith('mdt:PublicKeyCertificate')).toBe(true);
  });
  it('plugins de ECA ficam sob external client apps', () => {
    for (const id of ['mdt:ExtlClntAppPushSettings', 'mdt:ExtlClntAppCanvasSettings', 'mdt:ExtlClntAppSamlConfigurablePolicies']) {
      expect(ind.caminhoPreferido(id, 'funcionalidade'), id).toContain('func:external-client-apps');
    }
  });
});

describe('ConnectedApp e __e/__x (lote 5h)', () => {
  it('estruturas de ConnectedApp antes truncadas agora têm campos', () => {
    for (const id of ['mdx:ConnectedAppSamlConfig.samlSubjectType', 'mdx:ConnectedAppOauthPolicy.refreshTokenPolicy', 'mdx:ConnectedAppSessionPolicy.policyAction', 'mdx:ConnectedAppOauthIdToken.idTokenValidity']) {
      expect(ind.caminhoPreferido(id, 'funcionalidade'), id).toBeTruthy();
    }
  });
  it('CustomObject.externalDataSource referencia ExternalDataSource', () => {
    const e = exp0();
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('mdt:CustomObject.externalDataSource', 'funcionalidade')!);
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('mdt:ExternalDataSource', 'funcionalidade')!);
    const t = montarCena(ind, 'funcionalidade', e).arestas.find((a) => a.tecnica && a.aresta?.rel_id === 'rel:customobject-externaldatasource');
    expect(t?.destino.endsWith('mdt:ExternalDataSource')).toBe(true);
  });
});

describe('objetos API de integração (lote 5j)', () => {
  it('objetos ficam sob as funcionalidades de integração', () => {
    expect(ind.caminhoPreferido('obj:NamedCredential', 'funcionalidade')).toContain('func:named-credentials');
    expect(ind.caminhoPreferido('obj:OauthToken.UserId', 'funcionalidade')).toContain('func:connected-apps');
    expect(ind.caminhoPreferido('obj:CspTrustedSite', 'funcionalidade')).toContain('func:csp-trusted-sites');
  });
  it('ExternalDataSource.NamedCredentialId liga a fonte à named credential', () => {
    const e = exp0();
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('obj:ExternalDataSource.NamedCredentialId', 'funcionalidade')!);
    revelarCaminho(ind, 'funcionalidade', e, ind.caminhoPreferido('obj:NamedCredential', 'funcionalidade')!);
    const t = montarCena(ind, 'funcionalidade', e).arestas.find((a) => a.tecnica && a.aresta?.rel_id === 'rel:externaldatasource-namedcredential');
    expect(t?.destino.endsWith('obj:NamedCredential')).toBe(true);
  });
});

describe('Sobre este tema (#34): contagens do conteúdo do tema', () => {
  const nomeArq = (id: string) => `${id.startsWith('cls:') ? 'cls' : 'sub'}/${id.slice(4)}.json`;
  it('subclassificação: funcionalidades batem com o cadastro do tema', () => {
    for (const n of ind.nos.values()) {
      if (n.tipo !== 'subclassificacao') continue;
      const e = entidadeReal(nomeArq(n.id));
      const c = ind.conteudoDoTema(n.id);
      expect(c.temas, n.id).toBe(0);
      expect(c.funcionalidades, n.id).toBe(new Set(e.funcionalidades as string[]).size);
    }
  });
  it('classificação: temas internos e funcionalidades somam os cadastros das subclassificações', () => {
    for (const n of ind.nos.values()) {
      if (n.tipo !== 'classificacao') continue;
      const subs = entidadeReal(nomeArq(n.id)).subclassificacoes as string[];
      const funcs = new Set(subs.flatMap((s) => entidadeReal(nomeArq(s)).funcionalidades as string[]));
      const c = ind.conteudoDoTema(n.id);
      expect(c.temas, n.id).toBe(subs.length);
      expect(c.funcionalidades, n.id).toBe(funcs.size);
      expect(c.soSecundarias).toBeLessThanOrEqual(c.funcionalidades);
    }
  });
  it('metadata types e objetos API vêm das representações das funcionalidades do tema', () => {
    const c = ind.conteudoDoTema('sub:acoes-e-regras');
    const funcs = entidadeReal('sub/acoes-e-regras.json').funcionalidades as string[];
    const mdt = new Set(funcs.flatMap((f) => (ind.saindo.get(f) ?? []).filter((a) => a.tipo === 'representacao_xml').map((a) => a.destino)));
    expect(c.metadataTypes).toBe(mdt.size);
    expect(c.metadataTypes).toBeGreaterThan(0);
  });
});

describe('estado do recorte de um tema', () => {
  it('três estados, sem inventar verificação', async () => {
    const { estadoRecorte } = await import('../../src/rotulos');
    expect(estadoRecorte('desconhecido', false).rotulo).toBe('Curadoria do projeto');
    expect(estadoRecorte('desconhecido', true).rotulo).toBe('Parcialmente conferido');
    expect(estadoRecorte('verificado', true).rotulo).toBe('Conferido com fonte oficial');
  });
});
