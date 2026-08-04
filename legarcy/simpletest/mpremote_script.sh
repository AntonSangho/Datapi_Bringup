#!/bin/bash

# 스크립트를 루트 권한으로 실행해야 합니다.
if [ "$EUID" -ne 0 ]; then
  echo "이 스크립트는 루트 권한으로 실행되어야 합니다."
  exit 1
fi

# 라즈베리파이 피코 안에 lib 디렉터리를 생성합니다.
mpremote fs mkdir :lib
echo "lib 디렉터리를 생성했습니다."

# 1초 대기
sleep 1

# 라즈베리파이 피코 안에 lib 디렉터리에 라이브러리 파일을 복사합니다.
mpremote fs cp ../../lib/*.py :lib/
echo "마이크로파이썬 UF2 파일을 복사했습니다."

# 1초 대기
sleep 1

# 라즈베리파이 피코 안에 main.py 파일을 복사합니다.
mpremote fs cp ../main_v0_3.py :main.py
echo "main.py 파일을 복사했습니다."
