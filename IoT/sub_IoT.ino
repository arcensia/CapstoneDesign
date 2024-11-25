#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <time.h>
#include <Wire.h>

//wifi, mqtt server 설정
const char* ssid = "proj";
const char* password = "00000000";
const char* mqtt_server = "192.168.0.5";

int Current = A0;

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
int value = 0;

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
      client.publish("BTopic", "hello world B");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}9+
}

int Buffer;
int I = 0;
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  I = analogRead(Current);
  Serial.print(" i = ");
  Serial.println(I);

  Buffer = sizeof(I)+4;
  char data[Buffer];
  snprintf (data, Buffer, "%d", I);
//  Serial.println(Buffer);
  client.publish("BTopic", data);//pub, 전송
 

}
