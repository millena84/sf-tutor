"""Testes estruturais; executar com unittest discover, sem dependências."""

from pathlib import Path
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

from verificar_base import BASE, SVG_NS, verificar


class VerificadorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name) / "base"
        shutil.copytree(BASE, self.base, ignore=shutil.ignore_patterns("__pycache__"))
        self.svg = self.base / "svg" / "bloco-00-camadas.svg"
        self.roteiro = self.base / "roteiro-sf-para-techs" / "roteiro-salesforce-backend.md"

    def test_base_atual(self):
        self.assertEqual(verificar(self.base), [])

    def test_imagem_ausente(self):
        self.svg.unlink()
        erros = verificar(self.base)
        self.assertTrue(any("link inexistente" in erro for erro in erros))
        self.assertTrue(any("Esperados 11 diagramas" in erro for erro in erros))

    def test_svg_malformado(self):
        self.svg.write_text("<svg>", encoding="utf-8")
        self.assertTrue(any("SVG inválido" in erro for erro in verificar(self.base)))

    def test_texto_translucido(self):
        tree = ET.parse(self.svg)
        tree.getroot().find(".//" + SVG_NS + "text").set("fill-opacity", "0.16")
        tree.write(self.svg, encoding="utf-8")
        self.assertTrue(any("translúcido" in erro for erro in verificar(self.base)))

    def test_duracao_invalida(self):
        texto = self.roteiro.read_text(encoding="utf-8")
        self.roteiro.write_text(texto.replace("duração de 3 minutos", "duração de 13 minutos", 1),
                               encoding="utf-8")
        self.assertTrue(any("duração inválidos" in erro for erro in verificar(self.base)))

    def test_total_errado(self):
        texto = self.roteiro.read_text(encoding="utf-8")
        self.roteiro.write_text(texto.replace("**85 min**", "**95 min**", 1), encoding="utf-8")
        self.assertTrue(any("Total de minutos" in erro for erro in verificar(self.base)))

    def test_tabela_divergente(self):
        texto = self.roteiro.read_text(encoding="utf-8")
        self.roteiro.write_text(texto.replace("| Mapa geral | 3 min |", "| Mapa geral | 4 min |", 1),
                               encoding="utf-8")
        self.assertTrue(any("Tabela de tempos diverge" in erro for erro in verificar(self.base)))


if __name__ == "__main__":
    unittest.main()
