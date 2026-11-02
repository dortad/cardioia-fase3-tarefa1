# Parte 2 — Transmissão para nuvem e visualização (Fog/Cloud Computing)

O ESP32 simulado no Wokwi publica as leituras no HiveMQ Cloud via MQTT com TLS, e o Node-RED as exibe em um dashboard com gráfico, medidor e alerta. Os dados são simulados, e o protótipo não foi validado para uso clínico.

- **Relatório:** [relatorio_parte2.md](../../document/relatorio_parte2.md)
- **Prints do dashboard:** [document/prints_parte2/](../../document/prints_parte2/)
- **Enunciado:** [Parte 2](../../document/Enunciado.md)

## Arquivos

- `sketch.ino`: código em C++ comentado, com os dados do broker a preencher.
- `diagram.json`: circuito do Wokwi, igual ao da Parte 1.
- `libraries.txt`: bibliotecas usadas pelo Wokwi.
- `flow_nodered.json`: fluxo exportado do Node-RED, sem endereço nem credenciais.

## Como executar

1. Crie um cluster e um usuário no HiveMQ Cloud.
2. No Wokwi, crie um projeto com os três arquivos e preencha `MQTT_SERVIDOR`, `MQTT_USUARIO` e `MQTT_SENHA` no `sketch.ino`. Não publique esses dados.
3. Instale o Node-RED e o dashboard:

   ```powershell
   npm install -g --unsafe-perm node-red
   cd $HOME\.node-red
   npm install node-red-dashboard
   ```

4. Rode `node-red`, abra `http://localhost:1880` e importe o `flow_nodered.json`.
5. No nó **Assinar leituras**, edite o broker com o endereço, o usuário e a senha, e clique em **Deploy**.
6. Rode a simulação com a chave em ONLINE e abra `http://localhost:1880/ui`.

## Alertas

O indicador fica vermelho acima de 120 BPM ou de 38 °C. Esses limites vêm dos exemplos do enunciado, valem para esta simulação e não são critérios clínicos.
