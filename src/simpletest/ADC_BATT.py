"""
배터리 전압(GP27, BAT_DIV)을 2초마다 읽는 코드

GP27에는 배터리 전압이 저항 분배기를 거쳐 들어옵니다.
ADC가 읽는 최대 전압은 3.3V이고, 분배비만큼 곱해야 실제 배터리 전압이 됩니다.
DIVIDER_RATIO 값은 보드의 저항값에 맞추어 조정하세요. (1/2 분배면 2.0)
"""

from machine import ADC
from time import sleep

adc = ADC(27)

ADC_REF = 3.3           # ADC 기준 전압 [V]
DIVIDER_RATIO = 2.0     # 저항 분배비 (실제 전압 = 측정 전압 x 이 값)

while True:
    reading = adc.read_u16()                            # 0 ~ 65535
    voltage = reading * (ADC_REF / 65535) * DIVIDER_RATIO
    print("raw: {:5d}   battery: {:5.3f} V".format(reading, voltage))
    sleep(2)
