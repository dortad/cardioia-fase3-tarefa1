"""Valida os artefatos documentais exigidos pela entrega da Fase 3."""
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
# Acervos de fases anteriores ficam congelados como foram entregues e não são verificados.
IGNORAR = {".git", ".venv", "_interno", "Apostilas", "logs", "tmp", "__pycache__"}
IGNORAR_CAMINHOS = (Path("document/other"),)
OBRIGATORIOS = (
    "README.md",
    "document/Enunciado.md",
    "document/image.png",
    "document/image-1.png",
    "document/ai_project_document_fiap.md",
    "src/parte1_edge/README.md",
    "src/parte2_cloud/README.md",
)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)|!\[[^\]]*\]\(([^)]+)\)")


def validar_arquivos() -> None:
    ausentes = [nome for nome in OBRIGATORIOS if not (ROOT / nome).is_file()]
    if ausentes:
        raise AssertionError("Arquivos obrigatórios ausentes: " + ", ".join(ausentes))


def ignorado(relativo: Path) -> bool:
    if any(parte in IGNORAR for parte in relativo.parts):
        return True
    return any(relativo.is_relative_to(caminho) for caminho in IGNORAR_CAMINHOS)


def validar_links() -> int:
    ausentes: list[str] = []
    verificados = 0
    for markdown in ROOT.rglob("*.md"):
        relativo = markdown.relative_to(ROOT)
        if ignorado(relativo):
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
                ausentes.append(f"{relativo}:{linha} -> {alvo}")
    if ausentes:
        raise AssertionError("Links locais ausentes:\n" + "\n".join(ausentes))
    return verificados


def main() -> None:
    validar_arquivos()
    total_links = validar_links()
    print(f"Entrega estrutural válida; {total_links} links locais conferidos.")


if __name__ == "__main__":
    main()
