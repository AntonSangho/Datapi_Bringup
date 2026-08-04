"""
AHT20 온습도 센서 드라이버 (I2C, 고정 주소 0x38)

데이터시트 기준 동작 순서
1. 전원 인가 후 40ms 대기
2. 상태 레지스터(0x71)를 읽어 calibration 비트(bit3) 확인
3. 보정되지 않았으면 초기화 명령(0xBE 0x08 0x00) 전송
4. 측정 명령(0xAC 0x33 0x00) 전송 후 80ms 대기
5. 6바이트 읽기 -> 상태 1바이트 + 20bit 습도 + 20bit 온도
"""

from machine import I2C
import utime


class AHT20:
    ADDR = 0x38

    CMD_STATUS = b"\x71"
    CMD_INIT = b"\xbe\x08\x00"
    CMD_MEASURE = b"\xac\x33\x00"

    def __init__(self, i2c, addr=ADDR):
        self.i2c = i2c
        self.addr = addr

        utime.sleep_ms(40)          # 전원 인가 후 안정화 대기
        if not (self.status() & 0x08):   # bit3 = 보정 완료 플래그
            self.i2c.writeto(self.addr, self.CMD_INIT)
            utime.sleep_ms(10)

    def status(self):
        """상태 레지스터 1바이트를 반환합니다."""
        return self.i2c.readfrom(self.addr, 1)[0]

    def measure(self):
        """(온도[C], 습도[%RH]) 튜플을 반환합니다."""
        self.i2c.writeto(self.addr, self.CMD_MEASURE)
        utime.sleep_ms(80)          # 변환 완료 대기

        # bit7 = busy. 측정이 끝날 때까지 기다립니다.
        while self.status() & 0x80:
            utime.sleep_ms(10)

        data = self.i2c.readfrom(self.addr, 6)

        # data[1..2] + data[3] 상위 4bit = 20bit 습도
        raw_hum = (data[1] << 12) | (data[2] << 4) | (data[3] >> 4)
        # data[3] 하위 4bit + data[4..5] = 20bit 온도
        raw_temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

        humidity = raw_hum * 100 / 0x100000
        temperature = raw_temp * 200 / 0x100000 - 50
        return temperature, humidity

    @property
    def temperature(self):
        return self.measure()[0]

    @property
    def humidity(self):
        return self.measure()[1]
