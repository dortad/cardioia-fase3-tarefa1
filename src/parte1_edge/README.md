# Parte 1 — Armazenamento e processamento local (Edge Computing)

Nesta parte, o ESP32 no Wokwi lê os sinais vitais simulados, guarda as leituras em um buffer circular na memória e envia tudo quando a conexão volta. Os dados são simulados, e o protótipo não foi validado para uso clínico.

- **Projeto no Wokwi:** [CardioIA - Fase 3](https://wokwi.com/projects/478992650362063873)
- **Enunciado:** [Parte 1](../../document/Enunciado.md)

## Arquivos

- `sketch.ino`: código em C++ comentado.
- `diagram.json`: circuito do Wokwi.
- `libraries.txt`: biblioteca usada pelo Wokwi.

## Circuito

| Componente | Função | Ligação ao ESP32 |
|---|---|---|
| DHT22 | Temperatura e umidade | VCC → 3V3, SDA → D15, GND → GND |
| Botão | Simula os batimentos | 1.l → D4, 2.l → GND |
| Chave deslizante | Simula o Wi-Fi | 2 → D18, 1 → GND |

## Como executar

1. Abra o projeto no Wokwi e clique em **▶**.
2. Clique no botão para simular os batimentos.
3. Deslize a chave para alternar entre OFFLINE e ONLINE e acompanhe o Monitor Serial.

## Como funciona

A cada 5 segundos, o programa lê o DHT22 e grava uma leitura com a temperatura, a umidade e o BPM calculado a partir dos toques no botão. Toques com intervalo menor que 273 ms (mais de 220 BPM) são ignorados como artefato, e leituras inválidas do sensor (`NaN`) não são gravadas. O limite de 220 BPM vale só para esta simulação, não é um critério clínico.

O buffer guarda até 4.320 leituras, cerca de 6 horas e 67,5 KB. Quando enche, a leitura nova entra no lugar da mais antiga. Com a chave em ONLINE, o programa envia uma leitura por volta do `loop()`, da mais antiga para a mais nova, e libera a posição em seguida. O envio para a nuvem é simulado com `Serial.println`.

A explicação completa das escolhas está no [relatório da Parte 1](../../document/relatorio_parte1.md).

## Testes que fizemos no Wokwi

| Teste | Resultado |
|---|---|
| Toques rápidos | Ignorados como artefato; maior BPM aceito: 219 |
| Memória com o buffer em uso | 256 KB livres, de 323 KB |
| 5 leituras offline, depois online | Enviadas em ordem, de 5000 a 25000 ms |
| Capacidade temporária 3, 5 leituras offline | Enviadas as 3 mais recentes: 15000, 20000 e 25000 ms |
