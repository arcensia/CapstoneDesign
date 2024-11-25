import pymysql
import pandas as pd
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
        inputDB(payload)
        # return payload
    client.subscribe(topic) #1
    client.on_message = on_message



# #DB연결
con = pymysql.connect(host='localhost', user='root', password='a',
                       db='testt', charset='utf8') # 한글처리 (charset = 'utf8')
# DB 삽입 (테이블이름, 넣을 데이터)
def InsertDBtoPi(data):
    real = data.split(',')
    gas,volt,Acurrnt,Bcurrnt = real
    # print(f"{b}")
    cur = con.cursor()
    # cur.execute(f"INSERT INTO Voltage (value) VALUES({a})")
    cur.execute(f"INSERT INTO Current (value) VALUES({b})")
    con.commit()



def inputDB(data):
    #DB연결
    # con = pymysql.connect(host='localhost', user='root', password='root',
    #                     db='testt', charset='utf8') # 한글처리 (charset = 'utf8')

    cur = con.cursor()
    real = data.split(',')
    aa = int(real[0])
    # dommey = str(random.randrange(1, 50))

    
    # STEP 4: SQL문 실행 및 Fetch
    sql = "INSERT INTO testtable (V) VALUES (%s)"
    cur.execute(sql, aa)
    con.commit()

    # 데이타 Fetch
    rows = cur.fetchall()
    print(rows)     # 전체 rows

    # STEP 5: DB 연결 종료
    con.close()



def run():
    client = connect_mqtt() 
    subscribe(client)   
    client.loop_forever()
  

if __name__ == '__main__':
    run()