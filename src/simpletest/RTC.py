"""
실시간 시계(DS3231, I2C 0x68)의 시간을 읽어 Pico 내부 RTC와 비교하는 코드
"""

from machine import Pin, I2C, RTC
import utime as time

from ds3231_port import DS3231

rtc = RTC()

# Pico 내부 RTC의 현재 시간 출력
print()
print(rtc.datetime())

# DS3231 연결 (GP4 = SDA, GP5 = SCL)
print("Syncing with DS3231")
i2c = I2C(0, sda=Pin(4), scl=Pin(5))

ds3231 = DS3231(i2c)        # DS3231 객체 생성

print("Initial values")
print("DS3231 time:", ds3231.get_time())
print("RTC time:   ", time.localtime())

# 내부 RTC 시간을 DS3231에 기록하고 싶으면 아래 주석을 해제하고 실행
# ds3231.save_time()
# print('DS3231 time:', ds3231.get_time())

# DS3231과 내부 RTC의 오차를 확인하고 싶으면 아래 주석을 해제하고 실행 (2분 소요)
# print('Running RTC test for 2 mins')
# print('RTC leads DS3231 by', ds3231.rtc_test(120, True), 'ppm')
