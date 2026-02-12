# 아이온2 전투력 향상 AI 가이드 - 배포 가이드

## 목차
1. [로컬 개발 환경 설정](#로컬-개발-환경-설정)
2. [Docker를 이용한 배포](#docker를-이용한-배포)
3. [클라우드 배포](#클라우드-배포)
4. [모니터링 및 유지보수](#모니터링-및-유지보수)

---

## 로컬 개발 환경 설정

### 1. 사전 준비
```bash
# Git clone
git clone https://github.com/yourusername/aion2-power-guide.git
cd aion2-power-guide

# Python 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 환경변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 수정 (중요!)
nano .env
```

`.env` 파일 예시:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
```

### 3. 개발 서버 실행

#### Backend
```bash
python aion2_backend_server.py
# http://localhost:5000 에서 실행
```

#### Frontend
```bash
# 간단한 HTTP 서버
python -m http.server 8000
# http://localhost:8000/aion2-power-guide.html 접속
```

---

## Docker를 이용한 배포

### 1. Docker 설치
- Windows/Mac: [Docker Desktop](https://www.docker.com/products/docker-desktop) 설치
- Linux: 
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### 2. 환경변수 설정
```bash
# .env 파일 생성 및 수정
cp .env.example .env
nano .env
```

### 3. Docker Compose로 전체 스택 실행
```bash
# 컨테이너 빌드 및 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 상태 확인
docker-compose ps
```

### 4. 서비스 접속
- Frontend: http://localhost
- Backend API: http://localhost/api
- Redis: localhost:6379

### 5. 컨테이너 관리
```bash
# 중지
docker-compose stop

# 재시작
docker-compose restart

# 삭제
docker-compose down

# 볼륨까지 삭제
docker-compose down -v
```

---

## 클라우드 배포

### AWS EC2 배포

#### 1. EC2 인스턴스 생성
- Ubuntu 22.04 LTS 선택
- t3.small 이상 권장
- 보안 그룹: HTTP(80), HTTPS(443), SSH(22) 포트 오픈

#### 2. 서버 접속 및 설정
```bash
# SSH 접속
ssh -i your-key.pem ubuntu@your-ec2-ip

# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 3. 애플리케이션 배포
```bash
# 코드 클론
git clone https://github.com/yourusername/aion2-power-guide.git
cd aion2-power-guide

# 환경변수 설정
nano .env

# 실행
docker-compose up -d
```

#### 4. 도메인 연결 (선택사항)
```bash
# Nginx 설정 수정
nano nginx.conf
# server_name을 실제 도메인으로 변경

# Let's Encrypt로 SSL 인증서 발급
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com

# 인증서를 Docker 볼륨에 복사
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/key.pem

# 재시작
docker-compose restart nginx
```

### Google Cloud Platform (GCP) 배포

#### 1. Cloud Run 사용 (서버리스)
```bash
# gcloud CLI 설치 및 인증
gcloud auth login

# 프로젝트 설정
gcloud config set project YOUR_PROJECT_ID

# Docker 이미지 빌드
docker build -t gcr.io/YOUR_PROJECT_ID/aion2-backend .

# Container Registry에 푸시
docker push gcr.io/YOUR_PROJECT_ID/aion2-backend

# Cloud Run에 배포
gcloud run deploy aion2-backend \
  --image gcr.io/YOUR_PROJECT_ID/aion2-backend \
  --platform managed \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your-key
```

#### 2. Compute Engine 사용 (VM)
- AWS EC2와 유사한 방식으로 배포
- Ubuntu 이미지 선택
- Docker 설치 후 동일한 절차

### Heroku 배포 (간단한 방법)

#### 1. Heroku CLI 설치
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. 배포
```bash
# 로그인
heroku login

# 앱 생성
heroku create aion2-power-guide

# 환경변수 설정
heroku config:set ANTHROPIC_API_KEY=your-key

# Git 배포
git push heroku main

# 로그 확인
heroku logs --tail
```

---

## 모니터링 및 유지보수

### 1. 로깅

#### 애플리케이션 로그
```bash
# Docker 로그 확인
docker-compose logs -f backend

# 특정 시간 이후 로그
docker-compose logs --since 1h backend

# 로그 파일 직접 확인
tail -f logs/app.log
```

#### Nginx 액세스 로그
```bash
docker-compose exec nginx tail -f /var/log/nginx/access.log
```

### 2. 성능 모니터링

#### Docker 리소스 사용량
```bash
docker stats
```

#### 시스템 리소스
```bash
# CPU, 메모리 사용량
htop

# 디스크 사용량
df -h

# 네트워크 트래픽
iftop
```

### 3. 헬스체크
```bash
# API 헬스체크
curl http://localhost/health

# 자동화된 헬스체크 스크립트
while true; do
  curl -f http://localhost/health || echo "서비스 다운!"
  sleep 60
done
```

### 4. 백업

#### Redis 데이터 백업
```bash
# 수동 백업
docker-compose exec redis redis-cli SAVE

# 백업 파일 복사
docker cp aion2-redis:/data/dump.rdb ./backup/

# 자동 백업 스크립트 (cron)
0 2 * * * docker-compose exec redis redis-cli SAVE && \
  docker cp aion2-redis:/data/dump.rdb /backup/redis-$(date +\%Y\%m\%d).rdb
```

### 5. 업데이트 절차
```bash
# 1. 코드 가져오기
git pull origin main

# 2. 새 이미지 빌드
docker-compose build

# 3. 서비스 재시작 (무중단)
docker-compose up -d --no-deps backend

# 4. 헬스체크
curl http://localhost/health
```

### 6. 모니터링 도구 추가 (선택사항)

#### Prometheus + Grafana
```yaml
# docker-compose.yml에 추가
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
```

---

## 트러블슈팅

### 문제 1: API 키 오류
```
해결: .env 파일에 올바른 ANTHROPIC_API_KEY가 설정되었는지 확인
```

### 문제 2: CORS 오류
```
해결: nginx.conf의 CORS 설정 확인 또는 Backend의 CORS 설정 확인
```

### 문제 3: 메모리 부족
```
해결: 
1. Docker 메모리 제한 증가
2. Redis 메모리 정책 설정 (maxmemory-policy)
3. 더 큰 인스턴스로 업그레이드
```

### 문제 4: 연결 타임아웃
```
해결:
1. Nginx timeout 설정 증가
2. Backend timeout 설정 증가
3. 크롤링 delay 조정
```

---

## 보안 체크리스트

- [ ] API 키를 환경변수로 관리
- [ ] .env 파일을 .gitignore에 추가
- [ ] HTTPS 설정 (프로덕션)
- [ ] Rate Limiting 활성화
- [ ] CORS 설정 검토
- [ ] 정기적인 보안 업데이트
- [ ] 로그 민감 정보 마스킹
- [ ] 백업 암호화

---

## 성능 최적화 팁

1. **Redis 캐싱 활용**
   - 동일 캐릭터 조회 시 캐시 사용
   - TTL 적절히 설정 (1시간 권장)

2. **CDN 사용**
   - 프론트엔드 정적 파일은 CDN으로 서빙
   - Cloudflare 무료 플랜 활용 가능

3. **이미지 최적화**
   - WebP 포맷 사용
   - Lazy loading 적용

4. **데이터베이스 인덱싱**
   - 추후 DB 도입 시 적절한 인덱스 생성

5. **API 응답 압축**
   - Gzip 압축 활성화 (Nginx 설정에 포함됨)

---

## 라이센스 및 주의사항

- 이 프로젝트는 교육 목적으로 제공됩니다
- NC소프트의 이용약관을 준수하세요
- 크롤링 시 서버에 과부하를 주지 마세요
- 개인정보 보호법을 준수하세요

---

**문의사항이 있으시면 GitHub Issues를 이용해주세요!**
