"""
SD 카드(SPI0)에 파일을 쓰고 다시 읽어보는 코드

DataPi v0.3 핀 배치
    GP16 = MISO, GP17 = CS, GP18 = SCK, GP19 = MOSI
"""

import machine
import uos

import sdcard

# Chip select(CS) 핀을 지정합니다.
cs = machine.Pin(17, machine.Pin.OUT)

# SPI 주변장치를 초기화합니다. (처음에는 1MHz로 시작)
spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(18),
                  mosi=machine.Pin(19),
                  miso=machine.Pin(16))

# SD 카드 초기화
sd = sdcard.SDCard(spi, cs)

# 파일시스템 마운트
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/SDCARD")

print("files:", uos.listdir("/SDCARD"))

# 파일을 만들고 내용을 씁니다.
with open("/SDCARD/test01.txt", "w") as file:
    file.write("Hello, SD World!\r\n")
    file.write("This is a test\r\n")

# 방금 만든 파일을 열어 읽습니다.
with open("/SDCARD/test01.txt", "r") as file:
    print(file.read())

uos.umount("/SDCARD")   # 안전하게 마운트를 해제합니다.
