#!/bin/bash

# PDF Generator 실행 스크립트

echo "PDF Generator 시작..."

# 가상환경 확인
if [ ! -d "venv" ]; then
    echo "가상환경을 생성합니다..."
    python3.12 -m venv venv
fi

# 가상환경 활성화
source venv/bin/activate

# 의존성 설치
echo "의존성을 설치합니다..."
pip install -r requirements.txt

# Playwright 브라우저 설치 확인
echo "Playwright 브라우저를 설치합니다..."
playwright install chromium

# 애플리케이션 실행
echo "애플리케이션을 실행합니다..."
echo "http://localhost:5000 에서 접속 가능합니다."
python app.py
