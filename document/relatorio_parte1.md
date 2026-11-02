# Relatório da Parte 1 — Armazenamento e processamento local (Edge Computing)

CardioIA — Fase 3: Monitoramento Contínuo – IoT na Saúde
Grupo AI4Success — Turma 2TIAOR
Durval de Oliveira Dorta Junior (RM 567007) e Guilherme da Nobrega Gontijo (RM 562211)

Projeto no Wokwi: [CardioIA - Fase 3](https://wokwi.com/projects/478992650362063873)
Código: [src/parte1_edge/](../src/parte1_edge/)

Todos os dados deste trabalho são simulados. O protótipo não foi validado para uso clínico.

## 1. O que fizemos

Nesta parte, montamos no Wokwi um ESP32 que faz o papel de um monitor cardíaco vestível. Ele lê temperatura, umidade e batimentos, trata esses dados no próprio dispositivo e continua coletando mesmo sem internet. Quando a conexão volta, envia o que ficou guardado.

A ideia veio do Cap09, que descreve a borda (Edge) como a camada que continua funcionando sozinha quando a rede cai, mas com pouco espaço de armazenamento, usado basicamente para dados temporários. Por isso, o tamanho da memória acabou sendo a decisão mais importante desta parte.

## 2. Circuito

Usamos três componentes ligados ao ESP32:

| Componente | Para que serve | Pino |
|---|---|---|
| DHT22 | Temperatura e umidade | D15 |
| Botão | Simula os batimentos (cada toque é uma batida) | D4 |
| Chave deslizante | Simula o Wi-Fi ligado ou desligado | D18 |

O DHT22 é o sensor obrigatório. Para o segundo sensor, seguimos a sugestão do próprio enunciado e usamos um botão apertado algumas vezes por minuto.

## 3. Como o programa funciona

Não usamos `delay()` no `loop()`, porque o programa ficaria parado e perderia os toques no botão. Em vez disso, cada volta do `loop()` faz quatro coisas rápidas: lê a chave do Wi-Fi, verifica se houve um toque no botão, faz a leitura do DHT22 quando já passaram 5 segundos e, se estiver online, envia uma leitura guardada.

O BPM é calculado pelo tempo entre dois toques: `60000 / intervalo`, já que um minuto tem 60.000 ms. Com toques a cada 1 segundo, por exemplo, o resultado é 60 BPM.

## 4. Tratamento dos dados no dispositivo

O botão já tinha um debounce de 50 ms para ignorar a trepidação do contato. Mesmo assim, quando testamos clicando o mais rápido possível, chegamos a ver 363 BPM, um valor que não representa um batimento real. Para resolver, criamos um filtro: intervalos menores que 273 ms, que dariam mais de 220 BPM, são ignorados como artefato. O valor de 220 foi um limite que definimos para esta simulação, não um critério clínico.

Um ponto que precisou de uma conta para ficar claro: quando um toque é ignorado, ele não pode virar a referência para o próximo intervalo. Imagine um batimento em 0 ms, um ruído em 250 ms e outro batimento em 504 ms. Se o ruído virasse a referência, o intervalo seguinte seria de 254 ms, e a batida verdadeira também seria descartada. Por isso, o próximo intervalo é sempre medido a partir do último batimento aceito.

Também descartamos as leituras inválidas do DHT22. Quando o sensor falha, ele devolve `NaN`, e essa leitura não é gravada nem enviada.

Esse filtro é diferente do alerta da Parte 2. O filtro joga fora o que não parece um dado real. O alerta mantém o dado e avisa que ele merece atenção, por exemplo, acima de 120 BPM.

## 5. Resiliência offline

### 5.1 Quanto guardar

O SPIFFS é opcional e não funciona no simulador, então guardamos as leituras em um vetor na memória RAM, como alternativa prevista no enunciado. Cada leitura tem quatro campos (momento, temperatura, umidade e BPM) e ocupa 16 bytes. Com uma leitura a cada 5 segundos, são 720 leituras por hora, ou 11,25 KB.

Nossa primeira ideia foi guardar 12 horas, o que daria 8.640 leituras e 135 KB. Antes de programar, medimos a memória no Wokwi: havia 323 KB livres, mas o maior bloco contínuo tinha só 107 KB, e um vetor precisa de memória contínua. Além disso, a Parte 2 ainda ia precisar de RAM para o Wi-Fi e o MQTT. Decidimos então trabalhar com uma meta de uns 70 KB e comparamos duas opções:

| Opção | Autonomia | Intervalo | Leituras | Um pico de 8 s aparece? |
|---|---|---|---|---|
| A (escolhida) | 6 horas | 5 s | 4.320 | Sempre |
| B | 12 horas | cerca de 10 s | 4.480 | Às vezes |

Ficamos com a opção A, com 4.320 leituras (cerca de 6 horas e 67,5 KB). Preferimos perder horas de autonomia a perder detalhe: com leituras a cada 10 segundos, um pico curto poderia cair entre duas leituras e não ser registrado. Seis horas cobrem situações como um deslocamento longo ou uma queda da internet de casa. Depois de implementar, a RAM livre medida caiu para 256 KB, o que bateu com a conta.

### 5.2 Quando a memória enche

Escolhemos um buffer circular: quando as 4.320 posições estão ocupadas, a leitura nova entra no lugar da mais antiga. Assim, ficam sempre as últimas 6 horas, que são as mais úteis quando a conexão volta.

Chegamos a pensar em proteger as leituras fora da faixa normal, substituindo só as normais. Deixamos essa ideia para o futuro, porque complicaria bastante o código e a ordem de envio.

### 5.3 Quando a conexão volta

A chave deslizante simula o Wi-Fi. Ela também trepidava: no primeiro teste, cada deslize gerava vários ONLINE e OFFLINE seguidos. Corrigimos aceitando a mudança só depois de a chave ficar estável por 50 ms.

Ao reconectar, o programa envia uma leitura por volta do `loop()`, da mais antiga para a mais nova, usando `Serial.println` para simular a nuvem. Depois de cada envio, a posição é liberada, o que corresponde a apagar o arquivo local, como pede o enunciado. Enviando uma por vez, o botão e o DHT22 continuam funcionando durante a sincronização, e, se a conexão cair no meio, o que falta continua guardado. Como cada leitura leva o seu `momento`, os dados que chegam atrasados podem ser colocados de volta na ordem certa.

## 6. Testes

| Teste | Resultado |
|---|---|
| Cliques muito rápidos | Ignorados como artefato; o maior BPM aceito foi 219 |
| Primeiro toque depois de uma pausa | O BPM recomeça em 0, sem valor falso |
| Deslizar a chave | Uma mensagem por mudança |
| 5 leituras offline e depois online | Enviadas em ordem, de 5000 a 25000 ms |
| Capacidade reduzida para 3, com 5 leituras offline | Enviadas só as 3 mais recentes (15000, 20000 e 25000 ms) |
| Memória com o buffer em uso | 256 KB livres, de 323 KB |

Para testar o buffer cheio sem esperar 6 horas, reduzimos a capacidade para 3 temporariamente e depois voltamos para 4.320. Na revisão final do código, encontramos um problema que os testes não tinham mostrado: o primeiro toque depois de uma pausa longa usava a batida de antes dela e calculava um BPM muito baixo. Com 30 segundos de pausa, por exemplo, daria 2 BPM. Corrigimos fazendo a contagem recomeçar depois de 5 segundos sem toque e testamos de novo.

## 7. Limitações

O buffer fica na RAM, então se o ESP32 reiniciar os dados se perdem. Um dispositivo real precisaria de armazenamento permanente, como o SPIFFS ou um cartão microSD. O campo `momento` também não é a hora do relógio, e sim o tempo desde que o ESP32 ligou.

Como gravamos uma leitura a cada 5 segundos, variações muito curtas no BPM podem não ficar registradas. Também não conseguimos testar tudo: a capacidade de 4.320 leituras foi testada só em escala reduzida, e não simulamos falha do DHT22 nem queda da conexão no meio de uma sincronização. Por fim, a meta de 70 KB para o buffer partiu de uma estimativa do espaço que o Wi-Fi e o MQTT iam precisar; na Parte 2, com o TLS conectado, ainda sobraram 113 KB livres.

## 8. Referências

- FIAP. [Enunciado da atividade da Fase 3](Enunciado.md).
- FIAP. Fase 3, Cap09 — Inteligência na Borda: Fog e Edge Computing Transformando a IoT, p. 32.
