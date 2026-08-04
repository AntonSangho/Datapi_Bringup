"""
부저(GP22)로 간단한 멜로디(도레미파솔라시도)를 연주하는 코드
"""

from machine import Pin, PWM
from utime import sleep

buzzer = PWM(Pin(22))

# 음이름과 주파수(Hz) 표
NOTES = {
    "C4": 262, "D4": 294, "E4": 330, "F4": 349,
    "G4": 392, "A4": 440, "B4": 494, "C5": 523,
}

# (음이름, 길이[초]) 순서로 연주합니다.
MELODY = [
    ("C4", 0.3), ("D4", 0.3), ("E4", 0.3), ("F4", 0.3),
    ("G4", 0.3), ("A4", 0.3), ("B4", 0.3), ("C5", 0.6),
]


def play(note, duration):
    buzzer.freq(NOTES[note])
    buzzer.duty_u16(1000)       # 소리 켜기
    sleep(duration)
    buzzer.duty_u16(0)          # 소리 끄기
    sleep(0.05)                 # 음과 음 사이를 살짝 띄웁니다.


for note, duration in MELODY:
    print(note)
    play(note, duration)

buzzer.deinit()
