import network
import time

from get_wifi import setup_mode
from phew import access_point, connect_to_wifi, is_connected_to_wifi, dns, server
from phew.template import render_template
from tools.allocations import print_mem, print_storage
import json
import machine
import os
import utime
import _thread

print_mem()
print_storage()

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

SLEEP_TIME = 5 # 일단은 디버깅 쉽게 1초로 설정
EMERGENCY_TIME = 10
boot_time = time.time()
time_disconnected = 0

with open('log.txt', 'w') as f:
    f.write('Boot Time : ' + str(boot_time))
    f.write('\n')
f.close()
 

while True:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_ID, WIFI_PWD)
    print_mem()
    print_storage()
    print(wlan.isconnected() , wlan.status())
    if not wlan.isconnected() and wlan.status() != 0 and time_disconnected < EMERGENCY_TIME: #diconnected state
        print("Disconnected state")
        print(time_disconnected)
        time_disconnected += 5
        with open('log.txt', 'a') as f:
            f.write('Disconnected state: ' + str(time_disconnected))
            f.write('\n')
        f.close()
        time.sleep(SLEEP_TIME)
        
    elif wlan.isconnected() and wlan.status() >= 0: # normal state
        print("Connected state")
        if time_disconnected:
            time_disconnected = 0
        # with open('log.txt', 'a') as f:
        #     f.write('Connected state: ' + str(time_disconnected))
        #     f.write('\n')
        # f.close()
        print(wlan.ifconfig())
        time.sleep(SLEEP_TIME)
         
    elif time_disconnected >= EMERGENCY_TIME: # emergency state
        print('Emgergeny state')
        time_disconnected += 5
        with open('log.txt', 'a') as f:
            f.write('Disconnected state: ' + str(time_disconnected))
            f.write('\n')
        f.close()
        time.sleep(SLEEP_TIME)
        
    
