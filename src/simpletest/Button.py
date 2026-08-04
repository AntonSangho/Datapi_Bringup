"""
버튼(GP20)을 누르면 LED가 꺼지고, 누르지 않으면 LED가 켜지는 의사코드

1. LED 핀 설정
2. 버튼 핀 설정
3. 무한 루프
    4. 버튼의 상태 확인
    5. 버튼이 눌렸을 때 LED 끄기
    6. 버튼이 눌리지 않았을 때 LED 켜기
    7. 0.1초 대기
"""

from machine import Pin
import utime

led = Pin("LED", Pin.OUT)

# GP20에 연결된 버튼(SW1)을 입력 모드로 설정합니다. 내부 풀업 저항을 활성화합니다.
button = Pin(20, Pin.IN, Pin.PULL_UP)

# 무한 루프를 통해 버튼의 상태를 지속적으로 확인하고 LED를 제어합니다.
while True:
    # button의 상태를 출력합니다. (눌렸을 때 0, 눌리지 않았을 때 1)
    print(button.value())

    if button.value() == 0:
        led.value(False)
    else:
        led.value(True)

    utime.sleep(0.1)    # 0.1초마다 반복합니다.
