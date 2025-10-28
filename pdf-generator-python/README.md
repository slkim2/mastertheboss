# PDF Generator - URL to PDF Converter

Python 3.12 기반의 웹 애플리케이션으로, URI를 받아서 PDF 파일을 생성합니다. 웹 브라우저에서 간편하게 사용할 수 있습니다.

## 주요 기능

- 웹 페이지 URL을 PDF로 변환
- 사용자 친화적인 웹 인터페이스
- 다양한 PDF 생성 옵션 제공
  - 페이지 크기 선택 (A4, Letter, Legal, A3)
  - 배경 인쇄 옵션
  - 사용자 정의 여백 설정
- 브라우저에서 직접 PDF 다운로드

## 기술 스택

- **Python 3.12**
- **Flask**: 웹 애플리케이션 프레임워크
- **Playwright**: 웹 페이지를 PDF로 변환

## 설치 방법

### 1. 저장소 클론

```bash
cd pdf-generator-python
```

### 2. Python 가상 환경 생성 (권장)

```bash
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. Playwright 브라우저 설치

```bash
playwright install chromium
```

## 실행 방법

### 개발 모드

```bash
python app.py
```

애플리케이션이 `http://localhost:5000`에서 실행됩니다.

### 프로덕션 모드

프로덕션 환경에서는 Gunicorn 또는 uWSGI를 사용하는 것이 권장됩니다.

```bash
# Gunicorn 설치
pip install gunicorn

# 실행
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 사용 방법

### 웹 인터페이스

1. 브라우저에서 `http://localhost:5000` 접속
2. 변환하고 싶은 웹 페이지의 URL 입력
3. (선택사항) 고급 옵션에서 PDF 설정 조정
4. "PDF 생성 및 다운로드" 버튼 클릭
5. 생성된 PDF 파일이 자동으로 다운로드됩니다

### API 사용

REST API를 직접 호출할 수도 있습니다.

```bash
curl -X POST http://localhost:5000/api/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "options": {
      "format": "A4",
      "print_background": true,
      "margin_top": "1cm",
      "margin_right": "1cm",
      "margin_bottom": "1cm",
      "margin_left": "1cm"
    }
  }' \
  --output example.pdf
```

#### API 엔드포인트

**POST /api/generate-pdf**

요청 본문:
```json
{
  "url": "https://example.com",
  "options": {
    "format": "A4",
    "print_background": true,
    "margin_top": "1cm",
    "margin_right": "1cm",
    "margin_bottom": "1cm",
    "margin_left": "1cm"
  }
}
```

응답:
- 성공: PDF 파일 (application/pdf)
- 실패: JSON 오류 메시지

**GET /health**

헬스 체크 엔드포인트

응답:
```json
{
  "status": "healthy",
  "service": "PDF Generator"
}
```

## 프로젝트 구조

```
pdf-generator-python/
├── app.py                 # Flask 애플리케이션 메인 파일
├── requirements.txt       # Python 의존성
├── templates/
│   └── index.html        # 웹 인터페이스 HTML
└── README.md             # 프로젝트 문서
```

## 환경 변수

필요에 따라 `.env` 파일을 생성하여 환경 변수를 설정할 수 있습니다:

```env
FLASK_ENV=production
FLASK_PORT=5000
FLASK_HOST=0.0.0.0
```

## 보안 고려사항

- 프로덕션 환경에서는 `debug=False`로 설정해야 합니다
- URL 유효성 검사가 포함되어 있습니다
- 신뢰할 수 있는 URL만 변환하도록 제한하는 것이 좋습니다
- 필요에 따라 인증 및 권한 부여 메커니즘을 추가하세요

## 문제 해결

### Playwright 브라우저 설치 실패

```bash
playwright install-deps chromium
playwright install chromium
```

### 메모리 부족 오류

대용량 웹 페이지를 변환할 때 메모리 부족 오류가 발생할 수 있습니다. 이 경우:
- 시스템 메모리를 늘리거나
- 더 작은 페이지로 테스트하거나
- 워커 프로세스 수를 줄이세요

### 타임아웃 오류

일부 웹 페이지는 로딩에 시간이 오래 걸릴 수 있습니다. `app.py`의 타임아웃 설정을 조정하세요:

```python
page.goto(url, wait_until='networkidle', timeout=60000)  # 60초로 증가
```

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 기여

버그 리포트, 기능 요청, 풀 리퀘스트를 환영합니다!

## 개발자

Python 3.12 기반 PDF 생성 웹 애플리케이션
