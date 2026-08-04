# Datapi_Bringup

DataPi 보드의 하드웨어 브링업(bring-up) 및 기능 검증용 MicroPython 코드입니다.

**대상 하드웨어: DataPi v0.3**

## 하드웨어 연결 정보 (v0.3)

회로도: [`docs/datapi_0_3v_schematic.pdf`](./docs/datapi_0_3v_schematic.pdf)

### I2C0 — GP4 = SDA, GP5 = SCL

| 주소 | 부품 | 용도 |
|---|---|---|
| `0x23` | BH1750 | 조도 센서 |
| `0x38` | AHT20 | 온습도 센서 |
| `0x3C` | SSD1306 | OLED 128x64 |
| `0x68` | DS3231 | 실시간 시계 (RTC) |

> RP2040의 I2C0은 핀이 하드웨어로 고정되어 있습니다.
> SDA는 GP0/4/8/12/16/20, SCL은 GP1/5/9/13/17/21만 가능하므로
> **GP4 = SDA, GP5 = SCL** 외의 조합은 존재할 수 없습니다.

### SPI0 — SD 카드 (TF-115)

| 핀 | 신호 |
|---|---|
| GP16 | MISO |
| GP17 | CS |
| GP18 | SCK |
| GP19 | MOSI |

### 그 외

| 핀 | 부품 | 비고 |
|---|---|---|
| GP20 | 버튼 SW1 | 내부 풀업, 눌리면 0 |
| GP21 | 네오픽셀 WS2812B | |
| GP22 | 부저 MLT-7525 | PWM |
| GP27 | 배터리 전압 BAT_DIV | ADC1, R8/R9 = 10k/10k 분배 |
| — | 내장 LED | `Pin("LED")` (Pico W는 무선 칩에 연결) |

## MicroPython 펌웨어

| 항목 | 값 |
|---|---|
| 버전 | MicroPython **v1.28.0** (2026-04-06 빌드) |
| 빌드 | `RPI_PICO_W` |
| 보드 | Raspberry Pi Pico W (RP2040) |
| 포트 | `/dev/ttyACM0` |
| 펌웨어 파일 | [`RPI_PICO_W-20260406-v1.28.0.uf2`](./RPI_PICO_W-20260406-v1.28.0.uf2) |

보드에 설치된 버전 확인:

```bash
mpremote exec "import os; print(os.uname())"
```

