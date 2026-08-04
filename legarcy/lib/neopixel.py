from machine import Pin
import time
from neopixel import NeoPixel

np0 = NeoPixel(Pin(21), 1)

def np_on():
    for i in range(0, np0.n):
        np0[i] = (255,0,0)
    np0.write()
def np_off():
    for i in range(0, np0.n):
        np0[i] = (0,0,0)
    np0.write()

while True:
    # 네오픽셀 켜기
    np_on()
    time.sleep(1)
    # 네오픽셀 끄기
    #np_off()
    #time.sleep(1)