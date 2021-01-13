#!/usr/bin/env python3
# coding: utf-8

import os
import glob
import time
import paho.mqtt.client as mqtt

###### Edit variables to your environment #######
broker_address = "test.mosquitto.org"     #MQTT broker_address :192.168.0.31
Topic = "takeda"

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

print("creating new instance")
client = mqtt.Client("pub5") #create new instance

print("connecting to broker")
client.connect(broker_address) #connect to broker

# 生の温度データを取得する関数
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# 温度データのみを取り出して返す関数
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def loop():
    while True:
        d = read_temp()
        print ('室温: %s ℃' % d)
        client.publish(Topic, d)
        time.sleep(2)

if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        print ('The end !!')
