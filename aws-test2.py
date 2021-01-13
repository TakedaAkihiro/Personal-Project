#!/usr/bin/env python3
# coding: utf-8

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import os
import glob
from time import sleep
import datetime as dt

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

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

# 初期化
myMQTTClient = AWSIoTMQTTClient("Raspberry_Pi")

# MQTTクライアントの設定
myMQTTClient.configureEndpoint("a1zgqp33rfoox1-ats.iot.ap-northeast-1.amazonaws.com", 443)
myMQTTClient.configureCredentials("/home/pi/Parsonar-Project/Personal-Project/cert/AmazonRootCA1.pem", "/home/pi/Parsonar-Project/Personal-Project/cert/af5b640a0a-private.pem.key", "/home/pi/Parsonar-Project/Personal-Project/cert/af5b640a0a-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5000)


try:
# Connect to AWS IoT endpoint
    myMQTTClient.connect()
    print ("Connected to AWS IoT")

    while True:
        print(read_temp())
        temp = read_temp()
        now = dt.datetime.now()

#publish a message
        message = {"temperature":temp,
                   "sk_date":"{0:%Y-%m-%d}".format(now),
                   "sk_time":"{0:%H:%M:%S}".format(now),
                   "microsecond":now.microsecond}
        myMQTTClient.publish("awsiot/test", json.dumps(message), 0)
        sleep(1)

except KeyboardInterrupt:
    myMQTTClient.disconnect()
    pass
