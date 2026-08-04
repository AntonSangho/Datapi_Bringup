#!/bin/bash
# PC의 현재 시각을 Pico 내부 RTC와 DS3231에 기록합니다.
#
# v0.2의 RTC_Sync.py는 WiFi + NTP를 사용했지만(mywifi.py 필요),
# 이 스크립트는 PC 시각을 그대로 쓰므로 네트워크 설정이 필요 없습니다.
#
# 사용법: ./rtc_sync.sh
# 사전 조건: 보드의 :lib/ 에 ds3231_port.py 가 올라가 있어야 합니다.

set -e

# 앞자리 0이 붙으면 파이썬이 8진수로 오해하므로 %-m 처럼 0을 제거합니다.
NOW=$(date '+%Y,%-m,%-d,%-H,%-M,%-S,%u')
echo "PC 시각: $NOW"

mpremote exec "
from machine import RTC, Pin, I2C
from ds3231_port import DS3231

y, mo, d, h, mi, s, wd = $NOW

# MicroPython RTC의 요일은 0=월 ~ 6=일, date +%u는 1=월 ~ 7=일
RTC().datetime((y, mo, d, wd % 7, h, mi, s, 0))

ds = DS3231(I2C(0, sda=Pin(4), scl=Pin(5)))
ds.save_time()          # 내부 RTC 시간을 DS3231에 기록

print('DS3231 time:', ds.get_time())
print('DS3231 temp:', ds.get_temperature())
"
