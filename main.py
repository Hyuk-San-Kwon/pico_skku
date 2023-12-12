import network
import time

from LCD_2 import LCD_2inch
from get_wifi import setup_mode
from phew import access_point, connect_to_wifi, is_connected_to_wifi, dns, server
from phew.template import render_template
from tools.allocations import print_mem
from machine import Timer

import gc
import json
import machine
import os
import utime
import _thread
import urequests

print_mem()

AP_NAME = "pi pico"
AP_DOMAIN = "pipico.net"
AP_TEMPLATE_PATH = "ap_templates"
APP_TEMPLATE_PATH = "app_templates"
WIFI_FILE = "wifi.json"
WIFI_MAX_ATTEMPTS = 3


def LCD_init():
    gc.collect()
    LCD = LCD_2inch()
    LCD.fill(LCD.BLACK)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    LCD.wifi_check()
    LCD.firebase()
    gc.collect()
    LCD.num = True
    
    return LCD

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
BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_ID, WIFI_PWD)

LCD = LCD_init()
lcd_timer=None

url = "https://embeded-system-e8163-default-rtdb.firebaseio.com/"
phone_number = 0
phone_number = urequests.get(url+"/embeded_system/phone.json").json()

boot_time = time.time()
time_disconnected = 0



while True:
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_ID, WIFI_PWD)

    if not wlan.isconnected() and wlan.status() != 0 and time_disconnected < EMERGENCY_TIME: #diconnected state
        print("Disconnected state")
        print(time_disconnected)
        time_disconnected += 5
        if not lcd_timer:
            lcd_timer = Timer(period=5000,mode=Timer.ONE_SHOT,callback=LCD.polling_timer)
        for i, number in enumerate(phone_number):  #렌즈 있을 때 
            x = (310-((i % 6) * 50 + 15) if i<6 else 280-((i % 6) * 50 + 15))
            y = ((0 if i < 6 else 1)) * (90 + 20) + 10
            LCD.draw_number(number, x, y, LCD.BLACK)
        LCD.show()
        time.sleep(SLEEP_TIME)
        
    elif wlan.isconnected() and wlan.status() >= 0: # normal state
        print("Connected state")
        LCD.num = False
        LCD.fill(LCD.BLACK)
        print("LCD off")
        
        if time_disconnected:
            time_disconnected = 0
        time.sleep(SLEEP_TIME)
        gc.collect()     
        if lcd_timer:
            lcd_timer.deinit()  # 타이머 중지
            lcd_timer = None   
        LCD.fill(LCD.BLACK) #첫 루프때 화면 초기화 안되기에 다시 해줌. 
        LCD.show()
    
    elif time_disconnected >= EMERGENCY_TIME: # emergency state
        print('Emgergeny state')
        time_disconnected += 5
        time.sleep(SLEEP_TIME)
        
    
