// Reporte de erro de informação: monta o texto, o link de e-mail (mailto) e o link da issue no repositório público.
// Não há servidor: o e-mail sai do app de e-mail de quem reporta, e a issue é aberta pela própria pessoa no GitHub.

/** Ponto único de configuração do reporte. Para trocar o e-mail, gere o valor novo assim (no terminal):
 *  node -e "console.log(Buffer.from('novo@exemplo.com').toString('base64').split('').reverse().join(''))"
 *  O endereço não aparece no HTML: só é montado no clique. Isso barra robôs que coletam e-mails lendo páginas,
 *  mas não esconde o endereço de quem lê o código; ocultação total exigiria um servidor. */
export const REPORTE = {
  destinoCodificado: '==QbvNmLslWYtdGQvRmbhdWdiNXZk5SZ0J3bwV3c',
  assunto: 'ERRO REPORTADO: Metadata Desbugado',
  /** repositório público onde as issues são abertas (o repositório de trabalho, sf-tutor, é privado) */
  repoIssues: 'millena84/metadata-desbugando',
  modeloIssue: 'erro-reportado.yml',
  /** acima disso alguns apps de e-mail cortam o corpo; a janela sugere copiar o texto */
  limiteMailto: 1800,
} as const;

/** "O que aconteceu?": a primeira pergunta do formulário. Cada situação muda as perguntas seguintes.
 *  "org" não vira reporte: o formulário explica que o site não é suporte da Salesforce. */
export interface Situacao {
  id: 'errado' | 'desatualizado' | 'confuso' | 'fonte' | 'ligacao' | 'outro' | 'org';
  rotulo: string;
  perguntaAtual: string;
  ajudaAtual?: string;
  perguntaCorreto: string;
}

export const SITUACOES: readonly Situacao[] = [
  { id: 'errado', rotulo: 'Está errado', perguntaAtual: 'O que está escrito aqui que parece errado?', ajudaAtual: 'Pode colar o trecho da ficha.', perguntaCorreto: 'Como deveria ser?' },
  { id: 'desatualizado', rotulo: 'Está desatualizado', perguntaAtual: 'O que está desatualizado?', ajudaAtual: 'Pode colar o trecho da ficha.', perguntaCorreto: 'Como está hoje, e desde quando?' },
  { id: 'confuso', rotulo: 'Ficou confuso', perguntaAtual: 'O que ficou confuso?', perguntaCorreto: 'Como ficaria mais claro?' },
  { id: 'fonte', rotulo: 'Fonte quebrada ou errada', perguntaAtual: 'Qual fonte, e o que acontece com ela?', ajudaAtual: 'Por exemplo: o link abre uma página de erro ou fala de outra coisa.', perguntaCorreto: 'Qual seria a fonte certa?' },
  { id: 'ligacao', rotulo: 'Ligação errada no mapa', perguntaAtual: 'Qual ligação parece errada, e por quê?', perguntaCorreto: 'Como deveria ser?' },
  { id: 'outro', rotulo: 'Outra coisa', perguntaAtual: 'Conte o que aconteceu.', perguntaCorreto: 'O que você sugere?' },
  { id: 'org', rotulo: 'É um problema na minha org', perguntaAtual: '', perguntaCorreto: '' },
];

export const situacao = (id: string): Situacao | undefined => SITUACOES.find((x) => x.id === id);

export interface ContextoReporte {
  /** id do nó (ex.: mdt:SecuritySettings) */
  id: string;
  rotulo: string;
  tipo: string;
  /** campo ou propriedade, quando o reporte parte de uma linha da tabela */
  item?: { id: string; nome: string };
  /** status mostrado no site para o item (ou para o campo), já em texto: "Verificado", "Desconhecido"… */
  status?: string;
  /** link absoluto para o item, com o estado da tela */
  link: string;
  /** versão dos dados (API, contrato e commit dos insumos) */
  versao: string;
}

export interface CamposReporte {
  /** id da situação escolhida em "O que aconteceu?" */
  situacao: string;
  atual: string;
  correto?: string;
  /** "É outra parte desta ficha?" */
  parte?: string;
  fonte?: string;
  pratica?: boolean;
  nome?: string;
  github?: string;
  /** só para avisar da correção; vai no e-mail e no texto copiado, nunca na issue pública */
  email?: string;
}

export function destinatario(cod: string = REPORTE.destinoCodificado): string {
  return atob(cod.split('').reverse().join(''));
}

