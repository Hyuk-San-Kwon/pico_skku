import time
import network

from get_wifi import setup_mode
from get_KR_time import get_time
from phew import server
from get_gps import getPositionData 
from machine import Pin, UART, I2C

import json
import os
import urequests




AP_NAME = "pi pico"
AP_DOMAIN = "pipico.net"
AP_TEMPLATE_PATH = "ap_templates"
APP_TEMPLATE_PATH = "app_templates"
WIFI_FILE = "wifi.json"
WIFI_MAX_ATTEMPTS = 3


# 와이파이 기록한 json이 있다면 바로 동작
try:
    os.stat(WIFI_FILE)

# 없다면 Access Point 실행 후 사용자에게 WIFI 정보를 받아오게 됨
except Exception:
    # Either no wifi configuration file found, or something went wrong, 
    # so go into setup mode.
    setup_mode()
    # start web server
    server.run()

with open(WIFI_FILE) as f:
    wifi_credentials = json.load(f)
f.close()

WIFI_ID = wifi_credentials["ssid"]
WIFI_PWD = wifi_credentials["password"]
gps_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

get_time()
print(time.localtime())

SLEEP_TIME = 5 # 일단은 디버깅 쉽게 1초로 설정
EMERGENCY_TIME = 10
time_disconnected = 0


url = "https://embeded-system-e8163-default-rtdb.firebaseio.com/"

boot_time = time.localtime()
time_disconnected = 0

with open('log.txt', 'w') as f:
    f.write('Boot Time : ' + str(boot_time))
    f.write('\n')
f.close()

json_object = {}
json_object['Time'] = []
json_object['Latitude'] = []
json_object['Longitude'] = []


with open('log.json', 'w') as f:
    json.dump(json_object, f)
f.close()



while True:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_ID, WIFI_PWD)
    
    json_object['Time'].append(str(time.localtime()))
    
    latitude, longitude = getPositionData(gps_module)
    json_object['Latitude'].append(latitude)
    json_object['Longitude'].append(longitude)
    
    with open('log.json', 'w') as f:
        json.dump(json_object, f)
    f.close()
    
    if not wlan.isconnected() and wlan.status() != 0 and time_disconnected < EMERGENCY_TIME: #diconnected state
        print("Disconnected state")
        time_disconnected += 5
        time.sleep(SLEEP_TIME)
        
    elif wlan.isconnected() and wlan.status() >= 0: # normal state
        print("Connected state")
        if time_disconnected:
            time_disconnected = 0

        urequests.patch(url+"/time_gps.json", json = json_object).json()
        time.sleep(SLEEP_TIME)
         
    elif time_disconnected >= EMERGENCY_TIME: # emergency state
        print('Emgergeny state')
        time_disconnected += 5
        time.sleep(SLEEP_TIME)
        
    
