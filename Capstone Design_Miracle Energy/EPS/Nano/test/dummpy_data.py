
#import serial
import time
import schedule
import csv
import numpy as np
import datetime
from datetime import date
import pandas as pd
import os
from os import path
import math

#import numpy as np
from time import sleep

def genSine(f0, fs, dur):
    t = np.arange(dur)
    sinusoid = np.sin(2*np.pi*t*(f0/fs))
    sinusoid = normalise(sinusoid,MAX_INT16)
    return sinusoid

def genNoise(dur):
    noise = np.random.normal(0,1,dur)
    noise = normalise(noise,MAX_INT16)
    return noise

def normalise(x,MAX_INT16):
    maxamp = max(x)
    amp = math.floor(MAX_INT16/maxamp)
    norm = np.zeros(len(x))
    for i in range(len(x)):
        norm[i] = amp*x[i]
    return norm

def myreadline():
	global n
	n+=1
#	'x'.join((str(n) for n in l))
	
	
	return ','.join([ str(cons[n]), str(iv[n]), str(ia[n]) ])

def main_func():
    now = datetime.datetime.now()
    today = now.year
    week = now.isocalendar()[1]
    data=[]
    df=[]

    #arduino = serial.Serial('/dev/ttyACM0', 9600)
    print('Establishing serial connection with Arduino...')
    #arduino_data = arduino.readline()
    arduino_data = myreadline()

    #print(arduino_data)
    decoded_values = str(arduino_data[0:len(arduino_data)])
    #decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
    list_values = decoded_values.split('x')
    #print(list_values)

    for item in list_values:
        #print(item)
        list_in_floats.append(float(item))

    print(f'Collected readings from Arduino: {list_in_floats[0]}[W] {list_in_floats[1]}[V_ac] {list_in_floats[2]}[I_ac] ')
    time_stamp=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    print(f'Time stamp: {time_stamp}')
    if path.exists('data_'+str(today)+'W'+str(week)+'.csv') == True:
        data.append([time_stamp, list_in_floats[0],list_in_floats[1],list_in_floats[2]])
        node = pd.DataFrame(data, columns=['Time stamp','Active power consumed [W]','Voltage AC [V_ac]','Current AC [I_ac]'])
        node.to_csv('data_'+str(today)+'W'+str(week)+'.csv', index = None,  mode='a', header=False)
    else:
        data.append([time_stamp, list_in_floats[0],list_in_floats[1],list_in_floats[2]])
        node = pd.DataFrame(data, columns=['Time stamp','Active power consumed [W]','Voltage AC [V_ac]','Current AC [I_ac]'])
        node.to_csv('data_'+str(today)+'W'+str(week)+'.csv', index = None)

    print('Data saved in csv file')
    arduino_data = 0
    list_in_floats.clear()
    list_values.clear()
    data.clear()
    #arduino.close()
    print('Connection closed')
    print('<--------------------------------------------------------------------------->')


# ----------------------------------------Main Code------------------------------------
# Declare variables to be used
list_values = []
list_in_floats = []

n = -1
#noise1 = np.random.normal(0,1,100) # mean, stdev, num#
#noise2 = np.random.normal(0,1,100) # mean, stdev, num#
#noise3 = np.random.normal(0,1,100) # mean, stdev, num#

#iv = [200] * 100 * noise2
#ia = [20] * 100 * noise3
#cons = iv * ia

f0 = 44
fs = 10000
dur = 1*fs                      #seconds
global MAX_INT16
MAX_INT16 = 50
#sinusoid1 = genSine(f0,fs,dur)
noise = genNoise(dur)

MAX_INT16 = 10
iv = genSine(f0,fs,dur) + 220

MAX_INT16 = 5
ia = genSine(f0,fs,dur) + 10

cons = iv* ia

#print(sinusoid1)
#print(sinusoid2)
#print(sinusoid3)
#print(sinusoid1.shape)
#print(noise.shape)

print('Program started')

# Setting up the Arduino

time_stamp1=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
a = datetime.datetime(2022, 5, 11, 17, 11, 0)

for i in range(1, 10001): 
	a = a + datetime.timedelta(0,1)
	time_stamp1=str(a.strftime("%Y-%m-%d %H:%M:%S"))
	print(time_stamp1, ',',myreadline(), sep="")