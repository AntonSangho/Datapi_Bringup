# DataPi v0.3 하드웨어 검증 코드

Raspberry Pi Pico W + MicroPython 기준입니다.

## 핀 배치 (DataPi v0.3)

| 기능 | 부품 | 핀 |
|---|---|---|
| I2C0 | DS3231 / BH1750 / AHT20 / OLED | GP4 = SDA, GP5 = SCL |
| SPI0 | SD 카드 (TF-115) | GP16 = MISO, GP17 = CS, GP18 = SCK, GP19 = MOSI |
| 입력 | 버튼 SW1 | GP20 (내부 풀업, 눌리면 0) |
| 출력 | 네오픽셀 WS2812B | GP21 |
| 출력 | 부저 MLT-7525 | GP22 |
| 입력 | 배터리 전압 BAT_DIV | GP27 (ADC1) |

> v0.2와의 차이: 온도 센서가 OneWire DS18B20 → **I2C AHT20**으로 바뀌었습니다.
>
> ⚠️ 일부 하드웨어 문서에 GP4=SCL / GP5=SDA로 적혀 있으나 반대입니다.
> RP2040의 I2C0은 SDA가 GP0/4/8/12/16/20, SCL이 GP1/5/9/13/17/21로 고정되어 있어
> **GP4=SDA, GP5=SCL** 외의 조합은 하드웨어적으로 불가능합니다.
> (`legarcy/start_LCD.py`의 동작하는 설정과도 일치합니다.)

## 테스트 코드

| 파일 | 검증 대상 |
|---|---|
| [Blink.py](Blink.py) | 내장 LED — 보드가 살아 있는지 가장 먼저 확인 |
| [i2c.py](i2c.py) | I2C 버스 스캔 (0x23 / 0x38 / 0x3C / 0x68 검출 확인) |
| [Button.py](Button.py) | 버튼 입력 |
| [Buzzer.py](Buzzer.py) | 부저 단음 |
| [Buzzer_melody.py](Buzzer_melody.py) | 부저 멜로디 |
| [Neopixel.py](Neopixel.py) | 네오픽셀 RGB |
| [OLED.py](OLED.py) | OLED(SSD1306) 텍스트 표시 + 버튼 연동 |
| [Light.py](Light.py) | 조도 센서 BH1750 |
| [Temp.py](Temp.py) | 온습도 센서 AHT20 |
| [RTC.py](RTC.py) | 실시간 시계 DS3231 |
| [ADC_BATT.py](ADC_BATT.py) | 배터리 전압 |
| [sd_test.py](sd_test.py) | SD 카드 읽기/쓰기 |
| [logger.py](logger.py) | 통합 테스트 — 센서 전체를 읽어 OLED 표시 + SD 카드에 CSV 기록 |

권장 순서: `Blink` → `i2c` → 개별 센서 → `sd_test` → `logger`

## 실행 방법

라이브러리를 먼저 보드에 올립니다. (`src/lib/`)

```
mpremote mkdir :lib
mpremote cp ../lib/*.py :lib/
```

테스트 코드는 파일로 복사하지 않고 바로 실행할 수 있습니다.

```
mpremote run Blink.py
mpremote run i2c.py
```

부팅 시 자동 실행하려면 `main.py`로 복사합니다.

```
mpremote cp logger.py :main.py
```

기타 유용한 명령:

```
mpremote fs ls          # 보드의 파일 목록
mpremote fs cat :log.txt
mpremote reset          # 리셋
Ctrl-C                  # 실행 중인 스크립트 중단
```

## 필요한 라이브러리 (`src/lib/`)

- `aht20.py` — AHT20 온습도 드라이버 (v0.3에서 새로 작성)
- `bh1750.py` — 조도 센서
- `ds3231_port.py` — RTC
- `sdcard.py` — SD 카드
- `ssd1306.py` — OLED
- `neopixel` — MicroPython 펌웨어에 내장

## SD 카드 포맷 (Linux)

```
sudo umount /dev/sdc1
sudo parted /dev/sdc --script -- mklabel msdos
sudo parted /dev/sdc --script -- mkpart primary fat32 1MiB 100%
sudo mkfs.vfat -n SDCARD -F32 /dev/sdc1
sudo parted /dev/sdc --script -- print
```
