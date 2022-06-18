import random
import time
import paho.mqtt.client as mqtt_client


# broker 정보 #1
broker_address = "192.168.0.5" #my rpi
broker_port = 1883
topic = "ATopic"


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print(f"Failed to connect, Returned code: {rc}")

    def on_disconnect(client, userdata, flags, rc=0):
        print(f"disconnected result code {str(rc)}")

    def on_log(client, userdata, level, buf):
        print(f"log: {buf}")


    
    # client 생성 #2
    # 겹치면 안되니까
    client_id = f"mqtt_client_{random.randint(0, 1000)}"
    client = mqtt_client.Client(client_id)

    # 콜백 함수 설정 #3
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log

    # broker 연결 #4
    client.connect(host=broker_address, port=broker_port)
    return client


# def colectData():
#     temp, hum, = 1,2
#     extTemp = 3
#     lum = 4
#     butSts = 5
#     # temp, hum, = readDht()cd 
#     # extTemp = readDs()
#     # lum = readLdr()
#     # butSts = readBut()
#     return temp, hum, extTemp, lum, butSts

#정보를 pub하는 함수
def publish(client: mqtt_client):
    msg_count = 0
    temp, hum, = 1,2
    extTemp = 3
    lum = 4
    butSts = 5
    while True:
        
        time.sleep(1)
        #메세지 전달
        # msg = f"messages: {msg_count}"
        # result = client.publish(topic, msg)
        payload = str(temp)+","+str(hum)+","+str(extTemp)+","+str(lum)
        # payload = str(temp)+","+str(hum)+","+str(extTemp)+","+str(lum)+","+str(butSts)

        #기본 형태 : publish.single("paho/test/single", "payload", hostname="mqtt.eclipseprojects.io")
        result = client.publish(topic, payload)
        
        # result: [0, 1] [연결 성공/ 연결 실패]
        status = result[0]
        if status == 0:
            print(f"Send data`{payload}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1



def run():
    client = connect_mqtt()
    client.loop_start() #5
    print(f"connect to broker {broker_address}:{broker_port}")
    publish(client) #6

if __name__ == '__main__':
    run()
# #1 broker 정보 입력하기
# RabbitMQ를 docker로 띄운 상태입니다.
# 포트 포워딩을 통해서 local의 1883을 docker의 1883으로 연결했습니다.
# #4에서 client를 broker로 연결합니다.

#2 client 생성
# Client 생성자는 4개의 파라미터를 받습니다. 여기서 client_id는 필수값이고, 또한 유니크한 값이여야합니다.
# Client(client_id=”Topic”, clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)