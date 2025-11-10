# 🚀 배포 가이드

## 현재 상황

현재 개발 환경에서는 **네트워크 제한**으로 인해 외부 사이트(i-screammall.co.kr) 접속이 불가능합니다.
**실제 스크래핑을 실행하려면 로컬 컴퓨터나 클라우드 서버에 배포해야 합니다.**

---

## 📍 배포 옵션

### 옵션 1: 로컬 컴퓨터에서 실행 (권장 - 테스트용)

가장 간단한 방법입니다. 자세한 내용은 `LOCAL_SETUP_GUIDE.md`를 참조하세요.

**요약:**
```bash
# 1. 가상환경 설정
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 의존성 설치
pip install -r backend/requirements.txt
playwright install chromium

# 3. 백엔드 실행
python -m uvicorn backend.main:app --reload

# 4. 프론트엔드 실행 (새 터미널)
cd frontend
npm install
npm run dev

# 5. 스크래핑 테스트
python test_local_scraper.py
```

---

### 옵션 2: Docker로 배포

#### 로컬 Docker

```bash
# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 스크래핑 실행
curl -X POST http://localhost:8000/scraper/run

# 서비스 중지
docker-compose down
```

#### Docker Swarm/Kubernetes

프로덕션 배포를 위한 Kubernetes 매니페스트:

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: icecream-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: icecream-backend
  template:
    metadata:
      labels:
        app: icecream-backend
    spec:
      containers:
      - name: backend
        image: your-registry/icecream-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
---
apiVersion: v1
kind: Service
metadata:
  name: icecream-backend
spec:
  selector:
    app: icecream-backend
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

---

### 옵션 3: 클라우드 배포

#### AWS (Elastic Beanstalk)

```bash
# EB CLI 설치
pip install awsebcli

# 초기화
eb init -p python-3.11 icecream-scraper

# 생성 및 배포
eb create icecream-prod
eb deploy
```

#### Heroku

```bash
# Procfile 생성
echo "web: uvicorn backend.main:app --host=0.0.0.0 --port=\$PORT" > Procfile

# 배포
heroku create icecream-scraper
git push heroku main
```

#### DigitalOcean App Platform

```yaml
# .do/app.yaml
name: icecream-scraper
services:
- name: backend
  github:
    repo: your-username/icecream
    branch: main
  build_command: pip install -r backend/requirements.txt
  run_command: uvicorn backend.main:app --host 0.0.0.0 --port 8080
  envs:
  - key: DATABASE_URL
    value: ${db.DATABASE_URL}

- name: frontend
  github:
    repo: your-username/icecream
    branch: main
  build_command: cd frontend && npm install && npm run build
  static_sites:
  - source: frontend/dist
    route: /

databases:
- name: db
  engine: PG
```

#### Google Cloud Run

```bash
# 백엔드 배포
gcloud run deploy icecream-backend \
  --source ./backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# 프론트엔드 배포 (Firebase Hosting)
cd frontend
npm run build
firebase deploy
```

---

### 옵션 4: VPS 서버 (Ubuntu)

```bash
# 1. 서버 접속
ssh user@your-server-ip

# 2. 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 3. 필수 패키지 설치
sudo apt install -y python3-pip python3-venv nginx postgresql

# 4. 프로젝트 클론
git clone <repository-url>
cd icecream

# 5. Python 환경 설정
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
playwright install chromium
playwright install-deps

# 6. PostgreSQL 설정
sudo -u postgres psql
CREATE DATABASE icecream_db;
CREATE USER icecream WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE icecream_db TO icecream;
\q

# 7. 환경 변수 설정
nano .env
# DATABASE_URL=postgresql://icecream:your-password@localhost/icecream_db

# 8. Systemd 서비스 생성
sudo nano /etc/systemd/system/icecream.service
```

```ini
[Unit]
Description=Icecream Scraper API
After=network.target

[Service]
User=your-user
WorkingDirectory=/home/your-user/icecream
Environment="PATH=/home/your-user/icecream/venv/bin"
ExecStart=/home/your-user/icecream/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 9. 서비스 시작
sudo systemctl enable icecream
sudo systemctl start icecream

# 10. Nginx 설정
sudo nano /etc/nginx/sites-available/icecream
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        root /home/your-user/icecream/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

```bash
# 11. Nginx 활성화
sudo ln -s /etc/nginx/sites-available/icecream /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 12. 프론트엔드 빌드
cd frontend
npm install
npm run build

# 13. 크론 작업 설정 (자동 스크래핑)
crontab -e
# 매일 오전 9시에 스크래핑
0 9 * * * /home/your-user/icecream/venv/bin/python /home/your-user/icecream/test_local_scraper.py
```

---

## 🔒 보안 고려사항

### 프로덕션 환경 설정

1. **시크릿 키 변경**
   ```bash
   # Python으로 랜덤 키 생성
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **환경 변수 보안**
   - `.env` 파일을 절대 Git에 커밋하지 마세요
   - 클라우드 서비스의 Secret Manager 사용

3. **CORS 설정**
   ```python
   # backend/core/config.py
   CORS_ORIGINS = [
       "https://yourdomain.com",
       "https://www.yourdomain.com",
   ]
   ```

4. **Rate Limiting**
   ```python
   # backend/main.py
   from slowapi import Limiter
   from slowapi.util import get_remote_address

   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter

   @app.get("/products/")
   @limiter.limit("100/minute")
   async def get_products():
       ...
   ```

5. **HTTPS 활성화**
   ```bash
   # Let's Encrypt 사용
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

---

## 📊 모니터링

### 로그 설정

```python
# backend/core/logging.py
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10000000,
    backupCount=5
)
logging.basicConfig(handlers=[handler], level=logging.INFO)
```

### Sentry 통합 (에러 추적)

```bash
pip install sentry-sdk
```

```python
# backend/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

---

## 🎯 성능 최적화

### 데이터베이스

- PostgreSQL 사용 (SQLite 대신)
- 인덱스 추가
- Connection pooling

### 캐싱

```python
# Redis 캐싱
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="icecream-cache")

@app.get("/products/")
@cache(expire=3600)  # 1시간 캐싱
async def get_products():
    ...
```

### 비동기 작업 큐

```python
# Celery 사용
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
def scrape_task():
    # 스크래핑 로직
    pass
```

---

## ✅ 배포 체크리스트

- [ ] 환경 변수 설정 완료
- [ ] 시크릿 키 변경
- [ ] PostgreSQL/MySQL 설정 (프로덕션용)
- [ ] HTTPS 활성화
- [ ] CORS 도메인 제한
- [ ] Rate limiting 설정
- [ ] 로그 설정
- [ ] 에러 모니터링 (Sentry 등)
- [ ] 백업 시스템 구축
- [ ] 크론 작업 설정 (자동 스크래핑)
- [ ] 성능 테스트
- [ ] 보안 감사

---

## 📞 지원

문제가 발생하면:
1. `LOCAL_SETUP_GUIDE.md` 참조
2. GitHub Issues 등록
3. 로그 파일 확인 (`logs/app.log`)

---

**참고**: 실제 배포 전에 테스트 환경에서 충분히 테스트하세요!
