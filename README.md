# 🤖 아이스크림몰 고객 상담 챗봇

인터넷 쇼핑몰 판매를 위한 AI 고객 상담 챗봇 시스템입니다.

## ✨ 주요 기능

- **실시간 채팅**: 고객과 즉각적인 소통
- **자동 응답**: FAQ 기반 즉각적인 답변 제공
- **의도 파악**: 고객 질문의 의도를 자동으로 분석
- **빠른 응답 버튼**: 자주 묻는 질문 바로 선택
- **대화 히스토리**: 모든 상담 내역 저장 및 관리
- **FAQ 관리**: 카테고리별 FAQ 관리

### 지원하는 상담 유형

- 📦 상품 문의
- 🛒 주문 방법
- 🚚 배송 조회
- ↩️ 반품/교환
- ⏰ 영업시간/연락처

## 🏗️ 기술 스택

### Backend
- **FastAPI**: Python 웹 프레임워크
- **SQLAlchemy**: ORM 및 데이터베이스 관리
- **SQLite**: 데이터베이스 (PostgreSQL로 변경 가능)
- **WebSocket**: 실시간 통신

### Frontend
- **React**: UI 라이브러리
- **Vite**: 빠른 개발 환경
- **Axios**: HTTP 클라이언트

## 🚀 빠른 시작

### 1. 저장소 클론

```bash
git clone <repository-url>
cd icecream
```

### 2. 백엔드 실행

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r backend/requirements.txt

# 샘플 FAQ 데이터 초기화
python init_sample_data.py

# 서버 실행
python -m uvicorn backend.main:app --reload
```

백엔드는 http://localhost:8000 에서 실행됩니다.

### 3. 프론트엔드 실행

```bash
# 새 터미널에서
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

프론트엔드는 http://localhost:3000 에서 실행됩니다.

## 📖 API 문서

백엔드 실행 후 http://localhost:8000/docs 에서 자동 생성된 API 문서를 확인할 수 있습니다.

## 💡 챗봇 사용 방법

### 고객 입장

1. 웹사이트 접속
2. 채팅 창에서 질문 입력
3. 빠른 응답 버튼 클릭 또는 직접 입력
4. 실시간 답변 확인
5. FAQ 사이드바에서 관련 질문 검색

### 관리자 입장

1. FAQ 관리
   - API를 통해 FAQ 추가/수정/삭제
   - 카테고리별 FAQ 정리

2. 대화 모니터링
   - `/chat/conversations` API로 모든 대화 조회
   - 고객 응대 품질 확인

## ⚙️ 설정 커스터마이징

### 비즈니스 정보 변경

`backend/core/config.py` 파일에서 수정:

```python
BUSINESS_NAME: str = "아이스크림몰"
BUSINESS_HOURS: str = "평일 09:00-18:00"
SUPPORT_EMAIL: str = "support@i-screammall.co.kr"
SUPPORT_PHONE: str = "1588-0000"
```

### 챗봇 응답 커스터마이징

`backend/core/chatbot_engine.py` 파일에서:

- `INTENT_KEYWORDS`: 의도 감지 키워드 추가/수정
- `RESPONSES`: 응답 템플릿 수정

## 📝 라이선스

이 프로젝트는 교육 및 상업적 용도로 자유롭게 사용 가능합니다.

---

**Made with ❤️ for better customer service**
