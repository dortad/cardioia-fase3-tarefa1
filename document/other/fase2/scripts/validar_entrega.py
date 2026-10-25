"""Valida os artefatos documentais e o notebook exigidos pela entrega."""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
IGNORAR = {".git", ".venv", "Apostilas", "docs", "fase2", "logs", "tmp", "__pycache__"}
OBRIGATORIOS = (
    "README.md",
    "document/Enunciado.md",
    "document/image.png",
    "document/image-1.png",
    "document/ai_project_document_fiap.md",
    "src/parte1/sintomas_pacientes.txt",
    "src/parte1/mapa_sintomas_doencas.csv",
    "src/parte1/diagnostico_sintomas.py",
    "src/parte2/frases_risco.csv",
    "src/parte2/classificador_risco.ipynb",
)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)|!\[[^\]]*\]\(([^)]+)\)")


def validar_arquivos() -> None:
    ausentes = [nome for nome in OBRIGATORIOS if not (ROOT / nome).is_file()]
    if ausentes:
        raise AssertionError("Arquivos obrigatórios ausentes: " + ", ".join(ausentes))


def validar_notebook() -> None:
    caminho = ROOT / "src/parte2/classificador_risco.ipynb"
    notebook = json.loads(caminho.read_text(encoding="utf-8"))
    codigo = [celula for celula in notebook.get("cells", []) if celula.get("cell_type") == "code"]
    if not codigo:
        raise AssertionError("O notebook não contém células de código.")
    pendentes = [i for i, celula in enumerate(codigo, 1) if celula.get("execution_count") is None]
    erros = [
        i
        for i, celula in enumerate(codigo, 1)
        if any(saida.get("output_type") == "error" for saida in celula.get("outputs", []))
    ]
    if pendentes or erros:
        raise AssertionError(f"Notebook inválido: células pendentes={pendentes}; erros={erros}")


def validar_links() -> int:
    ausentes: list[str] = []
    verificados = 0
    for markdown in ROOT.rglob("*.md"):
        if any(parte in IGNORAR for parte in markdown.relative_to(ROOT).parts):
            continue
        texto = markdown.read_text(encoding="utf-8")
        for correspondencia in LINK.finditer(texto):
            bruto = next(grupo for grupo in correspondencia.groups() if grupo is not None).strip()
            alvo = bruto.split("#", 1)[0].strip().strip("<>")
            if not alvo or re.match(r"^(?:https?://|mailto:)", alvo, re.I):
                continue
            verificados += 1
            if not (markdown.parent / alvo).resolve().exists():
                linha = texto.count("\n", 0, correspondencia.start()) + 1
                ausentes.append(f"{markdown.relative_to(ROOT)}:{linha} -> {alvo}")
    if ausentes:
        raise AssertionError("Links locais ausentes:\n" + "\n".join(ausentes))
    return verificados


def main() -> None:
    validar_arquivos()
    validar_notebook()
    total_links = validar_links()
    print(f"Entrega estrutural válida; {total_links} links locais conferidos.")


if __name__ == "__main__":
    main()
