#!/usr/bin/env python3
# coding: utf-8

import os
import glob
from time import sleep
from flask import Flask

app = Flask(__name__)

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

@app.route('/')
def mainmenu():
    PIval = read_temp()
    return """
    <html><body>
    <center><h1>現在の室温をお知らせいたします！<br/>
        <h2><u>現在：{0}℃<br>
    </center>
    </body></html>
    """.format(PIval)

if __name__ == "__main__":
        app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))


try:
    while True:
        pass

except KeyboardInterrupt:
            print ('Cleanup ADC and end!')
