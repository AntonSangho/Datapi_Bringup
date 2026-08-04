"""
조도 센서(BH1750, I2C 0x23)로 밝기(lux)를 1초마다 읽는 코드
"""

from machine import Pin, I2C
from utime import sleep

from bh1750 import BH1750

# DataPi v0.3 핀 배치: GP4 = SDA, GP5 = SCL
i2c0 = I2C(0, sda=Pin(4), scl=Pin(5))

bh1750 = BH1750(0x23, i2c0)

while True:
    print("lux:", bh1750.measurement)
    sleep(1)
