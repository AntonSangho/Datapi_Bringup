"""
I2C 버스에 연결된 장치를 검색하는 코드

DataPi v0.3의 I2C0 버스에는 아래 3개 장치가 함께 연결되어 있습니다.
    0x23 : BH1750  (조도 센서)
    0x38 : AHT20   (온습도 센서)
    0x3C : SSD1306 (OLED)
    0x68 : DS3231  (실시간 시계, RTC)
    0x57 : AT24C32 (DS3231 모듈에 함께 실린 EEPROM, 모듈에 따라 없을 수 있음)
"""

from machine import Pin, I2C

# DataPi v0.3 핀 배치: GP4 = SDA, GP5 = SCL
sdaPIN = Pin(4)   # SDA
sclPIN = Pin(5)   # SCL

i2c = I2C(0, sda=sdaPIN, scl=sclPIN)    # 0번 I2C 사용

devices = i2c.scan()                    # I2C 장치 검색

# 주소별로 어떤 부품인지 알려주기 위한 표
KNOWN = {
    0x23: "BH1750 (조도)",
    0x38: "AHT20 (온습도)",
    0x3C: "SSD1306 (OLED)",
    0x57: "AT24C32 (EEPROM)",
    0x68: "DS3231 (RTC)",
}

if len(devices) == 0:
    print("No I2C device")
else:
    print("I2C device found :", len(devices))

for device in devices:
    print(" Hexa address:", hex(device), "-", KNOWN.get(device, "unknown"))
