"""
네오픽셀(WS2812B, GP21)의 색을 바꾸는 의사코드

1. 네오픽셀 핀 설정
2. 색을 채우는 함수 정의
3. 무한 루프
    4. 빨강 -> 초록 -> 파랑 -> 끄기 순서로 1초씩 표시
"""

from machine import Pin
import time
from neopixel import NeoPixel

# GP21에 연결된 네오픽셀 1개를 초기화합니다.
np = NeoPixel(Pin(21), 1)


def fill(color):
    """모든 픽셀을 같은 색(R, G, B)으로 채웁니다."""
    for i in range(np.n):
        np[i] = color
    np.write()          # 실제 LED에 값을 전송합니다.


while True:
    fill((255, 0, 0))   # 빨강
    time.sleep(1)
    fill((0, 255, 0))   # 초록
    time.sleep(1)
    fill((0, 0, 255))   # 파랑
    time.sleep(1)
    fill((0, 0, 0))     # 끄기
    time.sleep(1)
