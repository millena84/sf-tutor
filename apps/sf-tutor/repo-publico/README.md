# repo-publico/

Arquivos que vão para a raiz do repositório público do tutorial (millena84/tutorial-sf-grafo), além do site em `docs/`.
O script `scripts/publicar-docs.sh` copia `.github/ISSUE_TEMPLATE/` daqui para lá a cada publicação; não edite esses
arquivos direto no repositório público, porque a próxima publicação os sobrescreve.

- `.github/ISSUE_TEMPLATE/erro-reportado.yml`: modelo da issue aberta pelo botão "Reportar erro" do site. Os ids dos
  campos (item, link, versao, tipo, descricao, correto, fonte) são os que `src/reporte.ts` preenche pela URL.
- O label `erro-reportado` precisa existir no repositório público; o workflow de publicação tenta criá-lo.
