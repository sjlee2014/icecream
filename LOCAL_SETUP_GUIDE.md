# 🏠 로컬 컴퓨터에서 실행하기

현재 환경은 외부 네트워크 접속이 제한되어 실제 스크래핑이 불가능합니다.
**실제로 i-screammall.co.kr을 스크래핑하려면 로컬 컴퓨터에서 실행해야 합니다.**

## 📋 준비물

- Python 3.11+
- Node.js 18+
- Git

## 🚀 설치 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd icecream
```

### 2. 백엔드 설정

```bash
# 가상환경 생성
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 의존성 설치
pip install -r backend/requirements.txt

# Playwright 브라우저 설치
playwright install chromium
```

### 3. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 수정 (필요한 경우)
# DATABASE_URL은 이미 SQLite로 설정되어 있습니다
```

### 4. 프론트엔드 설정

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

### 5. 백엔드 실행

```bash
# 새 터미널에서 (프로젝트 루트 디렉토리)
source venv/bin/activate  # Windows: venv\Scripts\activate

# 서버 실행
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## 🎯 실제 스크래핑 실행

### 방법 1: 대시보드에서 실행

1. 브라우저에서 http://localhost:3000 열기
2. "스크래핑 시작" 버튼 클릭
3. 진행 상황 확인

### 방법 2: API로 직접 실행

```bash
curl -X POST http://localhost:8000/scraper/run
```

### 방법 3: Python 스크립트로 실행

```python
# test_scraper.py
import asyncio
from backend.core.database import SessionLocal
from backend.scraper.improved_scraper import run_improved_scraper

async def main():
    db = SessionLocal()
    try:
        result = await run_improved_scraper(db)
        print(f"Scraped {result.products_scraped} products!")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
```

```bash
python test_scraper.py
```

## 🔍 디버깅 및 문제 해결

### 스크래핑이 데이터를 못 찾는 경우

1. **사이트 구조 확인하기**

```bash
python debug_site_structure.py
```

이 스크립트는 다음 파일들을 생성합니다:
- `data/debug_page.html` - 전체 페이지 HTML
- `data/main_content.html` - 메인 콘텐츠 영역
- `data/debug_screenshot.png` - 페이지 스크린샷

2. **HTML 구조 분석**

`data/debug_page.html` 파일을 열어서:
- 상품 카드의 클래스명 확인
- 상품명, 가격, 이미지가 어떤 태그에 있는지 확인

3. **스크래퍼 셀렉터 수정**

`backend/scraper/improved_scraper.py` 파일에서:

```python
# 상품 리스트 셀렉터 (line ~100)
selectors_to_try = [
    "YOUR_SELECTOR_HERE",  # 실제 사이트 구조에 맞게 수정
    "li.product-item",
    # ... 기타 셀렉터
]

# 상품명 셀렉터 (line ~200)
name_selectors = [
    "YOUR_NAME_SELECTOR",  # 수정
    '.product-name',
    # ... 기타
]

# 가격 셀렉터 (line ~220)
price_selectors = [
    "YOUR_PRICE_SELECTOR",  # 수정
    '.price',
    # ... 기타
]
```

### Headless 모드 비활성화 (디버깅용)

`.env` 파일에서:
```
SCRAPER_HEADLESS=false
```

이렇게 하면 실제 브라우저 창이 열려서 스크래핑 과정을 볼 수 있습니다.

### 로그 확인

백엔드 터미널에서 스크래핑 로그를 실시간으로 확인할 수 있습니다:
```
INFO:backend.scraper.improved_scraper:✓ Found 24 products with: li.product-item
INFO:backend.scraper.improved_scraper:Successfully scraped 24 products
```

## 🎨 프론트엔드 커스터마이징

프론트엔드 코드 수정:
```bash
cd frontend/src

# 컴포넌트 수정
# - components/Dashboard.jsx (메인 대시보드)
# - components/ProductGrid.jsx (상품 그리드)
# - App.css (스타일)
```

변경사항은 자동으로 반영됩니다 (Hot Reload).

## 📊 데이터베이스 확인

SQLite 데이터베이스를 직접 확인하려면:

```bash
# SQLite CLI 사용
sqlite3 data/icecream.db

# 상품 수 확인
SELECT COUNT(*) FROM products;

# 최근 상품 확인
SELECT name, price FROM products ORDER BY created_at DESC LIMIT 10;

# 종료
.quit
```

또는 DB Browser for SQLite 같은 GUI 도구 사용.

## ⚡ 성능 최적화

### 스크래핑 속도 개선

1. **Headless 모드 사용** (기본값)
   - 더 빠르고 리소스를 적게 사용

2. **타임아웃 조정**
   ```python
   # backend/scraper/improved_scraper.py
   self.page.set_default_timeout(10000)  # 10초로 줄이기
   ```

3. **병렬 처리**
   - 여러 카테고리를 동시에 스크래핑
   - 현재는 순차 처리

### 데이터베이스 최적화

PostgreSQL로 전환 (대량 데이터용):
```bash
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/icecream_db
```

## 🐳 Docker로 실행 (선택사항)

로컬에서 Docker가 설치되어 있다면:

```bash
# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 종료
docker-compose down
```

## 📈 자동화 설정

### 크론 작업으로 자동 스크래핑

```bash
# 크론탭 편집
crontab -e

# 매일 오전 9시에 스크래핑
0 9 * * * cd /path/to/icecream && /path/to/venv/bin/python test_scraper.py
```

### 백그라운드 서비스로 실행

systemd 서비스 파일 생성 또는 PM2 사용:

```bash
npm install -g pm2

pm2 start backend/main.py --interpreter python --name icecream-api
pm2 startup
pm2 save
```

## 🆘 자주 하는 질문

**Q: 스크래핑이 너무 느려요**
A: Headless 모드를 사용하고, 타임아웃을 줄이세요. 또는 덜 중요한 페이지는 건너뛰세요.

**Q: 데이터가 수집되지 않아요**
A: `debug_site_structure.py`를 실행해서 실제 HTML 구조를 확인하고, 셀렉터를 수정하세요.

**Q: 특정 카테고리만 스크래핑하고 싶어요**
A: `improved_scraper.py`의 `scrape_product_list()` 함수에서 URL을 카테고리 페이지로 변경하세요.

**Q: 스크래핑이 차단되나요?**
A: 너무 빠르게 요청하면 차단될 수 있습니다. 적절한 딜레이를 추가하세요:
```python
await asyncio.sleep(1)  # 1초 대기
```

## 📞 문제 발생 시

1. GitHub Issues에 문제 등록
2. 다음 정보 포함:
   - 에러 메시지
   - `data/debug_page.html` 파일
   - 스크린샷

---

**참고**: 웹 스크래핑 시 해당 사이트의 `robots.txt`와 이용 약관을 준수하세요.
과도한 요청은 서버에 부담을 줄 수 있으므로 적절한 간격을 두고 실행하세요.
