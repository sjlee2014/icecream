# 🚀 빠른 시작 가이드

## 최소 요구사항

- Docker & Docker Compose (권장)
- 또는:
  - Python 3.11+
  - Node.js 18+
  - PostgreSQL 15+

## ⚡ 5분 안에 시작하기

### 1. 저장소 클론
```bash
git clone <repository-url>
cd icecream
```

### 2. Docker Compose로 실행
```bash
docker-compose up -d
```

### 3. 브라우저에서 열기
```
http://localhost:3000
```

### 4. 첫 스크래핑 실행
1. 대시보드에서 "스크래핑 시작" 버튼 클릭
2. 잠시 기다리면 상품 데이터가 수집됩니다
3. 트렌딩, 베스트셀러 등의 탭에서 데이터 확인

## 🎯 주요 기능 사용법

### 스크래핑 실행
```bash
# API로 직접 실행
curl -X POST http://localhost:8000/scraper/run

# 또는 대시보드 UI에서 버튼 클릭
```

### 데이터 확인
```bash
# 전체 통계
curl http://localhost:8000/products/stats

# 트렌딩 상품
curl http://localhost:8000/products/trending

# 베스트셀러
curl http://localhost:8000/products/best-sellers
```

### 서비스 중지
```bash
docker-compose down
```

### 데이터 초기화
```bash
docker-compose down -v  # 볼륨도 함께 삭제
docker-compose up -d
```

## 🔍 로그 확인

```bash
# 모든 서비스 로그
docker-compose logs -f

# 특정 서비스만
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

## 💡 팁

1. **첫 실행 시**: 데이터베이스 초기화에 몇 초가 걸릴 수 있습니다
2. **스크래핑 시간**: 사이트 크기에 따라 1-5분 정도 소요됩니다
3. **디버깅**: `data/debug_page.html`에서 스크래핑한 페이지 구조를 확인할 수 있습니다
4. **API 문서**: http://localhost:8000/docs 에서 전체 API를 테스트할 수 있습니다

## 🆘 문제 해결

### "Container exited" 오류
```bash
# 로그 확인
docker-compose logs backend

# 컨테이너 재시작
docker-compose restart
```

### 포트 충돌
```bash
# docker-compose.yml에서 포트 변경
ports:
  - "3001:80"  # 3000 대신 3001 사용
  - "8001:8000"  # 8000 대신 8001 사용
```

### 데이터베이스 연결 실패
```bash
# PostgreSQL 상태 확인
docker-compose ps postgres

# 재시작
docker-compose restart postgres backend
```

## 📚 다음 단계

- [전체 README](README.md) - 상세 문서
- [API 문서](http://localhost:8000/docs) - 실시간 API 테스트
- 프로젝트 커스터마이징하기
