from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import json
import os
from urllib.parse import quote

# Anthropic import
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Warning: Anthropic SDK not available")

app = Flask(__name__, static_folder='.')
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

def get_anthropic_client():
    """Anthropic 클라이언트를 안전하게 생성"""
    if not ANTHROPIC_AVAILABLE:
        raise Exception("Anthropic SDK is not installed")
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise Exception("ANTHROPIC_API_KEY environment variable is not set")
    
    return Anthropic(api_key=api_key)


class Aion2APIClient:
    """아이온2 공식 API 클라이언트"""
    
    BASE_URL = "https://aion2.plaync.com/api"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://aion2.plaync.com/',
            'Accept': 'application/json'
        })
    
    def get_character_info(self, character_id, server_id):
        """캐릭터 기본 정보"""
        # URL을 직접 구성 (인코딩하지 않음)
        url = f"{self.BASE_URL}/character/info?lang=ko&characterId={character_id}&serverId={server_id}"
        
        print(f"=== Character Info API Request ===")
        print(f"Character ID (raw): {character_id}")
        print(f"Server ID: {server_id}")
        print(f"Full URL: {url}")
        
        response = self.session.get(url, timeout=10)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response URL (actual): {response.url}")
        
        response.raise_for_status()
        return response.json()
    
    def get_character_equipment(self, character_id, server_id):
        """캐릭터 장비 정보"""
        # URL을 직접 구성 (인코딩하지 않음)
        url = f"{self.BASE_URL}/character/equipment?lang=ko&characterId={character_id}&serverId={server_id}"
        
        print(f"=== Character Equipment API Request ===")
        print(f"Full URL: {url}")
        
        response = self.session.get(url, timeout=10)
        print(f"Response Status: {response.status_code}")
        
        response.raise_for_status()
        return response.json()
    
    def search_character(self, keyword, race, server_id, page=1, size=30):
        """캐릭터 검색
        
        Args:
            keyword: 캐릭터 이름
            race: 1 (천족 light) 또는 2 (마족 dark)
            server_id: 서버 ID
            page: 페이지 번호
            size: 결과 개수
        """
        url = "https://aion2.plaync.com/ko-kr/api/search/aion2/search/v2/character"
        params = {
            'keyword': keyword,
            'race': race,
            'serverId': server_id,
            'page': page,
            'size': size
        }
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def get_servers(self):
        """서버 목록"""
        url = f"{self.BASE_URL}/gameinfo/servers"
        params = {'lang': 'ko'}
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()


