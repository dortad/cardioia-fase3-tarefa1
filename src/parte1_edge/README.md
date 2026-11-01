# Parte 1 — Armazenamento e processamento local (Edge Computing)

Simulação no Wokwi de um ESP32 que lê sinais vitais simulados, guarda as leituras em um buffer circular na memória e as sincroniza quando a conexão volta. Os dados são simulados, e o protótipo não foi validado para uso clínico.

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

## Lógica

- **Leitura:** a cada 5 s, o sistema lê o DHT22 e usa o BPM calculado a partir dos toques no botão.
- **Filtro de artefato:** intervalos menores que 273 ms, equivalentes a mais de 220 BPM, são ignorados. Esse limite vale para esta simulação e não é um critério clínico.
- **Leituras inválidas:** leituras `NaN` do DHT22 não entram no buffer.
- **Armazenamento:** o buffer circular guarda até 4.320 leituras (6 horas, 67,5 KB). Quando ele enche, a leitura nova substitui a mais antiga.
- **Sincronização:** com a chave em ONLINE, sai uma leitura por volta do `loop()`, da mais antiga para a mais nova, e a posição é liberada em seguida. O envio é simulado com `Serial.println`.

## Testes realizados no Wokwi

| Teste | Resultado |
|---|---|
| Toques rápidos | Ignorados como artefato; maior BPM aceito: 219 |
| Memória com o buffer em uso | 256 KB livres, de 323 KB |
| 5 leituras offline, depois online | Enviadas em ordem, de 5000 a 25000 ms |
| Capacidade temporária 3, 5 leituras offline | Enviadas as 3 mais recentes: 15000, 20000 e 25000 ms |
