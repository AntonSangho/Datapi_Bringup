"""
보드 내장 LED를 0.5초 간격으로 깜박이는 의사 코드

1. LED 핀 설정
2. 무한 루프
    3. LED 켜기
    4. 0.5초 대기
    5. LED 끄기
    6. 0.5초 대기
"""

from machine import Pin
import utime                    # 시간 관련 라이브러리

# Pico W의 내장 LED는 무선 칩에 연결되어 있어 번호 대신 "LED" 이름을 사용합니다.
led = Pin("LED", Pin.OUT)

while True:                     # 무한 루프
    led.value(1)                # LED 켜기
    utime.sleep(0.5)            # 0.5초 대기
    led.value(0)                # LED 끄기
    utime.sleep(0.5)            # 0.5초 대기
