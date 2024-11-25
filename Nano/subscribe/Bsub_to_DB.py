import pymysql
import pandas as pd
import random
import time
from typing import Tuple
import numpy as np
from numpy.core import numeric
import paho.mqtt.client as mqtt_client
from datetime import datetime

# broker information
broker_address = "192.168.0.5"
broker_port = 1883
topic = "BTopic"

#make client
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

    # client create
    client_id = f"mqtt_client_{random.randint(0, 1000)}"
    client = mqtt_client.Client(client_id)


    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log

    # broker connect
    client.connect(host=broker_address, port=broker_port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        payload = msg.payload.decode()
        inputDB(payload)
    client.subscribe(topic) #1
    client.on_message = on_message


def inputDB(data):
    #DB connect
    con = pymysql.connect(host='localhost', user='root', password='',
                        db='TESTDB', charset='utf8')
    cur = con.cursor()

    
    # STEP 4:
    sql = "INSERT INTO Bsensertable (Bcurrent) VALUES (%s)"
    cur.execute(sql,data)
    con.commit()

    # Fetch
    rows = cur.fetchall()
    print(rows)     # totle rows

    # STEP 5
    con.close()



def run():
    client = connect_mqtt() 
    subscribe(client)   
    client.loop_forever()
  

if __name__ == '__main__':
    run()
