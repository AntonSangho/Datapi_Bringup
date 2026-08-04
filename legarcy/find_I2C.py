from machine import Pin, I2C
import time

# --- 1. I2C 버스 초기화 (핀 확인 필수!) ---
# RPi Pico W의 I2C 0번 버스 (GP4=SDA, GP5=SCL)를 사용한다고 가정
# 확장보드에 따라 핀 번호가 다를 수 있습니다.
try:
    i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000) 
except:
    print("I2C 초기화 실패: 핀 연결을 확인하세요.")
    exit()

# --- 2. I2C 장치 주소 검색 ---
print("I2C 장치 스캔 시작...")
devices = i2c.scan()

# --- 3. 결과 출력 ---
if devices:
    print('\n✅ I2C 버스에서 다음 장치 주소가 발견되었습니다:')
    # 검색된 주소 목록을 16진수(Hex) 형태로 출력
    for device in devices:
        print('  - 주소: 0x{:02X}'.format(device))
        
    # LCD 주소 (가장 흔한 주소)
    # LCD-I2C 모듈은 주로 0x27 또는 0x3F 주소를 사용합니다.
    print("\n💡 LCD-I2C 모듈은 보통 0x27 또는 0x3F 주소를 사용합니다.")
    
else:
    print('\n❌ I2C 버스에서 응답하는 장치가 없습니다. 연결 상태를 확인해주세요.')