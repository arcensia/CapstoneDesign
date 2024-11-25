import random
import time
from typing import Tuple
import numpy as np
from numpy.core import numeric
import paho.mqtt.client as mqtt_client
import csv
from datetime import datetime

# broker 정보
broker_address = "192.168.0.5"
broker_port = 1883
topic = "ATopic"

CSVFileName = "test.csv"

#클라이언트 만들기
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print(f"Failed to connect, Returned code: {rc}")

    def on_disconnect(client, userdata, flags, rc=0):
        print(f"disconnected result code {str(rc)}")

    def on_log(client, userdata, level, buf):
        # print(f"log: {1}")
        print("")

    # client 생성
    client_id = f"mqtt_client_{random.randint(0, 1000)}"
    client = mqtt_client.Client(client_id)

    # 콜백 함수 설정
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log

    # broker 연결
    client.connect(host=broker_address, port=broker_port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        #msg.payload.decode()에서 메세지와 토픽을 받음
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        payload = msg.payload.decode()
        inputCSV(payload)
        # return payload
    client.subscribe(topic) #1
    client.on_message = on_message

def ReadCSV():
    f = open('data/'+CSVFileName, 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        print(line)
        print(line[0])
        num = int(line[0])
    f.close()


def inputCSV(data):
    Rtime = str(datetime.now().time())
    print(data)

    real = data.split(',')
    a,b,c,d = real
    # real = data.split(',')
    # a = real

    # # You must to do make "mkdir date" where delet.py is. 
 
    fa = open('data/test.csv', 'a', encoding='utf-8', newline='')
    wr = csv.writer(fa)
    # wr.writerow([data])
    # wr.writerow([real])
    # wr.writerow([Rtime, a,b])
    wr.writerow([d])
    #Rtime, 시간
    fa.close()

def run():
    client = connect_mqtt()
    subscribe(client)   
    client.loop_forever()
  

if __name__ == '__main__':
    run()