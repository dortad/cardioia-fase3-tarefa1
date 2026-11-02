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

O CardioIA vem crescendo a cada fase. Na Fase 1, reunimos bases numéricas, textuais e visuais de cardiologia. Na Fase 2, usamos processamento de linguagem natural e classificação de risco em relatos sintéticos. Agora, na Fase 3, o foco é o monitoramento contínuo de sinais vitais com IoT, passando pelas camadas de Edge, Fog e Cloud.

### 1.1.2 Descrição da solução desenvolvida

Simulamos no Wokwi um monitor cardíaco vestível feito com um ESP32. O DHT22 mede temperatura e umidade, e um botão faz o papel dos batimentos. O ESP32 filtra os toques que não parecem reais, guarda as leituras em um buffer circular e continua coletando mesmo sem internet. Quando a conexão volta, ele publica as leituras em ordem no HiveMQ Cloud, via MQTT com TLS, e o Node-RED mostra tudo em um dashboard com gráfico, medidor e alerta.

# <a name="c2"></a>2. Visão geral do projeto

## 2.1 Objetivos do projeto

- Capturar sinais vitais simulados com ESP32 no Wokwi.
- Armazenar as leituras localmente e garantir resiliência offline (Edge Computing).
- Transmitir os dados para a nuvem via MQTT.
- Visualizar as informações em dashboard com alertas automáticos.
- Refletir sobre eficiência, segurança e boas práticas em IoT médico.

## 2.2 Público-alvo

Este trabalho foi feito para a avaliação da FIAP. Os dados são simulados, e o protótipo não foi validado para uso clínico.

## 2.3 Metodologia

Fomos construindo o projeto aos poucos: começamos com um "Hello" no Monitor Serial, depois a leitura do DHT22, o botão, o buffer, o Wi-Fi simulado e, por fim, o MQTT e o dashboard. Cada etapa foi testada no Wokwi antes de passarmos para a próxima. Nas decisões mais importantes, como o tamanho do buffer, fizemos as contas e medimos a memória antes de escolher, sempre olhando o enunciado e as apostilas.

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

Na borda, o ESP32 descarta os toques acima de 220 BPM e as leituras inválidas do sensor e guarda até 4.320 leituras, o que dá cerca de 6 horas e 67,5 KB. As leituras saem do buffer da mais antiga para a mais nova. Do outro lado, o Node-RED assina o tópico `cardioia/ai4success/leituras`, confere os limites e atualiza o dashboard. Explicamos tudo com mais detalhe nos relatórios da [Parte 1](relatorio_parte1.md) e da [Parte 2](relatorio_parte2.md).

## 3.3 Testes e simulação

Testamos no Wokwi o filtro de artefatos, a coleta sem conexão, o envio em ordem, o buffer cheio (com a capacidade reduzida para 3), a publicação MQTT, o dashboard e os alertas de temperatura e de BPM. A função que decide o alerta também foi testada separadamente, com 7 casos. Os resultados estão em tabelas nos dois relatórios. Ficaram de fora a falha do DHT22, uma queda real de conexão e o buffer cheio com as 4.320 leituras.

# <a name="c4"></a>4. Resultados e avaliações

## 4.1 Análise dos resultados

O fluxo completo funcionou: as leituras saíram do ESP32 e chegaram ao dashboard, e o alerta acendeu acima de 120 BPM e de 38 °C, limites que tiramos dos exemplos do enunciado e que não são critérios clínicos. Depois de uma queda simulada, as leituras guardadas foram publicadas na ordem certa. Medindo a memória, encontramos 323 KB livres sem o buffer, 256 KB com o buffer e 113 KB com o TLS conectado. Como o maior bloco contínuo tinha só 107 KB, reduzimos a autonomia planejada de 12 para 6 horas, mantendo uma leitura a cada 5 s.

## 4.2 Feedback dos usuários

Não fizemos testes com usuários. Como os dados são simulados, avaliamos o protótipo só pelos testes técnicos descritos aqui.

# <a name="c5"></a>5. Conclusões e trabalhos futuros

Conseguimos montar o ciclo inteiro: captura, processamento, transmissão, visualização e alerta. O que mais aprendemos foi a importância da borda, que mantém a coleta funcionando quando a conexão cai, e como a memória limitada do ESP32 obriga a fazer escolhas.

Se fôssemos continuar, guardaríamos as leituras em memória permanente, usaríamos a hora real em cada leitura, verificaríamos o certificado do broker, passaríamos para QoS 1, protegeríamos as leituras fora da faixa normal e guardaríamos o histórico com InfluxDB e Grafana. Para usar com dados reais, ainda seria preciso validação clínica e adequação à LGPD.

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
