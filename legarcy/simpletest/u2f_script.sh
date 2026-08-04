#!/bin/bash

# 스크립트를 루트 권한으로 실행해야 합니다.
if [ "$EUID" -ne 0 ]; then
  echo "이 스크립트는 루트 권한으로 실행되어야 합니다."
  exit 1
fi

# 마이크로파이썬 UF2 파일을 복사할 디바이스를 찾습니다.
cp /home/anton/Projects/MicropythonU2F/RPI_PICO_W-20231005-v1.21.0.uf2 /media/anton/RPI-RP2
echo "마이크로파이썬 UF2 파일을 복사했습니다."
