# Parte 1 — Armazenamento e processamento local (Edge Computing)

> **Em desenvolvimento.** Esta pasta reservará o projeto do ESP32 no Wokwi.

## Escopo previsto

Conforme a Parte 1 do [enunciado](../../document/Enunciado.md):

- ESP32 com no mínimo dois sensores distintos, sendo obrigatório o DHT22 (temperatura e umidade);
- leitura periódica e armazenamento local das amostras;
- conectividade Wi-Fi simulada por variável booleana: quando “conectado”, os dados armazenados são enviados via `Serial.println` e o armazenamento local é limpo;
- resiliência offline: a coleta continua sem conexão, com limite de armazenamento justificado pelo cenário do projeto, e os dados pendentes são sincronizados na reconexão.

## Entregáveis previstos

- link do projeto no Wokwi;
- código C++ comentado;
- relatório de no mínimo uma página sobre o fluxo de funcionamento e a lógica de resiliência.
