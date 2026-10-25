"""Extração simbólica de sintomas para a atividade CardioIA, Parte 1.

O CSV fornece as associações; os grupos abaixo evitam contar sinônimos como
evidências independentes. A pontuação é didática, não probabilidade clínica.
"""
from pathlib import Path
import csv
import re
import unicodedata
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent
TXT_PATH = BASE_DIR / "sintomas_pacientes.txt"
CSV_PATH = BASE_DIR / "mapa_sintomas_doencas.csv"

# Conceitos linguísticos do mapa, sem atribuir doenças fora do CSV.
GRUPOS = {
    "dor no peito": "dor ou desconforto torácico",
    "desconforto no peito": "dor ou desconforto torácico",
    "aperto no peito": "dor ou desconforto torácico",
    "pressao no peito": "dor ou desconforto torácico",
    "dor no braco esquerdo": "dor no braço esquerdo",
    "suor frio": "suor frio",
    "falta de ar": "falta de ar",
    "enjoo": "náusea",
    "cansaco": "cansaço ou fadiga",
    "cansaco constante": "cansaço ou fadiga",
    "cansaco extremo": "cansaço ou fadiga",
    "inchaco nas pernas": "inchaço nas pernas",
    "dificuldade para dormir deitado": "dificuldade para dormir deitado",
    "palpitacao": "percepção de batimentos alterados",
    "coracao acelerado": "percepção de batimentos alterados",
    "batimentos irregulares": "percepção de batimentos alterados",
    "tontura": "tontura",
    "desmaio": "desmaio",
}


def normalizar(texto: str) -> str:
    """Padroniza caixa, acentos e espaços tanto no relato quanto no mapa."""
    texto = unicodedata.normalize("NFD", texto.casefold())
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto).strip()


def carregar_mapa(caminho: Path = CSV_PATH) -> list[dict]:
    """Lê e valida o CSV; cada expressão mantém suas associações e conceito."""
    entradas = {}
    with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        colunas = {"Sintoma 1", "Sintoma 2", "Doença Associada"}
        if not colunas.issubset(leitor.fieldnames or []):
            raise ValueError("O mapa deve conter Sintoma 1, Sintoma 2 e Doença Associada.")
        for numero, linha in enumerate(leitor, start=2):
            if not all((linha.get(c) or "").strip() for c in colunas):
                raise ValueError(f"Linha {numero} do mapa contém campos vazios.")
            principal = normalizar(linha["Sintoma 1"])
            if principal not in GRUPOS:
                raise ValueError(f"Defina um grupo linguístico para: {linha['Sintoma 1']}")
            grupo = GRUPOS[principal]
            for coluna in ("Sintoma 1", "Sintoma 2"):
                expressao = normalizar(linha[coluna])
                if expressao in entradas and entradas[expressao]["grupo"] != grupo:
                    raise ValueError(f"Expressão com grupos conflitantes: {expressao}")
                entrada = entradas.setdefault(expressao, {
                    "expressao": expressao, "grupo": grupo, "condicoes": set()
                })
                entrada["condicoes"].add(linha["Doença Associada"].strip())
    if not entradas:
        raise ValueError("O mapa está vazio.")
    return list(entradas.values())


def esta_negado(trecho: str, inicio: int) -> bool:
    """Regra local e limitada: negação anterior no mesmo segmento de texto.

    Pontuação, adversativas e uma nova afirmação encerram o escopo.
    'Não consigo dormir deitado' é uma expressão positiva do mapa: o 'não'
    faz parte da expressão, não do prefixo examinado aqui.
    """
    prefixo = trecho[:inicio]
    segmento = re.split(
        r"[.,;:!?\n]|\b(?:mas|porem|contudo)\b|"
        r"\be\s+(?=(?:sinto|tenho|percebo|noto|estou)\b)",
        prefixo,
    )[-1]
    return bool(re.search(
        r"\b(?:sem|nego|nega|negou)\b|"
        r"\bnao\s+(?:(?:estou|esta)\s+(?:com|sentindo)|"
        r"(?:tenho|tem|sinto|sente|apresento|apresenta))\b",
        segmento,
    ))