/** Usuário do GitHub: opcional; aceita com ou sem @; devolve "@usuario" ou "" (inválido ou vazio). */
export function normalizarGithub(v: string | undefined): string {
  const s = (v ?? '').trim().replace(/^@/, '');
  return /^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$/.test(s) ? `@${s}` : '';
}

/** E-mail para aviso: opcional; devolve o endereço aparado ou "" se vazio ou malformado. */
export function normalizarEmail(v: string | undefined): string {
  const s = (v ?? '').trim();
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s) ? s : '';
}

export function assunto(c: ContextoReporte): string {
  return `${REPORTE.assunto} (${c.item ? `${c.id} > ${c.item.nome}` : c.id})`;
}

function bloco(titulo: string, valor: string | undefined): string[] {
  const v = (valor ?? '').trim();
  return v ? [`${titulo}`, v, ''] : [];
}

/** "Como você sabe?" em uma linha: link oficial, prática, ambos ou nada. */
export function comoSabe(f: CamposReporte): string {
  return [f.fonte?.trim() ? `documentação oficial: ${f.fonte.trim()}` : '', f.pratica ? 'pela prática' : ''].filter(Boolean).join('; ');
}

/** Texto do reporte. Com incluirEmail (envio por e-mail e "Copiar texto"), leva o e-mail para aviso da correção. */
export function montarTexto(c: ContextoReporte, f: CamposReporte, o: { hoje?: Date; incluirEmail?: boolean } = {}): string {
  const s = situacao(f.situacao);
  const gh = normalizarGithub(f.github);
  const quem = [f.nome?.trim(), gh ? `GitHub ${gh}` : ''].filter(Boolean).join(' · ');
  const email = o.incluirEmail ? normalizarEmail(f.email) : '';
  const sabe = comoSabe(f);
  return [
    'ERRO REPORTADO no Metadata Desbugado',
    '',
    `Item: ${c.rotulo} (${c.id}), ${c.tipo}`,
    ...(c.item ? [`Campo ou propriedade: ${c.item.nome} (${c.item.id})`] : []),
    ...(f.parte?.trim() ? [`Parte da ficha: ${f.parte.trim()}`] : []),
    ...(c.status ? [`Status no site: ${c.status}`] : []),
    `Link: ${c.link}`,
    `Versão dos dados: ${c.versao}`,
    `Data do reporte: ${(o.hoje ?? new Date()).toISOString().slice(0, 10)}`,
    '',
    `O que aconteceu: ${s?.rotulo ?? f.situacao}`,
    '',
    ...bloco(s?.perguntaAtual ?? 'Descrição', f.atual),
    ...bloco(s?.perguntaCorreto ?? 'Sugestão', f.correto),
    ...(sabe ? [`Como sabe: ${sabe}`, ''] : []),
    ...(quem ? [`Reportado por: ${quem}`] : ['Reportado por: (anônimo)']),
    ...(email ? [`Avisar a correção em: ${email}`] : []),
  ].join('\n');
}

export function urlMailto(c: ContextoReporte, f: CamposReporte, destino: string = destinatario()): string {
  return `mailto:${destino}?subject=${encodeURIComponent(assunto(c))}&body=${encodeURIComponent(montarTexto(c, f, { incluirEmail: true }))}`;
}

/** Link "nova issue" com o modelo do repositório público e os campos já preenchidos (ids do modelo erro-reportado.yml).
 *  O e-mail para aviso nunca entra: a issue é pública. */
export function urlIssue(c: ContextoReporte, f: CamposReporte): string {
  const s = situacao(f.situacao);
  const parte = f.parte?.trim() ? ` · parte: ${f.parte.trim()}` : '';
  const p = new URLSearchParams({
    template: REPORTE.modeloIssue,
    title: assunto(c),
    item: `${c.rotulo} (${c.id})${c.item ? ` > ${c.item.nome} (${c.item.id})` : ''}${parte}`,
    link: c.link,
    versao: c.versao,
    tipo: s?.rotulo ?? f.situacao,
    descricao: f.atual.trim(),
  });
  if (c.status) p.set('status', c.status);
  if (f.correto?.trim()) p.set('correto', f.correto.trim());
  const sabe = comoSabe(f);
  if (sabe) p.set('fonte', sabe);
  return `https://github.com/${REPORTE.repoIssues}/issues/new?${p.toString()}`;
}
