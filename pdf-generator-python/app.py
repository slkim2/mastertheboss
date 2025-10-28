"""
PDF Generator Web Application
URI를 받아서 PDF로 변환하는 Flask 웹 애플리케이션
Python 3.12 기반
"""

from flask import Flask, request, send_file, render_template, jsonify
from playwright.sync_api import sync_playwright
import os
import tempfile
from datetime import datetime
import logging
from urllib.parse import urlparse

app = Flask(__name__)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PDF 저장 디렉토리
PDF_OUTPUT_DIR = os.path.join(tempfile.gettempdir(), 'pdf_generator')
os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)


def is_valid_url(url):
    """URL 유효성 검사"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def generate_pdf_from_url(url, options=None):
    """
    Playwright를 사용하여 URL을 PDF로 변환

    Args:
        url: 변환할 웹 페이지 URL
        options: PDF 생성 옵션 (dict)

    Returns:
        생성된 PDF 파일 경로
    """
    if options is None:
        options = {}

    # 기본 옵션 설정
    pdf_options = {
        'format': options.get('format', 'A4'),
        'print_background': options.get('print_background', True),
        'margin': {
            'top': options.get('margin_top', '1cm'),
            'right': options.get('margin_right', '1cm'),
            'bottom': options.get('margin_bottom', '1cm'),
            'left': options.get('margin_left', '1cm'),
        }
    }

    # 고유한 파일명 생성
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    pdf_filename = f'pdf_{timestamp}.pdf'
    pdf_path = os.path.join(PDF_OUTPUT_DIR, pdf_filename)

    try:
        with sync_playwright() as p:
            # 브라우저 실행 (headless 모드)
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # URL 로드
            logger.info(f"Loading URL: {url}")
            page.goto(url, wait_until='networkidle', timeout=30000)

            # PDF 생성
            logger.info(f"Generating PDF: {pdf_path}")
            page.pdf(path=pdf_path, **pdf_options)

            browser.close()

        return pdf_path

    except Exception as e:
        logger.error(f"PDF generation failed: {str(e)}")
        raise


@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@app.route('/api/generate-pdf', methods=['POST'])
def api_generate_pdf():
    """PDF 생성 API 엔드포인트"""
    try:
        data = request.get_json()

        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400

        url = data['url']

        # URL 유효성 검사
        if not is_valid_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400

        # URL이 http/https로 시작하는지 확인
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # 옵션 가져오기
        options = data.get('options', {})

        logger.info(f"Generating PDF for URL: {url}")

        # PDF 생성
        pdf_path = generate_pdf_from_url(url, options)

        # 파일명 생성 (URL 기반)
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace('.', '_')
        download_filename = f'{domain}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'

        # PDF 파일 전송
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=download_filename
        )

    except Exception as e:
        logger.error(f"Error in PDF generation: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health_check():
    """헬스 체크 엔드포인트"""
    return jsonify({'status': 'healthy', 'service': 'PDF Generator'}), 200


if __name__ == '__main__':
    # 개발 서버 실행
    app.run(host='0.0.0.0', port=5000, debug=True)
