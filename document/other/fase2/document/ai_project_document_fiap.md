<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="30%">
  </a>
</p>

# AI Project Document — CardioIA — Fase 2

## Grupo AI4Success — Turma 2TIAOR

### Integrantes

- Durval de Oliveira Dorta Junior — RM 567007
- Guilherme da Nobrega Gontijo — RM 562211

## Sumário

1. [Introdução](#c1)
2. [Visão geral do projeto](#c2)
3. [Desenvolvimento do projeto](#c3)
4. [Resultados e avaliações](#c4)
5. [Conclusões e trabalhos futuros](#c5)
6. [Referências](#c6)
7. [Anexos](#c7)

# <a name="c1"></a>1. Introdução

## 1.1 Escopo do projeto

### 1.1.1 Contexto da Inteligência Artificial

O projeto explora técnicas introdutórias de inteligência artificial aplicadas a textos sintéticos de saúde. A atividade combina representação simbólica de conhecimento, processamento de linguagem natural e classificação supervisionada. Seu uso é exclusivamente acadêmico: os dados não pertencem a pacientes, e os resultados não foram validados para diagnóstico, triagem ou decisão clínica.

### 1.1.2 Descrição da solução desenvolvida

O CardioIA possui duas partes. Na primeira, um programa lê dez relatos, normaliza o texto, identifica expressões de sintomas e as relaciona a possíveis condições por meio de um mapa CSV fundamentado. Na segunda, 60 frases rotuladas como “alto risco” ou “baixo risco” são representadas com TF-IDF e classificadas por regressão logística. O notebook registra treinamento, teste, métricas, matriz de confusão, análise de erros e limitações.

# <a name="c2"></a>2. Visão geral do projeto

## 2.1 Objetivos do projeto

- Demonstrar leitura e processamento de arquivos TXT e CSV em Python.
- Extrair sintomas por regras explícitas e sugerir associações de forma explicável.
- Construir uma base textual pequena com origem e critérios documentados.
- Treinar e avaliar um classificador de texto com TF-IDF.
- Discutir erros, vieses e limites sem apresentar o exercício como sistema médico.

## 2.2 Público-alvo

A entrega destina-se à avaliação acadêmica da FIAP e a estudantes que queiram acompanhar uma implementação introdutória e auditável. Ela não se destina a pacientes nem a profissionais em contexto assistencial.

## 2.3 Metodologia

O trabalho partiu da leitura do enunciado e das apostilas da fase. Os relatos, o mapa de sintomas e as frases classificadas passaram por revisão incremental. As associações de saúde foram fundamentadas em fontes institucionais, distinguindo referência clínica, autoria das frases e decisão didática de rótulo. Na Parte 2, famílias de cenários semelhantes foram mantidas no mesmo conjunto para reduzir vazamento entre treino e teste. Dados, parâmetros e divisão foram fixados antes da avaliação final.

# <a name="c3"></a>3. Desenvolvimento do projeto

## 3.1 Tecnologias utilizadas

- Python 3.12;
- pandas e NumPy para dados tabulares;
- scikit-learn para TF-IDF, regressão logística e métricas;
- Jupyter Notebook para execução e apresentação do experimento;
- Matplotlib e Seaborn para a matriz de confusão;
- arquivos TXT, CSV, JSON e Markdown para dados, rastreabilidade e documentação.

As versões principais da execução registrada estão em [`config/requirements-reproducao.txt`](../config/requirements-reproducao.txt).

## 3.2 Modelagem e algoritmos

Na Parte 1, o algoritmo normaliza caixa, acentos e espaços, procura expressões completas, trata sobreposições e aplica uma regra limitada de negação local. Cada conceito distinto soma um ponto às condições relacionadas no mapa; empates são preservados e as evidências são mostradas.

Na Parte 2, um `TfidfVectorizer` transforma as frases em vetores e uma regressão logística faz a classificação binária. O modelo foi escolhido por ser adequado ao objetivo didático, interpretável por pesos de termos e compatível com uma base pequena. Os identificadores, fontes, famílias e justificativas de rótulo não entram como atributos.

## 3.3 Treinamento e teste

A base consolidada contém 60 frases sintéticas, com 30 exemplos por classe. Foram usadas 41 frases para treinamento e 19 para teste. A separação ocorreu por grupos de cenários, sem sobreposição de famílias. O conjunto de teste contém 12 casos de alto risco e sete de baixo risco. Cinco testes automatizados verificam a integridade da base, a divisão e o isolamento do vocabulário; outros 13 validam a Parte 1.

# <a name="c4"></a>4. Resultados e avaliações

## 4.1 Análise dos resultados

O classificador acertou 17 das 19 frases de teste, obtendo 89,47% de acurácia, contra 36,84% do baseline da classe mais frequente no treino. O recall de alto risco foi 83,33%, e o de baixo risco foi 100%. Os dois erros foram falsos negativos: P23, com negação parcial, e P32, com formas linguísticas pouco representadas no treino.

O resultado supera o baseline nesta divisão, mas não mede desempenho clínico. O teste possui somente dois grupos, a base é pequena e sintética, e há dependência linguística residual. Também não houve avaliação de justiça por características demográficas, validação externa ou calibração.

## 4.2 Feedback dos usuários

Durante a construção, o responsável pelo projeto aprovou os relatos da Parte 1, o comportamento de preservação de empates, os critérios do mapa e os lotes P01–P30 da Parte 2. Os lotes P31–P60 foram concluídos após autorização expressa para seguir sem aprovações individuais. Não houve teste com pacientes, profissionais de saúde ou usuários finais externos; portanto, não se afirma validação de usabilidade ou adequação clínica.

# <a name="c5"></a>5. Conclusões e trabalhos futuros

A atividade principal atingiu os objetivos técnicos: os dois programas foram implementados, os dados possuem rastreabilidade, o notebook foi executado e os resultados foram analisados. A explicação das evidências da Parte 1 e o registro dos falsos negativos da Parte 2 tornam claros os limites do comportamento observado.

Antes da entrega, ainda é necessário gravar o vídeo de até quatro minutos, publicá-lo como não listado, inserir o link no README e tornar público o repositório. Mudanças futuras no modelo exigiriam um novo conjunto independente de teste. Os itens “Ir Além” permanecem fora do escopo atual.

# <a name="c6"></a>6. Referências

- FIAP. [Enunciado da atividade](Enunciado.md).
- Ministério da Saúde. [Infarto](https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/i/infarto).
- NHLBI/NIH. [Heart Attack — Symptoms](https://www.nhlbi.nih.gov/health/heart-attack/symptoms).
- NHLBI/NIH. [Angina (Chest Pain) — Symptoms](https://www.nhlbi.nih.gov/health/angina/symptoms).
- NHLBI/NIH. [Heart Failure — Symptoms](https://www.nhlbi.nih.gov/health/heart-failure/symptoms).
- NHLBI/NIH. [Arrhythmias — Symptoms](https://www.nhlbi.nih.gov/health/arrhythmias/symptoms).
- NHS. [Back pain](https://www.nhs.uk/conditions/back-pain/).
- NHS. [Sprains and strains](https://www.nhs.uk/conditions/sprains-and-strains/).
- Projeto CardioIA. [Fundamentação do mapa](../src/parte1/FONTES_MAPA.md) e [origem do dataset](../src/parte2/FONTES_DATASET.md).

# <a name="c7"></a>7. Anexos

- [Atendimento ao enunciado](STATUS_TAREFA.md)
- [Mapeamento das apostilas](MAPEAMENTO_APOSTILAS_FASE2.md)
- [Notebook executado](../src/parte2/classificador_risco.ipynb)
- [Resultados completos](../src/parte2/RESULTADOS.md)
- [Protocolo de avaliação](../src/parte2/PROTOCOLO_AVALIACAO.md)
