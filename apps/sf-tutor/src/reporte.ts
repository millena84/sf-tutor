// Reporte de erro de informação: monta o texto, o link de e-mail (mailto) e o link da issue no repositório público.
// Não há servidor: o e-mail sai do app de e-mail de quem reporta, e a issue é aberta pela própria pessoa no GitHub.

/** Ponto único de configuração do reporte. Para trocar o e-mail, gere o valor novo assim (no terminal):
 *  node -e "console.log(Buffer.from('novo@exemplo.com').toString('base64').split('').reverse().join(''))"
 *  O endereço não aparece no HTML: só é montado no clique. Isso barra robôs que coletam e-mails lendo páginas,
 *  mas não esconde o endereço de quem lê o código; ocultação total exigiria um servidor. */
export const REPORTE = {
  destinoCodificado: '==QbvNmLslWYtdGQvRmbhdWdiNXZk5SZ0J3bwV3c',
  assunto: 'ERRO REPORTADO: tutorial Salesforce - sf-tutor',
  /** repositório público onde as issues são abertas (o sf-tutor, onde o conteúdo é trabalhado, é privado) */
  repoIssues: 'millena84/tutorial-sf-grafo',
  modeloIssue: 'erro-reportado.yml',
  /** acima disso alguns apps de e-mail cortam o corpo; a janela sugere copiar o texto */
  limiteMailto: 1800,
} as const;

export const TIPOS_PROBLEMA = [
  'Informação incorreta',
  'Informação desatualizada',
  'Fonte quebrada ou errada',
  'Texto confuso ou difícil de entender',
  'Ligação errada no mapa',
  'Outro',
] as const;

export interface ContextoReporte {
  /** id do nó (ex.: mdt:SecuritySettings) */
  id: string;
  rotulo: string;
  tipo: string;
  /** campo ou propriedade, quando o reporte parte de uma linha da tabela */
  item?: { id: string; nome: string };
  /** link absoluto para o item, com o estado da tela */
  link: string;
  /** versão dos dados (API, contrato e commit dos insumos) */
  versao: string;
}

export interface CamposReporte {
  tipo: string;
  descricao: string;
  correto?: string;
  fonte?: string;
  nome?: string;
  github?: string;
}

export function destinatario(cod: string = REPORTE.destinoCodificado): string {
  return atob(cod.split('').reverse().join(''));
}

/** Usuário do GitHub: opcional; aceita com ou sem @; devolve "@usuario" ou "" (inválido ou vazio). */
export function normalizarGithub(v: string | undefined): string {
  const s = (v ?? '').trim().replace(/^@/, '');
  return /^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$/.test(s) ? `@${s}` : '';
}

export function assunto(c: ContextoReporte): string {
  return `${REPORTE.assunto} (${c.item ? `${c.id} > ${c.item.nome}` : c.id})`;
}

function bloco(titulo: string, valor: string | undefined): string[] {
  const v = (valor ?? '').trim();
  return v ? [`${titulo}:`, v, ''] : [];
}

export function montarTexto(c: ContextoReporte, f: CamposReporte, hoje: Date = new Date()): string {
  const gh = normalizarGithub(f.github);
  const quem = [f.nome?.trim(), gh ? `GitHub ${gh}` : ''].filter(Boolean).join(' · ');
  return [
    'ERRO REPORTADO no sf-tutor',
    '',
    `Item: ${c.rotulo} (${c.id}), ${c.tipo}`,
    ...(c.item ? [`Campo ou propriedade: ${c.item.nome} (${c.item.id})`] : []),
    `Link: ${c.link}`,
    `Versão dos dados: ${c.versao}`,
    `Data do reporte: ${hoje.toISOString().slice(0, 10)}`,
    '',
    `Tipo de problema: ${f.tipo}`,
    '',
    ...bloco('O que está errado', f.descricao),
    ...bloco('Qual seria o correto', f.correto),
    ...bloco('Fonte', f.fonte),
    ...(quem ? [`Reportado por: ${quem}`] : ['Reportado por: (anônimo)']),
  ].join('\n');
}

export function urlMailto(c: ContextoReporte, f: CamposReporte, destino: string = destinatario()): string {
  return `mailto:${destino}?subject=${encodeURIComponent(assunto(c))}&body=${encodeURIComponent(montarTexto(c, f))}`;
}

/** Link "nova issue" com o modelo do repositório público e os campos já preenchidos (ids do modelo erro-reportado.yml). */
export function urlIssue(c: ContextoReporte, f: CamposReporte): string {
  const p = new URLSearchParams({
    template: REPORTE.modeloIssue,
    title: assunto(c),
    item: `${c.rotulo} (${c.id})${c.item ? ` > ${c.item.nome} (${c.item.id})` : ''}`,
    link: c.link,
    versao: c.versao,
    tipo: f.tipo,
    descricao: f.descricao.trim(),
  });
  if (f.correto?.trim()) p.set('correto', f.correto.trim());
  if (f.fonte?.trim()) p.set('fonte', f.fonte.trim());
  return `https://github.com/${REPORTE.repoIssues}/issues/new?${p.toString()}`;
}
