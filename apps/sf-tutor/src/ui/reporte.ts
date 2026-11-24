// Janela "Reportar erro": formulário curto que monta um e-mail (mailto) ou abre uma issue no repositório público.
import { assunto, type CamposReporte, type ContextoReporte, montarTexto, REPORTE, TIPOS_PROBLEMA, urlIssue, urlMailto } from '../reporte';
import { h, limpar } from './dom';

function campo(rotulo: string, controle: HTMLElement, ajuda?: string): HTMLElement {
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
  const tipo = h('select', { id: 'rep-tipo', required: '' },
    h('option', { value: '' }, 'Escolha…'), TIPOS_PROBLEMA.map((t) => h('option', { value: t }, t)));
  const descricao = h('textarea', { id: 'rep-descricao', required: '', rows: '4', maxlength: '1500' });
  const correto = h('textarea', { id: 'rep-correto', rows: '3', maxlength: '1000' });
  const fonte = h('input', { id: 'rep-fonte', type: 'url', placeholder: 'https://developer.salesforce.com/docs/…', maxlength: '500' });
  const nome = h('input', { id: 'rep-nome', type: 'text', autocomplete: 'name', maxlength: '80' });
  const github = h('input', { id: 'rep-github', type: 'text', placeholder: '@seu-usuario', maxlength: '40',
    pattern: '@?[A-Za-z0-9][A-Za-z0-9\\-]{0,38}', autocomplete: 'off', spellcheck: 'false' });
  const status = h('p', { class: 'nota', role: 'status' });
  const valores = (): CamposReporte => ({ tipo: tipo.value, descricao: descricao.value, correto: correto.value, fonte: fonte.value,
    nome: nome.value, github: github.value });
  const form = h('form', { class: 'form-reporte', novalidate: '' }) as HTMLFormElement;
  const valido = (): boolean => {
    if (form.checkValidity()) return true;
    form.reportValidity();
    status.textContent = 'Preencha o tipo de problema e o que está errado.';
    return false;
  };
  const btnEmail = h('button', { type: 'button', class: 'btn btn-primario' }, 'Enviar por e-mail');
  btnEmail.addEventListener('click', () => {
    if (!valido()) return;
    const url = urlMailto(c, valores());
    status.textContent = url.length > REPORTE.limiteMailto
      ? 'Abrindo o seu app de e-mail. O texto é longo e alguns apps cortam o final: se faltar algo, use "Copiar texto".'
      : 'Abrindo o seu app de e-mail. Se nada abrir, use "Copiar texto" e envie pelo seu e-mail.';
    location.href = url;
  });
  const btnIssue = h('button', { type: 'button', class: 'btn' }, 'Abrir issue no GitHub');
  btnIssue.addEventListener('click', () => {
    if (!valido()) return;
    window.open(urlIssue(c, valores()), '_blank', 'noopener');
    status.textContent = 'A issue abre numa nova aba, já preenchida; confira e clique em "Submit new issue" no GitHub.';
  });
  const btnCopiar = h('button', { type: 'button', class: 'btn' }, 'Copiar texto');
  btnCopiar.addEventListener('click', async () => {
    if (!valido()) return;
    const txt = `Assunto: ${assunto(c)}\n\n${montarTexto(c, valores())}`;
    try { await navigator.clipboard.writeText(txt); status.textContent = 'Texto copiado. Cole no seu e-mail ou numa issue.'; }
    catch { status.textContent = 'Não foi possível copiar automaticamente. Selecione o texto da prévia abaixo.'; previa.hidden = false; previa.textContent = txt; }
  });
  const previa = h('pre', { class: 'previa-reporte', hidden: '' });
  const fechar = h('button', { type: 'button', class: 'btn' }, 'Cancelar');
  fechar.addEventListener('click', () => dlg!.close());
  form.append(
    h('dl', { class: 'kv contexto-reporte' },
      h('dt', null, 'Item'), h('dd', null, `${c.rotulo} (${c.id})`),
      c.item ? [h('dt', null, 'Campo ou propriedade'), h('dd', null, c.item.nome)] : null,
      h('dt', null, 'Versão dos dados'), h('dd', null, c.versao)),
    h('p', { class: 'aviso aviso-sensivel', role: 'note' }, h('strong', null, 'Não inclua dados da sua org. '),
      'Nada de credenciais, tokens, IDs de registros, nomes de clientes ou dados pessoais de terceiros. Descreva o erro com o que aparece neste tutorial e, se puder, ',
      'aponte a página oficial da Salesforce que mostra o correto. A issue no GitHub é pública.'),
    campo('Tipo de problema (obrigatório)', tipo),
    campo('O que está errado (obrigatório)', descricao, 'Diga o que a ficha afirma e por que parece errado.'),
    campo('Qual seria o correto', correto),
    campo('Fonte', fonte, 'Link para a documentação oficial que confirma o correto, se tiver.'),
    h('fieldset', { class: 'campos-opcionais' },
      h('legend', null, 'Quem reporta (opcional)'),
      campo('Nome', nome, 'Para dar crédito nas Novidades quando a correção for publicada.'),
      campo('Usuário do GitHub', github, 'Para mencionar você na issue e nas Novidades. Pelo botão do GitHub, a issue já sai no seu usuário.')),
    h('div', { class: 'acoes acoes-reporte' }, btnEmail, btnIssue, btnCopiar, fechar),
    status, previa);
  dlg.append(
    h('div', { class: 'dialogo-cab' }, h('h2', { id: 'reporte-titulo' }, 'Reportar erro'), h('button', { type: 'button', class: 'btn', on: { click: () => dlg!.close() } }, 'Fechar')),
    h('div', { class: 'dialogo-corpo-reporte' },
      h('p', null, 'Achou uma informação errada, desatualizada ou confusa? Conte aqui. O texto sai pelo seu e-mail ou vira uma issue pública no GitHub; esta página não guarda nada.'),
      form));
  dlg.showModal();
  tipo.focus();
}
