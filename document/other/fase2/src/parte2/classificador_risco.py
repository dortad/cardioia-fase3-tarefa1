"""TF-IDF + regressão logística, com divisão fixa por cenários documentados."""
from pathlib import Path
import hashlib
import json
import platform
import re
import unicodedata
from importlib.metadata import version

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent
CLASSES = ["alto risco", "baixo risco"]


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.casefold())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return " ".join(re.findall(r"\w+", texto))


def carregar_dados(base=BASE_DIR):
    """Confere texto, proveniência, snapshot e grupos antes de permitir treino."""
    base = Path(base)
    dados = pd.read_csv(base / "frases_risco.csv", keep_default_na=False)
    origem = pd.read_csv(base / "proveniencia_frases.csv", keep_default_na=False)
    divisao = pd.read_csv(base / "divisao_avaliacao.csv", keep_default_na=False)
    meta = json.loads((base / "protocolo_avaliacao.json").read_text(encoding="utf-8"))
    if list(dados.columns) != ["frase", "situacao"]:
        raise ValueError("O CSV de treinamento deve conter somente frase,situacao.")
    if len(dados) != 60 or dados["situacao"].value_counts().to_dict() != dict.fromkeys(CLASSES, 30):
        raise ValueError("Esperados 60 registros e equilíbrio 30/30.")
    if not dados.equals(origem[["frase", "situacao"]]):
        raise ValueError("Texto/rótulo divergente entre dataset e proveniência.")
    ids = {f"P{i:02}" for i in range(1, 61)}
    for tabela in (origem, divisao):
        if len(tabela) != 60 or not tabela["id"].is_unique or set(tabela["id"]) != ids:
            raise ValueError("IDs incompletos, repetidos ou desconhecidos.")
    if dados["frase"].map(normalizar).duplicated().any():
        raise ValueError("Frases duplicadas após normalização.")
    df = origem.merge(divisao, on="id", validate="one_to_one")
    if set(df["conjunto"]) != {"treino", "teste"} or (df["grupo_avaliacao"] == "").any():
        raise ValueError("Divisão inválida ou grupo vazio.")
    if (df.groupby("grupo_avaliacao")["conjunto"].nunique() != 1).any():
        raise ValueError("Vazamento: grupo aparece em treino e teste.")
    if (df.groupby("familia_cenario")["conjunto"].nunique() != 1).any():
        raise ValueError("Vazamento: família aparece em treino e teste.")
    for conjunto, esperado in (("treino", 41), ("teste", 19)):
        parte = df[df["conjunto"] == conjunto]
        if len(parte) != esperado or set(parte["situacao"]) != set(CLASSES):
            raise ValueError("Tamanho ou classes da divisão divergentes do protocolo.")
    for nome, esperado in meta["sha256"].items():
        if hashlib.sha256((base / nome).read_bytes()).hexdigest() != esperado:
            raise ValueError(f"Arquivo alterado após congelar a divisão: {nome}")
    return df


def criar_modelo():
    # Sem remoção de stopwords: preserva não/sem. O fit recebe apenas frases de treino.
    return Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, strip_accents="unicode", ngram_range=(1, 2))),
        ("classificador", LogisticRegression(C=1.0, solver="lbfgs", max_iter=1000, random_state=42)),
    ])


def avaliar(modelo, treino, teste):
    previsto = modelo.predict(teste["frase"])
    # Referência ingênua ajustada somente com os rótulos de treino.
    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(np.zeros((len(treino), 1)), treino["situacao"])
    pred_base = baseline.predict(np.zeros((len(teste), 1)))
    saidas = teste[["id", "grupo_avaliacao", "frase", "situacao"]].copy()
    saidas["previsto"] = previsto
    saidas["acerto"] = saidas["situacao"] == saidas["previsto"]
    resultado = {
        "n_treino": len(treino), "n_teste": len(teste),
        "acuracia": float(accuracy_score(teste["situacao"], previsto)),
        "acuracia_baseline": float(accuracy_score(teste["situacao"], pred_base)),
        "classe_baseline": str(pred_base[0]),
        "relatorio": classification_report(teste["situacao"], previsto, labels=CLASSES, output_dict=True, zero_division=0),
        "ordem_classes_matriz": CLASSES,
        "matriz_confusao": confusion_matrix(teste["situacao"], previsto, labels=CLASSES).tolist(),
        "ids_treino": treino["id"].tolist(), "ids_teste": teste["id"].tolist(),
        "versoes": {nome: version(nome) for nome in ("pandas", "numpy", "scikit-learn")},
        "python": platform.python_version(),
    }
    return resultado, saidas


def exportar(resultado, saidas, base=BASE_DIR):
    destino = Path(base) / "resultados"
    destino.mkdir(exist_ok=True)
    (destino / "metricas.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    saidas.to_csv(destino / "previsoes_teste.csv", index=False, encoding="utf-8")


def main():
    dados = carregar_dados()
    treino = dados[dados["conjunto"] == "treino"]
    teste = dados[dados["conjunto"] == "teste"]
    modelo = criar_modelo()
    modelo.fit(treino["frase"], treino["situacao"])
    resultado, saidas = avaliar(modelo, treino, teste)
    exportar(resultado, saidas)
    print(f"Treino: {len(treino)} | Teste: {len(teste)} | grupos sem sobreposição")
    print(f"Acurácia: {resultado['acuracia']:.2%} | baseline: {resultado['acuracia_baseline']:.2%}")
    print(classification_report(teste["situacao"], saidas["previsto"], labels=CLASSES, zero_division=0))
    print("Erros no teste:")
    print(saidas.loc[~saidas["acerto"], ["id", "frase", "situacao", "previsto"]].to_string(index=False))
    print("Resultado didático em 19 frases sintéticas; não é desempenho clínico.")


if __name__ == "__main__":
    main()
