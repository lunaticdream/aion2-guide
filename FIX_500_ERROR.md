# 🔥 Railway 500 에러 즉시 해결

## 🎯 현재 상황

```
POST /api/character/analyze → 500 Internal Server Error
```

배포는 성공했지만 API 호출 시 500 에러 발생

---

## ⚡ 즉시 실행 (5분 해결!)

### Step 1: Railway Variables 확인 (가장 중요!)

```
Railway → Variables 탭

반드시 있어야 할 4개:
✅ ANTHROPIC_API_KEY = sk-ant-api03-xxxxxxxxxxxxx
✅ FLASK_ENV = production  
✅ SECRET_KEY = your-secret-key-here
✅ PORT = 5000
```

**없으면 추가하고 2-3분 대기 (자동 재배포)**

### Step 2: Railway 로그 확인

```
Deployments → View Logs

찾을 에러:
❌ KeyError: 'ANTHROPIC_API_KEY'
❌ AuthenticationError
❌ ModuleNotFoundError
❌ AttributeError
```

**에러 발견 시 → 복사해서 알려주세요!**

### Step 3: 최신 파일로 재배포

**다운로드한 파일을 GitHub에 푸시:**

```bash
# VS Code 터미널
git add .
git commit -m "Fix: Latest files"
git push origin main
```

**Railway 자동 재배포 확인 (3분)**

---

## 🔍 가능한 원인 (우선순위별)

### 1. ANTHROPIC_API_KEY 없음 (90%)

**증상:**
```
Railway Logs:
ANTHROPIC_API_KEY environment variable is not set
```

**해결:**
```
Railway → Variables → New Variable
Name: ANTHROPIC_API_KEY
Value: sk-ant-api03-xxxxx
→ Add
```

### 2. API 키 잘못됨 (5%)

**증상:**
```
AuthenticationError: Invalid API key
```

**해결:**
```
1. https://console.anthropic.com
2. API Keys → Create Key
3. 새 키 복사
4. Railway Variables에서 업데이트
```

### 3. 크레딧 소진 (3%)

**확인:**
```
https://console.anthropic.com → Usage
잔액 확인
```

### 4. 코드 오류 (2%)

**증상:**
```
SyntaxError, AttributeError, ImportError
```

**해결:**
```
제공한 최신 파일로 교체
```

---

## 🚀 완전 재배포 (확실한 방법)

### 단계 1: 로컬 폴더 정리

```
1. 현재 폴더 백업
   aion2-guide → aion2-guide-old

2. 새 폴더 생성
   mkdir aion2-guide
```

### 단계 2: 최신 파일 복사

**다운로드한 6개 파일:**
```
✅ aion2_backend_server.py
✅ index.html
✅ requirements.txt
✅ Procfile
✅ runtime.txt
✅ .gitignore
```

### 단계 3: Git 설정

```bash
cd aion2-guide
git init
git remote add origin https://github.com/YOUR_USERNAME/aion2-guide.git
git branch -M main
```

### 단계 4: 푸시

```bash
git add .
git commit -m "Complete refresh"
git push -f origin main
```

### 단계 5: Railway 확인

```
1. Variables 설정 (4개)
2. 재배포 확인 (3-5분)
3. 로그 확인
4. 테스트
```

---

## 📋 체크리스트

### Railway 설정:
- [ ] ANTHROPIC_API_KEY 있음 (sk-ant-api03로 시작)
- [ ] FLASK_ENV = production
- [ ] SECRET_KEY 있음
- [ ] PORT = 5000

### GitHub 파일:
- [ ] aion2_backend_server.py (최신)
- [ ] index.html (최신)
- [ ] requirements.txt (anthropic>=0.40.0)
- [ ] Procfile 정확
- [ ] runtime.txt (python-3.11)

### 배포 상태:
- [ ] Deployments → Success
- [ ] Logs → 에러 없음
- [ ] /health → 200 OK

---

## 🔧 디버깅 명령어

### /health 테스트:

```bash
# PowerShell
Invoke-WebRequest https://your-app.up.railway.app/health

# 또는 브라우저
https://your-app.up.railway.app/health
```

**응답:**
```json
{"status": "healthy"}
```

### /api 테스트:

```
https://your-app.up.railway.app/api
```

**응답:**
```json
{
  "name": "Aion2 Power Guide API",
  "endpoints": {...}
}
```

---

## 💡 Git 일괄 푸시 (요약)

### 방법 1: 간단하게

```bash
git add .
git commit -m "Update"
git push origin main
```

### 방법 2: 강제로

```bash
git add .
git commit -m "Force update"
git push -f origin main
```

### 방법 3: 완전 초기화

```bash
rm -rf .git
git init
git remote add origin https://github.com/USER/REPO.git
git branch -M main
git add .
git commit -m "Fresh start"
git push -f origin main
```

---

## 🎯 즉시 실행 순서

```
1. 📦 파일 다운로드 (7개 파일)
   ↓
2. 📁 로컬 폴더에 복사 (기존 파일 교체)
   ↓
3. 💻 Git 푸시
   git add .
   git commit -m "Fix 500 error"
   git push origin main
   ↓
4. ⚙️ Railway Variables 확인 (ANTHROPIC_API_KEY)
   ↓
5. 🚀 재배포 대기 (3-5분)
   ↓
6. 📝 로그 확인 (에러 없는지)
   ↓
7. ✅ 테스트 (웹사이트 작동)
```

---

## 🆘 여전히 500 에러?

**다음 정보를 보내주세요:**

### 1. Railway Logs

```
Deployments → View Logs → 전체 복사
특히 "ERROR", "Failed", "exception" 포함된 줄
```

### 2. Railway Variables

```
Variables 탭 스크린샷
(API 키는 앞 10자만)
```

### 3. GitHub 파일 목록

```
저장소 메인 페이지 스크린샷
```

### 4. /health 응답

```
https://your-app.up.railway.app/health
→ 응답 복사
```

---

## ✅ 성공 확인

### 모든 단계 OK:

```
✅ Railway Variables 4개 설정
✅ GitHub 파일 푸시 완료
✅ Railway 배포 Success
✅ Logs에 에러 없음
✅ /health → 200 OK
✅ 웹사이트 로드
✅ AI 분석 작동!
```

---

**지금 바로 실행:**

```bash
# 1. 파일 다운로드
# 2. 로컬 복사
# 3. Git 푸시
git add .
git commit -m "Fix 500 error"
git push origin main

# 4. Railway Variables 확인
# 5. 테스트!
```

**막히는 부분 있으면 바로 알려주세요!** 🚀
