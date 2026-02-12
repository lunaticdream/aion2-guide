# 🔥 Railway 캐시 문제 완벽 해결 가이드

## ❌ 현재 상황

에러 로그를 보니:
```
POST https://api.anthropic.com/v1/messages
Access to fetch ... has been blocked by CORS policy
```

이것은 **구버전 HTML 파일**이 실행되고 있다는 증거입니다!

새 버전은 이렇게 호출해야 합니다:
```
POST https://your-app.up.railway.app/api/character/analyze
```

## 🔍 심층 원인 분석

### 3가지 가능성:

1. ❌ **GitHub에 HTML 파일이 업데이트 안됨**
2. ❌ **Railway가 구버전을 캐싱**
3. ❌ **브라우저가 구버전을 캐싱**

---

## ✅ 해결 방법 (단계별)

### Step 1: GitHub 파일 확인 (가장 중요!)

**반드시 확인하세요!**

```
1. GitHub 저장소 접속
2. aion2-power-guide.html 클릭
3. "Raw" 버튼 클릭
4. Ctrl+F로 검색: "api.anthropic.com"
```

**결과:**
- ✅ 검색 결과 없음 → GitHub 파일은 올바름
- ❌ 검색 결과 있음 → **다시 교체 필요!**

### Step 2: GitHub에서 완전히 다시 업로드

**기존 방법(Edit)이 안됐다면, 파일을 삭제하고 새로 업로드:**

#### 2-1. 기존 파일 삭제

```
1. GitHub → aion2-power-guide.html 클릭
2. 오른쪽 위 휴지통 아이콘 🗑️ 클릭
3. "Commit changes" 클릭
```

#### 2-2. 새 파일 업로드

```
1. 제가 제공한 aion2-power-guide.html 다운로드
2. GitHub 저장소 메인 → "Add file" → "Upload files"
3. 파일 드래그
4. "Commit changes" 클릭
```

### Step 3: Railway 강제 재배포

**단순 재배포로는 부족합니다!**

#### 방법 A: 환경변수 더미 추가/삭제

```
1. Railway → Variables 탭
2. "New Variable" 클릭
3. FORCE_REBUILD = true
4. "Add" 클릭
5. 재배포 시작 확인
6. 배포 완료 후 FORCE_REBUILD 삭제
```

#### 방법 B: Railway CLI로 강제 재배포

```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 연결
railway link

# 강제 재배포
railway up --force
```

#### 방법 C: Git 강제 푸시

```bash
git commit --allow-empty -m "Force rebuild"
git push
```

### Step 4: 브라우저 캐시 완전 삭제

**단순 새로고침으로는 부족합니다!**

#### Chrome/Edge:

```
1. F12 (개발자 도구)
2. 개발자 도구가 열린 상태에서
3. 새로고침 버튼 우클릭
4. "캐시 비우기 및 강력 새로고침" 선택
```

#### 또는:

```
1. Ctrl + Shift + Delete
2. "캐시된 이미지 및 파일" 체크
3. "데이터 삭제"
4. 브라우저 재시작
```

#### 시크릿 모드로 확인:

```
Ctrl + Shift + N (시크릿 창)
→ URL 접속
→ 여기서도 같은 오류면 서버 문제
→ 정상이면 브라우저 캐시 문제
```

---

## 🔬 디버깅: 어느 파일이 실행되는지 확인

### 브라우저에서 직접 확인:

```
1. F12 (개발자 도구)
2. Sources 탭
3. 왼쪽에서 aion2-power-guide.html 찾기
4. Ctrl+F로 검색: "api.anthropic.com"
```

**결과:**
- ✅ 검색 결과 없음 → 새 버전 로드됨
- ❌ 검색 결과 있음 → **구버전이 캐싱됨!**

### Network 탭에서 확인:

```
1. F12 → Network 탭
2. "Disable cache" 체크 ✅
3. F5 (새로고침)
4. aion2-power-guide.html 클릭
5. Response 탭 확인
```

**Response에서 검색:**
```
Ctrl+F → "api.anthropic.com"
→ 있으면 구버전!
```

---

## 🎯 확실한 해결책 (파일명 변경)

**캐시를 완전히 우회하는 방법:**

### 파일명을 변경하세요!

```
aion2-power-guide.html
→ index.html (또는)
→ aion2-guide-v2.html
```

### 백엔드 코드도 수정:

```python
# aion2_backend_server.py
html_files = [
    'index.html',  # 새 파일명
    'aion2-guide-v2.html',
    'aion2-power-guide.html',
]
```

### GitHub에 업로드:

```
1. 파일명을 index.html로 변경
2. GitHub에 업로드
3. Railway 재배포
4. 캐시 무시됨!
```

---

