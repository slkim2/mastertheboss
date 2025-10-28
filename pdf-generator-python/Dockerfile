FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright 브라우저 설치
RUN playwright install-deps chromium
RUN playwright install chromium

# 애플리케이션 파일 복사
COPY . .

# 포트 노출
EXPOSE 5000

# 환경 변수 설정
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Gunicorn 설치
RUN pip install gunicorn

# 애플리케이션 실행
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
