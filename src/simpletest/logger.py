"""
DataPi v0.3 통합 로깅 예제

DS3231에서 시간을 읽고, AHT20 / BH1750 / 배터리 전압을 측정하여
SD 카드의 log.csv 파일에 한 줄씩 기록합니다.
측정값은 OLED에도 함께 표시하고,
기록할 때마다 네오픽셀을 초록색으로 잠깐 켜서 동작을 알려줍니다.
"""

import machine
import uos
from machine import Pin, I2C, ADC
from utime import sleep

import sdcard
import ssd1306
from neopixel import NeoPixel
from aht20 import AHT20
from bh1750 import BH1750
from ds3231_port import DS3231

INTERVAL = 10           # 기록 간격 [초]
ADC_REF = 3.3
DIVIDER_RATIO = 2.0

# --- I2C 센서 3종 + OLED (GP4 = SDA, GP5 = SCL) ---
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
aht20 = AHT20(i2c)
bh1750 = BH1750(0x23, i2c)
ds3231 = DS3231(i2c)

# OLED가 없어도 로깅은 계속되도록 실패를 무시합니다.
try:
    oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
except Exception as e:
    print("OLED 초기화 실패 (OLED 출력 없이 진행):", e)
    oled = None

# --- 배터리 전압 ---
adc = ADC(27)

# --- 네오픽셀 ---
np = NeoPixel(Pin(21), 1)

# --- SD 카드 (SPI0) ---
cs = machine.Pin(17, machine.Pin.OUT)
spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(18),
                  mosi=machine.Pin(19),
                  miso=machine.Pin(16))
sd = sdcard.SDCard(spi, cs)
uos.mount(uos.VfsFat(sd), "/SDCARD")

LOG_PATH = "/SDCARD/log.csv"


def blink(color=(0, 32, 0)):
    """네오픽셀을 잠깐 켰다 끕니다."""
    np[0] = color
    np.write()
    sleep(0.1)
    np[0] = (0, 0, 0)
    np.write()


def show(lines):
    """OLED에 측정값을 줄 단위로 표시합니다."""
    if oled is None:
        return
    oled.fill(0)
    for i, line in enumerate(lines):
        oled.text(line, 0, i * 16)
    oled.show()


def write_line(text):
    with open(LOG_PATH, "a") as file:
        file.write(text + "\n")


# 파일이 비어 있으면 헤더를 먼저 씁니다.
try:
    header_needed = uos.stat(LOG_PATH)[6] == 0
except OSError:
    header_needed = True

if header_needed:
    write_line("datetime,temperature_c,humidity_pct,lux,battery_v")

while True:
    t = ds3231.get_time()    # (year, month, day, hour, min, sec, weekday, yearday)
    timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    temperature, humidity = aht20.measure()
    lux = bh1750.measurement
    battery = adc.read_u16() * (ADC_REF / 65535) * DIVIDER_RATIO

    line = "{},{:.2f},{:.2f},{:.1f},{:.3f}".format(
        timestamp, temperature, humidity, lux, battery)

    print(line)
    write_line(line)

    show([
        "{:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5]),
        "T {:.1f}C H {:.0f}%".format(temperature, humidity),
        "LUX {:.0f}".format(lux),
        "BAT {:.2f}V".format(battery),
    ])

    blink()

    sleep(INTERVAL)
