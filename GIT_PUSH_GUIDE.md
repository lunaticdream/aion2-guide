# 🚀 최신 파일 일괄 Git 푸시 가이드

## 📦 필수 파일 목록 (Railway 배포용)

```
aion2-guide/
├── aion2_backend_server.py    (백엔드 서버)
├── index.html                  (프론트엔드)
├── requirements.txt            (Python 패키지)
├── Procfile                    (Railway 실행 명령)
├── runtime.txt                 (Python 버전)
├── .gitignore                  (Git 제외 파일)
└── README.md                   (프로젝트 설명)
```

---

## ⚡ 방법 1: 한 번에 푸시 (가장 빠름!)

### Step 1: 로컬 폴더 정리

**현재 폴더의 모든 기존 파일 삭제:**

```
1. Windows 탐색기에서 aion2-guide 폴더 열기
2. 다음 파일들만 남기고 전부 삭제:
   - .git 폴더 (숨김, 삭제 금지!)
   - .gitignore
```

### Step 2: 새 파일들 복사

**다운로드한 최신 파일을 폴더에 복사:**

```
✅ aion2_backend_server.py
✅ index.html
✅ requirements.txt
✅ Procfile
✅ runtime.txt
✅ .gitignore (덮어쓰기)
✅ README.md (선택)
```

### Step 3: Git 일괄 푸시

