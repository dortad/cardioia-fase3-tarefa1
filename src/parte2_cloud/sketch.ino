// CardioIA - Fase 3, Parte 2: transmissão para a nuvem via MQTT (Fog/Cloud Computing)
// Dados simulados no Wokwi; o protótipo não foi validado para uso clínico.
// Wokwi: DHT22 VCC->3V3, SDA->D15, GND->GND; Pushbutton 1.l->D4, 2.l->GND; Slide switch 2->D18, 1->GND

#include <DHT.h>               // biblioteca da Adafruit para sensores DHT
#include <WiFi.h>              // conexão Wi-Fi do ESP32
#include <WiFiClientSecure.h>  // conexão com criptografia TLS
#include <PubSubClient.h>      // cliente MQTT

// ---------- Rede e broker MQTT (preencher somente no Wokwi) ----------
const char* WIFI_SSID       = "Wokwi-GUEST";  // rede virtual do Wokwi, sem senha
const char* WIFI_SENHA      = "";
const char* MQTT_SERVIDOR   = "COLE_AQUI_O_ENDERECO_DO_CLUSTER";  // ex.: xxxxxxxx.s1.eu.hivemq.cloud
const int   MQTT_PORTA      = 8883;                               // porta segura (TLS)
const char* MQTT_USUARIO    = "COLE_AQUI_O_USUARIO";
const char* MQTT_SENHA      = "COLE_AQUI_A_SENHA";
const char* MQTT_CLIENTE_ID = "cardioia-esp32-ai4success";        // identifica este dispositivo no broker
const char* MQTT_TOPICO     = "cardioia/ai4success/leituras";     // tópico assinado pelo Node-RED

const unsigned long INTERVALO_TENTATIVA_MS = 5000;  // espera entre tentativas de conexão ao broker
const unsigned long INTERVALO_ENVIO_MS     = 100;   // no máximo 10 publicações por segundo
unsigned long ultimaTentativa = 0;                  // momento da última tentativa de conexão
unsigned long ultimoEnvio     = 0;                  // momento da última publicação

WiFiClientSecure clienteSeguro;      // conexão criptografada com o broker
PubSubClient mqtt(clienteSeguro);    // cliente MQTT que usa essa conexão

// ---------- Configuração do hardware ----------
const int PINO_DHT   = 15;    // GPIO do pino SDA do DHT22
const int PINO_BOTAO = 4;     // GPIO do botão de batimentos
const int PINO_WIFI  = 18;    // GPIO da chave que simula a queda de conexão
DHT dht(PINO_DHT, DHT22);     // objeto que representa o sensor

// ---------- Controle de tempo ----------
const unsigned long INTERVALO_LEITURA_MS = 5000;  // ler o DHT22 e gravar uma leitura a cada 5 segundos
unsigned long ultimaLeitura = 0;                  // momento da última leitura do DHT22

// ---------- Batimentos ----------
const unsigned long DEBOUNCE_MS         = 50;    // ignora trepidação do botão e da chave menor que 50 ms
const unsigned long SEM_BATIMENTO_MS    = 5000;  // sem toque por 5 s => BPM zera
const unsigned long INTERVALO_MINIMO_MS = 273;
/*
O 60000 é a quantidade de milissegundos em 1 minuto.
Por exemplo, com toques a cada 1000 ms: 60000 / 1000 = 60 BPM.
Quanto menor o intervalo, maior o BPM. Por isso, para bloquear um BPM alto demais,
basta bloquear um intervalo curto demais (porque estamos simulando com o botão).
Definimos que o BPM máximo aceito nesta simulação é 220 (não é critério clínico) e
então calculamos o intervalo correspondente:
intervalo mínimo = 60000 / 220 = 272,7 ms, arredondado para 273 ms
*/
int estadoAnteriorBotao  = HIGH;      // HIGH = solto (por causa do INPUT_PULLUP)
unsigned long ultimaMudancaBotao = 0; // momento da última mudança aceita do botão
unsigned long ultimoBatimento    = 0; // momento do último batimento (0 = nenhum ainda)
int bpm = 0;                          // batimentos por minuto calculados

