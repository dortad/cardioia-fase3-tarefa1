# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%">
  </a>
</p>

<br>

> **Acervo preservado.** Este é o README da entrega da Fase 2, mantido sem alterações de conteúdo para rastreabilidade. A versão publicada e avaliada está no [repositório da Fase 2](https://github.com/dortad/cardioia-fase2-tarefa1). Os caminhos citados abaixo são relativos a esta pasta, e alguns documentos internos mencionados não foram publicados. O projeto atual é a [Fase 3](../../../README.md).

# CardioIA — Fase 2: Diagnóstico Automatizado

## Grupo AI4Success — Turma 2TIAOR

[![CI](https://github.com/dortad/cardioia-fase2-tarefa1/actions/workflows/ci.yml/badge.svg)](https://github.com/dortad/cardioia-fase2-tarefa1/actions/workflows/ci.yml)

## 👨‍🎓 Integrantes

- Durval de Oliveira Dorta Junior — RM 567007
- Guilherme da Nobrega Gontijo — RM 562211

## 👩‍🏫 Professores

### Tutor

- Leonardo Ruiz Orabona

### Coordenador

- [Andre Godoi Chiovato](https://www.linkedin.com/in/andregodoi/)

## 📜 Descrição

O CardioIA desta fase simula duas etapas de apoio ao diagnóstico automatizado usando textos clínicos sintéticos. Na [Parte 1](src/parte1/README.md), dez relatos de pacientes são normalizados e comparados com um mapa de conhecimento que relaciona expressões de sintomas a possíveis condições. O programa mostra as evidências encontradas, conta conceitos distintos e preserva associações empatadas, sem apresentar a saída como diagnóstico clínico.

Na [Parte 2](src/parte2/README.md), uma base didática de 60 frases, equilibrada entre alto e baixo risco, é transformada em vetores TF-IDF. Uma regressão logística é treinada e avaliada com grupos de cenários separados entre treino e teste. O notebook executado apresenta métricas, matriz de confusão, análise dos erros e limitações do conjunto sintético.

A Parte 1 segue uma abordagem **simbólica**: as associações ficam explícitas no mapa e cada sugestão apresenta suas evidências. A Parte 2 segue uma abordagem **estatística**: as associações são aprendidas das frases pelo modelo. A comparação evidencia a auditabilidade das regras e os limites de generalização de uma base textual pequena.

A solução aplica os conteúdos dos capítulos 02, 07, 10 e 11 das apostilas: leitura de arquivos, processamento simbólico de linguagem, TF-IDF, classificação supervisionada e análise responsável de vieses. Os dados não vieram de pacientes e o sistema não foi validado para triagem ou uso clínico.

**Estado atual:** todos os entregáveis obrigatórios da atividade principal estão concluídos: as duas partes técnicas, a documentação, o repositório público e o vídeo de demonstração. Os itens “Ir Além” não fazem parte do escopo desta entrega.

## 🔗 Links rápidos

- [Parte 1 — extração de sintomas](src/parte1/README.md)
- [Parte 2 — classificador de risco](src/parte2/README.md)
- [Notebook executado](src/parte2/classificador_risco.ipynb)
- [Resultados e limitações](src/parte2/RESULTADOS.md)
- [Documento do projeto no formato FIAP](document/ai_project_document_fiap.md)
- [Atendimento ao enunciado](document/STATUS_TAREFA.md)
- [Enunciado da atividade](document/Enunciado.md)
- [Repositório no GitHub](https://github.com/dortad/cardioia-fase2-tarefa1)

## 📁 Estrutura de pastas

A organização segue o [template de repositório da FIAP](https://github.com/agodoi/templateFiapVfinal):

```text
.
├── .github/                  arquivos de apoio à gestão do repositório
├── assets/                   imagens usadas na documentação
├── config/                   registro das versões e notas de configuração
├── document/                 documento do projeto, enunciado, status e complementos
│   └── other/fase1/          acervo preservado da fase anterior
├── scripts/                  orientação para scripts auxiliares
├── src/
│   ├── parte1/               relatos, mapa, extrator, fontes e testes
│   └── parte2/               dataset, notebook, modelo, resultados e testes
├── requirements.txt          dependências para executar a atividade
└── README.md                 apresentação e instruções da entrega
```

Os materiais locais de estudo em `Apostilas/`, o ambiente `.venv/` e o registro interno `HISTORICO.md` não fazem parte da entrega publicada. O código atual não depende do acervo preservado em `document/other/fase1/`.

## 🔧 Como executar o código

### Pré-requisitos

- Python 3.12
- Git, para clonar o repositório
- PowerShell nos exemplos abaixo; os comandos Python também funcionam em outros terminais

Clone o repositório, entre na pasta e prepare o ambiente:

```powershell
git clone https://github.com/dortad/cardioia-fase2-tarefa1.git
cd cardioia-fase2-tarefa1
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Execute a Parte 1:

```powershell
python src/parte1/diagnostico_sintomas.py
python -B src/parte1/test_diagnostico_sintomas.py
```

Execute a Parte 2 e suas verificações:

```powershell
python src/parte2/executar_notebook.py
python src/parte2/classificador_risco.py
python -B src/parte2/test_classificador_risco.py
```

Confira a estrutura documental e o notebook executado:

```powershell
python scripts/validar_entrega.py
```

Essas verificações e os testes são executados automaticamente pelo [GitHub Actions](.github/workflows/ci.yml) a cada push e pull request.

Para abrir o notebook interativamente:

```powershell
python -m jupyterlab src/parte2/classificador_risco.ipynb
```

As principais versões usadas na execução registrada estão em [config/requirements-reproducao.txt](config/requirements-reproducao.txt). Esse arquivo não é um lock completo das dependências transitivas.

## 📊 Resultados

Na Parte 1, os 13 testes automatizados passaram e os dez relatos produziram sugestões explicadas. Os empates dos relatos 1, 3 e 9 são intencionais e estão documentados.

Na Parte 2, o modelo foi treinado com 41 frases e avaliado em 19 frases pertencentes a grupos de cenários retidos:

| Medida | Resultado |
|---|---:|
| Acurácia do modelo | 89,47% — 17/19 |
| Baseline da classe mais frequente | 36,84% — 7/19 |
| Recall de alto risco | 83,33% — 10/12 |
| Recall de baixo risco | 100,00% — 7/7 |

Os dois erros foram frases de alto risco classificadas como baixo risco. A divisão, os erros e os limites de interpretação estão registrados no [protocolo](src/parte2/PROTOCOLO_AVALIACAO.md) e no [relatório de resultados](src/parte2/RESULTADOS.md). A acurácia descreve somente esta base sintética e não representa desempenho clínico.

## 🗂️ Dados, fontes e limitações

Os relatos e rótulos são didáticos. A [proveniência das 60 frases](src/parte2/proveniencia_frases.csv) diferencia exemplos do enunciado, adaptações e elaborações sintéticas. As fontes institucionais fundamentam os cenários, mas não são autoras das frases ou dos rótulos.

As associações da Parte 1 estão justificadas em [FONTES_MAPA.md](src/parte1/FONTES_MAPA.md), e os critérios da Parte 2 em [FONTES_DATASET.md](src/parte2/FONTES_DATASET.md). O projeto não mede justiça por características demográficas, não usa dados reais de pacientes e não deve ser empregado para decisões médicas.

## 🎥 Vídeo de demonstração

[Assistir ao vídeo de demonstração no YouTube](https://youtu.be/VMgk0PW0n3A) — duração: 3min54s; publicado como não listado.

## 🗃 Histórico de lançamentos

- **0.2.0 — 22/09/2026**
  - Parte 1 concluída e validada.
  - Dataset da Parte 2 consolidado com 60 frases e proveniência.
  - Notebook executado, métricas e análise de vieses documentadas.
- **0.1.0 — 20/09/2026**
  - Estrutura inicial da Fase 2 e protótipo do classificador.

## 📋 Licença e atribuição do template

Este repositório acadêmico segue o [Modelo Git FIAP](https://github.com/agodoi/templateFiapVfinal), disponibilizado pela FIAP sob [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). Fontes, datasets e demais materiais de terceiros permanecem sujeitos às condições de seus respectivos autores.
