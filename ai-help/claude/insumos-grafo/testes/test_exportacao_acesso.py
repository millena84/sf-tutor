import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
ARQUIVO = ROOT / "exportacoes/acesso/gerar.py"
SPEC = importlib.util.spec_from_file_location("exportacao_acesso", ARQUIVO)
EXPORTACAO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORTACAO)


class TestExportacaoAcesso(unittest.TestCase):
    def test_exportacao_reproduz_catalogo_e_e_deterministica(self):
        with tempfile.TemporaryDirectory() as diretorio:
            destino = Path(diretorio)
            with patch.object(EXPORTACAO, "DESTINO", destino):
                EXPORTACAO.gerar()
                arquivos = {p.name: p.read_bytes() for p in destino.glob("*.json")}
                EXPORTACAO.gerar()
                self.assertEqual(arquivos, {p.name: p.read_bytes() for p in destino.glob("*.json")})
                for nome, conteudo in arquivos.items():
                    self.assertEqual(conteudo, (ARQUIVO.parent / nome).read_bytes())

                user = json.loads(arquivos["User.json"])
                self.assertIsNone(user["metadata_type"])
                self.assertEqual(
                    user["objetos_api_relacionados"][0],
                    EXPORTACAO.ler(ROOT / "catalogo/objetos-api/User.json"),
                )
                self.assertEqual(user["estado"], "parcial")

                profile = json.loads(arquivos["Profile.json"])
                self.assertEqual(
                    len(profile["estruturas_xml"]),
                    len(profile["metadata_type"]["estruturas"]),
                )
                role = json.loads(arquivos["Role.json"])
                self.assertIsNone(role["metadata_type"]["propriedades"])
                self.assertIsNone(role["objetos_api_relacionados"][0]["campos"])

                owd = json.loads(arquivos["OWD.json"])
                nomes = {p["nome"] for p in owd["metadata_type"]["propriedades"]}
                self.assertTrue({"sharingModel", "externalSharingModel"} <= nomes)
                self.assertEqual(owd["metadata_type"]["nome"], "CustomObject")


if __name__ == "__main__":
    unittest.main()