class Aion2PowerAnalyzer:
    """AI 기반 전투력 분석기"""
    
    def __init__(self):
        pass
    
    def _build_analysis_prompt(self, character_data):
        """분석 프롬프트 구성"""
        
        name = character_data.get('name', '알 수 없음')
        level = character_data.get('level', 0)
        class_name = character_data.get('class', '알 수 없음')
        combat_power = character_data.get('combatPower', 0)
        equipment = character_data.get('equipment', {})
        stats = character_data.get('stats', {})
        info = character_data.get('info', {})
        
        # 장비와 스탯 정보
        equipment_str = json.dumps(equipment, ensure_ascii=False, indent=2)[:1000] if equipment else "정보 없음"
        stats_str = json.dumps(stats, ensure_ascii=False, indent=2)[:500] if stats else "정보 없음"
        info_str = json.dumps(info, ensure_ascii=False, indent=2)[:1500] if info else "정보 없음"
        
        prompt = f"""당신은 아이온2 전문가입니다. **아툴 점수 계산 로직**을 정확히 이해하고 분석하세요.

# 아이온2 게임 기본 정보

## 레벨 시스템
- **최대 레벨: 45레벨** (절대 75레벨 아님!)
- 만렙 = 45레벨

## 전투력 범위 (45레벨)
- 중수: 12,000 ~ 18,000
- 고수: 18,000 ~ 25,000
- 초고수: 25,000 ~ 35,000

---

# 아툴 점수 산출 핵심 원칙 (aion2tool.com)

## 1. PVE DPS 중심
**생존력(방어, 생명력) < 화력(공격력, 피해량 증폭)**
- 방어구 강화는 점수 영향 매우 낮음
- 무기/가더 강화가 압도적으로 중요

## 2. 부위별 차등 가중치
**우선순위 (높음 → 낮음):**
```
1순위: 무기, 가더 (1.5배 가중치)
2순위: 장신구 (목걸이, 귀걸이, 반지) (1.0배)
3순위: 스티그마, 영혼각인 (0.8배)
4순위: 방어구 (상의, 하의, 장갑, 신발, 허리, 투구, 어깨) (최하)
```

## 3. 계단식 성장
**특정 구간 도달 시 보너스 점수 폭등:**
- 장비 돌파: 15강 → 20강 시 점수 급상승
- 스티그마: 5, 10, 15, 20레벨 등 특성 활성화 시 대폭 증가

---

# 세부 로직 및 가중치

## 1. 장비 돌파 (강화)

### 무기/가더 (최고 가중치 1.5x)
- +10 → +15: 점수 +500~800
- +15 → +20: 점수 +1,000~1,500 (폭등!)
- **가장 효율적인 투자처**

### 장신구 (중간 가중치 1.0x)
- +10 → +15: 점수 +300~500
- 세트 효과보다 개별 돌파 수치가 중요
- 목걸이 > 귀걸이 > 반지 순

### 방어구 (최하 가중치)
- +10 → +15: 점수 +50~100
- +15 → +20: 점수 +100~200
- **투자 대비 효율 매우 낮음 (후순위)**

## 2. 영혼 각인

### 등급별 배점
- **S급**: +300~500점 (최상)
- **A급**: +150~300점 (상)
- **B급**: +50~150점 (중)

### 유효 옵션 (가산점)
- **PVE 피해 증폭**: +200~300점
- **무기 피해 증폭**: +150~250점
- **공격력**: +100~200점
- **치명타 피해 증폭**: +100~150점

## 3. 스티그마/스킬

### 임계점 로직 (계단식)
- **5레벨**: +100~200점 (추가 특성 활성화)
- **10레벨**: +300~500점 (중요 특성)
- **15레벨**: +500~800점 (강력 특성)
- **20레벨**: +800~1,200점 (최종 특성)

### 주력 스킬 우선
- 데바이온/아르카나 강화 시 가산점
- 전체 레벨 합산보다 **주력 스킬 집중 육성**이 효율적

## 4. 스탯 가중치 (PVE DPS 중심)

### 1순위 (핵심 스탯) - 1.2배 가중치
- **PVE 피해 증폭**: 최우선!
- **무기 피해 증폭**: 최우선!
- **강타 확률**: 매우 중요
- **다단 히트 적중**: 매우 중요

### 2순위 (일반 스탯) - 1.0배
- 공격력
- 명중
- 치명타 피해 증폭
- 전투 속도

### 3순위 (저효율 스탯) - 0.3배
- 생명력
- 방어력
- 막기
- 회피
- 저항

## 5. 내실 및 기타

### 제작 아이템
- 동일 성능이라도 제작(Crafted) 착용 시: **+200~300점**

### 타이틀
- 상위 티어 타이틀 (나생문 등): +100~200점

### 만신전
- 지혜 스탯 통한 공격 효율: +50~100점

---

# 아툴 점수 계산 공식

```
Score = (무기×1.5) + (가더×1.5) + (장신구×1.0) + 
        (영혼각인×0.8) + (스티그마×0.8) + 
        (PVE스탯×1.2) + (방어구×0.3) + 보너스
```

## 실제 점수 범위 (45레벨)
- 하위: 5,000 ~ 8,000
- 중하위: 8,000 ~ 12,000
- 중위: 12,000 ~ 16,000
- 중상위: 16,000 ~ 20,000
- 상위: 20,000 ~ 25,000

---

# 분석 대상 캐릭터

**{name}** / {class_name} / Lv.{level}/45 / 전투력 {combat_power:,}

```
Info: {info_str}
Equipment: {equipment_str}
Stats: {stats_str}
```

---

# 분석 요청

**위의 아툴 점수 계산 로직을 정확히 적용하여** 분석하세요.

## 1. 아툴 점수 분석

### 현재 점수 계산
- **무기/가더 점수** (×1.5): XXX점
- **장신구 점수** (×1.0): XXX점
- **영혼각인 점수** (×0.8): XXX점
- **스티그마 점수** (×0.8): XXX점
- **PVE스탯 점수** (×1.2): XXX점
- **방어구 점수** (×0.3): XXX점
- **보너스**: XXX점
- **총 아툴 점수**: X,XXX점

### 백분위
- 상위 XX% (45레벨 기준)

## 2. 점수 향상 우선순위 TOP 5

**효율 높은 순서로 정렬:**

### 1순위: [무기/가더 강화 등]
- 현재: +X
- 목표: +Y
- 이유: 가중치 1.5배로 가장 효율적
- 아툴 점수: +XXX점
- 기간: X주

### 2순위: [PVE 피해 증폭 등]
- 현재: X%
- 목표: Y%
- 이유: 1순위 핵심 스탯
- 아툴 점수: +XXX점
- 기간: X주

### 3~5순위:
(계속 효율 순서로)

## 3. 효율 비교

### 투자 대비 점수 효율
- 무기 +1 강화 = 아툴 +XX점 (최고효율!)
- 스티그마 5레벨 = 아툴 +XX점
- 방어구 +1 강화 = 아툴 +XX점 (비효율)

### 피해야 할 것
- 방어구 강화 우선 투자 (점수 낮음)
- 생존 스탯 집중 (가중치 0.3배)

## 4. 로드맵

- **1주**: 1순위 시작 → +XXX점
- **1개월**: 1~3순위 → X,XXX점 도달
- **3개월**: 최종 → X,XXX점 목표

---

**원칙:**
- 무기/가더 최우선
- PVE 피해 증폭 핵심
- 방어구는 후순위
- 계단식 성장 활용"""

        return prompt
    
    def analyze_character(self, character_data):
        """캐릭터 분석"""
        prompt = self._build_analysis_prompt(character_data)
        
        try:
            client = get_anthropic_client()
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,  # 간결한 분석에 적합
                temperature=1,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            raise Exception(f"AI 분석 실패: {str(e)}")