def analisar_relato(frase: str, mapeamento: list[dict]) -> dict:
    """Extrai expressões e conta conceitos distintos associados a cada condição."""
    texto = normalizar(frase)
    candidatos = []
    for entrada in mapeamento:
        base = re.escape(entrada["expressao"])
        # Variação controlada do relato 10, preservando a expressão completa.
        if entrada["expressao"] == "desconforto no peito":
            base = r"desconforto(?:\s+constante)?\s+no\s+peito"
        padrao = r"(?<!\w)" + base + r"(?!\w)"
        for match in re.finditer(padrao, texto):
            candidatos.append({**entrada, "expressao": match.group(),
                               "inicio": match.start(), "fim": match.end()})

    # A expressão mais específica prevalece no mesmo trecho: "fadiga extrema"
    # não será contada novamente como "fadiga". A ordem do CSV não decide.
    escolhidos = []
    for item in sorted(candidatos, key=lambda x: (
        -(x["fim"] - x["inicio"]), x["inicio"], x["expressao"]
    )):
        if any(item["inicio"] < outro["fim"] and outro["inicio"] < item["fim"]
               for outro in escolhidos):
            continue
        escolhidos.append(item)

    encontrados, negados = [], []
    evidencias = defaultdict(set)
    for item in sorted(escolhidos, key=lambda x: x["inicio"]):
        if esta_negado(texto, item["inicio"]):
            negados.append(item)
            continue
        encontrados.append(item)
        for condicao in item["condicoes"]:
            evidencias[condicao].add(item["grupo"])

    pontuacoes = {nome: len(grupos) for nome, grupos in sorted(evidencias.items())}
    maior = max(pontuacoes.values(), default=0)
    sugestoes = [nome for nome, pontos in pontuacoes.items() if pontos == maior]
    return {
        "encontrados": encontrados, "negados": negados,
        "evidencias": dict(evidencias), "pontuacoes": pontuacoes,
        "sugestoes": sugestoes,
    }


def descrever_sugestao(resultado: dict) -> str:
    if not resultado["sugestoes"]:
        return "Sem correspondência afirmativa no mapa; isso não exclui doença."
    nomes = "; ".join(resultado["sugestoes"])
    if len(resultado["sugestoes"]) > 1:
        return f"Associações empatadas: {nomes}. O mapa não permite escolher uma só."
    return f"Sugestão didática com mais sintomas associados: {nomes}."


def sugerir_diagnostico(frase: str, mapeamento: list[dict]) -> str:
    return descrever_sugestao(analisar_relato(frase, mapeamento))


def main() -> None:
    mapa = carregar_mapa()
    frases = [linha.strip() for linha in TXT_PATH.read_text(encoding="utf-8-sig").splitlines()
              if linha.strip()]
    if len(frases) != 10:
        raise ValueError(f"Esperados 10 relatos; encontrados {len(frases)}.")
    print("=== Extração de sintomas e sugestões didáticas ===")
    print("Contagem de conceitos do mapa; não é probabilidade nem diagnóstico clínico.")
    for indice, frase in enumerate(frases, start=1):
        resultado = analisar_relato(frase, mapa)
        print(f"\n{indice}. {frase}")
        print("   Expressões reconhecidas (normalizadas):")
        for item in resultado["encontrados"]:
            nomes = ", ".join(sorted(item["condicoes"]))
            print(f"   - {item['expressao']} -> {item['grupo']} -> {nomes}")
        if not resultado["encontrados"]:
            print("   - Nenhuma expressão afirmativa reconhecida.")
        if resultado["negados"]:
            print("   Negadas pela regra local: " +
                  ", ".join(item["expressao"] for item in resultado["negados"]))
        for nome, pontos in sorted(resultado["pontuacoes"].items(),
                                   key=lambda par: (-par[1], par[0])):
            grupos = ", ".join(sorted(resultado["evidencias"][nome]))
            print(f"   {nome}: {pontos} conceito(s) distinto(s) [{grupos}]")
        print("   " + descrever_sugestao(resultado))


if __name__ == "__main__":
    main()
