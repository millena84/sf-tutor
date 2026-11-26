// Janela "Reportar erro": uma entrevista curta sobre o conteúdo do site, que monta um e-mail (mailto) ou abre uma issue no
// repositório público. A primeira pergunta ("O que aconteceu?") muda as seguintes; "É um problema na minha org" não vira reporte.
import { assunto, type CamposReporte, type ContextoReporte, montarTexto, normalizarEmail, REPORTE, situacao, SITUACOES, urlIssue, urlMailto } from '../reporte';
import { h, limpar } from './dom';

function campo(rotulo: HTMLElement | string, controle: HTMLElement, ajuda?: string): HTMLElement {
  const id = controle.id;
  const idAjuda = ajuda ? `${id}-ajuda` : undefined;
  if (idAjuda) controle.setAttribute('aria-describedby', idAjuda);
  return h('div', { class: 'campo-form' },
    h('label', { for: id }, rotulo),
    controle,
    ajuda ? h('p', { class: 'nota', id: idAjuda }, ajuda) : null);
}

/** Abre a janela de reporte (um diálogo próprio, que pode ficar por cima da tabela de campos). */
export function abrirReporte(c: ContextoReporte): void {
  let dlg = document.getElementById('dialogo-reporte') as HTMLDialogElement | null;
  if (!dlg) {
    dlg = h('dialog', { id: 'dialogo-reporte', 'aria-labelledby': 'reporte-titulo' }) as HTMLDialogElement;
    document.body.append(dlg);
  }
  limpar(dlg);

  // 1. O que aconteceu? (botões de escolha única, nativos, com cara de etiqueta)
  const opcoes = SITUACOES.map((x) => {
    const r = h('input', { type: 'radio', name: 'rep-situacao', id: `rep-sit-${x.id}`, value: x.id }) as HTMLInputElement;
    return { x, r, el: h('label', { class: 'opcao-situacao', for: r.id }, r, h('span', null, x.rotulo)) };
  });
  const escolhida = (): string => opcoes.find((o) => o.r.checked)?.x.id ?? '';
  const grupoSituacao = h('fieldset', { class: 'pergunta pergunta-situacao' },
    h('legend', null, h('span', { class: 'num-pergunta' }, '1'), 'O que aconteceu? (obrigatório)'),
    h('div', { class: 'opcoes-situacao' }, opcoes.map((o) => o.el)));

  const avisoOrg = h('div', { class: 'aviso aviso-org', role: 'note', hidden: '' },
    h('p', null, h('strong', null, 'Este formulário é só para o conteúdo do Metadata Desbugado. '),
      'Problemas na sua org Salesforce, como algo que não funciona, um erro de deploy ou uma configuração, não são atendidos aqui.'),
    h('p', null, 'Procure a ', h('a', { href: 'https://help.salesforce.com', target: '_blank', rel: 'noopener' }, 'Ajuda da Salesforce'),
      ', o suporte do seu contrato ou a comunidade Trailblazer.'));

  // 2. perguntas que mudam conforme a situação
  const rotAtual = h('span', null);
  const rotCorreto = h('span', null);
  const atual = h('textarea', { id: 'rep-atual', rows: '4', maxlength: '1500' }) as HTMLTextAreaElement;
  const ajudaAtual = h('p', { class: 'nota', id: 'rep-atual-ajuda' });
  atual.setAttribute('aria-describedby', 'rep-atual-ajuda');
  const correto = h('textarea', { id: 'rep-correto', rows: '3', maxlength: '1000' }) as HTMLTextAreaElement;
  const parte = h('input', { id: 'rep-parte', type: 'text', maxlength: '120', placeholder: 'o resumo, a seção Avançado…' }) as HTMLInputElement;
  // 3. como você sabe
  const fonte = h('input', { id: 'rep-fonte', type: 'url', placeholder: 'https://developer.salesforce.com/docs/…', maxlength: '500' }) as HTMLInputElement;
  const pratica = h('input', { id: 'rep-pratica', type: 'checkbox' }) as HTMLInputElement;
  // 4. crédito e aviso
  const nome = h('input', { id: 'rep-nome', type: 'text', autocomplete: 'name', maxlength: '80' }) as HTMLInputElement;
  const github = h('input', { id: 'rep-github', type: 'text', placeholder: '@seu-usuario', maxlength: '40',
    pattern: '@?[A-Za-z0-9][A-Za-z0-9\\-]{0,38}', autocomplete: 'off', spellcheck: 'false' }) as HTMLInputElement;
  const email = h('input', { id: 'rep-email', type: 'email', autocomplete: 'email', maxlength: '120', placeholder: 'voce@exemplo.com' }) as HTMLInputElement;

  const status = h('p', { class: 'nota status-reporte', role: 'status' });
  const avisar = (texto: string): void => { status.textContent = texto; status.classList.add('aviso'); };
  const valores = (): CamposReporte => ({ situacao: escolhida(), atual: atual.value, correto: correto.value, parte: parte.value,
    fonte: fonte.value, pratica: pratica.checked, nome: nome.value, github: github.value, email: email.value });

  const perguntas = h('div', { class: 'perguntas-seguintes', hidden: '' },
    h('div', { class: 'pergunta' },
      h('p', { class: 'titulo-pergunta' }, h('span', { class: 'num-pergunta' }, '2'), 'Conte o que viu'),
      h('div', { class: 'campo-form' }, h('label', { for: 'rep-atual' }, rotAtual, ' (obrigatório)'), atual, ajudaAtual),
      campo(rotCorreto, correto),
      campo('É outra parte desta ficha? (opcional)', parte, 'Se o erro não está no item indicado acima, diga onde está.')),
    h('div', { class: 'pergunta' },
      h('p', { class: 'titulo-pergunta' }, h('span', { class: 'num-pergunta' }, '3'), 'Como você sabe? (opcional)'),
      campo('Link da documentação oficial', fonte, 'É o que permite confirmar a correção.'),
      h('div', { class: 'campo-check' }, pratica, h('label', { for: 'rep-pratica' }, 'Sei pela prática'))),
    h('fieldset', { class: 'pergunta campos-opcionais' },
      h('legend', null, h('span', { class: 'num-pergunta' }, '4'), 'Crédito e aviso da correção (opcional)'),
      campo('Nome', nome, 'Para dar crédito nas notas de versão quando a correção for publicada.'),
      campo('Usuário do GitHub', github, 'Para mencionar você na issue e nas notas de versão.'),
      campo('E-mail para avisar da correção', email,
        'Vai só no envio por e-mail e no texto copiado, nunca na issue do GitHub, que é pública. Pelo GitHub, as notificações da issue já avisam você.')));

  const form = h('form', { class: 'form-reporte', novalidate: '' }) as HTMLFormElement;
  const valido = (): boolean => {
    const s = escolhida();
    if (!s) { status.textContent = 'Escolha o que aconteceu.'; opcoes[0].r.focus(); return false; }
    if (!atual.value.trim()) { status.textContent = `Responda: ${situacao(s)?.perguntaAtual ?? 'o que aconteceu'}`; atual.focus(); return false; }
    if (email.value.trim() && !normalizarEmail(email.value)) { status.textContent = 'O e-mail para aviso parece incompleto. Corrija ou deixe em branco.'; email.focus(); return false; }
    if (!form.checkValidity()) { form.reportValidity(); status.textContent = 'Confira os campos marcados.'; return false; }
    return true;
  };

  let pararAcompanhamento: (() => void) | undefined;
  const btnEmail = h('button', { type: 'button', class: 'btn btn-primario' }, 'Enviar por e-mail');
  btnEmail.addEventListener('click', () => {
    if (!valido()) return;
    const url = urlMailto(c, valores());
    const longo = url.length > REPORTE.limiteMailto
      ? ' O texto é longo e alguns apps cortam o final: se faltar algo, use "Copiar texto".' : '';
    avisar(`Abrindo o seu app de e-mail com a mensagem pronta. O reporte só é enviado quando você tocar em Enviar no app.${longo}`);
    pararAcompanhamento?.();
    pararAcompanhamento = acompanharMailto(avisar);
    location.href = url;
  });
  const btnIssue = h('button', { type: 'button', class: 'btn' }, 'Abrir issue no GitHub');
  btnIssue.addEventListener('click', () => {
    if (!valido()) return;
    window.open(urlIssue(c, valores()), '_blank', 'noopener');
    const semEmail = email.value.trim() ? ' Seu e-mail não foi incluído, porque a issue é pública; o GitHub avisa você pelas notificações da issue.' : '';
    avisar('A página do GitHub abre numa nova aba, já preenchida. A issue só é criada quando você marcar a confirmação no fim do formulário '
      + 'e tocar em "Create" (ou "Submit new issue"). Se o GitHub pedir login, entre e confira se os campos continuam preenchidos; '
      + `se o app do GitHub abrir sem os campos, volte aqui e use "Enviar por e-mail".${semEmail}`);
  });
  const btnCopiar = h('button', { type: 'button', class: 'btn' }, 'Copiar texto');
  btnCopiar.addEventListener('click', async () => {
    if (!valido()) return;
    const txt = `Assunto: ${assunto(c)}\n\n${montarTexto(c, valores(), { incluirEmail: true })}`;
    try { await navigator.clipboard.writeText(txt); status.textContent = 'Texto copiado. Cole no seu e-mail para o suporte. Se for colar numa issue, apague o seu e-mail antes.'; }
    catch { status.textContent = 'Não foi possível copiar automaticamente. Selecione o texto da prévia abaixo.'; previa.hidden = false; previa.textContent = txt; }
  });
  const previa = h('pre', { class: 'previa-reporte', hidden: '' });
  const fechar = h('button', { type: 'button', class: 'btn' }, 'Cancelar');
  fechar.addEventListener('click', () => dlg!.close());
  const acoes = h('div', { class: 'acoes acoes-reporte', hidden: '' }, btnEmail, btnIssue, btnCopiar, fechar);

  const aoEscolher = (): void => {
    const s = situacao(escolhida());
    const org = s?.id === 'org';
    avisoOrg.hidden = !org;
    perguntas.hidden = !s || org;
    acoes.hidden = !s || org;
    status.textContent = '';
    if (s && !org) {
      rotAtual.textContent = s.perguntaAtual;
      rotCorreto.textContent = `${s.perguntaCorreto} (opcional)`;
      ajudaAtual.textContent = s.ajudaAtual ?? '';
      ajudaAtual.hidden = !s.ajudaAtual;
    }
  };
  for (const o of opcoes) o.r.addEventListener('change', aoEscolher);

  const onde = c.item ? `${c.rotulo} › ${c.item.nome}` : c.rotulo;
  form.append(
    h('dl', { class: 'kv contexto-reporte' },
      h('dt', null, 'Você está reportando'), h('dd', null, `${onde} (${c.item ? c.item.id : c.id})`),
      c.status ? [h('dt', null, 'Status no site'), h('dd', null, c.status)] : null,
      h('dt', null, 'Versão dos dados'), h('dd', null, c.versao)),
    h('p', { class: 'aviso aviso-sensivel', role: 'note' }, h('strong', null, 'Não inclua dados da sua org. '),
      'Nada de credenciais, IDs de registros ou dados de clientes. A issue no GitHub é pública.'),
    grupoSituacao, avisoOrg, perguntas, acoes, status, previa);
  dlg.append(
    h('div', { class: 'dialogo-cab' }, h('h2', { id: 'reporte-titulo' }, 'Reportar erro no conteúdo'), h('button', { type: 'button', class: 'btn', on: { click: () => dlg!.close() } }, 'Fechar')),
    h('div', { class: 'dialogo-corpo-reporte' },
      h('p', { class: 'intro-reporte' }, 'É sobre o que está neste site: uma ficha, um campo ou uma ligação do mapa. ',
        h('strong', null, 'Não é suporte da Salesforce.'), ' O texto sai pelo seu e-mail ou vira uma issue pública no GitHub; esta página não guarda nada.'),
      form));
  dlg.showModal();
  opcoes[0].r.focus();
}

