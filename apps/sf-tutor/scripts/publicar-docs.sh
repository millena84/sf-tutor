#!/usr/bin/env bash
# Prepara a pasta docs/ do repositório público (millena84/tutorial-sf-grafo) a partir de apps/sf-tutor/dist.
# Faz só a parte local da publicação: copia dist/ para docs/, remove docs/__teste-sintetico e cria docs/.nojekyll.
# Não faz commit, push nem PR: isso fica com quem chama (o workflow publicar.yml ou a pessoa).
#
# Uso: scripts/publicar-docs.sh <pasta do clone do repositório público>
# Saída: a última linha é "mudou=sim" ou "mudou=nao". "nao" quer dizer que só o build-info.json mudaria
#        (mesmo conteúdo, outro commit ou outra data); nesse caso docs/ é devolvida ao estado anterior.
#        Se GITHUB_OUTPUT estiver definido, a mesma linha é gravada lá.
set -euo pipefail

app="$(cd "$(dirname "$0")/.." && pwd)"
destino="${1:?Informe a pasta do clone do repositório público}"
dist="$app/dist"
info="$dist/data/build-info.json"

[ -f "$dist/index.html" ] || { echo "ERRO: $dist/index.html não existe. Rode 'npm run build' antes." >&2; exit 1; }
[ -f "$info" ] || { echo "ERRO: $info não existe. Rode 'npm run build' antes." >&2; exit 1; }
git -C "$destino" rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "ERRO: $destino não é um repositório git." >&2; exit 1; }

# O build precisa vir de um estado commitado e sem a fixture de performance.
if grep -q 'alterações-locais' "$info"; then
  echo "ERRO: o build foi feito com alterações locais nos insumos (veja $info). Faça o commit e rode 'npm run build' de novo." >&2
  exit 1
fi
if [ -e "$dist/__teste-sintetico" ]; then
  echo "ERRO: dist/ contém a fixture sintética de performance. Rode 'npm run build' depois de 'npm run perf'." >&2
  exit 1
fi

rm -rf "$destino/docs"
cp -r "$dist" "$destino/docs"
rm -rf "$destino/docs/__teste-sintetico"
touch "$destino/docs/.nojekyll"

git -C "$destino" add -A docs
alterados="$(git -C "$destino" diff --cached --name-only -- docs | grep -v '^docs/data/build-info\.json$' || true)"
if [ -z "$alterados" ]; then
  # Só o build-info mudaria: não vale uma publicação.
  git -C "$destino" reset -q HEAD -- docs
  git -C "$destino" checkout -q -- docs
  git -C "$destino" clean -qfd -- docs
  resultado="mudou=nao"
else
  echo "Arquivos alterados em docs/: $(printf '%s\n' "$alterados" | wc -l)"
  resultado="mudou=sim"
fi
if [ -n "${GITHUB_OUTPUT:-}" ]; then echo "$resultado" >> "$GITHUB_OUTPUT"; fi
echo "$resultado"
