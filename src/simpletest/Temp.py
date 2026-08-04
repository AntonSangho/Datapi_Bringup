"""
온습도 센서(AHT20, I2C 0x38)로 온도와 습도를 1초마다 읽는 코드

v0.2에서는 OneWire 방식의 DS18B20을 사용했지만,
v0.3에서는 I2C 방식의 AHT20으로 바뀌었습니다. (GP4=SDA, GP5=SCL)
"""

from machine import Pin, I2C
from utime import sleep

from aht20 import AHT20

i2c0 = I2C(0, sda=Pin(4), scl=Pin(5))

aht20 = AHT20(i2c0)

while True:
    temperature, humidity = aht20.measure()
    print("temperature: {:6.2f} C   humidity: {:6.2f} %".format(temperature, humidity))
    sleep(1)
