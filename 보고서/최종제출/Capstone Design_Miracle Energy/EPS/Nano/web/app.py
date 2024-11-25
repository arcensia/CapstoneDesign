from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response
import pymysql

#import paho.mqtt.client as mqtt

app = Flask(__name__)


#mqttc = mqtt.C



def takedb(tablename, col): #데이터베이스의 마지막 행 데이터를 가져오기 위한 함수
    con = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='TESTDB',
                       charset='utf8')

    cur=con.cursor()

    sql="select %s from %s order by seq desc LIMIT 1"%(col, tablename)
    cur.execute(sql)
    last = cur.fetchone()
    for last in last:
        return last
    con.close()

def dd():
    return takedb('Asensertable','gas')  
    
@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')


#@app.route('/data', methods=["GET", "POST"])
#def data():
    # Data Format
    # [TIME, Temperature, Humidity]

 #   Temperature = random() * 100
  #  Humidity = random() * 55

   # data = [time() * 1000, Temperature, Humidity]

    #response = make_response(json.dumps(data))

    #response.content_type = 'application/json'

#    return responseRR

@app.route('/live-data')
def live_data1():
    # PHP 배열 작성 및 JSON으로 출력
    data = [(time()+32400) * 1000 ,takedb("Asensertable", "Acurrent"), dd(),int(takedb("Asensertable", "Acurrent"))*takedb("Asensertable", "volt")] #(time()+32400) = 한국 표준시 맞춤
    # data = [(time()+32400) * 1000, takedb("CURRENT"), takedb("VOLTAGE")]
    print(data)
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/image', methods=['GET', 'POST'])
def homePage():
    return render_template("index2.html", image_file='s1.png')



if __name__ == "__main__":
    app.run(debug=True)
