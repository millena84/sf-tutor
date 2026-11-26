# repo-publico/

Arquivos que vão para a raiz do repositório público do Metadata Desbugado (millena84/metadata-desbugando), além do site em `docs/`.
O script `scripts/publicar-docs.sh` copia `.github/ISSUE_TEMPLATE/` daqui para lá a cada publicação; não edite esses
arquivos direto no repositório público, porque a próxima publicação os sobrescreve.

- `.github/ISSUE_TEMPLATE/erro-reportado.yml`: modelo da issue aberta pelo botão "Reportar erro" do site. Os ids dos
  campos (item, link, versao, tipo, descricao, correto, fonte) são os que `src/reporte.ts` preenche pela URL.
- `LICENSE` (MIT, código) e `LICENSE-CONTEUDO.md` (CC BY 4.0 para textos e dados; marca, mascote e ícones Desbugando
  com todos os direitos reservados): copiados para a raiz do repositório público.
- `README-publico.md`: vira o `README.md` da raiz do repositório público a cada publicação.
- Os labels da triagem (`erro-reportado`, `confirmado`, `sem-mudanca`, `aguardando-fonte`, `duplicado`, `creditar`) precisam existir no repositório público; o workflow de publicação tenta criá-los. A rotina está em `ai-help/claude/insumos-grafo/relatorios/triagem-erros-reportados.md`.
