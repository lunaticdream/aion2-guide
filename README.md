# 아이온2 전투력 향상 AI 가이드 시스템

NC소프트의 아이온2 공식 API(또는 크롤링)를 활용하여 캐릭터 정보를 조회하고, AI(Claude)가 맞춤형 전투력 향상 전략을 제공하는 웹 서비스입니다.

## 📋 주요 기능

### 1. 캐릭터 정보 조회
- 캐릭터 이름으로 검색
- 서버별 검색 지원
- 실시간 캐릭터 정보 조회
  - 기본 정보 (레벨, 직업, 전투력)
  - 장비 정보 (무기, 방어구, 악세서리)
  - 스탯 정보 (공격력, 방어력, 치명타 등)
  - 스티그마 정보
  - 펫 컬렉션
  - 영혼 각인

### 2. AI 전투력 분석
- Claude AI 기반 심층 분석
- 개인화된 전투력 향상 전략 제공
- 우선순위별 실행 계획
- 예상 전투력 증가량 산출
- 필요 재화/시간 예측

### 3. 대화형 Q&A
- 캐릭터 관련 추가 질문 가능
- 컨텍스트 기반 맞춤 답변
- 대화 히스토리 유지

## 🛠 기술 스택

### Frontend
- **React 18**: UI 프레임워크
- **Tailwind CSS**: 스타일링
- **Anthropic API**: Claude AI 통합

### Backend
- **Flask**: Python 웹 프레임워크
- **BeautifulSoup4**: 웹 크롤링
- **Anthropic Python SDK**: AI 분석
- **Flask-CORS**: CORS 처리

## 📦 설치 및 실행

### 사전 요구사항
- Python 3.8 이상
- Node.js (프론트엔드 개발 시)
- Anthropic API 키

### 1. 백엔드 설치

```bash
# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 필요한 패키지 설치
pip install flask flask-cors requests beautifulsoup4 anthropic

# 환경변수 설정
export ANTHROPIC_API_KEY="your-api-key-here"

# 서버 실행
python aion2_backend_server.py
```

서버가 `http://localhost:5000`에서 실행됩니다.

### 2. 프론트엔드 실행

#### 방법 1: HTML 파일 직접 실행 (간단)
- `aion2-power-guide.html` 파일을 웹브라우저로 열기
- 단, 백엔드 API 연동을 위해서는 CORS 설정 필요

#### 방법 2: 로컬 서버로 실행 (권장)
```bash
# Python의 간단한 HTTP 서버 사용
python -m http.server 8000

# 브라우저에서 접속
# http://localhost:8000/aion2-power-guide.html
```

## 🔌 API 엔드포인트

### 1. 캐릭터 검색
```http
POST /api/character/search
Content-Type: application/json

{
  "characterName": "캐릭터이름",
  "server": "서버이름"  // 선택사항
}
```

**응답:**
```json
{
  "name": "캐릭터이름",
  "server": "서버1",
  "level": 70,
  "class": "검투사",
  "combatPower": 12450,
  "equipment": { ... },
  "stats": { ... },
  "skills": { ... },
  "petCollection": { ... },
  "soulEngraving": { ... }
}
```

### 2. AI 분석
```http
POST /api/character/analyze
Content-Type: application/json

{
  "name": "캐릭터이름",
  "class": "검투사",
  "combatPower": 12450,
  ...
}
```

**응답:**
```json
{
  "analysis": "## 1. 현재 상태 평가\n강점:\n- ...\n\n## 2. 전투력 향상 우선순위\n..."
}
```

### 3. 추가 질문
```http
POST /api/character/question
Content-Type: application/json

{
  "characterData": { ... },
  "question": "펫 컬렉션을 빠르게 올리는 방법은?",
  "conversationHistory": [ ... ]  // 선택사항
}
```

## 🎯 사용 시나리오

### 시나리오 1: 신규 유저
```
1. 캐릭터 검색으로 현재 상태 확인
2. AI 분석으로 기초 가이드 받기
3. "초보자가 가장 먼저 해야 할 일은?" 질문
4. 단계별로 실행
```