// ---------- Armazenamento local (buffer circular) ----------
/*
720 leituras por hora * 6 horas = 4320 leituras * 16 bytes = 67,5 KB.
Medimos no Wokwi 323 KB de RAM livre, com maior bloco contínuo de 107 KB. Com o buffer
em uso, restaram 256 KB e, com o TLS conectado, 113 KB. Mantivemos as leituras a cada
5 s, em vez de 12 horas a cada 10 s, para que um pico de 8 s não caia entre duas leituras.
*/
const unsigned long CAPACIDADE_BUFFER = 4320;  // 6 horas sem conexão

struct Leitura {           // reúne os dados de uma leitura em um bloco de 16 bytes
  unsigned long momento;   // ms desde que o ESP32 ligou: preserva a ordem no envio tardio
  float temperatura, umidade;
  int bpm;
};

Leitura buffer[CAPACIDADE_BUFFER];  // guarda as leituras ainda não enviadas
int totalLeituras  = 0;             // quantas leituras aguardam envio
int proximaPosicao = 0;             // posição do buffer onde a próxima leitura será gravada

// ---------- Queda de conexão simulada ----------
bool wifiConectado = false;           // true = online, false = offline
bool leituraChave  = false;           // última leitura da chave, ainda sem confirmar
unsigned long ultimaMudancaChave = 0; // momento da última oscilação da chave

// Mantém a conexão com o broker. Espera entre as tentativas para não travar o loop
void manterConexaoMqtt(unsigned long agora) {
  if (mqtt.connected()) {
    mqtt.loop();  // mantém a sessão MQTT ativa
    return;
  }

  if (ultimaTentativa > 0 && agora - ultimaTentativa < INTERVALO_TENTATIVA_MS) {
    return;
  }
  ultimaTentativa = agora;

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Aguardando a rede Wi-Fi do Wokwi...");
    return;
  }

  Serial.println("Conectando ao broker MQTT...");
  if (mqtt.connect(MQTT_CLIENTE_ID, MQTT_USUARIO, MQTT_SENHA)) {
    Serial.println("Broker MQTT conectado");
  } else {
    Serial.print("Falha na conexão com o broker, código: ");
    Serial.println(mqtt.state());
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();                        // prepara o sensor
  pinMode(PINO_BOTAO, INPUT_PULLUP);  // botão com resistor interno
  pinMode(PINO_WIFI, INPUT_PULLUP);   // chave com resistor interno
  Serial.println("CardioIA iniciado - DHT22 a cada 5 s + botao de batimentos + MQTT");

  WiFi.begin(WIFI_SSID, WIFI_SENHA, 6);  // canal 6 acelera a conexão no Wokwi
  clienteSeguro.setInsecure();           // usa TLS sem verificar o certificado, como no Cap08
  mqtt.setServer(MQTT_SERVIDOR, MQTT_PORTA);
}

