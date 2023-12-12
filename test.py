import network
import urequests
import time
WIFI_FILE = "wifi.json"

with open(WIFI_FILE) as f:
    wifi_credentials = json.load(f)
f.close()

WIFI_ID = wifi_credentials["ssid"]
WIFI_PWD = wifi_credentials["password"]


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_ID, WIFI_PWD)
i = 0
while i < 10:
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_ID, WIFI_PWD)
    time.sleep(1)
    i += 1


print(wlan.isconnected(), wlan.status())
url = "https://embeded-system-e8163-default-rtdb.firebaseio.com/"
phone_number = "01020515928"


try:
    phone_number = urequests.get(url+"/embeded_system/phone.json").json()
    
except:
    print("Don't get phone number")