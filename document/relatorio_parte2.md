# Relatório da Parte 2 — Transmissão para nuvem e visualização (Fog/Cloud Computing)

CardioIA — Fase 3: Monitoramento Contínuo – IoT na Saúde
Grupo AI4Success — Turma 2TIAOR
Durval de Oliveira Dorta Junior (RM 567007) e Guilherme da Nobrega Gontijo (RM 562211)

Projeto no Wokwi: [CardioIA - Fase 3 - Parte 2](https://wokwi.com/projects/479534021698400257)
Código: [src/parte2_cloud/](../src/parte2_cloud/)

Tiramos o usuário e a senha do broker do projeto publicado no Wokwi. Sem eles, a coleta e o buffer funcionam, mas o MQTT não conecta. Os resultados e os prints deste relatório são de uma execução com as credenciais preenchidas.

Todos os dados deste trabalho são simulados. O protótipo não foi validado para uso clínico.

## 1. O que fizemos

Nesta parte, levamos as leituras do ESP32 até um dashboard. O ESP32 publica os dados em um broker MQTT na nuvem, e o Node-RED recebe essas mensagens e mostra tudo em tempo real, com um alerta quando algum valor passa do limite.

Mantivemos o que fizemos na Parte 1. As leituras continuam passando pelo buffer circular e só saem dele depois de publicadas. Se a conexão cair, elas ficam guardadas por até 6 horas.

## 2. Arquitetura

```text
ESP32 no Wokwi  →  HiveMQ Cloud  →  Node-RED  →  Dashboard
Borda (Edge)       Nuvem (broker)   Névoa (Fog)   Visualização
```

O ESP32 fica na borda: captura os sinais, filtra os artefatos e guarda as leituras quando está sem conexão. O HiveMQ Cloud é o broker na nuvem, que recebe as mensagens e repassa para quem assinou o tópico. O Node-RED roda no nosso computador e funciona como a camada de névoa, porque interpreta as mensagens e decide quando mostrar um alerta.

Uma coisa que achamos interessante no MQTT é que o ESP32 e o Node-RED não se conhecem. Os dois só conversam com o broker: um publica e o outro assina. Com isso, daria para adicionar outros assinantes, como um banco de dados, sem mexer no ESP32.

## 3. Comunicação MQTT

### 3.1 Escolha do broker

O enunciado dá o HiveMQ Cloud como exemplo, e é ele que o Cap08 usa, em uma versão gratuita com TLS. Quando fomos criar o nosso, a primeira tela que encontramos era a do HiveMQ instalado no próprio computador (com Docker), que não serviria, porque o Wokwi não alcança um broker na nossa máquina. Procurando na documentação da HiveMQ, vimos que o plano gratuito Serverless não aceita mais clusters novos. Usamos então o plano Starter, um teste grátis de 15 dias, com o servidor em Frankfurt.

### 3.2 Configuração da conexão

| Item | O que usamos |
|---|---|
| Porta | 8883, que é o MQTT com TLS |
| Protocolo | MQTT 3.1.1 |
| Autenticação | Usuário e senha criados no HiveMQ |
| Tópico | `cardioia/ai4success/leituras` |
| QoS | 0 |
| Formato | JSON |

No código, usamos as mesmas bibliotecas do exemplo do Cap08: `WiFi`, `WiFiClientSecure` e `PubSubClient`. No Wokwi, o ESP32 se conecta à rede virtual `Wokwi-GUEST`. O usuário e a senha não estão no repositório nem no projeto publicado; no `sketch.ino`, esses campos estão para preencher.

### 3.3 Publicação

Cada leitura vira uma mensagem JSON, com os mesmos campos guardados no buffer:

```json
{"momento":131742,"temperatura":36.5,"umidade":40.0,"bpm":152}
```

As leituras saem uma de cada vez, da mais antiga para a mais nova, com no máximo 10 mensagens por segundo. A posição no buffer só é liberada se a publicação der certo; se falhar, a leitura fica guardada para a próxima tentativa. Quando a conexão com o broker cai, o programa tenta de novo a cada 5 segundos, em vez de ficar tentando sem parar. A chave deslizante continua simulando a queda: em OFFLINE, a coleta segue normalmente, mas nada é publicado.

## 4. Dashboard no Node-RED

O fluxo exportado está em [flow_nodered.json](../src/parte2_cloud/flow_nodered.json), sem o endereço do broker e sem senha. Para usar, é preciso importar o arquivo e preencher esses dados no próprio Node-RED. Usamos o Node-RED 5.0.9 com o pacote `node-red-dashboard` 3.6.6.

![Fluxo no editor do Node-RED, com o nó MQTT conectado](prints_parte2/04_fluxo_node_red.png)

O fluxo é simples. O nó **Assinar leituras** recebe as mensagens do tópico e já converte o JSON. Uma função separa os sinais e verifica os limites, e o resultado vai para três elementos do dashboard: um gráfico do BPM nos últimos 10 minutos, um gauge de temperatura de 30 a 45 °C e um indicador de alerta, que funciona como um LED virtual verde ou vermelho com o motivo escrito embaixo. Também deixamos um nó de debug para ver as mensagens chegando.

O alerta acende acima de 120 BPM ou de 38 °C, os dois exemplos do enunciado. São limites desta simulação, não critérios clínicos. Esse alerta não tem relação com o filtro de 220 BPM da Parte 1: o filtro descarta o que não parece real, e o alerta mantém o dado e avisa que ele precisa de atenção.

## 5. Testes

| Teste | O que fizemos | Resultado |
|---|---|---|
| Publicação | Simulação rodando, com leituras a cada 5 s | Mensagens chegando no Node-RED |
| Alerta de temperatura | DHT22 em 39 °C | Indicador vermelho, com o motivo |
| Sem alerta | DHT22 em 36,5 °C, BPM abaixo de 120 | Indicador verde e gauge em 36,5 |
| Alerta de BPM | Cliques rápidos, chegando a 152 BPM | Indicador vermelho e gráfico subindo |
| Queda simulada | Chave em OFFLINE por 3 leituras (antes de montar o dashboard) | Publicadas em ordem ao voltar (26655, 31655 e 36655 ms) |
| Função do alerta | Código da função testado fora do Node-RED, com 7 casos, incluindo os valores no limite e mensagens inválidas | Todos corretos |

![Dashboard com alerta de temperatura](prints_parte2/01_dashboard_com_alerta.png)

![Dashboard sem alerta](prints_parte2/02_dashboard_sem_alerta.png)

![Dashboard com alerta de BPM](prints_parte2/03_alerta_bpm.png)

No print do alerta de BPM, dá para ver também uma linha "Toque ignorado (artefato)" no Monitor Serial, ou seja, o filtro da Parte 1 continuou funcionando junto com o alerta.

Medimos de novo a memória com o TLS conectado. A RAM livre caiu de 256 KB para 113 KB, e o maior bloco contínuo ficou em 59 KB. O TLS consumiu cerca de 143 KB, mais do que esperávamos quando limitamos o buffer a uns 70 KB na Parte 1, mas ainda sobrou espaço, então mantivemos o buffer de 4.320 leituras.

## 6. Eficiência

O enunciado também pede uma reflexão sobre eficiência, e ela apareceu em várias escolhas do projeto. A primeira foi o próprio MQTT, que o Cap08 (p. 23) destaca pela leveza e pelo baixo consumo de banda. Cada uma das nossas mensagens tem cerca de 60 bytes. Com uma leitura a cada 5 segundos, isso dá uns 44 KB por hora, pouco até para uma conexão de celular fraca.

Boa parte da economia vem de tratar os dados no próprio ESP32, antes de enviar. Os toques descartados pelo filtro e as leituras inválidas do sensor nem chegam a ser transmitidos. Sem conexão, o ESP32 não fica tentando enviar o tempo todo: ele guarda as leituras e tenta reconectar a cada 5 segundos. Quando a conexão volta, envia no máximo 10 mensagens por segundo, para não sobrecarregar o broker nem o dashboard.

A memória também foi tratada como um recurso limitado. Em vez de escolher o tamanho do buffer no chute, medimos a RAM em cada etapa (sem o buffer, com o buffer e com o TLS) e escolhemos 4.320 leituras, que cabem com folga. Uma melhoria possível seria enviar várias leituras em uma só mensagem durante a sincronização, o que reduziria o número de mensagens depois de uma queda longa.

## 7. Segurança

A comunicação com o broker é criptografada com TLS, e o broker só aceita conexões com usuário e senha. Criamos no HiveMQ um usuário para esta atividade e deixamos a senha fora do repositório e do projeto publicado no Wokwi. No ESP32, porém, usamos o `setInsecure()`, como no exemplo da apostila: a conexão é criptografada, mas o certificado do broker não é verificado. Em um produto real, essa verificação seria necessária.

Também pensamos na LGPD. O nosso broker fica em Frankfurt, fora do Brasil. Como os dados aqui são simulados, isso não é um problema, mas com dados reais de pacientes, que são dados sensíveis, seria preciso avaliar a transferência internacional, quem tem acesso e por quanto tempo os dados ficam guardados. Por último, configuramos o Node-RED para aceitar acesso só do próprio computador, já que o editor dele não tem senha.

## 8. Limitações

O gráfico usa a hora em que a mensagem chegou ao Node-RED, e não a hora da leitura. Por isso, quando a conexão volta, as leituras atrasadas aparecem todas juntas no gráfico, mesmo com o `momento` guardando a ordem certa. Pelo mesmo motivo, durante a sincronização o indicador de alerta mostra a última leitura recebida, que pode ser antiga.

Usamos QoS 0, então o broker não confirma o recebimento, e uma leitura poderia se perder. O QoS 1 resolveria isso. Também percebemos que a conexão com TLS trava o `loop()` por uns 2 segundos, e toques nesse tempo não são contados. Nos nossos testes a conexão com o broker não caiu de verdade, então não testamos a reconexão depois de uma queda real.

Por fim, o plano Starter é só um teste de 15 dias: depois disso, o cluster é apagado, e o projeto precisaria de outro broker. O Node-RED também só mostra os dados, sem guardar histórico. O Cap08 usa o InfluxDB e o Grafana Cloud para isso, mas eles eram opcionais e não fizemos.

## 9. Referências

- FIAP. [Enunciado da atividade da Fase 3](Enunciado.md).
- FIAP. Fase 3, Cap08 — Cloud Computing como Pilar da IoT Moderna, p. 21-25.
- HiveMQ. [Getting Started with HiveMQ Cloud](https://docs.hivemq.com/hivemq-cloud/quick-start-guide.html).
