import network
import time
import os

WIFI_ID = 'KT_GIGA_5G_718E'
WIFI_PWD = '34dk16jg15'
SLEEP_TIME = 1 # 일단은 디버깅 쉽게 1초로 설정
EMERGENCY_TIME = 10

boot_time = time.time()
time_disconnected = 0

with open('log.txt', 'w') as f:
    f.write('Boot Time : ' + str(boot_time))
    f.write('\n')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_ID, WIFI_PWD)

while True:
    print(wlan.isconnected(), wlan.status())
    if not wlan.isconnected() and wlan.status() != 0 and time_disconnected < EMERGENCY_TIME: #diconnected state
        print("Disconnected state")
        print(time_disconnected)
        time_disconnected += 1
        with open('log.txt', 'a') as f:
            f.write('Disconnected state: ' + str(time_disconnected))
            f.write('\n')
        time.sleep(SLEEP_TIME)
    elif time_disconnected >= EMERGENCY_TIME: # emergency state
        print('Emgergeny state')
        time_disconnected += 1
        with open('log.txt', 'a') as f:
            f.write('Disconnected state: ' + str(time_disconnected))
            f.write('\n')
        time.sleep(SLEEP_TIME)
    elif wlan.isconnected() and wlan.status() == 0: # normal state
        print("Connected state")
        if time_disconnected:
            time_disconnected = 0
        with open('log.txt', 'a') as f:
            f.write('Connected state: ' + str(time_disconnected))
            f.write('\n')
        print(wlan.ifconfig())
        time.sleep(SLEEP_TIME)
