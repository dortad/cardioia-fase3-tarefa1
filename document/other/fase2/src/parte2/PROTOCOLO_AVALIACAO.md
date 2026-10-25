# Protocolo de avaliação — definido antes do treino

As 24 famílias iniciais foram reunidas em seis grupos por semelhança de cenário, sem alterar as frases ou rótulos. O mapeamento completo está em `protocolo_avaliacao.json` e a destinação de cada ID em `divisao_avaliacao.csv`.

| Grupo | Conteúdo | Destino |
|---|---|---|
| G01 | Queixas respiratórias com sintomas torácicos/palpitações e combinações com suor frio | Teste |
| G02 | Bem-estar afirmado e sintomas negados | Teste |
| G03 | Queixas torácicas com irradiação ou tontura/sensação de desmaio | Treino |
| G04 | Esforço muscular com melhora, reunindo diferentes regiões | Treino |
| G05 | Lesões/torções de membros, tanto melhora quanto sinais de alerta | Treino |
| G06 | Dor nas costas com sinais de alerta | Treino |

A divisão foi fixada por conteúdo e contagens antes do ajuste: 41 exemplos de treino (18 altos, 23 baixos) e 19 de teste (12 altos, 7 baixos). Não houve tentativa de sementes para melhorar resultados. A escolha de dois grupos inteiros aproxima um terço dos dados e mantém as duas classes em ambos os conjuntos. G01 e G02 ficam juntos no teste para manter os contrastes lexicais P05/P10 e as demais paráfrases de bem-estar fora do treino.

Este é um teste de transferência para cenários retidos, não uma amostra aleatória representativa. Nenhum exemplo de bem-estar é visto no treino; isso torna a classe baixa do teste particularmente diferente da classe baixa do treino. Dois grupos no teste não permitem estimar desempenho populacional, e as 19 frases não são 19 observações clínicas independentes. A linguagem e sintomas comuns entre G01/G03 podem ainda facilitar predições: agrupar reduz vazamento óbvio, sem garantir independência semântica completa.

Os hashes SHA256 detectam mudanças nos CSVs depois de congelar a divisão. Não usar IDs, fontes, justificativas, famílias ou grupos como atributos; apenas `frase`. Ajustar vocabulário, IDF e regressão logística exclusivamente com o treino. Preservar as negações; não há stopwords removidas.

TF-IDF usa unigramas/bigramas e remoção de acentos. A regressão logística usa C=1, solver lbfgs, max_iter=1000 e random_state=42. Não há seleção de hiperparâmetros, calibração ou ajuste de limiar. O baseline prevê a classe mais frequente do treino. Avaliar acurácia, precisão, recall, F1, matriz de confusão, erros individuais e exemplos de negação. Provas adicionais de comportamento reutilizam exemplos da base e são identificadas como demonstração, não somadas à métrica de teste.

O enunciado exige acurácia e discussão de comportamento/distorções, sem meta numérica. A divisão manual por grupos é uma decisão metodológica do projeto para controlar a semelhança dos dados sintéticos. Se houver revisão futura do modelo com base nestes erros, este conjunto passa a ser desenvolvimento e será necessário um novo teste independente.

Referências metodológicas: capítulo 11 (TF-IDF e classificação) e capítulo 07 (vieses), conforme [mapeamento das apostilas](../../document/MAPEAMENTO_APOSTILAS_FASE2.md). Documentação técnica: [Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) e [prevenção de vazamento](https://scikit-learn.org/stable/common_pitfalls.html). O agrupamento é específico deste projeto; não atribuí-lo como exigência das apostilas.
