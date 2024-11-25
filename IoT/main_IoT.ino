#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <time.h>
#include <Wire.h>
#include "ZMPT101B.h" // 라이브러리에서 zmpt101b 설치
#include <Adafruit_ADS1X15.h>// 라이브러리에서 설치

//wifi, mqtt server 설정
const char* ssid = "proj";
const char* password = "00000000";
const char* mqtt_server = "192.168.0.5";


WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
int value = 0;

Adafruit_ADS1115 ads;

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);
  } else {
    digitalWrite(BUILTIN_LED, HIGH);
  }

}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      client.publish("ATopic", "hello world A");
      // ... and resubscribe
      client.subscribe("inTopic");//sub?
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
//  voltageSensor.calibrate();
  Serial.begin(115200);
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  ads.begin();
  
  delay(1000);
}

float V = 0;
int Buffer;
int i = 0;
int flag = 0;


void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  int adc0, adc1, adc2, adc3;
  adc0 = 0.01*ads.readADC_SingleEnded(0);
  adc1 = ads.readADC_SingleEnded(1);
  adc2 = 0.01*(ads.readADC_SingleEnded(2));
  adc3 = ads.readADC_SingleEnded(3);
//  Serial.println(adc2);
//  Buffer = sizeof(adc2);
//  Serial.println(Buffer);
  
  Serial.print("0 : ");
  Serial.print(adc0);
  Serial.print(" 1 : ");
  Serial.print(adc1);
  Serial.print(" 2 : ");
  Serial.print(adc2);
  Serial.print(" 3 : ");
  Serial.println(adc3);

  Buffer = sizeof(adc0)+sizeof(adc1)+sizeof(adc2)+sizeof(adc3)+6;// , 데이터값
  
  char data[Buffer];
  snprintf (data, Buffer, "%d,%d,%d,%d", adc0, adc1, adc2, adc3);//0 : 가스. 1: 총 전압값 2: 총 전류값 3: 비접촉전류센서
  Serial.println(Buffer);
  Serial.println(sizeof(data));
  client.publish("ATopic", data);//pub, 전송
 
}