최신 펌웨어: [micropython.org/download/RPI_PICO_W](https://micropython.org/download/RPI_PICO_W/)

## 펌웨어 설치 / 초기화 (flash_nuke.uf2)

플래시에 남은 파일을 완전히 지우고 깨끗한 상태에서 다시 시작할 때 사용합니다.
파일이 꼬였거나, 이전에 올린 `main.py`가 계속 실행될 때 유용합니다.

1. **BOOTSEL 버튼을 누른 채로** USB를 연결합니다.
   (이미 연결되어 있다면 BOOTSEL을 누른 채 RESET 버튼(S3)을 눌렀다 뗍니다)
2. `RPI-RP2` USB 드라이브가 나타납니다.
3. `flash_nuke.uf2`를 그 드라이브에 복사합니다.

   ```bash
   cp flash_nuke.uf2 /media/$USER/RPI-RP2/
   ```

4. 보드가 자동으로 재부팅되며 플래시가 전부 지워지고, 다시 `RPI-RP2`로 나타납니다.
5. 이어서 MicroPython 펌웨어를 같은 방식으로 복사합니다.

   ```bash
   cp RPI_PICO_W-20260406-v1.28.0.uf2 /media/$USER/RPI-RP2/
   ```

6. 보드가 재부팅되고 `/dev/ttyACM0`으로 잡히면 완료입니다.

   ```bash
   ls /dev/ttyACM*
   mpremote exec "print('hello')"
   ```

> ⚠️ flash_nuke는 **보드에 올린 모든 파일(`main.py`, `lib/` 포함)을 삭제**합니다.
> SD 카드의 데이터에는 영향이 없습니다.

## 하드웨어 점검 스킬 (`/datapi-hwtest`)

주변장치를 한 번에 점검하고 `PASS / SKIP / WARN / FAIL` 리포트를 출력합니다.
**OLED · SD 카드 · 배터리는 장착되지 않았으면 실패가 아니라 `SKIP` 처리**됩니다.

```bash
# 라이브러리 업로드 + 전체 점검
~/.claude/skills/datapi-hwtest/scripts/datapi_test.sh

# 라이브러리가 이미 올라가 있으면 (더 빠름)
~/.claude/skills/datapi-hwtest/scripts/datapi_test.sh --no-upload

# DS3231 시각이 1900년으로 나올 때 PC 시각으로 동기화
~/.claude/skills/datapi-hwtest/scripts/rtc_sync.sh
```

Claude Code 안에서는 `/datapi-hwtest` 로 호출할 수 있습니다.

출력 예시:

```
[PASS] I2C scan   4개 - 0x23 BH1750, 0x38 AHT20, 0x3c SSD1306, 0x68 DS3231
[PASS] AHT20      27.05 C / 64.76 %RH
[PASS] SDcard     마운트 + 쓰기/읽기 정상, 파일 4개
[SKIP] OLED       미장착 (0x3C 없음)
[WARN] Battery    raw 65535 포화 - 분배 저항(R8/R9) 확인 필요
====================================================
PASS 10  SKIP 0  WARN 1  FAIL 0
```

| 판정 | 의미 |
|---|---|
| `PASS` | 정상 |
| `SKIP` | 부품이 장착되지 않아 건너뜀 |
| `WARN` | 응답은 하지만 값이 의심스러움 |
| `FAIL` | 실제 고장 |

부저 소리와 네오픽셀 색, OLED 화면은 소프트웨어로 확인할 수 없으니 직접 봐주세요.

## 개별 테스트 코드

기능별 예제는 [`src/simpletest/`](./src/simpletest/)에 있습니다.
자세한 실행 방법은 [src/simpletest/README.md](./src/simpletest/README.md)를 참고하세요.

```bash
cd src
mpremote fs mkdir :lib          # 최초 1회
mpremote fs cp lib/*.py :lib/   # 드라이버 업로드

cd simpletest
mpremote run Blink.py           # 복사 없이 바로 실행
mpremote run i2c.py             # I2C 장치 스캔
```

| 파일 | 검증 대상 |
|---|---|
| `Blink.py` | 내장 LED |
| `i2c.py` | I2C 버스 스캔 |
| `Button.py` | 버튼 |
| `Buzzer.py` / `Buzzer_melody.py` | 부저 |
| `Neopixel.py` | 네오픽셀 |
| `OLED.py` | OLED + 버튼 연동 |
| `Light.py` | 조도 센서 |
| `Temp.py` | 온습도 센서 |
| `RTC.py` | 실시간 시계 |
| `ADC_BATT.py` | 배터리 전압 |
| `sd_test.py` | SD 카드 |
| `logger.py` | 통합 — 센서 전체를 OLED 표시 + SD 카드에 CSV 기록 |

## mpremote 유용한 명령어

```bash
mpremote fs ls              # 보드의 파일 목록
mpremote fs ls :lib         # lib 디렉터리 목록
mpremote cp main.py :main.py    # PC -> 보드로 복사 (부팅 시 자동 실행)
mpremote cp :log.txt log.txt    # 보드 -> PC로 복사
mpremote run test.py        # 복사하지 않고 즉시 실행
mpremote reset              # 리셋
mpremote                    # REPL 접속 (나올 때 Ctrl-])
```

- 실행 중인 스크립트 중단: `Ctrl-C`
- 무한 루프 스크립트의 출력을 저장할 때는 파이프 대신 파일로 리다이렉트하세요.
  파이프로 받다가 `Ctrl-C`로 끊으면 버퍼가 날아가 출력이 비어 보입니다.

  ```bash
  mpremote run logger.py > log.out
  ```

#### 참고링크
- [micropython remote control: mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html#mpremote-command-reset)
- [MicroPython for Raspberry Pi Pico W](https://micropython.org/download/RPI_PICO_W/)

## 알려진 이슈

### 배터리 전압(GP27) ADC 포화 — v0.3 회로도 배선 오류

**원인: R9가 GND가 아니라 VBAT(+)에 연결되어 있습니다.**
R8과 R9가 직렬 분배가 아니라 **병렬**로 묶여 있고, GND로 가는 경로가 회로도에 없습니다.

KiCad 네트리스트 확인 결과:

| 부품 | 핀 1 | 핀 2 |
|---|---|---|
| R8 (10k/1%) | `Net-(JP3-A)` | `/VBAT(+)` |
| R9 (10k/1%) | `Net-(JP3-A)` | **`/VBAT(+)`** ← GND여야 함 |
| JP3 | `Net-(JP3-A)` | `/BAT_DIV` |

```
현재:  VBAT ──┬─[R8 10k]─┬── JP3 ── BAT_DIV ── GP27
              └─[R9 10k]─┘          (GND 연결 없음)

정상:  VBAT ──[R8 10k]──┬── JP3 ── BAT_DIV ── GP27
                        │
                    [R9 10k]
                        │
                       GND
```

전류가 흐를 경로가 없으므로 R8에 전압 강하가 생기지 않고(`V = I × R = 0`),
BAT_DIV가 VBAT 그대로 올라가 ADC가 포화합니다.

측정 결과 (배터리·USB 제거 후):

| 측정 지점 | 결과 | 정상 회로였다면 |
|---|---|---|
| TP1 (VBAT 노드) | 3.75 V | 배터리 전압 — 정상 |
| GP27 | 3.65 V | 1.88 V |
| 중점 ↔ GND | OL (개방) | 10 kΩ |
| VBAT ↔ GND | OL (개방) | 20 kΩ |
| R8 양단 | 5 kΩ | 10 kΩ |
| R9 양단 | 5 kΩ | 10 kΩ |

> R8·R9를 재면 둘 다 5kΩ으로 나오는 것은 **병렬 연결의 증거**입니다
> (`10k ∥ 10k = 5k`). 두 부품의 양 끝이 같은 노드라 어느 쪽을 재도 같은 값이 나옵니다.
> 저항 부품 자체는 표기대로 **10k가 맞습니다.**

GP27이 3.75V가 아니라 3.65V인 것은 RP2040 내부 ESD 클램프 다이오드가
3V3 레일로 도통하며 물고 있기 때문입니다. 즉 **현재 핀이 정격을 초과해 동작 중**입니다.
전류는 5kΩ으로 제한되어 즉시 손상되지는 않습니다.

> ⚠️ 수리 전까지 **18650을 만충(4.2V)해서 연결하지 마세요.**
> GP27 절대최대정격(3.3V + 0.3V)을 넘어 핀이 손상될 수 있습니다.

**v0.3 보드 임시 수리** (재납땜으로는 해결되지 않습니다 — 기판에 GND 배선 자체가 없음):

1. R9의 VBAT 측 패드로 가는 트레이스를 커팅
2. 그 패드에서 가까운 GND(J4의 2번 핀, 마운팅 패드 MP1/MP2)로 점퍼선 연결
3. GP27이 1.88 V로 떨어지는지 확인 → 점검 결과가 `[PASS] Battery`로 바뀝니다

**분배비는 수정 불필요** — R8/R9 모두 10k이므로 `DIVIDER_RATIO = 2.0`이 그대로 유효합니다.
수리 후 GP27은 1.88 V(raw ≈ 37200)로 읽혀야 합니다.
