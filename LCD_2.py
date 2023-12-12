
from machine import Pin,SPI,PWM,Timer
import framebuf
import time
import os
import gc
##################### FIREBASE ########################
import network
import urequests

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

'2inch frames'
class LCD_2inch(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 320
        self.height = 200
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        self.bl =Pin(BL,Pin.OUT)
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,1000_000_00,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width*2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.RED   =   0x07E0
        self.GREEN =   0x001F
        self.BLUE  =   0xF800
        self.WHITE =   0xffff
        self.BLACK =   0x0000
        
        self.num = True



# Example usage:  # Assuming this is your LCD object

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)
        
        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x3f)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
    def draw_number(self, num, x, y, color):
        # 숫자별 사각형 정의 (크기 조정)
       numbers = {
    '0': [(x, y + 72, 45, 18), (x + 35, y, 10, 90), (x, y, 10, 90), (x, y, 45, 18)],
    '1': [(x + 18, y, 10, 90)],
    '2': [(x, y + 72, 45, 18), (x, y + 18, 10, 36), (x, y + 36, 45, 18), (x + 35, y + 54, 10, 36), (x, y, 45, 18)],
    '3': [(x, y + 72, 45, 18), (x, y, 10, 90), (x, y + 36, 45, 18), (x, y, 45, 18)],
    '4': [(x + 35, y, 10, 54), (x, y + 36, 45, 18), (x, y, 10, 90)],
    '5': [(x, y + 72, 45, 18), (x + 35, y + 18, 10, 36), (x, y + 36, 45, 18), (x, y + 36, 10, 54), (x, y, 45, 18)],
    '6': [(x, y + 72, 45, 18), (x + 35, y, 10, 90), (x, y + 36, 45, 18), (x, y + 36, 10, 54), (x, y, 45, 18)],
    '7': [(x, y, 45, 18), (x, y, 10, 90)],
    '8': [(x, y + 72, 45, 18), (x + 35, y, 10, 90), (x, y, 10, 90), (x, y + 36, 45, 18), (x, y, 45, 18)],
    '9': [(x, y + 72, 45, 18), (x + 35, y, 10, 54), (x, y, 10, 90), (x, y + 36, 45, 18), (x, y, 45, 18)],
    '-': [(x + 25, y + 35, 20, 10)]
    }#렌즈를 쓸때->USB 포트가 오른쪽으로 가야함. '''


       for rect in numbers.get(num, []):
            self.fill_rect(*rect, color)
            
    def polling_timer(timer,self): #Polling 되었을 시 화면 켜기
        if not wlan.isconnected(): #Floating point 방지
            LCD.fill(LCD.WHITE)
            LCD.show()

    def wifi_check(self):

        # 와이파이에 연결합니다
        if not wlan.isconnected():
            wlan.connect("AndroidHotspot", "12345678") # 와이파이 정보 입력
            print("Waiting for Wi-Fi connection", end="...")
            while not wlan.isconnected():
                gc.collect()
                wlan.connect("AndroidHotspot", "12345678") # 와이파이 정보 입력
                print(".", end="")
                time.sleep(10)#Pico wifi delay=10~11초   
                if wlan.isconnected()==True:
                    break
        else:
            print(wlan.ifconfig())
            print("WiFi is Connected")
    def firebase(self):  #서버 통신 조절
        '''url = "https://embeded-system-e8163-default-rtdb.firebaseio.com/"'''
        gc.collect()#
        pwm = PWM(Pin(BL))
        pwm.freq(1000)
        pwm.duty_u16(32768)#max 65535
    
        
if __name__=='__main__':
    # WLAN 객체를 생성하고, 무선 LAN을 활성화합니다
    gc.collect()
    LCD = LCD_2inch()
    LCD.fill(LCD.BLACK)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    LCD.wifi_check()
    LCD.firebase()
    lcd_timer=None
    phone_number = urequests.get(url+"/embeded_system/phone.json").json()
    gc.collect()
    num=True
    while(1):
        print("return")
        while wlan.isconnected():
            num= not num
            LCD.fill(LCD.BLACK) #화면 초기화
            
            print("off now")
            time.sleep(5)
            print("don't off now")#이때 wifi 끌 시 Floating Point err
            time.sleep(11)
            
            if not wlan.isconnected():
                break
            
            gc.collect()
            if wlan.isconnected():
                phone_number=None #필수) 메모리 문제로 매번 초기화.
                response= urequests.get(url+"/embeded_system/phone.json").json()#번호 받아오기
                phone_number = response #업데이트
                gc.collect()
                urequests.patch(url+"/embeded_system.json", json ={'state':num }).json()
                #state의 값이 주기마다 달라질경우: connect// 아닐경우: disconnect
                
            if lcd_timer:
                 lcd_timer.deinit()  # 타이머 중지
                 lcd_timer = None
            LCD.fill(LCD.BLACK) #첫 루프때 화면 초기화 안되기에 다시 해줌. 
            LCD.show()
        time.sleep(7)
        if not wlan.isconnected():
            print("no wifi loop")
            if not lcd_timer:
                print("Go here")
                lcd_timer=Timer(period=5000,mode=Timer.ONE_SHOT,callback=LCD.polling_timer)
        for i, number in enumerate(phone_number):  #렌즈 있을 때 
            x = (310-((i % 6) * 50 + 15) if i<6 else 280-((i % 6) * 50 + 15))
            y = ((0 if i < 6 else 1)) * (90 + 20) + 10
            LCD.draw_number(number, x, y, LCD.BLACK)
        print("Final loop")
        LCD.show()
        time.sleep(5)
    
        
        







