from machine import Pin, I2C, PWM
from utime import sleep
import ssd1306 

# --- 1. 통신 및 장치 설정 (이전과 동일) ---
# I2C 0번 버스: SCL=GP5, SDA=GP4
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000) 

# OLED 설정
OLED_WIDTH = 128
OLED_HEIGHT = 64
I2C_ADDR = 0x3C # 주소

try:
    oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=I2C_ADDR)
except:
    print("OLED 초기화 실패.")
    exit()

# 버튼 및 LED 설정 (이전과 동일)
button = Pin(20, Pin.IN, Pin.PULL_UP) 
led = Pin('LED', Pin.OUT) 
buzzer = PWM(Pin(22))
buzzer.freq(440)        # 주파수 440Hz = 음

# --- 2. 텍스트 표시 함수 (반복문으로 수정) ---

def display_text(text_list):
    """
    주어진 리스트의 텍스트를 OLED에 라인별로 출력합니다.
    (OLED 기본 폰트 높이 8px, 줄 간격을 고려하여 16px 단위로 출력)
    """
    oled.fill(0) # 화면 전체를 지움
    
    # 텍스트 리스트를 순회하며 출력
    for i, line_text in enumerate(text_list):
        # Y 좌표 계산: 인덱스(i) * 한 줄 높이(16)
        y_pos = i * 16
        
        # OLED 높이를 초과하지 않도록 검사
        if y_pos < OLED_HEIGHT:
            oled.text(line_text, 0, y_pos) # (텍스트, X좌표, Y좌표)
        else:
            # OLED 화면을 초과하는 텍스트는 출력하지 않고 루프 종료
            break 
            
    oled.show() # 디스플레이에 반영


# --- 3. 메인 루프 (Loop) ---
print("프로젝트 시작: OLED 및 버튼 대기 중...")
while True:
    
    # 버튼 눌림 감지 (0 = 눌림)
    if button.value() == 0:
        # 1. LED 끄기
        led.value(False)
        #buzzer.duty_u16(30000)  # 2. 볼륨 켜기 (0 ~ 65535 중간값 정도) 
        
        # 2. 버튼이 눌렸을 때 표시할 텍스트 목록
        text_on = [
            "|==============|",  # 라인 1 (y=0)
            "START SENSING",    # 라인 2 (y=16)
            "RPI PICO W"        # 라인 3 (y=32)
        ]
        display_text(text_on)
        
    else:
        # 1. LED 켜기
        led.value(True)
        buzzer.duty_u16(0)      # 볼륨 끄기
        
        # 2. 버튼이 떼어졌을 때 표시할 텍스트 목록
        text_off = [
            "<Chungnam Tour>", # 라인 1 (y=0)
            "READY",               # 라인 2 (y=16)
            "Press the button",    # 라인 3 (y=32)
            "(GP20)"               # 라인 4 (y=48)
        ]
        display_text(text_off)
        
    # 루프 지연
    sleep(0.1)