/**
 * Depois de chamar o mailto, a página não sabe se o app de e-mail abriu nem se a pessoa enviou.
 * Heurística honesta: se a página não sair de foco em alguns segundos, provavelmente nenhum app abriu;
 * se sair e voltar, lembra que o envio só acontece no app. Nunca diz que o e-mail foi enviado.
 */
export function acompanharMailto(avisar: (texto: string) => void, doc: Document = document, esperaMs = 2500): () => void {
  let saiu = false;
  const aoMudar = (): void => {
    if (doc.visibilityState === 'hidden') { saiu = true; return; }
    if (saiu) {
      avisar('Voltou do app de e-mail? O reporte só chega se você tocou em Enviar lá. Se cancelou, nada foi enviado: tente de novo, use "Copiar texto" ou abra uma issue no GitHub.');
      parar();
    }
  };
  const temporizador = setTimeout(() => {
    if (!saiu) {
      avisar('Parece que nenhum app de e-mail abriu, então nada foi enviado. Use "Copiar texto" e envie pelo seu e-mail, ou abra uma issue no GitHub.');
      parar();
    }
  }, esperaMs);
  function parar(): void { clearTimeout(temporizador); doc.removeEventListener('visibilitychange', aoMudar); }
  doc.addEventListener('visibilitychange', aoMudar);
  return parar;
}
