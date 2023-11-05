import network
import time
import os

WIFI_ID = 'KT_GIGA_5G_718E'
WIFI_PWD = '34dk16jg15'
SLEEP_TIME = 1 # 일단은 디버깅 쉽게 1초로 설정

boot_time = time.time()
time_disconnected = 0

with open('log.txt', 'w') as f:
    f.write('Boot Time : ' + str(boot_time))
    f.write('\n')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_ID, WIFI_PWD)

while True:

    if not wlan.isconnected() and wlan.status() >= 0: #diconnected state
        print("Disconnected state")
        if not time_disconnected:
            time_disconnected = time.time() - boot_time
        with open('log.txt', 'a') as f:
            f.write('Disconnected state: ' + str(time.time() - boot_time))
            f.write('\n')
        time.sleep(SLEEP_TIME)
    if time_disconnected - time.time() > 500: # emergency state
        print('Emgergeny state')
        with open('log.txt', 'a') as f:
            f.write('Disconnected state: ' + str(time.time() - boot_time))
            f.write('\n')
        time.sleep(SLEEP_TIME)
    else: # normal state
        print("Connected state")
        if time_disconnected:
            time_disconnected = 0
        with open('log.txt', 'a') as f:
            f.write('Connected state: ' + str(time.time() - boot_time))
            f.write('\n')
        print(wlan.ifconfig())
        time.sleep(SLEEP_TIME)