# 클라이언트 초기화
api_client = Aion2APIClient()
analyzer = Aion2PowerAnalyzer()


@app.route('/')
def index():
    """메인 페이지"""
    try:
        html_files = ['index.html', 'aion2-power-guide.html']
        for html_file in html_files:
            if os.path.exists(html_file):
                return send_file(html_file)
        return "<h1>아이온2 AI 가이드 API</h1><p>정상 작동 중</p>"
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route('/health')
def health():
    """헬스체크"""
    return jsonify({'status': 'healthy'})


@app.route('/api/character/search', methods=['POST'])
def search_character():
    """캐릭터 검색"""
    try:
        data = request.get_json()
        
        print("=== Character Search Request ===")
        print(f"Request Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        keyword = data.get('keyword')
        race = data.get('race')  # 1: 천족, 2: 마족
        server_id = data.get('serverId')
        
        print(f"Keyword: {keyword}")
        print(f"Race: {race}")
        print(f"Server ID: {server_id}")
        
        if not keyword or not race or not server_id:
            error_msg = 'keyword, race, serverId required'
            print(f"❌ Validation Error: {error_msg}")
            return jsonify({'success': False, 'error': error_msg}), 400
        
        # 검색 API 호출
        print(f"Calling search API...")
        result = api_client.search_character(keyword, race, server_id)
        
        print(f"Search API Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        print("=== Search Error ===")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        import traceback
        print(f"Traceback:\n{traceback.format_exc()}")
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/gameinfo/servers', methods=['GET'])
def get_servers():
    """서버 목록"""
    try:
        url = "https://aion2.plaync.com/api/gameinfo/servers"
        params = {'lang': 'ko'}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://aion2.plaync.com/',
            'Accept': 'application/json'
        }
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print("=== Server List API Response ===")
        print(f"Type: {type(data)}")
        print(f"Keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
        print(f"Full Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        # 응답 그대로 반환 (프론트엔드에서 파싱)
        return jsonify(data)
        
    except Exception as e:
        print(f"Error fetching servers: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # 에러 시 빈 객체 반환
        return jsonify({'error': str(e), 'servers': []}), 500


@app.route('/api/character/fetch', methods=['POST'])
def fetch_character():
    """캐릭터 정보 가져오기"""
    try:
        data = request.get_json()
        
        print("=== Character Fetch Request ===")
        print(f"Request Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        character_id = data.get('characterId')
        server_id = data.get('serverId')
        
        print(f"Character ID: {character_id}")
        print(f"Server ID: {server_id}")
        
        if not character_id or not server_id:
            error_msg = 'characterId and serverId required'
            print(f"❌ Validation Error: {error_msg}")
            return jsonify({'success': False, 'error': error_msg}), 400
        
        # API 호출
        print("Fetching character info...")
        char_info = api_client.get_character_info(character_id, server_id)
        print(f"✓ Character Info: {json.dumps(char_info, indent=2, ensure_ascii=False)}")
        
        print("Fetching character equipment...")
        char_equipment = api_client.get_character_equipment(character_id, server_id)
        print(f"✓ Character Equipment: {json.dumps(char_equipment, indent=2, ensure_ascii=False)}")
        
        return jsonify({
            'success': True,
            'info': char_info,
            'equipment': char_equipment
        })
        
    except Exception as e:
        print("=== Fetch Character Error ===")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        import traceback
        print(f"Traceback:\n{traceback.format_exc()}")
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/character/analyze', methods=['POST'])
def analyze_character():
    """AI 분석"""
    try:
        data = request.get_json()
        print("=== Analysis request ===")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        analysis = analyzer.analyze_character(data)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        print(f"=== ERROR: {str(e)} ===")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
