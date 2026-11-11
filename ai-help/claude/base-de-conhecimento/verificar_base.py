#!/usr/bin/env python3
"""Validação estrutural local, sem rede, dependências ou acesso a uma org."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


BASE = Path(__file__).resolve().parent
SVG_NS = "{http://www.w3.org/2000/svg}"


def verificar(base=BASE):
    """Retorna falhas, permitindo testar o verificador em uma cópia temporária."""
    erros = []
    markdowns = sorted(base.rglob("*.md"))
    for caminho in markdowns:
        texto = caminho.read_text(encoding="utf-8")
        sem_codigo = re.sub(r"```.*?```", "", texto, flags=re.S)
        for destino in re.findall(r"!?\[[^\]]*\]\(([^)\s]+)\)", sem_codigo):
            partes = urlsplit(destino)
            if partes.scheme or partes.netloc or not partes.path:
                continue
            alvo = caminho.parent / unquote(partes.path)
            if not alvo.exists():
                erros.append(f"{caminho.relative_to(base)}: link inexistente {destino}")
        for numero, xml in enumerate(re.findall(r"```xml\s*\n(.*?)```", texto, re.S), 1):
            try:
                ET.fromstring(xml)
            except ET.ParseError as exc:
                erros.append(f"{caminho.relative_to(base)}: XML {numero}: {exc}")

    diagramas = sorted((base / "svg").glob("bloco-*.svg"))
    if len(diagramas) != 11:
        erros.append(f"Esperados 11 diagramas; encontrados {len(diagramas)}")
    for caminho in sorted(base.rglob("*.svg")):
        try:
            raiz = ET.parse(caminho).getroot()
        except ET.ParseError as exc:
            erros.append(f"{caminho.relative_to(base)}: SVG inválido: {exc}")
            continue
        if caminho.parent != base / "svg":
            continue
        for tag in ("title", "desc"):
            elemento = raiz.find(SVG_NS + tag)
            if elemento is None or not "".join(elemento.itertext()).strip():
                erros.append(f"{caminho.name}: falta {tag} acessível")
        if raiz.get("role") != "img":
            erros.append(f"{caminho.name}: falta role=img")
        if not raiz.findall(f".//{SVG_NS}g[@data-brand-footer='true']"):
            erros.append(f"{caminho.name}: rodapé de marca ausente")
        # O corpo é claro; o rodapé escuro contém texto claro intencionalmente.
        def checar_texto(elemento):
            if elemento.get("data-brand-footer") == "true":
                return
            if elemento.tag == SVG_NS + "text":
                if elemento.get("fill") not in {"#0B0F2A", "#1C1440"}:
                    erros.append(f"{caminho.name}: texto fora da paleta escura do corpo")
                if float(elemento.get("fill-opacity", "1")) < 1:
                    erros.append(f"{caminho.name}: texto translúcido no corpo claro")
            for filho in elemento:
                checar_texto(filho)
        checar_texto(raiz)

    roteiro = base / "roteiro-sf-para-techs" / "roteiro-salesforce-backend.md"
    if not roteiro.exists():
        erros.append("Roteiro principal ausente")
        return erros
    texto = roteiro.read_text(encoding="utf-8")
    parte = texto.split("## Roteiro completo\n", 1)
    if len(parte) != 2:
        erros.append("Seção Roteiro completo ausente")
        return erros
    apresentacao = parte[1].split("\n## Apoio prático", 1)[0]
    blocos = re.findall(r"### ([^\n]+)\n(.*?)(?=\n### |\Z)", apresentacao, re.S)
    if len(blocos) != 11:
        erros.append(f"Esperados 11 blocos; encontrados {len(blocos)}")
    duracoes = []
    for numero, (titulo, corpo) in enumerate(blocos):
        duracao = re.search(r"Bloco (\d+), duração de (\d+) minutos\. Objetivo:", corpo)
        if not duracao or int(duracao[1]) != numero or not 1 <= int(duracao[2]) <= 10:
            erros.append(f"{titulo}: identificação, objetivo ou duração inválidos")
        if duracao:
            duracoes.append(int(duracao[2]))
        pontos = len(re.findall(r"^- \*\*", corpo, re.M))
        if not 3 <= pontos <= 5:
            erros.append(f"{titulo}: {pontos} pontos principais; esperados 3 a 5")
        for marcador in ("Analogia back-end:", "Desenho de lousa:", "Pergunta de fixação:"):
            if marcador not in corpo:
                erros.append(f"{titulo}: falta {marcador}")
        imagens = re.findall(r"!\[[^\]]+\]\(([^)]+)\)", corpo)
        if len(imagens) != 1 or not imagens[0].startswith(f"../svg/bloco-{numero:02d}-"):
            erros.append(f"{titulo}: referência do SVG não corresponde ao bloco")
    tabela = texto.split("## Distribuição de tempo\n", 1)
    if len(tabela) != 2:
        erros.append("Tabela de tempos ausente")
    else:
        linhas = re.findall(r"^\| (\d+) \| [^\n]+ \| (\d+) min \|$", tabela[1], re.M)
        esperado = [(str(i), str(tempo)) for i, tempo in enumerate(duracoes)]
        if linhas != esperado:
            erros.append("Tabela de tempos diverge das durações dos blocos")
        total = re.search(r"\| \*\*Total\*\* \| \| \*\*(\d+) min\*\* \|", tabela[1])
        if not total or int(total[1]) != sum(duracoes):
            erros.append("Total de minutos diverge da soma dos blocos")
    return erros


if __name__ == "__main__":
    falhas = verificar()
    if falhas:
        print("FALHA\n" + "\n".join(f"- {falha}" for falha in falhas))
        sys.exit(1)
    print("OK: links locais, SVG/XML e estrutura dos 11 blocos.")
    print("Não valida org, compilação Apex, âncoras ou disponibilidade de URLs externas.")
