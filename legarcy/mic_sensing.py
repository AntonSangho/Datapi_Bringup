from machine import Pin, I2C, ADC, PWM
import utime
import ssd1306
import neopixel

# --- 1. 통신 및 장치 설정 (필수 장치만 초기화) ---

# I2C 통신 초기화 (OLED)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
OLED_WIDTH = 128
OLED_HEIGHT = 64
I2C_ADDR = 0x3C

try:
    oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=I2C_ADDR)
except:
    print("OLED 초기화 실패. 연결을 확인하세요.")
    exit()

# 🎚️ 마이크 설정 (A0 핀 = GP26)
MIC_PIN = 26
mic_adc = ADC(MIC_PIN)

# 💡 네오픽셀 설정 (GP21 핀, 1개)
NEOPIXEL_PIN = 21
NEOPIXEL_COUNT = 1
np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NEOPIXEL_COUNT)
# 초기 상태: 파란색 (대기)
np[0] = (0, 0, 255)
np.write()

# 🚨 부저 설정 (GP15)
BUZZER_PIN = 15
buzzer_pwm = PWM(Pin(BUZZER_PIN))
# 초기 상태: 부저 멈춤
buzzer_pwm.duty_u16(0) 


# --- 2. 함수 정의 ---

def display_text(line1, line2):
    """OLED에 두 줄의 텍스트를 출력"""
    oled.fill(0)
    oled.text(line1, 0, 0)
    oled.text(line2, 0, 16)
    oled.show()


# --- 3. 메인 루프 (Loop) ---
print("마이크 ADC 값 읽기 시작...")
oled.text("Microphone Test", 0, 32)
oled.show()
utime.sleep(1) # 초기 메시지 표시

while True:
    
   # 1. 마이크 데이터 읽기: Peak-to-Peak 측정
    sample_size = 100 # 100번 샘플링
    max_val = 0
    min_val = 65535 # 16비트 ADC의 최대값
    
    # 짧은 시간 동안 100개의 샘플을 빠르게 읽어 최대/최소값을 찾습니다.
    for _ in range(sample_size):
        val = mic_adc.read_u16()
        if val > max_val:
            max_val = val
        if val < min_val:
            min_val = val
        
    # 소음 크기 (진폭) 계산
    peak_to_peak = max_val - min_val 
    
    # 2. OLED 출력 업데이트
    line1 = "Volume (Pk-Pk): {}".format(peak_to_peak) # 소리 크기 출력
    line2 = "Max: {} / Min: {}".format(max_val, min_val) # 참고용 최대/최소값
    
    display_text(line1, line2)
    
    # 3. 루프 지연
    utime.sleep(0.05)