**VS Code 터미널 (Ctrl + `)에서:**

```bash
# 1. 모든 변경사항 확인
git status

# 2. 모든 파일 추가
git add .

# 3. 커밋
git commit -m "Fix: Update all files to latest version"

# 4. 푸시
git push origin main
```

**완료!** 🎉

---

## ⚡ 방법 2: 강제 재설정 (확실!)

### Step 1: .git 제외 모두 삭제

```bash
# PowerShell
Get-ChildItem -Exclude .git | Remove-Item -Recurse -Force
```

**또는 탐색기에서:**
```
.git 폴더 빼고 전부 선택 → Delete
```

### Step 2: 새 파일 복사

**다운로드한 파일 전부 복사**

### Step 3: 푸시

```bash
git add .
git commit -m "Complete refresh with latest files"
git push -f origin main
```

---

## 📋 단계별 상세 가이드

### 1. 현재 상태 백업

```bash
# 현재 폴더 이름 변경 (안전)
# 탐색기에서: aion2-guide → aion2-guide-old
```

### 2. 새 폴더에서 시작

```bash
# PowerShell
cd Documents
mkdir aion2-guide-new
cd aion2-guide-new
```

### 3. Git 초기화

```bash
git init
git remote add origin https://github.com/YOUR_USERNAME/aion2-guide.git
git branch -M main
```

### 4. 최신 파일 복사

**다운로드한 파일을 aion2-guide-new에 복사**

### 5. 일괄 푸시

```bash
git add .
git commit -m "Fresh start with latest files"
git push -f origin main
```

### 6. VS Code로 열기

```bash
code .
```

---

## 🎯 Git 명령어 완전 정리

### 기본 워크플로우:

```bash
# 1. 상태 확인
git status

# 2. 모든 파일 추가
git add .

# 3. 커밋 (메시지 작성)
git commit -m "메시지"

# 4. 푸시
git push origin main
```

### 특정 파일만 추가:

```bash
# 파일 하나
git add index.html

# 여러 파일
git add index.html aion2_backend_server.py requirements.txt

# 모든 Python 파일
git add *.py

# 모든 변경사항
git add .
```

### 파일 삭제:

```bash
# Git에서만 제거 (로컬 파일 유지)
git rm --cached filename.txt

# Git과 로컬 모두 삭제
git rm filename.txt

# 폴더 삭제
git rm -r foldername/
```

### 변경사항 취소:

```bash
# 파일 변경 취소
git checkout -- filename.txt

# 모든 변경 취소
git reset --hard

# 커밋 취소 (1개)
git reset --soft HEAD~1
```

---

## 🔧 VS Code에서 GUI로 푸시

### 방법 1: Source Control 사용

```
1. 왼쪽 Git 아이콘 (세 번째) 클릭
2. Changes에서 모든 파일 확인
3. "+" 버튼 (Stage All Changes)
4. 위쪽 입력창에 메시지: "Update files"
5. "✓" 버튼 (Commit)
6. "..." 메뉴 → "Push"
```

### 방법 2: GitHub Desktop

```
1. GitHub Desktop 실행
2. Changes 탭에서 파일 확인
3. Summary: "Update all files"
4. "Commit to main" 버튼
5. "Push origin" 버튼
```

---

## 📊 각 파일의 역할

### 필수 파일:

**aion2_backend_server.py**
```
Flask 백엔드 서버
API 엔드포인트 처리
Anthropic API 호출
```

**index.html**
```
프론트엔드 UI
React 컴포넌트
사용자 인터페이스
```

**requirements.txt**
```
Python 패키지 목록
Railway가 자동 설치
```

**Procfile**
```
Railway 실행 명령어
gunicorn으로 서버 시작
```

**runtime.txt**
```
Python 버전 지정
python-3.11
```

**.gitignore**
```
Git에서 제외할 파일
.env, __pycache__ 등
```

---

## ✅ 푸시 전 체크리스트

### 파일 확인:
- [ ] aion2_backend_server.py (최신 버전)
- [ ] index.html (최신 버전)
- [ ] requirements.txt (anthropic>=0.40.0 포함)
- [ ] Procfile (정확한 내용)
- [ ] runtime.txt (python-3.11)
- [ ] .gitignore (민감 정보 보호)

### Git 설정:
- [ ] git remote -v 확인 (올바른 URL)
- [ ] git status 확인 (변경사항 확인)
- [ ] git log 확인 (커밋 히스토리)

### Railway 확인:
- [ ] Variables에 ANTHROPIC_API_KEY
- [ ] 환경변수 4개 모두 설정
- [ ] 이전 배포 로그 확인

---

## 🚨 주의사항

### 1. .env 파일 푸시 금지!

```bash
# .gitignore에 반드시 포함
.env
.env.local
```

**실수로 푸시했다면:**
```bash
git rm --cached .env
git commit -m "Remove .env"
git push
```

### 2. API 키 노출 확인

```bash
# 파일에서 API 키 검색
grep -r "sk-ant-api" .

# 있으면 안됨!
```

### 3. 대용량 파일 주의

```bash
# 100MB 이상 파일은 Git LFS 사용
git lfs install
git lfs track "*.psd"
```

---

## 🔍 푸시 후 확인

### 1. GitHub 웹사이트

```
https://github.com/YOUR_USERNAME/aion2-guide

✅ 파일 목록 확인
✅ 최신 커밋 확인
✅ 커밋 시간 확인
```

### 2. Railway 재배포

```
Railway → Deployments
✅ 새 배포 자동 시작
✅ 3-5분 대기
✅ "Success" 확인
```

### 3. 로그 확인

```
Railway → View Logs
✅ 에러 없음
✅ "Listening at: http://0.0.0.0:5000"
```

### 4. 웹사이트 테스트

```
https://your-app.up.railway.app
✅ 페이지 로드
✅ 캐릭터 검색
✅ AI 분석 작동
```

---

## 💡 자주 하는 실수

### 실수 1: Procfile 파일명 오타

```
❌ procfile (소문자)
❌ Procfile.txt (확장자)
✅ Procfile (정확히)
```

### 실수 2: 인코딩 문제

```bash
# PowerShell에서 UTF-8로 저장
[System.IO.File]::WriteAllText("Procfile", "web: gunicorn...", [System.Text.Encoding]::UTF8)
```

### 실수 3: 줄바꿈 문제

```bash
# Windows CRLF → Unix LF 변환
git config --global core.autocrlf true
```

---

## 🆘 트러블슈팅

### "rejected - non-fast-forward"

```bash
# 강제 푸시
git push -f origin main
```

### "remote: Permission denied"

```bash
# URL 확인
git remote -v

# HTTPS로 변경
git remote set-url origin https://github.com/USER/REPO.git
```

### "Nothing to commit"

```bash
# 변경사항 확인
git status

# 파일 추가 확인
git add .
```

---

## 📈 성공 확인

### 전체 플로우:

```
1. 로컬 파일 최신화 ✅
   ↓
2. Git 푸시 완료 ✅
   ↓
3. GitHub 파일 확인 ✅
   ↓
4. Railway 자동 배포 ✅
   ↓
5. 로그 확인 (에러 없음) ✅
   ↓
6. 웹사이트 작동 ✅
```

---

## 🎯 빠른 명령어 모음

### 완전 초기화:

```bash
rm -rf .git
git init
git remote add origin https://github.com/USER/REPO.git
git branch -M main
git add .
git commit -m "Fresh start"
git push -f origin main
```

### 일반 푸시:

```bash
git add .
git commit -m "Update files"
git push origin main
```

### 강제 푸시:

```bash
git add .
git commit -m "Force update"
git push -f origin main
```

---

**이제 최신 파일을 다운로드하고 위 가이드대로 푸시하세요!** 🚀

**파일은 다음 메시지에서 제공하겠습니다!** 📦