### 시나리오 2: 중급 유저
```
1. 캐릭터 검색
2. AI 분석으로 전투력 병목 지점 파악
3. "무기와 방어구 중 어느 것을 먼저 강화?" 질문
4. 우선순위에 따라 집중 투자
```

### 시나리오 3: 고급 유저
```
1. 여러 캐릭터 비교 분석
2. 세부 스탯 최적화 질문
3. "영혼 각인 옵션 재작업 우선순위는?" 질문
4. 효율적인 리소스 배분
```

## 🔧 커스터마이징

### 1. 크롤링 대상 변경
`aion2_backend_server.py`의 `Aion2CharacterCrawler` 클래스를 수정하여 실제 크롤링 로직을 구현하세요.

```python
def search_character(self, character_name, server=None):
    # 실제 크롤링 코드 작성
    # 옵션 1: 공식 홈페이지 크롤링
    # 옵션 2: 비공식 API 활용 (aion2tool.com 등)
    pass
```

### 2. AI 분석 프롬프트 수정
`_build_analysis_prompt` 메서드를 수정하여 분석 내용을 조정할 수 있습니다.

```python
def _build_analysis_prompt(self, data):
    prompt = f"""
    # 원하는 분석 형식으로 프롬프트 작성
    """
    return prompt
```

### 3. UI 테마 변경
`aion2-power-guide.html`의 Tailwind CSS 클래스를 수정하여 색상 테마를 변경할 수 있습니다.

## ⚠️ 주의사항

### 법적 고려사항
1. **이용약관 준수**: NC소프트의 이용약관을 확인하고 준수하세요
2. **robots.txt 확인**: 크롤링 시 robots.txt 규칙을 따라야 합니다
3. **요청 제한**: 과도한 요청으로 서버에 부담을 주지 마세요
4. **개인정보 보호**: 타인의 캐릭터 정보를 무단으로 수집/공개하지 마세요

### 기술적 고려사항
1. **API 키 보안**: API 키를 절대 코드에 하드코딩하지 마세요
2. **에러 처리**: 네트워크 오류, API 오류 등을 적절히 처리하세요
3. **캐싱**: 동일한 캐릭터 정보 반복 조회 시 캐싱 활용 권장
4. **Rate Limiting**: API 호출 횟수 제한 구현 필요

## 🚀 향후 개선 계획

### Phase 1: 기본 기능 (현재)
- [x] 캐릭터 정보 조회
- [x] AI 분석 기능
- [x] 대화형 Q&A

### Phase 2: 고급 기능
- [ ] 공식 API 연동 (출시 시)
- [ ] 캐릭터 비교 기능
- [ ] 진행 상황 추적
- [ ] 알림 기능 (목표 달성 시)

### Phase 3: 커뮤니티 기능
- [ ] 사용자 등록/로그인
- [ ] 분석 결과 공유
- [ ] 커뮤니티 팁 게시판
- [ ] 랭킹 시스템

### Phase 4: 모바일 앱
- [ ] React Native 앱 개발
- [ ] 푸시 알림
- [ ] 위젯 지원

## 📊 성능 최적화

### 백엔드 최적화
```python
# Redis 캐싱 예시
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

def search_character_cached(character_name, server):
    cache_key = f"char:{server}:{character_name}"
    cached = r.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    data = crawler.search_character(character_name, server)
    r.setex(cache_key, 3600, json.dumps(data))  # 1시간 캐시
    return data
```

### 프론트엔드 최적화
- React.memo로 불필요한 리렌더링 방지
- debounce로 검색 입력 최적화
- lazy loading으로 초기 로딩 속도 개선

## 🤝 기여 방법

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이센스

이 프로젝트는 교육 및 개인 사용 목적으로 제공됩니다. 
상업적 사용 전에 NC소프트의 이용약관을 확인하시기 바랍니다.

## 💬 문의 및 지원

- 이슈 제보: GitHub Issues
- 기능 요청: GitHub Discussions
- 이메일: support@example.com

## 🙏 감사의 말

- NC소프트의 아이온2 게임
- Anthropic의 Claude AI
- 아이온2 커뮤니티

---

**면책 조항**: 이 도구는 비공식 프로젝트이며 NC소프트와 관련이 없습니다. 
게임 데이터 사용 시 공식 정책을 준수하시기 바랍니다.
