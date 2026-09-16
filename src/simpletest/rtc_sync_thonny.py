"""PC 시각을 Thonny Shell에 붙여넣을 MicroPython 명령으로 출력합니다.

사용법:
    1) python rtc_sync_thonny.py 실행
    2) 출력된 한 줄을 복사
    3) Thonny에서 Pico에 연결한 상태로 Shell 탭에 붙여넣고 Enter

사전 조건: 보드의 lib/ 에 ds3231_port.py 가 올라가 있어야 합니다.
"""
import datetime

now = datetime.datetime.now()
# MicroPython RTC 요일: 0=월 ~ 6=일 / Python weekday(): 0=월 ~ 6=일 (동일)
y, mo, d, wd, h, mi, s = now.year, now.month, now.day, now.weekday(), now.hour, now.minute, now.second

cmd = (
    "from machine import RTC, Pin, I2C; from ds3231_port import DS3231; "
    f"RTC().datetime(({y}, {mo}, {d}, {wd}, {h}, {mi}, {s}, 0)); "
    "ds = DS3231(I2C(0, sda=Pin(4), scl=Pin(5))); ds.save_time(); "
    "print('DS3231 time:', ds.get_time())"
)

print(f"PC 시각: {y}-{mo:02d}-{d:02d} {h:02d}:{mi:02d}:{s:02d}")
print()
print("아래 줄을 복사해서 Thonny Shell에 붙여넣으세요:")
print()
print(cmd)
