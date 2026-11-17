"""Auditoria de conteúdo dos nós (rodada D1, fechamento do MVP).

Procura, nos textos explicativos do catálogo, sinais de conteúdo genérico ou incompleto:
- campo explicativo vazio ou curto demais;
- texto idêntico em nós diferentes (o mesmo parágrafo servindo para dois itens);
- texto que só repete o nome do nó;
- frases-modelo conhecidas de preenchimento genérico;
- propriedades e campos sem descrição ou com a explicação marcada como pendente (contados por nó).

Não corrige nada: grava relatorios/auditoria-conteudo.md e devolve código 0.
Uso: python3 ferramentas/auditoria_conteudo.py
"""
import collections
import glob
import json
import os
import re

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CAT = os.path.join(RAIZ, "catalogo")
SAIDA = os.path.join(RAIZ, "relatorios", "auditoria-conteudo.md")

# pasta -> campos de texto explicativo que um nó dessa pasta deve ter
CAMPOS = {
    "funcionalidades": ["o_que_e", "finalidade", "exemplo"],
    "metadata-types": ["o_que_e", "finalidade"],
    "objetos-api": ["o_que_e", "papel"],
    "estruturas": ["o_que_e"],
    "nuvens": ["resumo", "o_que_e"],
    "classificacoes": ["descricao", "escopo"],
    "subclassificacoes": ["descricao", "escopo"],
}
PENDENTE = "Explicação pendente"  # texto padrão da carga quando a fonte não traz descrição
MINIMO = 40  # caracteres; abaixo disso o texto quase sempre não explica nada
MODELOS = [
    r"\bdescri[cç][aã]o n[aã]o dispon[ií]vel\b", r"\blorem ipsum\b",
    r"\bem constru[cç][aã]o\b", r"\ba definir\b", r"\bpreencher\b", r"\bplaceholder\b",
]
MODELOS_CASO = [r"\bTODO\b", r"\bTBD\b", r"\bFIXME\b"]  # só em maiúsculas: "todo" é palavra comum em português


def normal(t):
    return re.sub(r"\s+", " ", (t or "").strip().lower())


def carregar():
    nos = []
    for pasta in CAMPOS:
        for f in sorted(glob.glob(os.path.join(CAT, pasta, "*.json"))):
            with open(f, encoding="utf-8") as h:
                nos.append((pasta, os.path.basename(f)[:-5], json.load(h)))
    return nos


def auditar(nos):
    curtos, vazios, eco, modelo = [], [], [], []
    textos = collections.defaultdict(list)
    sem_desc = []
    for pasta, nome, d in nos:
        rotulo = d.get("nome") or d.get("nome_oficial") or nome
        for campo in CAMPOS[pasta]:
            t = d.get(campo)
            if not isinstance(t, str) or not t.strip():
                vazios.append((pasta, nome, campo))
                continue
            n = normal(t)
            if len(n) < MINIMO:
                curtos.append((pasta, nome, campo, t.strip()))
            if n.rstrip(".") == normal(rotulo):
                eco.append((pasta, nome, campo))
            if any(re.search(p, n, re.I) for p in MODELOS) or any(re.search(p, t) for p in MODELOS_CASO):
                modelo.append((pasta, nome, campo, t.strip()[:120]))
            if len(n) >= MINIMO:
                textos[n].append(f"{pasta}/{nome}.{campo}")
        itens = d.get("propriedades") or d.get("campos") or []
        faltam = [p for p in itens if isinstance(p, dict) and
                  (not (p.get("o_que_e") or "").strip() or p["o_que_e"].startswith(PENDENTE))]
        if faltam:
            sem_desc.append((pasta, nome, len(faltam), len(itens)))
    duplicados = [(t, ls) for t, ls in textos.items() if len(ls) > 1]
    return vazios, curtos, eco, modelo, duplicados, sem_desc


def escrever(nos, vazios, curtos, eco, modelo, duplicados, sem_desc):
    cont = collections.Counter(p for p, _, _ in nos)
    L = ["# Auditoria de conteúdo dos nós", "",
         "Gerado por `ferramentas/auditoria_conteudo.py`. Não edite à mão.",
         "Mede sinais de texto genérico ou incompleto; não julga se o conteúdo está correto (isso exige fonte).", "",
         "## Universo auditado", ""]
    L += [f"- {p}: {cont[p]} nós; campos {', '.join('`'+c+'`' for c in CAMPOS[p])}" for p in CAMPOS]
    L += ["", "## Resumo", "",
          f"- Campos explicativos vazios: {len(vazios)}",
          f"- Campos com menos de {MINIMO} caracteres: {len(curtos)}",
          f"- Campos que só repetem o nome do nó: {len(eco)}",
          f"- Campos com frase-modelo de preenchimento: {len(modelo)}",
          f"- Textos idênticos em mais de um nó: {len(duplicados)}",
          f"- Nós com propriedades ou campos sem explicação: {len(sem_desc)} "
          f"({sum(k for _, _, k, _ in sem_desc)} itens de {sum(t for _, _, _, t in sem_desc)} nesses nós)", ""]

    def secao(titulo, linhas):
        L.extend([f"## {titulo}", ""] + (linhas or ["Nenhum."]) + [""])

    secao("Campos vazios", [f"- `{p}/{n}`: `{c}`" for p, n, c in vazios])
    secao("Campos curtos", [f"- `{p}/{n}`.`{c}`: {t}" for p, n, c, t in curtos])
    secao("Campos que repetem o nome", [f"- `{p}/{n}`: `{c}`" for p, n, c in eco])
    secao("Frases-modelo", [f"- `{p}/{n}`.`{c}`: {t}" for p, n, c, t in modelo])
    secao("Textos idênticos", [f"- {', '.join('`'+x+'`' for x in ls)}: \"{t[:100]}…\"" for t, ls in duplicados])
    secao("Propriedades ou campos sem explicação (vazia ou marcada como pendente), por nó",
          [f"- `{p}/{n}`: {k} de {tot}" for p, n, k, tot in sorted(sem_desc, key=lambda x: -x[2])])
    with open(SAIDA, "w", encoding="utf-8") as h:
        h.write("\n".join(L).rstrip() + "\n")


def main():
    nos = carregar()
    r = auditar(nos)
    escrever(nos, *r)
    print("auditoria de conteúdo:", ", ".join(f"{k}={len(v)}" for k, v in
          zip(["vazios", "curtos", "eco", "modelo", "duplicados", "sem_descricao"], r)), "->", os.path.relpath(SAIDA, RAIZ))


if __name__ == "__main__":
    main()
