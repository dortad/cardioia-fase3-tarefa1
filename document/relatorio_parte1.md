# Relatório da Parte 1 — Armazenamento e processamento local (Edge Computing)

**CardioIA — Fase 3: Monitoramento Contínuo – IoT na Saúde**
**Grupo AI4Success — Turma 2TIAOR**
Durval de Oliveira Dorta Junior (RM 567007) e Guilherme da Nobrega Gontijo (RM 562211)

**Projeto no Wokwi:** [CardioIA - Fase 3](https://wokwi.com/projects/478992650362063873) | **Código:** [src/parte1_edge/](../src/parte1_edge/)

Os dados deste trabalho são simulados, e o protótipo não foi validado para uso clínico.

## 1. Objetivo

Esta parte simula o dispositivo vestível do CardioIA em um ESP32 no Wokwi. O dispositivo lê sinais vitais simulados, trata os dados no próprio equipamento e continua coletando sem conexão. Quando a conexão volta, ele envia o que ficou guardado.

Essa escolha segue o papel da borda descrito no Cap09: dispositivos que operam de forma autônoma mesmo sem rede externa, com alta resiliência a falhas de conexão, mas com armazenamento restrito, usado principalmente para logs e dados temporários. O limite de memória é, portanto, uma decisão central do projeto.

## 2. Componentes

| Componente | Função | Ligação ao ESP32 |
|---|---|---|
| DHT22 | Temperatura e umidade | SDA em D15 |
| Botão | Simula os batimentos: cada toque é uma batida | D4 |
| Chave deslizante | Simula o Wi-Fi, com a variável booleana `wifiConectado` | D18 |

O DHT22 é o sensor obrigatório, e o botão é o segundo sensor, de livre escolha, conforme a sugestão do enunciado.

## 3. Fluxo de funcionamento

O `loop()` não usa `delay()`, para que o botão seja verificado o tempo todo. Em cada volta, ele executa quatro tarefas:

1. **Conexão:** lê a chave. O novo estado só é aceito depois de 50 ms estável, para eliminar a trepidação do contato.
2. **Batimentos:** cada toque válido gera um intervalo em relação ao batimento anterior, e o BPM é calculado por `60000 / intervalo`.
3. **Leitura periódica:** a cada 5 s, lê o DHT22 e grava no buffer uma leitura com momento, temperatura, umidade e BPM.
4. **Sincronização:** com a conexão ativa e havendo leituras pendentes, envia uma leitura e libera sua posição.

## 4. Processamento local

Dois tratamentos ocorrem antes de o dado seguir adiante:

- **Filtro de artefato:** intervalos menores que 273 ms, equivalentes a mais de 220 BPM, são ignorados. Esse limite foi definido para esta simulação e não é um critério clínico. Um toque ignorado não atualiza o último batimento. Assim, o intervalo seguinte é medido a partir do último batimento aceito, e um ruído não invalida a batida verdadeira que vem depois dele.
- **Leituras inválidas:** quando o DHT22 devolve `NaN`, a leitura é descartada antes da gravação e não chega à nuvem.

O filtro é diferente do alerta previsto para a Parte 2. O filtro descarta o que não parece um dado real. O alerta mantém o dado e sinaliza que ele merece atenção, como uma leitura acima de 120 BPM.

## 5. Lógica de resiliência

### 5.1 Limite de armazenamento

O SPIFFS é opcional e não persiste no simulador. Por isso, as leituras ficam em um buffer na RAM, com o Monitor Serial como alternativa de registro, como prevê o enunciado. Cada leitura ocupa 16 bytes. A 1 leitura a cada 5 s, são 720 leituras por hora, ou 11,25 KB.

A primeira proposta foi guardar 12 horas (8.640 leituras, 135 KB). Medimos a memória no Wokwi e encontramos 323 KB livres, mas o maior bloco contínuo tinha 107 KB. Como o vetor precisa de memória contínua e a Parte 2 ainda vai usar RAM para Wi-Fi e MQTT, adotamos uma meta de até cerca de 70 KB. Havia duas formas de atingi-la:

| Opção | Autonomia | Intervalo | Leituras | Pico de 8 s |
|---|---|---|---|---|
| A (escolhida) | 6 horas | 5 s | 4.320 | Sempre registrado |
| B | 12 horas | ~10 s | 4.480 | Pode cair entre duas leituras |

Escolhemos manter uma leitura a cada 5 segundos, com um buffer de 4.320 leituras (cerca de 6 horas e 67,5 KB), porque o paciente pode ficar sem conexão durante um deslocamento longo ou uma queda temporária da internet, e nesse período o sistema precisa continuar registrando os sinais simulados com detalhe suficiente para que um pico curto, de 8 segundos, não caia entre duas leituras. Com o buffer em uso, a RAM livre medida foi de 256 KB.

### 5.2 Buffer circular

Sem conexão, a coleta continua normalmente. Quando o buffer enche, cada leitura nova substitui a mais antiga, preservando as 6 horas mais recentes. Quando a conexão volta, esse é o trecho mais útil para acompanhar o estado atual.

### 5.3 Sincronização

Ao reconectar, o sistema envia uma leitura por volta do `loop()`, da mais antiga para a mais nova, simulando a nuvem com `Serial.println`. Depois de cada envio, a posição é liberada, o que faz o papel de apagar o arquivo local citado no enunciado.

Enviar uma leitura por vez mantém o botão e o DHT22 ativos durante a sincronização, e uma queda no meio do envio preserva o que falta. Cada leitura carrega seu `momento`, então os dados enviados com atraso voltam ao lugar certo na linha do tempo.

## 6. Testes no Wokwi

| Teste | Resultado |
|---|---|
| Toques muito rápidos | Ignorados como artefato; o maior BPM aceito nesse teste foi 219 |
| Primeiro toque depois de pausa maior que 5 s | BPM reinicia em 0, sem valor falso |
| Deslizar a chave | Uma mensagem por mudança de estado |
| 5 leituras offline, depois online | Enviadas em ordem, de 5000 a 25000 ms |
| Capacidade temporária de 3, com 5 leituras offline | Enviadas apenas as 3 mais recentes: 15000, 20000 e 25000 ms |
| Memória com o buffer em uso | 256 KB livres, de 323 KB |

## 7. Limitações e melhorias futuras

- **Memória volátil:** o buffer fica na RAM e se perde se o ESP32 reiniciar. Um dispositivo real precisaria de armazenamento persistente, como SPIFFS ou cartão microSD.
- **Tempo relativo:** `momento` conta os milissegundos desde que o ESP32 ligou, não a hora do relógio.
- **Eventos curtos:** variações menores que 5 s podem não ser guardadas, porque o buffer registra o BPM apenas no momento de cada leitura.
- **Testes pendentes:** a capacidade de 4.320 leituras só foi testada em escala reduzida. A falha do DHT22 e a queda da conexão no meio de uma sincronização não foram exercitadas.
- **Folga de memória:** a meta de 70 KB é uma estimativa, a ser confirmada com Wi-Fi e MQTT na Parte 2.
- **Retenção por prioridade:** o buffer poderia preservar as leituras fora da faixa normal antes de substituir as demais. Essa ideia foi deixada para o futuro porque aumenta a complexidade e dificulta manter a ordem de envio.

## 8. Referências

- FIAP. [Enunciado da atividade da Fase 3](Enunciado.md).
- FIAP. Fase 3, Cap09 — Inteligência na Borda: Fog e Edge Computing Transformando a IoT, p. 32.
