from machine import Pin, I2C
import network
import time
import urequests
import random

# WLAN 객체를 생성하고, 무선 LAN을 활성화합니다
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# 와이파이에 연결합니다
if not wlan.isconnected():
    wlan.connect("AndroidHotspot", "minakusi12400")
    print("Waiting for Wi-Fi connection", end="...")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
else:
    print(wlan.ifconfig())
    print("WiFi is Connected")

print("Wifi is connected")
# Firebase의 Realtime Database와 연결하기 위한 URL을 설정합니다
url = "https://embeded-system-e8163-default-rtdb.firebaseio.com/"

# 초기 상태를 설정하여 Firebase에 업데이트합니다
초기값 = {'phone': "0",}
urequests.patch(url+"/embeded_system.json", json = 초기값).json()

phone_number = "0"

# 무한 루프를 실행하면서 Firebase에서 데이터를 계속 가져옵니다.
while True:
    response = urequests.get(url+"/embeded_system.json").json()
    time.sleep(0.1)
    if (phone_number != response['phone']): # 값이 바뀌었을 때만 phone number 업데이트
        phone_number = response['phone']
        print(phone_number)