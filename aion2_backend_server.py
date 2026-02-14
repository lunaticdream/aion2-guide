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
        
        # 장비와 스탯 정보를 간결하게 요약
        equipment_summary = str(equipment)[:500] if equipment else "정보 없음"
        stats_summary = str(stats)[:300] if stats else "정보 없음"
        
        prompt = f"""아이온2 전문 코치로서 '아툴 점수' 향상 분석을 해주세요.

# 캐릭터
{name} / {class_name} / Lv.{level} / 전투력 {combat_power:,}

# 데이터
장비: {equipment_summary}
스탯: {stats_summary}

# 아툴 점수 시스템
1. 전투력 (최우선)
2. 장비 등급/강화/세트
3. 스킬 완성도
4. 수집품 (펫, 변신체)
5. 영혼각인
6. 특성 강화

# 분석 요청 (간결하게)

## 1. 현재 평가
- 추정 아툴 점수: X,XXX점
- 동급 대비: 상위 XX%
- 강점 2가지
- 약점 2가지

## 2. 아툴 점수 향상 TOP 5

### 1순위: [항목]
현재 → 목표 / 방법 / 아툴점수 +XX / 기간

### 2순위: [항목]
현재 → 목표 / 방법 / 아툴점수 +XX / 기간

### 3순위: [항목]
현재 → 목표 / 방법 / 아툴점수 +XX / 기간

### 4순위: [항목]
현재 → 목표 / 방법 / 아툴점수 +XX / 기간

### 5순위: [항목]
현재 → 목표 / 방법 / 아툴점수 +XX / 기간

## 3. 로드맵
- 1주: +XX점 (일일 필수)
- 1개월: +YY점 (주간 목표)
- 3개월: +ZZ점 (최종 목표)

## 4. 핵심 팁
- 가성비 최고 루트 1가지
- 피해야 할 함정 1가지

**중요**: 모든 수치는 구체적으로, 실행 가능한 내용만"""

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
