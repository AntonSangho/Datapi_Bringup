from machine import Pin, I2C, PWM 
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

# 🎚️ 초음파 센서 설정 (GP16: Trig, GP17: Echo)
TRIG_PIN = 16
ECHO_PIN = 17
trigger = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

# 🚨 부저 설정 (GP22)
BUZZER_PIN = 22
buzzer_pwm = PWM(Pin(BUZZER_PIN))

# 💡 네오픽셀 설정 (GP21)
NEOPIXEL_PIN = 21
NEOPIXEL_COUNT = 1
np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NEOPIXEL_COUNT)


# --- 2. 상수 및 임계치 설정 ---

# 🚨 3단계 임계치
THR_DANGER = 10         # 10cm 미만 (3단계)
THR_WARNING = 30        # 10cm ~ 30cm (2단계)

PERSISTENCE_MS = 1000   # 상태 변화를 위한 최소 지속 시간 (1초)

# 🌊 수위 변화율 설정 (5cm/초)
RATE_THRESHOLD_CM = 5.0 #초당 5cm로 높이 계산
MIN_TIME_DELTA_MS = 1000 #높이 계산 간격 

# 상태 정의
STATE_SAFE = 0
STATE_WARN = 1
STATE_DANGER = 2

# 알람 및 깜빡임 설정
ALARM_FREQUENCY = 1000
BEEP_CYCLE_MS = 800     # 2단계 부저 주기 (0.3초 ON/OFF)
BLINK_INTERVAL_MS = 250 # 3단계 깜빡임 주기

# 🖥️ 화면 업데이트 제어 변수 (추가)
RATE_PERSISTENCE_MS = 5000 # STABLE 상태로 전환하기 위한 최소 지속 시간 (5초)
rate_persistence_start_time = 0 # STABLE 상태 진입 시간 (0이면 타이머 미작동)
displayed_rate_status = "STABLE" # OLED에 표시되는 최종 상태

# 현재 OLED에 표시되고 있는 RATE 상태 (업데이트 주기 제어용)
displayed_rate_status = "STABLE"


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
    """부저로 경보음을 재생 (Continuous Beep)"""
    buzzer_pwm.freq(ALARM_FREQUENCY)
    buzzer_pwm.duty_u16(32768)

def stop_alarm():
    """부저 멈춤"""
    buzzer_pwm.duty_u16(0)

def distance_cm():
    """
    초음파 센서로 거리를 측정하여 센티미터(cm)로 반환합니다.
    (time_pulse_us 오류 해결을 위해 수동 타이밍 루프 사용)
    """
    # 1. 트리거 펄스 발생
    trigger.value(0)
    utime.sleep_us(2)
    trigger.value(1)
    utime.sleep_us(10)
    trigger.value(0)

    # 2. 펄스 시작/종료 시간 측정
    timeout_count = 0
    while echo.value() == 0:
        utime.sleep_us(1)
        timeout_count += 1
        if timeout_count > 10000: return 400.0
            
    start_time = utime.ticks_us()

    timeout_count = 0
    while echo.value() == 1:
        utime.sleep_us(1)
        timeout_count += 1
        if timeout_count > 30000: return 400.0
            
    end_time = utime.ticks_us()
    
    # 3. 펄스 길이 계산 및 거리 공식 적용
    duration = utime.ticks_diff(end_time, start_time)
    
    if duration > 0:
        distance = duration / 58.0
        return min(distance, 400.0)
    else:
        return 400.0


# --- 4. 메인 루프 (Loop) ---
print("3단계 초음파 수위/근접 경보 시스템 시작...")

# 상태 추적 변수
current_state = STATE_SAFE
pending_state = STATE_SAFE
state_change_time = 0

# 🌊 수위 변화율 계산을 위한 변수
last_distance = 0.0
last_time = 0

