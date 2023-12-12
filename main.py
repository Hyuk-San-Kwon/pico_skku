import network
import time

from LCD_2 import LCD_2inch
from get_wifi import setup_mode
from phew import server
from tools.allocations import print_mem
from machine import Timer

import gc
import json
import os
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
    LCD.firebase()
    gc.collect()
    LCD.num = True
    
    return LCD
def polling_timer(LCD): #Polling 되었을 시 화면 켜기
    # if not wlan.isconnected(): #Floating point 방지
    LCD.fill(LCD.WHITE)
    LCD.show()
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

SLEEP_TIME = 1 # 일단은 디버깅 쉽게 1초로 설정
EMERGENCY_TIME = 2

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_ID, WIFI_PWD)
time.sleep(2)


print(wlan.isconnected())
url = "https://embeded-system-e8163-default-rtdb.firebaseio.com/"
phone_number = "01020515928"


gc.collect()
LCD = LCD_init()
lcd_timer=None

boot_time = time.time()
time_disconnected = 0
gc.collect()


while True:
    
    gc.collect()
    print_mem()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_ID, WIFI_PWD)
    
    try:
        phone_number = urequests.get(url+"/embeded_system/phone.json").json()
        time.sleep(1)
    except:
        print("Don't get phone number")
    
    print(phone_number)

    if not wlan.isconnected() and wlan.status() != 0 and time_disconnected < EMERGENCY_TIME: #diconnected state
        print("Disconnected state")
        time_disconnected += 5   
        print(time_disconnected)
        time.sleep(SLEEP_TIME)
        
    elif wlan.isconnected() and wlan.status() >= 0: # normal state
        print("Connected state")
        LCD.num = False
        LCD.fill(LCD.BLACK)
        LCD.show()
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
     
        if not lcd_timer:
            lcd_timer = Timer(period=5000,mode=Timer.ONE_SHOT,callback=polling_timer(LCD))
        if phone_number:
            print(phone_number)
            for i, number in enumerate(phone_number):  #렌즈 있을 때 
                x = (285-((i % 6) * 50 + 15) if i<6 else 280-((i % 6) * 50 + 15))
                y = ((0 if i < 6 else 1)) * (90 + 15) + 5
                LCD.draw_number(number, x, y, LCD.BLACK)
            
            LCD.show()
        time_disconnected += 5
        time.sleep(SLEEP_TIME)
        