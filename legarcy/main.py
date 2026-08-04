from machine import Pin, I2C, ADC, PWM
import utime
import ssd1306
import neopixel

# --- 1. 통신 및 장치 설정 ---

# I2C 통신 초기화 (OLED)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
OLED_WIDTH = 128
OLED_HEIGHT = 64
I2C_ADDR = 0x3C

try:
    oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=I2C_ADDR)
except:
    print("OLED 초기화 실패.")
    exit()

# 🎚️ 마이크 설정 (A0 핀 = GP26)
MIC_PIN = 26
mic_adc = ADC(MIC_PIN)

# 🚨 부저 설정 (패시브 부저를 이용해 톤을 낼 수 있도록 PWM 사용, GP22)
BUZZER_PIN = 22
buzzer_pwm = PWM(Pin(BUZZER_PIN))

# 💡 네오픽셀 설정 (GP21 핀, 1개)
NEOPIXEL_PIN = 21
NEOPIXEL_COUNT = 1
np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NEOPIXEL_COUNT)


# --- 2. 상수 및 임계치 설정 ---

NOISE_THRESHOLD_ADC = 1500 # 소음 임계치
PERSISTENCE_MS = 200      # 1초 지속 후 상태 전환

# 부저 알람 설정
ALARM_FREQUENCY = 1000
ALARM_DURATION_MS = 2000


# --- 3. 함수 정의 ---

def display_text(line1, line2, line3, line4):
    """OLED에 네 줄의 텍스트를 출력"""
    oled.fill(0)
    oled.text(line1, 0, 0)
    oled.text(line2, 0, 16)
    oled.text(line3, 0, 32)
    oled.text(line4, 0, 48)
    oled.show()

def play_alarm():
    """부저로 경보음을 재생"""
    buzzer_pwm.freq(ALARM_FREQUENCY)
    buzzer_pwm.duty_u16(60000)

def stop_alarm():
    """부저 멈춤"""
    buzzer_pwm.duty_u16(0)


# --- 4. 메인 루프 (Loop) ---
print("소음 감지 시스템 시작...")
is_alarming = False
alarm_end_time = 0

loud_condition_start_time = 0
quiet_condition_start_time = 0

while True:
    current_time = utime.ticks_ms()
    
    # 1. 마이크 Peak-to-Peak 데이터 측정
    sample_size = 100
    max_val = 0
    min_val = 65535
    for _ in range(sample_size):
        val = mic_adc.read_u16()
        if val > max_val:
            max_val = val
        if val < min_val:
            min_val = val
    peak_to_peak = max_val - min_val

    is_loud_now = peak_to_peak > NOISE_THRESHOLD_ADC
    
    # 볼륨 바 생성
    length = 14
    
    # 1. 계산된 값을 구하고
    calculated_bar_val = (peak_to_peak / NOISE_THRESHOLD_ADC) * length

    # 2. loud_bar가 length(14)를 초과하지 않도록 상한선을 설정합니다.
    loud_bar = min(calculated_bar_val, length)

    # 3. 문자열 생성 시, 정수로 변환하여 사용합니다.
    loud_bar_int = int(loud_bar)

    # 4. 문자열 생성 시, 음수 오류를 방지합니다.
    loud_bar_str = "|" + "=" * loud_bar_int + " " * (length - loud_bar_int) + "|"
        
    # -----------------------------------------------
    # 2. 상태 전환 로직 (1초 지속 시간 추적)
    # -----------------------------------------------

    if is_loud_now:
        if quiet_condition_start_time != 0: quiet_condition_start_time = 0
        if loud_condition_start_time == 0: loud_condition_start_time = current_time
    else:
        if loud_condition_start_time != 0: loud_condition_start_time = 0
        if quiet_condition_start_time == 0: quiet_condition_start_time = current_time

    # 2.1. LOUD 상태로 전환 (1초 이상 소리 감지)
    if not is_alarming and loud_condition_start_time != 0 and \
       utime.ticks_diff(current_time, loud_condition_start_time) >= PERSISTENCE_MS:
        
        is_alarming = True
        alarm_end_time = current_time + ALARM_DURATION_MS # 부저 타이머 설정
        play_alarm()

    # 2.2. QUIET 상태로 전환 (1초 이상 소리 미만 감지)
    elif is_alarming and quiet_condition_start_time != 0 and \
         utime.ticks_diff(current_time, quiet_condition_start_time) >= PERSISTENCE_MS:
        
        is_alarming = False

    # -----------------------------------------------
    # 3. 장치 작동 (확정된 상태에 따라)
    # -----------------------------------------------

    # 🚨 부저 작동 상태 확인 (2초 타이머가 아직 만료되지 않았으면 True)
    is_buzzer_active_now = utime.ticks_diff(current_time, alarm_end_time) < 0
    
    # 1. 부저 제어 (타이머 만료 시 멈춤)
    if not is_buzzer_active_now:
        stop_alarm()

    # 2. 메시지 및 LED 제어 (부저 작동 상태 우선)
    if is_buzzer_active_now:
        # 부저가 켜져 있는 2초 동안 MSG와 LED를 고정
        np[0] = (255, 0, 0)      # 네오픽셀: 빨간색
        line2_status = "TOO LOUD!!" 
        
    elif is_alarming:
        # 소리가 1초 지속된 상태이지만 부저는 끝난 경우 (이 코드는 사실상 실행되지 않음)
        np[0] = (255, 0, 0)
        line2_status = "TOO LOUD!!"
        
    else: # QUIET 상태 (부저 타이머 만료 & 소리 임계치 이하)
        # 1. 네오픽셀: 초록색
        np[0] = (0, 255, 0)
        line2_status = "GET LOUD!" 
        
    # 3. 네오픽셀 업데이트
    np.write()

    # 4. OLED 출력 업데이트
    line1 = f"Vol:{peak_to_peak:5}/{NOISE_THRESHOLD_ADC}"
    line2 = "MSG: {}".format(line2_status)
    line3 = "---Status Bar---"
    line4 = "{}".format(loud_bar_str)

    display_text(line1, line2, line3, line4)

    # 5. 루프 지연
    utime.sleep(0.05)