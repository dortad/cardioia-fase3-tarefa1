# Parte 2 — Classificador básico de texto

Implementação e avaliação concluídas para a base didática de 60 frases. O [notebook executado](classificador_risco.ipynb) apresenta TF-IDF, regressão logística, baseline, matriz de confusão, erros, negações e vieses.

**Resultado:** 17/19 acertos (89,47%), com dois altos classificados como baixos. O baseline obteve 36,84%. São resultados sintéticos em cenários retidos, sem validação clínica. Veja [RESULTADOS.md](RESULTADOS.md).

## Executar

Na raiz do repositório, com o ambiente virtual ativado:

```powershell
python -m pip install -r requirements.txt
python src/parte2/executar_notebook.py
python src/parte2/classificador_risco.py
python -B src/parte2/test_classificador_risco.py
```

`executar_notebook.py` usa o Python atual em um kernel temporário, sem depender de configurações globais do Jupyter, executa todas as células e salva as saídas. O script de terminal compartilha o modelo e o protocolo do notebook. Ambos regeneram os arquivos derivados em `resultados/`, preservando os CSVs de entrada. Para visualizar e editar interativamente:

```powershell
python -m jupyterlab src/parte2/classificador_risco.ipynb
```

Selecione o kernel do ambiente virtual. O notebook funciona com o diretório de trabalho na raiz ou em `src/parte2/`. As principais versões usadas estão em [requirements-reproducao.txt](../../config/requirements-reproducao.txt); este registro não é um lock completo de todas as dependências transitivas.

## Arquivos e rastreabilidade

- [frases_risco.csv](frases_risco.csv): 60 registros com `frase,situacao`.
- [proveniencia_frases.csv](proveniencia_frases.csv): texto exato, origem, referências, justificativas, famílias e revisão.
- [FONTES_DATASET.md](FONTES_DATASET.md) e [RELATORIO_CURADORIA.md](RELATORIO_CURADORIA.md): fundamentos e conferências da base.
- [PROTOCOLO_AVALIACAO.md](PROTOCOLO_AVALIACAO.md): grupos e decisões fixadas antes do treino.
- [divisao_avaliacao.csv](divisao_avaliacao.csv) e [protocolo_avaliacao.json](protocolo_avaliacao.json): IDs por conjunto, parâmetros e hashes dos dados.
- [classificador_risco.py](classificador_risco.py): carregamento validado, pipeline e avaliação compartilhados.
- [test_classificador_risco.py](test_classificador_risco.py): cinco testes de integridade, separação por grupos e isolamento do vocabulário.
- [Lote 2](LOTE_02_REVISAO.md), [lote 3](LOTE_03_REVISAO.md), [lote 4](LOTE_04.md), [lote 5](LOTE_05.md) e [lote 6](LOTE_06.md): registros de elaboração; primeiro lote no documento de fontes.
- [Base inicial arquivada](historico/frases_risco_inicial_12.csv): preservada, fora do treinamento.

P01–P30 foram aprovadas pelo responsável; P31–P60 foram elaboradas e revisadas pelo assistente sob autorização para concluir sem aprovações individuais. Fontes institucionais não fornecem os textos sintéticos nem seus rótulos. IDs, fontes e grupos não são atributos do classificador. Os capítulos 11 e 07 fundamentam o método e a discussão de vieses.

Para a entrega geral, ainda faltam vídeo de até quatro minutos, link no README, publicação da versão final e confirmação da visibilidade pública do repositório.