while True:
    current_time = utime.ticks_ms()
    
    # 1. 초음파 센서 데이터 측정
    current_distance = distance_cm()

    # 1.5. 🌊 수위 변화율 측정 및 상태 결정 (RATE 상태는 매번 계산됨)
    calculated_rate_status = "STABLE"
    
    # 1초 간격으로 거리 변화량을 측정하여 RISING/FALLING/STABLE 결정
    if last_distance != 0.0 and last_time != 0:
        time_delta_ms = utime.ticks_diff(current_time, last_time)
        
        if time_delta_ms >= MIN_TIME_DELTA_MS:
            distance_delta = current_distance - last_distance
            
            if distance_delta > RATE_THRESHOLD_CM:
                calculated_rate_status = "FALLING" # 거리가 늘어남 -> 물 빠짐
            elif distance_delta < -RATE_THRESHOLD_CM:
                calculated_rate_status = "RISING"  # 거리가 줄어듦 -> 물 차오름
            # else: STABLE 유지

            # 다음 계산을 위해 값 업데이트
            last_distance = current_distance
            last_time = current_time

    elif last_distance == 0.0:
        # 최초 측정 시점 초기화
        last_distance = current_distance
        last_time = current_time
        calculated_rate_status = "STABLE"
    
    # --- 1.6. RATE 상태 화면 업데이트 로직 (Persistence 적용) ---
    
    if calculated_rate_status != "STABLE":
        # 1. RISING/FALLING 감지 시: 즉시 화면 업데이트 및 타이머 리셋
        displayed_rate_status = calculated_rate_status
        rate_persistence_start_time = 0 # STABLE 대기 타이머 초기화
        
    elif calculated_rate_status == "STABLE":
        # 2. STABLE 감지 시: 
        
        if displayed_rate_status != "STABLE":
            # 2-1. RISING/FALLING 상태에서 STABLE로 전환을 시도하는 경우:
            
            if rate_persistence_start_time == 0:
                # 타이머가 시작되지 않았으면, 지금 시작
                rate_persistence_start_time = current_time
                
            elif utime.ticks_diff(current_time, rate_persistence_start_time) >= RATE_PERSISTENCE_MS:
                # 5초 이상 STABLE 상태가 유지되었으면, 화면 전환
                displayed_rate_status = "STABLE"
                rate_persistence_start_time = 0 # 타이머 리셋
                
        else:
            # 2-2. 이미 STABLE 상태인 경우:
            rate_persistence_start_time = 0 # 타이머 미사용 상태 유지
            # displayed_rate_status는 "STABLE" 유지
            
    # 2. 원하는 상태 결정 (근접 경보)
    if current_distance < THR_DANGER:
        target_state = STATE_DANGER
    elif current_distance < THR_WARNING:
        target_state = STATE_WARN
    else:
        target_state = STATE_SAFE
    
    # 3. 1초 지속 시간 확인 로직 (근접 경보 상태 변화 안정화)
    if target_state != current_state:
        if target_state != pending_state:
            pending_state = target_state
            state_change_time = current_time
        
        if utime.ticks_diff(current_time, state_change_time) >= PERSISTENCE_MS:
            current_state = target_state
            pending_state = target_state
    else:
        pending_state = current_state
        
    # 4. 장치 작동 (확정된 상태에 따라)
    
    if current_state == STATE_DANGER:
        # 3단계: danger!!
        line2_status = "danger!!"
        play_alarm()
        if utime.ticks_diff(current_time, 0) % (BLINK_INTERVAL_MS * 2) < BLINK_INTERVAL_MS:
            np[0] = (255, 0, 0)
        else:
            np[0] = (0, 0, 0)

    elif current_state == STATE_WARN:
        # 2단계: Warning!
        line2_status = "Warning!"
        
        # 부저: 짧게 삐삐
        if utime.ticks_diff(current_time, 0) % BEEP_CYCLE_MS < BEEP_CYCLE_MS / 2:
            play_alarm()
        else:
            stop_alarm()
            
        # 네오픽셀: 주황색
        np[0] = (255, 128, 0)

    else: # current_state == STATE_SAFE
        # 1단계: SAFE
        line2_status = "SAFE"
        stop_alarm()
        
        # 네오픽셀: 초록색
        np[0] = (0, 255, 0)
        
    # 5. 네오픽셀 업데이트
    np.write()

    # 6. 거리 바 생성 및 OLED 출력
    max_range = 50.0
    length = 14
    mapped_distance = max_range - min(current_distance, max_range)
    bar_val = int((mapped_distance / max_range) * length)
    loud_bar_str = "|" + "=" * bar_val + " " * (length - bar_val) + "|"
    
    # OLED 출력 업데이트
    line1 = "DST: {:.1f} cm".format(current_distance)
    line2 = "RATE: {}".format(displayed_rate_status) # 5초 Persistence가 적용된 최종 상태
    line3 = "MSG: {}".format(line2_status)
    line4 = "{}".format(loud_bar_str)

    display_text(line1, line2, line3, line4)

    # 7. 루프 지연
    utime.sleep(0.05)