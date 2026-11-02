# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%">
  </a>
</p>

<br>

# CardioIA — Fase 3: Monitoramento Contínuo – IoT na Saúde

## Grupo AI4Success — Turma 2TIAOR

[![CI](https://github.com/dortad/cardioia-fase3-tarefa1/actions/workflows/ci.yml/badge.svg)](https://github.com/dortad/cardioia-fase3-tarefa1/actions/workflows/ci.yml)

## 👨‍🎓 Integrantes

- Durval de Oliveira Dorta Junior — RM 567007
- Guilherme da Nobrega Gontijo — RM 562211

## 👩‍🏫 Professores

### Tutor

- Leonardo Ruiz Orabona

### Coordenador

- [Andre Godoi Chiovato](https://www.linkedin.com/in/andregodoi/)

## 📜 Descrição

Nesta fase, simulamos um monitor cardíaco vestível. Um ESP32 no Wokwi lê sinais vitais simulados, guarda e trata as leituras no próprio dispositivo, envia os dados para a nuvem via MQTT e mostra tudo em um dashboard com alertas. O caminho completo é: captura → processamento → transmissão → visualização → alerta.

A Fase 3 continua o trabalho das fases anteriores. Na [Fase 1](document/other/fase1/README.md), reunimos bases numéricas, textuais e visuais de cardiologia, e na [Fase 2](document/other/fase2/README.md) fizemos a extração de sintomas e a classificação de risco de relatos sintéticos. Agora o projeto passa a trabalhar com sinais vitais coletados de forma contínua.

Os dados são simulados e o protótipo não foi validado para uso clínico.

As duas partes estão prontas: a [Parte 1 — Edge Computing](src/parte1_edge/README.md) e a [Parte 2 — Fog/Cloud Computing](src/parte2_cloud/README.md). Não fizemos os itens opcionais do "Ir Além".

## 🔗 Links rápidos

- [Parte 1 — armazenamento e processamento local](src/parte1_edge/README.md)
- [Projeto da Parte 1 no Wokwi](https://wokwi.com/projects/478992650362063873)
- [Relatório da Parte 1](document/relatorio_parte1.md)
- [Parte 2 — transmissão MQTT e dashboard](src/parte2_cloud/README.md)
- [Projeto da Parte 2 no Wokwi](https://wokwi.com/projects/479534021698400257), sem as credenciais do broker
- [Relatório da Parte 2](document/relatorio_parte2.md)
- [Documento do projeto no formato FIAP](document/ai_project_document_fiap.md)
- [Enunciado da atividade](document/Enunciado.md)
- [Repositório da Fase 2](https://github.com/dortad/cardioia-fase2-tarefa1)

## 📁 Estrutura de pastas

A organização segue o [template de repositório da FIAP](https://github.com/agodoi/templateFiapVfinal):

```text
.
├── .github/                  integração contínua e modelos de issue
├── assets/                   imagens usadas na documentação
├── config/                   registro de versões e configurações
├── document/                 documento do projeto, enunciado e relatórios
│   └── other/                acervos preservados das fases 1 e 2
├── scripts/                  validação automática da entrega
├── src/
│   ├── parte1_edge/          ESP32 no Wokwi: sensores e resiliência offline
│   └── parte2_cloud/         MQTT e dashboard no Node-RED
├── requirements.txt          dependências Python acumuladas das fases 1 a 3
└── README.md                 apresentação e instruções da entrega
```

## 🔧 Como executar o código

As instruções de execução estão nos READMEs da [Parte 1](src/parte1_edge/README.md) e da [Parte 2](src/parte2_cloud/README.md).

As Partes 1 e 2 não exigem dependências Python. Para usar os códigos Python das fases anteriores, crie o ambiente com Python 3.12 e instale a lista acumulada:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

A estrutura documental pode ser conferida com Python 3.12, sem instalar dependências:

```powershell
python scripts/validar_entrega.py
```

Essa verificação é executada automaticamente pelo [GitHub Actions](.github/workflows/ci.yml) a cada push e pull request.

## 🗃 Histórico de lançamentos

- **1.0.0 — 01/11/2026**
  - Parte 1 no Wokwi, com filtro de artefatos, buffer circular e sincronização.
  - Parte 2 com MQTT no HiveMQ Cloud e dashboard no Node-RED.
  - Relatórios das duas partes e prints do dashboard.
- **0.1.0 — 25/10/2026**
  - Estrutura inicial da Fase 3 a partir da entrega da Fase 2, preservada em `document/other/fase2/`.

## 📋 Licença e atribuição do template

Este repositório acadêmico segue o [Modelo Git FIAP](https://github.com/agodoi/templateFiapVfinal), disponibilizado pela FIAP sob [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). Fontes, datasets e demais materiais de terceiros permanecem sujeitos às condições de seus respectivos autores.
