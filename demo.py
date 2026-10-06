"""Demonstração sintética. Sem rede ou gravações fora de diretório temporário."""
import copy
import hashlib
import json
import sqlite3
import tempfile
from pathlib import Path

from harness import Harness, canonical_url, merge_patch


def main():
    with tempfile.TemporaryDirectory() as directory:
        path = str(Path(directory) / "demo.sqlite3")
        h = Harness(path)
        try:
            h.start("demo-001")
            h.reserve("demo-001", searches=4, descriptions=7)
            h.reserve("demo-001", searches=2, descriptions=3)
            try:
                h.reserve("demo-001", searches=1)
                raise AssertionError("Excesso de orçamento aceito")
            except ValueError:
                pass
            assert canonical_url("https://example.com/jobs/42?utm_source=demo") == canonical_url("https://example.com/jobs/42")
            old = {"sua_leitura": "Não vista", "availability": "Aberta"}
            current = {**old, "sua_leitura": "Salva"}
            merged = merge_patch(old, current, {"sua_leitura": "Vista", "availability": "Encerrada"})
            assert merged["patch"] == {"availability": "Encerrada"}
            package = {
                "vacancy_id": "V-DEMO-001",
                "destination": "https://example.com/apply/42",
                "documents": [{"name": "cv-ficticio.txt", "sha256": hashlib.sha256(b"Documento ficticio").hexdigest()}],
                "answers": {"availability": "Resposta fictícia, não representa pessoa real"},
                "version": "demo-v1",
            }
            h.approve("C-DEMO-001", package, "Evidência fictícia somente para teste")
            changed = copy.deepcopy(package)
            changed["answers"]["availability"] = "Outro conteúdo"
            try:
                h.claim_submission("C-DEMO-001", changed, "Autorizada")
                raise AssertionError("Material alterado aceito")
            except ValueError:
                pass
            h.claim_submission("C-DEMO-001", package, "Autorizada")
            h.close()
            h = Harness(path)
            try:
                h.claim_submission("C-DEMO-001", package, "Autorizada")
                raise AssertionError("Tentativa repetida aceita")
            except sqlite3.IntegrityError:
                pass
            h.finish("demo-001", "Demonstração local concluída; nenhum envio externo")
            print(json.dumps({
                "resultado": "OK",
                "consultas_reservadas": 6,
                "descricoes_reservadas": 10,
                "excesso_de_orcamento": "bloqueado",
                "edicao_humana": "preservada",
                "pacote_modificado": "bloqueado",
                "repeticao_apos_interrupcao": "bloqueada",
                "estado_da_tentativa": "Envio em verificação",
                "envios_reais": 0,
            }, ensure_ascii=False, indent=2))
        finally:
            h.close()


if __name__ == "__main__":
    main()