## 📝 완전 새로 시작 (최종 수단)

**모든 방법이 실패하면:**

### 1. 로컬에 새 폴더 생성

```bash
mkdir aion2-guide-v2
cd aion2-guide-v2
```

### 2. 필수 파일만 복사

```
aion2_backend_server.py (수정된 버전)
index.html (aion2-power-guide.html 이름 변경)
requirements.txt
Procfile
runtime.txt
.gitignore
```

### 3. 새 GitHub 저장소 생성

```
이름: aion2-guide-v2
```

### 4. 업로드

```bash
git init
git add .
git commit -m "Clean rebuild"
git remote add origin https://github.com/USERNAME/aion2-guide-v2.git
git push -u origin main
```

### 5. Railway에서 새 프로젝트

```
1. Railway → New Project
2. aion2-guide-v2 선택
3. 환경변수 설정
4. 배포
```

---

## 🔍 Railway 배포 로그 확인

**정확한 원인 파악:**

```
Railway → Deployments → 최신 배포 → View Logs
```

**확인할 것:**

### 빌드 로그:

```
✅ Copying files...
✅ aion2-power-guide.html
✅ aion2_backend_server.py
```

**파일 목록에 HTML이 있나요?**
- 있음 → 파일은 배포됨
- 없음 → GitHub에 파일이 없음!

### 실행 로그:

```
✅ Starting gunicorn
✅ Listening at: http://0.0.0.0:5000
```

**에러가 없나요?**

---

## 🧪 최종 테스트

### 1. 직접 HTML 파일 요청

```
브라우저에서:
https://your-app.up.railway.app/aion2-power-guide.html
```

**Ctrl+U (소스 보기)**
```
검색: api.anthropic.com
→ 있으면 구버전!
→ 없으면 새 버전!
```

### 2. API 엔드포인트 직접 테스트

```bash
curl -X POST https://your-app.up.railway.app/api/character/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "name": "테스트",
    "class": "검투사", 
    "combatPower": 12000,
    "level": 70,
    "equipment": {"weapon": {"name": "test", "level": 1}},
    "stats": {"attack": 1000, "defense": 500, "hp": 10000, "criticalRate": 10, "criticalDamage": 50, "accuracy": 100, "evasion": 50},
    "skills": {"stigma": [], "completionRate": 0},
    "petCollection": {"wild": 0, "intelligence": 0, "nature": 0, "transformation": 0},
    "soulEngraving": {"weapon": [], "armor": []}
  }'
```

**응답:**
```json
{
  "analysis": "## 1. 현재 상태 평가..."
}
```

**이게 작동하면:**
- ✅ 백엔드는 정상
- ❌ 프론트엔드(HTML) 문제

---

## 📊 체크리스트

### GitHub 확인:
- [ ] aion2-power-guide.html 파일 있음
- [ ] 파일에 "api.anthropic.com" 없음
- [ ] 파일에 "/api/character/analyze" 있음
- [ ] 파일에 "window.location.origin" 있음

### Railway 확인:
- [ ] 배포 상태 "Success"
- [ ] Logs에 HTML 파일 복사됨
- [ ] /health 응답 정상
- [ ] /api/character/analyze 엔드포인트 존재

### 브라우저 확인:
- [ ] 캐시 완전 삭제
- [ ] 시크릿 모드 테스트
- [ ] F12 → Sources에서 파일 확인
- [ ] Network에서 실제 요청 URL 확인

---

## 💡 핵심 포인트

**문제의 근본 원인:**

Railway가 서빙하는 HTML 파일이:
```html
<!-- ❌ 이렇게 되어 있음 (구버전) -->
<script>
fetch("https://api.anthropic.com/v1/messages", ...)
</script>

<!-- ✅ 이렇게 되어야 함 (신버전) -->
<script>
const apiUrl = window.location.origin;
fetch(`${apiUrl}/api/character/analyze`, ...)
</script>
```

**해결:**
1. GitHub에서 파일 완전 교체 (삭제 후 재업로드)
2. Railway 강제 재배포
3. 브라우저 캐시 완전 삭제
4. 또는 파일명 변경 (index.html)

---

## 🆘 제게 알려주세요

**다음 정보를 제공해주시면 정확히 진단할 수 있습니다:**

1. **GitHub Raw 파일 URL**
   ```
   https://raw.githubusercontent.com/USERNAME/aion2-guide/main/aion2-power-guide.html
   ```

2. **Railway 배포 로그** (최근 100줄)

3. **브라우저 F12 → Sources → aion2-power-guide.html 스크린샷**

4. **브라우저 F12 → Network → 실패한 요청 클릭 → 스크린샷**

**이 정보로 정확한 원인을 찾아드릴 수 있습니다!** 😊
