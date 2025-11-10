# 🍦 아이스크림몰 상품 분석 시스템

i-screammall.co.kr의 상품 정보를 스크래핑하고 분석하는 풀스택 웹 애플리케이션입니다.

## 📋 주요 기능

- **자동 웹 스크래핑**: Playwright를 사용한 동적 페이지 크롤링
- **실시간 데이터 분석**: 인기 상품, 베스트셀러, 신상품, 세일 상품 트렌드 분석
- **대시보드 UI**: 직관적인 상품 정보 시각화
- **REST API**: FastAPI 기반 고성능 백엔드
- **PostgreSQL 데이터베이스**: 안정적인 데이터 저장 및 관리
- **Docker 지원**: 간편한 배포 및 확장

## 🏗️ 기술 스택

### Backend
- **FastAPI**: 고성능 Python 웹 프레임워크
- **SQLAlchemy**: ORM 및 데이터베이스 관리
- **Playwright**: 동적 웹 스크래핑
- **PostgreSQL**: 관계형 데이터베이스
- **Pydantic**: 데이터 검증

### Frontend
- **React**: UI 라이브러리
- **Vite**: 빌드 도구
- **Axios**: HTTP 클라이언트
- **Recharts**: 데이터 시각화

### DevOps
- **Docker & Docker Compose**: 컨테이너화
- **Nginx**: 리버스 프록시 및 정적 파일 서빙

## 📁 프로젝트 구조

```
icecream/
├── backend/
│   ├── api/
│   │   ├── products.py       # 상품 API 엔드포인트
│   │   └── scraper.py        # 스크래퍼 제어 API
│   ├── core/
│   │   ├── config.py         # 설정 관리
│   │   └── database.py       # 데이터베이스 연결
│   ├── models/
│   │   ├── product.py        # 상품 모델
│   │   └── scrape_log.py     # 스크래핑 로그 모델
│   ├── scraper/
│   │   └── icecream_scraper.py  # Playwright 스크래퍼
│   ├── main.py               # FastAPI 앱
│   └── requirements.txt      # Python 의존성
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js     # API 클라이언트
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ProductGrid.jsx
│   │   │   ├── StatsOverview.jsx
│   │   │   └── ScraperControl.jsx
│   │   ├── App.jsx
│   │   └── App.css
│   └── package.json
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

## 🚀 시작하기

### 방법 1: Docker Compose (권장)

가장 간단한 방법으로 모든 서비스를 한 번에 실행할 수 있습니다.

```bash
# 프로젝트 클론
git clone <repository-url>
cd icecream

# Docker Compose로 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

서비스가 시작되면:
- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432

### 방법 2: 로컬 개발 환경

#### Backend 설정

```bash
# Python 가상환경 생성 및 활성화
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# Playwright 브라우저 설치
playwright install chromium

# PostgreSQL 데이터베이스 생성
createdb icecream_db

# 환경 변수 설정
cp ../.env.example ../.env
# .env 파일을 편집하여 DATABASE_URL 등을 설정

# 서버 실행
cd ..
python -m uvicorn backend.main:app --reload
```

#### Frontend 설정

```bash
# 새 터미널에서
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

## 📖 사용 방법

### 1. 스크래핑 실행

대시보드에서 "스크래핑 시작" 버튼을 클릭하여 i-screammall.co.kr에서 상품 정보를 수집합니다.

### 2. 데이터 확인

- **트렌딩 상품**: 판매량, 조회수, 평점을 기반으로 한 인기 상품
- **베스트셀러**: 판매량 기준 상위 상품
- **신상품**: 최근 추가된 상품
- **세일 상품**: 할인 중인 상품

### 3. API 사용

#### 상품 목록 조회
```bash
curl http://localhost:8000/products/
```

#### 통계 조회
```bash
curl http://localhost:8000/products/stats
```

#### 트렌딩 상품
```bash
curl http://localhost:8000/products/trending?limit=20
```

#### 스크래핑 시작
```bash
curl -X POST http://localhost:8000/scraper/run
```

#### 스크래핑 로그 조회
```bash
curl http://localhost:8000/scraper/logs
```

자세한 API 문서는 http://localhost:8000/docs 에서 확인할 수 있습니다.

## 🔧 환경 변수

`.env` 파일에서 다음 환경 변수를 설정할 수 있습니다:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/icecream_db

# API
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Scraper
SCRAPER_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
SCRAPER_HEADLESS=true
SCRAPER_INTERVAL_HOURS=6
```

## 🗄️ 데이터베이스 스키마

### Products 테이블
- 상품 ID, 이름, 카테고리
- 가격, 할인율
- 이미지 URL
- 상태 플래그 (신상품, 베스트, 세일)
- 인기 메트릭 (조회수, 판매량, 리뷰, 평점)
- 타임스탬프

### ScrapeLog 테이블
- 스크래핑 상태
- 수집된 상품 수
- 시작/완료 시간
- 에러 정보

## 🛠️ 개발

### 백엔드 테스트
```bash
cd backend
pytest
```

### 프론트엔드 빌드
```bash
cd frontend
npm run build
```

### 코드 포맷팅
```bash
# Backend (Black)
black backend/

# Frontend (Prettier)
cd frontend
npm run format
```

## 🐛 문제 해결

### 스크래핑이 작동하지 않는 경우

1. **Playwright 브라우저 확인**
   ```bash
   playwright install chromium
   ```

2. **사이트 구조 변경 확인**
   - `backend/scraper/icecream_scraper.py`의 CSS 셀렉터를 업데이트해야 할 수 있습니다
   - `data/debug_page.html` 파일을 확인하여 실제 페이지 구조를 분석하세요

3. **Headless 모드 비활성화**
   ```bash
   # .env 파일에서
   SCRAPER_HEADLESS=false
   ```

### 데이터베이스 연결 오류

1. PostgreSQL이 실행 중인지 확인
   ```bash
   # Docker
   docker-compose ps

   # 로컬
   pg_isready
   ```

2. DATABASE_URL이 올바른지 확인
   ```bash
   echo $DATABASE_URL
   ```

### 프론트엔드가 백엔드에 연결되지 않는 경우

1. CORS 설정 확인 (`backend/core/config.py`)
2. API URL 확인 (`frontend/.env`)
3. 백엔드가 실행 중인지 확인

## 📊 성능 최적화

- **스크래핑 간격**: `SCRAPER_INTERVAL_HOURS`로 자동 스크래핑 주기 설정
- **캐싱**: Nginx를 통한 정적 파일 캐싱
- **데이터베이스 인덱스**: 주요 쿼리 필드에 인덱스 설정
- **페이지네이션**: API에서 대량의 데이터를 효율적으로 처리

## 🔒 보안 고려사항

- 환경 변수를 통한 민감 정보 관리
- SQL Injection 방지 (SQLAlchemy ORM)
- CORS 설정으로 허용된 도메인만 접근
- Rate limiting 구현 권장 (프로덕션)

## 📝 라이선스

이 프로젝트는 교육 및 개인 사용 목적으로 만들어졌습니다.

## 🤝 기여

이슈와 Pull Request는 언제나 환영합니다!

## 📮 연락처

문의사항이나 제안사항이 있으시면 이슈를 등록해주세요.

---

**참고**: 이 도구는 i-screammall.co.kr의 robots.txt 정책을 준수해야 하며,
과도한 스크래핑은 서버에 부담을 줄 수 있으므로 적절한 간격을 두고 사용해주세요.
