"""
부저(GP22)를 1초 동안 울리는 코드
"""

from machine import Pin, PWM
from utime import sleep

# GP22번 핀에 연결된 부저를 PWM(Pulse Width Modulation) 모드로 설정합니다.
buzzer = PWM(Pin(22))

# 부저의 주파수를 500Hz로 설정합니다. 이것은 부저가 내는 소리의 톤을 결정합니다.
buzzer.freq(500)

# 듀티 사이클을 설정하여 소리를 활성화합니다. duty_u16 값은 0에서 65535 사이입니다.
buzzer.duty_u16(1000)

sleep(1)                # 1초 동안 소리를 냅니다.

buzzer.duty_u16(0)      # 듀티 사이클을 0으로 만들어 소리를 끕니다.
buzzer.deinit()         # PWM을 해제합니다.
