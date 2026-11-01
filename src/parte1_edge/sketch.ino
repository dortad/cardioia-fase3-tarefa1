// CardioIA - Fase 3, Parte 1: armazenamento e processamento local (Edge Computing)
// Dados simulados no Wokwi; o protótipo não foi validado para uso clínico.
// Wokwi: DHT22 VCC->3V3, SDA->D15, GND->GND; Pushbutton 1.l->D4, 2.l->GND; Slide switch 2->D18, 1->GND

#include <DHT.h>  // biblioteca da Adafruit para sensores DHT

// ---------- Configuração do hardware ----------
const int PINO_DHT   = 15;    // GPIO do pino SDA do DHT22
const int PINO_BOTAO = 4;     // GPIO do botão de batimentos
const int PINO_WIFI  = 18;    // GPIO da chave que simula o Wi-Fi
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
em uso, restaram 256 KB. Mantivemos as leituras a cada 5 s, em vez de 12 horas a cada
10 s, para que um pico de 8 s não caia entre duas leituras.
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

// ---------- Wi-Fi simulado ----------
bool wifiConectado = false;           // true = online, false = offline
bool leituraChave  = false;           // última leitura da chave, ainda sem confirmar
unsigned long ultimaMudancaChave = 0; // momento da última oscilação da chave

void setup() {
  Serial.begin(115200);
  dht.begin();                        // prepara o sensor
  pinMode(PINO_BOTAO, INPUT_PULLUP);  // botão com resistor interno
  pinMode(PINO_WIFI, INPUT_PULLUP);   // chave do Wi-Fi com resistor interno
  Serial.println("CardioIA iniciado - DHT22 a cada 5 s + botao de batimentos");
}

void loop() {
  unsigned long agora = millis();  // ms desde que o ESP32 ligou

  // ===== Wi-Fi simulado: a chave define o estado da conexão =====
  bool conectadoAgora = (digitalRead(PINO_WIFI) == LOW);  // LOW = chave ligada ao GND

  if (conectadoAgora != leituraChave) {  // a chave oscilou: reinicia a contagem
    leituraChave = conectadoAgora;
    ultimaMudancaChave = agora;
  }

  // Só aceita o novo estado depois de a chave ficar estável por DEBOUNCE_MS
  if (leituraChave != wifiConectado && agora - ultimaMudancaChave >= DEBOUNCE_MS) {
    wifiConectado = leituraChave;
    Serial.println(wifiConectado ? "Wi-Fi simulado: ONLINE" : "Wi-Fi simulado: OFFLINE");
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

  // ===== Sincronização: envia uma leitura por volta, da mais antiga para a mais nova =====
  // Assim o botão e o DHT22 seguem ativos, e uma queda no meio preserva o que falta enviar
  if (wifiConectado && totalLeituras > 0) {
    // A mais antiga fica totalLeituras posições antes de proximaPosicao
    int maisAntiga = (proximaPosicao + CAPACIDADE_BUFFER - totalLeituras) % CAPACIDADE_BUFFER;

    // Serial.println simula o envio para a nuvem, como pede o enunciado
    Serial.print("Enviado a nuvem: ");
    Serial.print(buffer[maisAntiga].momento);
    Serial.print(" ms | ");
    Serial.print(buffer[maisAntiga].temperatura, 1);
    Serial.print(" C | ");
    Serial.print(buffer[maisAntiga].umidade, 1);
    Serial.print(" % | BPM: ");
    Serial.print(buffer[maisAntiga].bpm);

    totalLeituras--;  // leitura enviada: libera a posição no buffer

    Serial.print(" | Pendentes: ");
    Serial.println(totalLeituras);
  }
}
