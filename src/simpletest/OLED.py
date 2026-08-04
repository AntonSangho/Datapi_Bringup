"""
OLED(SSD1306, I2C 0x3C)에 텍스트를 표시하는 코드

OLED는 다른 I2C 센서(BH1750 / AHT20 / DS3231)와 같은 I2C0 버스를 공유합니다.
    GP4 = SDA, GP5 = SCL

1. I2C / OLED 초기화
2. 텍스트 리스트를 줄 단위로 출력하는 함수 정의
3. 무한 루프
    4. 버튼(GP20)이 눌리면 START 화면, 떼어지면 READY 화면 표시
"""

from machine import Pin, I2C
from utime import sleep

import ssd1306

OLED_WIDTH = 128
OLED_HEIGHT = 64
OLED_ADDR = 0x3C

# 400kHz fast mode로 I2C0을 초기화합니다. (OLED는 화면 전송량이 많아 빠른 편이 좋습니다)
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

try:
    oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=OLED_ADDR)
except Exception as e:
    print("OLED 초기화 실패:", e)
    raise SystemExit

button = Pin(20, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT)

LINE_HEIGHT = 16    # 기본 폰트는 8px이지만 줄 간격을 두어 16px 단위로 출력합니다.


def display_text(text_list):
    """주어진 리스트의 텍스트를 OLED에 라인별로 출력합니다."""
    oled.fill(0)                        # 화면 전체를 지웁니다.

    for i, line_text in enumerate(text_list):
        y_pos = i * LINE_HEIGHT

        if y_pos >= OLED_HEIGHT:        # 화면을 넘어가는 줄은 출력하지 않습니다.
            break

        oled.text(line_text, 0, y_pos)  # (텍스트, X좌표, Y좌표)

    oled.show()                         # 디스플레이에 반영합니다.


TEXT_PRESSED = [
    "|==============|",
    "START SENSING",
    "RPI PICO W",
]

TEXT_READY = [
    "<  DataPi v0.3 >",
    "READY",
    "Press the button",
    "(GP20)",
]

print("OLED 및 버튼 대기 중...")

while True:
    if button.value() == 0:     # 버튼 눌림 (0 = 눌림)
        led.value(False)
        display_text(TEXT_PRESSED)
    else:
        led.value(True)
        display_text(TEXT_READY)

    sleep(0.1)