void loop() {
  unsigned long agora = millis();  // ms desde que o ESP32 ligou

  // ===== Queda de conexão simulada: a chave libera ou bloqueia o envio =====
  bool conectadoAgora = (digitalRead(PINO_WIFI) == LOW);  // LOW = chave ligada ao GND

  if (conectadoAgora != leituraChave) {  // a chave oscilou: reinicia a contagem
    leituraChave = conectadoAgora;
    ultimaMudancaChave = agora;
  }

  // Só aceita o novo estado depois de a chave ficar estável por DEBOUNCE_MS
  if (leituraChave != wifiConectado && agora - ultimaMudancaChave >= DEBOUNCE_MS) {
    wifiConectado = leituraChave;
    Serial.println(wifiConectado ? "Conexao simulada: ONLINE" : "Conexao simulada: OFFLINE");
  }

  if (wifiConectado) {
    manterConexaoMqtt(agora);
  }

  // ===== Verificação do botão (roda em TODA volta do loop) =====
  int estadoBotao = digitalRead(PINO_BOTAO);

  // Houve mudança e já passou o tempo de debounce?
  if (estadoBotao != estadoAnteriorBotao && agora - ultimaMudancaBotao >= DEBOUNCE_MS) {
    ultimaMudancaBotao  = agora;
    estadoAnteriorBotao = estadoBotao;

    // Borda de descida: passou de solto (HIGH) para apertado (LOW) = 1 batimento
    if (estadoBotao == LOW) {
      if (ultimoBatimento > 0) {                  // precisa de 2 toques para ter um intervalo
        unsigned long intervalo = agora - ultimoBatimento;
        if (intervalo < INTERVALO_MINIMO_MS) {
          Serial.println("Toque ignorado (artefato)");
          /*
          Intervalo menor que INTERVALO_MINIMO_MS equivale a mais de 220 BPM, o limite
          definido para esta simulação. O return impede que este toque atualize
          ultimoBatimento: o próximo intervalo é medido do último batimento aceito.
          */
          return;
        }
        bpm = 60000 / intervalo;                  // 1 minuto = 60000 ms
      }
      ultimoBatimento = agora;
      Serial.print("Batimento! BPM: ");
      Serial.println(bpm);
    }
  }

  // Sem toques há muito tempo: considera ausência de batimento
  if (ultimoBatimento > 0 && agora - ultimoBatimento > SEM_BATIMENTO_MS) {
    bpm = 0;
    ultimoBatimento = 0;  // recomeça: o próximo toque não forma intervalo com o anterior
  }

  // ===== Leitura periódica do DHT22 e gravação no buffer =====
  if (agora - ultimaLeitura >= INTERVALO_LEITURA_MS) {
    ultimaLeitura = agora;

    float temperatura = dht.readTemperature();  // em °C
    float umidade     = dht.readHumidity();     // em %

    if (isnan(temperatura) || isnan(umidade)) {  // leitura inválida devolve NaN
      Serial.println("Falha na leitura do DHT22!");
      return;  // leitura inválida não entra no buffer nem vai para a nuvem
    }

    Serial.print("Temperatura: ");
    Serial.print(temperatura, 1);
    Serial.print(" C | Umidade: ");
    Serial.print(umidade, 1);
    Serial.print(" % | BPM: ");
    Serial.println(bpm);

    // Buffer circular: quando cheio, a leitura nova substitui a mais antiga
    buffer[proximaPosicao].momento     = agora;
    buffer[proximaPosicao].temperatura = temperatura;
    buffer[proximaPosicao].umidade     = umidade;
    buffer[proximaPosicao].bpm         = bpm;

    proximaPosicao = (proximaPosicao + 1) % CAPACIDADE_BUFFER;  // no fim, volta para 0

    if (totalLeituras < CAPACIDADE_BUFFER) {  // o total para de subir na capacidade
      totalLeituras++;
    }

    Serial.print("Leituras no buffer: ");
    Serial.print(totalLeituras);
    Serial.print(" | Proxima posicao: ");
    Serial.println(proximaPosicao);
  }

  // ===== Publicação MQTT: uma leitura por vez, da mais antiga para a mais nova =====
  if (wifiConectado && mqtt.connected() && totalLeituras > 0 && agora - ultimoEnvio >= INTERVALO_ENVIO_MS) {
    ultimoEnvio = agora;

    // A mais antiga fica totalLeituras posições antes de proximaPosicao
    int maisAntiga = (proximaPosicao + CAPACIDADE_BUFFER - totalLeituras) % CAPACIDADE_BUFFER;

    char mensagem[120];  // leitura em JSON, formato que o Node-RED interpreta
    snprintf(mensagem, sizeof(mensagem),
             "{\"momento\":%lu,\"temperatura\":%.1f,\"umidade\":%.1f,\"bpm\":%d}",
             buffer[maisAntiga].momento,
             buffer[maisAntiga].temperatura,
             buffer[maisAntiga].umidade,
             buffer[maisAntiga].bpm);

    // Só libera a posição se a publicação der certo; senão, a leitura fica para depois
    if (mqtt.publish(MQTT_TOPICO, mensagem)) {
      totalLeituras--;
      Serial.print("Publicado: ");
      Serial.print(mensagem);
      Serial.print(" | Pendentes: ");
      Serial.println(totalLeituras);
    } else {
      Serial.println("Falha ao publicar; leitura mantida no buffer");
    }
  }
}
