작업 환경 Ubuntu 22.04

1. 마이크로 파이썬 설치 -->> https://www.raspberrypi.com/documentation/microcontrollers/micropython.htm

요약 : 마이크로 파이썬 uf2 파일 받아서 드래그드롭 하면 설치 완료

2. vscode에서 micropython 작업 후 피코 실행까지 자동으로 하고 싶으면 하기(선택)

https://randomnerdtutorials.com/raspberry-pi-pico-vs-code-micropython/#flash-micropython

리눅스 보안때문에 포트막혀서 pico 인식 못할시 
https://github.com/paulober/MicroPico/wiki/Linux 
배쉬 파일 실행

근데 이 방법은 pico 파일 내부 자체는 못 보는 듯?
해결되면 따로 공지

3. thonny 설치하기

구글 검색 후 설치

이걸로 하면 pico 내부 파일을 보고 저장가능 
UI가 불편해서 파일 보는데만 쓰는거 추천

## 파일 설명

ble_advertising.py 

--> pico 내부에서 블루투스 통신 하는 헤더파일, 무조건 피코에 넣고 하는거, 근데 저 혼자 작업할거라 굳이 건드릴 필요는 없어요.

get_WIFI_bt.py

--> 외부에서 집어넣어서 하는 파일, 사용자가 처음 사용시 wifi설정이 안되어있는 관계로 블루투스 연결 후 사용(왜냐? 와이파이 연결이 안되서 연결방법이 블루투스밖에 없어서... 사용자가 직접 터미널로 하긴 그러니까..)

핸드폰으로 블루투스 연결후 wifi id, 비번 입력 받게 해서 피코 내부 파일인 pwd.py 에 저장

90% 완성함. 보니까 핸드폰에서 쉘끼리 연결해서 작동하는데 이건 디테일 작업용이라 굳이 안해도 되긴하는데 완성도 높일 목적

blinking.py

--> 피코에 포팅 잘되는지 테스트용. 불들어오면 잘되는거

main.py

--> 일단 3가지 상태 구현 완료. 디버깅 쉽기 위해 sleep time 1초
배터리 절약 위해선 sleep time늘리는 형식이 맞을듯

log.txt에 로그 저장하는 방식. 디버깅 쉽게 하기 위해

WIFI_ID, WIFI_PWD는 추후 블루투스로 입력한 후 가져오게 설계할 예정
지금은 하드코딩하자


그밖에도 pico w documentation 보면 http 통신하고 여러 예제들 있으니 보시면 좋을듯 합니다. 앱 인벤터, firebase 예제도 꽤나 있더라고요. 
