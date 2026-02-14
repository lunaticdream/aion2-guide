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
        
        prompt = f"""당신은 아이온2 전문가입니다. 다음 **정확한 게임 정보**를 반드시 따라주세요:

# 아이온2 게임 기본 정보 (절대 틀리면 안됨!)

## 레벨 시스템
- **현재 최대 레벨: 45레벨** (절대 75레벨 아님!)
- 만렙 캐릭터 = 45레벨
- 45레벨 이상은 존재하지 않음

## 전투력 시스템 (45레벨 기준)
- 입문: 5,000 ~ 8,000
- 초보: 8,000 ~ 12,000
- 중수: 12,000 ~ 18,000
- 고수: 18,000 ~ 25,000
- 초고수: 25,000 ~ 35,000
- 최강자: 35,000+

## 장비 시스템
- 등급: 일반(회색) < 고급(녹색) < 희귀(파랑) < 영웅(보라) < 전설(주황)
- 강화: +0 ~ +20
- 세트 효과: 2세트, 4세트, 6세트
- 주요 부위: 무기, 상의, 하의, 장갑, 신발, 어깨, 투구, 허리, 목걸이, 귀걸이(2), 반지(2)

## 스킬 시스템
- 일반 스킬: 자동 습득
- **스티그마 스킬**: 별도 습득 필요 (총 10개 슬롯)
- 스티그마 완성도 = 습득 개수 / 10

---

# 아툴 점수 계산 공식 (aion2tool.com 기준)

## 점수 구성 비율
1. **전투력**: 40% (가장 중요!)
2. **장비 점수**: 25%
3. **스킬 완성도**: 15%
4. **수집품**: 10%
5. **영혼각인**: 5%
6. **기타**: 5%

## 실제 점수 범위 (45레벨 기준)
- 하위 10%: 5,000 ~ 7,000점
- 하위 30%: 7,000 ~ 10,000점
- 중위 40%: 10,000 ~ 14,000점
- 상위 20%: 14,000 ~ 18,000점
- 상위 5%: 18,000 ~ 22,000점
- 상위 1%: 22,000점+

## 전투력 → 아툴 점수 대응표 (현실적인 수치)
```
전투력 8,000  → 아툴 약 6,000 ~ 7,000
전투력 10,000 → 아툴 약 7,500 ~ 9,000
전투력 12,000 → 아툴 약 9,000 ~ 11,000
전투력 15,000 → 아툴 약 11,000 ~ 13,500
전투력 18,000 → 아툴 약 13,500 ~ 16,000
전투력 20,000 → 아툴 약 15,000 ~ 17,500
전투력 25,000 → 아툴 약 18,000 ~ 21,000
전투력 30,000 → 아툴 약 21,000 ~ 24,000
```

## 점수 향상 효과 (경험치)
- 장비 +1 강화 → 전투력 +150~300, 아툴 +50~100
- 장비 등급업 → 전투력 +1,000~2,000, 아툴 +300~600
- 스티그마 1개 습득 → 전투력 +150~300, 아툴 +100~200
- 펫 1마리 수집 → 전투력 +50~100, 아툴 +30~50

---

# 분석 대상 캐릭터

**이름**: {name}
**직업**: {class_name}
**레벨**: {level}/45 (만렙 {'' if level == 45 else '아님'})
**전투력**: {combat_power:,}

## API 데이터
```
Info: {info_str}

Equipment: {equipment_str}

Stats: {stats_str}
```

---

# 분석 지침

**반드시 지켜야 할 규칙:**
1. 최대 레벨은 45레벨입니다 (절대 75레벨 언급 금지!)
2. 아툴 점수는 위의 전투력 대응표를 **정확히** 참고
3. 점수 향상 예측은 위의 효과표 기준으로만 계산
4. 추측 금지 - 제공된 데이터만 사용
5. 모든 수치는 현실적이고 달성 가능한 범위로

---

# 요청 분석

## 1. 현재 상태 평가

### 아툴 점수 추정
- **추정 점수**: X,XXX점 (위 대응표 참고하여 정확히)
- **백분위**: 상위 XX% (위 범위표 참고)
- **평가**: 전투력 {combat_power:,} 기준 [평가]

### 강점/약점
- **강점**: (실제 데이터 기반 2가지)
- **약점**: (실제 데이터 기반 2가지)

## 2. 아툴 점수 향상 우선순위 TOP 5

**각 항목 형식:**
### N순위: [구체적 항목명]
- 현재: [실제 수치]
- 목표: [달성 가능한 수치]
- 방법: [1-2문장으로 간단히]
- 아툴 점수: +XXX점 (위 효과표 기준으로 계산)
- 기간: X주

**(가장 효율 높은 순서로 정렬)**

## 3. 단계별 로드맵

- **1주 후**: 현재 X,XXX → X,XXX점 (+XXX)
- **1개월 후**: X,XXX → X,XXX점 (+XXX)
- **3개월 후**: X,XXX → X,XXX점 (+XXX)

## 4. 핵심 조언 (각 1줄)

- **가성비 팁**: 
- **주의사항**:

---

**다시 한번 강조**: 
- 최대 레벨 = 45레벨
- 아툴 점수는 전투력 대응표 정확히 사용
- 모든 수치는 현실적으로"""

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
