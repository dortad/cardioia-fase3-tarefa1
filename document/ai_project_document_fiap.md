<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="30%">
  </a>
</p>

# AI Project Document — CardioIA — Fase 3

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

O CardioIA evolui a cada fase. A Fase 1 reuniu bases numéricas, textuais e visuais; a Fase 2 aplicou processamento de linguagem natural e classificação de risco a relatos sintéticos. A Fase 3 acrescenta o monitoramento contínuo de sinais vitais com IoT, integrando Edge, Fog e Cloud Computing.

### 1.1.2 Descrição da solução desenvolvida

A solução simula um dispositivo vestível de monitoramento cardíaco em um ESP32 no Wokwi. O DHT22 mede temperatura e umidade, e um botão simula os batimentos. O dispositivo filtra artefatos, guarda as leituras em um buffer circular e continua coletando sem conexão. Quando a conexão volta, as leituras são publicadas em ordem no HiveMQ Cloud via MQTT com TLS. O Node-RED as recebe e exibe em um dashboard com gráfico, medidor e alerta automático.

# <a name="c2"></a>2. Visão geral do projeto

## 2.1 Objetivos do projeto

- Capturar sinais vitais simulados com ESP32 no Wokwi.
- Armazenar as leituras localmente e garantir resiliência offline (Edge Computing).
- Transmitir os dados para a nuvem via MQTT.
- Visualizar as informações em dashboard com alertas automáticos.
- Refletir sobre eficiência, segurança e boas práticas em IoT médico.

## 2.2 Público-alvo

A entrega destina-se à avaliação acadêmica da FIAP. Os dados são simulados, e o protótipo não foi validado para uso clínico.

## 2.3 Metodologia

O desenvolvimento seguiu etapas incrementais, partindo da leitura de um sensor até o fluxo completo. Cada etapa foi executada e testada no Wokwi antes da seguinte. Decisões de engenharia, como o tamanho do buffer, foram baseadas em cálculos e em medições de memória, e o enunciado e as apostilas orientaram as escolhas.

# <a name="c3"></a>3. Desenvolvimento do projeto

## 3.1 Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| ESP32 no Wokwi, em C++ | Simulação do dispositivo |
| DHT22, botão e chave deslizante | Temperatura e umidade, batimentos e queda de conexão simulada |
| MQTT 3.1.1 com TLS, `PubSubClient` | Publicação das leituras |
| HiveMQ Cloud | Broker MQTT na nuvem |
| Node-RED e `node-red-dashboard` | Processamento e dashboard |

## 3.2 Arquitetura e fluxo de dados

```text
ESP32 no Wokwi  →  HiveMQ Cloud  →  Node-RED  →  Dashboard
Borda (Edge)       Nuvem (broker)   Névoa (Fog)   Visualização
```

Na borda, o ESP32 captura os sinais, descarta toques acima de 220 BPM e leituras inválidas e guarda até 4.320 leituras, cerca de 6 horas e 67,5 KB. As leituras saem do buffer da mais antiga para a mais nova. O Node-RED assina o tópico `cardioia/ai4success/leituras`, avalia os limites e atualiza o dashboard. Os detalhes estão nos relatórios das [Parte 1](relatorio_parte1.md) e [Parte 2](relatorio_parte2.md).

## 3.3 Testes e simulação

Os testes foram feitos no Wokwi e cobriram o filtro de artefatos, a coleta offline, a sincronização em ordem, o buffer cheio em escala reduzida, a publicação MQTT, o dashboard e os alertas de temperatura e de BPM. As tabelas com os resultados e as limitações estão nos dois relatórios. A falha do DHT22, a queda real da conexão e a capacidade de 4.320 leituras em escala completa não foram exercitadas.

# <a name="c4"></a>4. Resultados e avaliações

## 4.1 Análise dos resultados

O fluxo completo funcionou: as leituras saíram do ESP32 simulado e chegaram ao dashboard, e os alertas dispararam acima de 120 BPM e de 38 °C. Esses limites vêm dos exemplos do enunciado e não são critérios clínicos. Depois de uma queda simulada, as leituras guardadas foram publicadas em ordem. A RAM livre medida ficou em 323 KB sem o buffer, 256 KB com o buffer e 113 KB com o TLS conectado. O maior bloco contínuo de 107 KB levou a reduzir a autonomia planejada de 12 para 6 horas, mantendo uma leitura a cada 5 s.

## 4.2 Feedback dos usuários

Não houve teste com usuários. O protótipo usa dados simulados e foi avaliado apenas pelos testes técnicos descritos neste documento.

# <a name="c5"></a>5. Conclusões e trabalhos futuros

O protótipo demonstra o ciclo de captura, processamento, transmissão, visualização e alerta, com a borda garantindo a continuidade da coleta quando a conexão falha. Entre os trabalhos futuros estão guardar as leituras em memória persistente, usar a hora real em cada leitura, verificar o certificado do broker, adotar QoS 1, preservar por prioridade as leituras fora da faixa normal e armazenar o histórico com InfluxDB e Grafana. O uso com dados reais exigiria validação clínica e adequação à LGPD.

# <a name="c6"></a>6. Referências

- FIAP. [Enunciado da atividade da Fase 3](Enunciado.md).
- FIAP. Fase 3, Cap08 — Cloud Computing como Pilar da IoT Moderna.
- FIAP. Fase 3, Cap09 — Inteligência na Borda: Fog e Edge Computing Transformando a IoT.
- HiveMQ. [Getting Started with HiveMQ Cloud](https://docs.hivemq.com/hivemq-cloud/quick-start-guide.html).

# <a name="c7"></a>7. Anexos

- [Relatório da Parte 1](relatorio_parte1.md)
- [Relatório da Parte 2](relatorio_parte2.md)
- [Prints do dashboard](prints_parte2/)
- [Acervo da Fase 2](other/fase2/README.md)
- [Acervo da Fase 1](other/fase1/README.md)
