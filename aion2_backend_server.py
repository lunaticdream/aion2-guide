"""
아이온2 캐릭터 정보 조회 및 AI 전투력 분석 백엔드 서버
Flask + BeautifulSoup + Anthropic API

설치 필요 패키지:
pip install flask flask-cors requests beautifulsoup4 anthropic
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import os

# Anthropic import는 나중에 필요할 때만 사용
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

# Anthropic API 클라이언트는 함수 내에서 초기화 (전역 초기화 제거)
def get_anthropic_client():
    """Anthropic 클라이언트를 안전하게 생성"""
    if not ANTHROPIC_AVAILABLE:
        raise Exception("Anthropic SDK is not installed")
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise Exception("ANTHROPIC_API_KEY environment variable is not set")
    
    return Anthropic(api_key=api_key)


class Aion2CharacterCrawler:
    """아이온2 공식 홈페이지 캐릭터 정보 크롤러"""
    
    BASE_URL = "https://aion2.plaync.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_character(self, character_name, server=None):
        """
        캐릭터 정보 검색
        
        Args:
            character_name: 캐릭터 이름
            server: 서버 이름 (선택사항)
            
        Returns:
            dict: 캐릭터 정보
        """
        try:
            # 실제 크롤링 구현 예시
            # 주의: 실제 사용시 NC소프트 이용약관 및 robots.txt 확인 필요
            
            # 방법 1: 공식 홈페이지 캐릭터 검색 페이지 크롤링
            search_url = f"{self.BASE_URL}/ko-kr/characters/index"
            
            # 방법 2: 비공식 API가 있다면 활용
            # 예: aion2tool.com, aon2.info 등의 API (이용 가능 여부 확인 필요)
            
            # 임시 응답 (실제 구현시 크롤링 결과로 대체)
            character_data = {
                'name': character_name,
                'server': server or '서버1',
                'level': 70,
                'class': '검투사',
                'combatPower': 12450,
                'equipment': {
                    'weapon': {'name': '진룡왕의 대검', 'level': 15, 'grade': '전설'},
                    'armor': {'name': '백룡왕의 흉갑', 'level': 12, 'grade': '전설'},
                    'accessories': [
                        {'slot': '목걸이', 'name': '건룡왕의 목걸이', 'level': 10},
                        {'slot': '귀걸이', 'name': '흑룡왕의 귀걸이', 'level': 8}
                    ]
                },
                'stats': {
                    'attack': 3420,
                    'defense': 2180,
                    'hp': 45600,
                    'criticalRate': 42.5,
                    'criticalDamage': 178.3,
                    'accuracy': 215,
                    'evasion': 168
                },
                'skills': {
                    'stigma': ['강타', '회오리베기', '광폭화', '방패막기'],
                    'completionRate': 75
                },
                'petCollection': {
                    'wild': 68,
                    'intelligence': 52,
                    'nature': 45,
                    'transformation': 38
                },
                'soulEngraving': {
                    'weapon': ['치명타 피해 +15%', '공격력 +120'],
                    'armor': ['방어력 +8%', '체력 +2500']
                }
            }
            
            return character_data
            
        except Exception as e:
            raise Exception(f"캐릭터 검색 실패: {str(e)}")


class Aion2PowerAnalyzer:
    """AI 기반 전투력 분석기"""
    
    def __init__(self):
        """클라이언트는 사용할 때마다 생성"""
        pass
    
    def analyze_character(self, character_data):
        """
        캐릭터 전투력 분석 및 향상 전략 제공
        
        Args:
            character_data: 캐릭터 정보 딕셔너리
            
        Returns:
            str: AI 분석 결과
        """
        
        # 프롬프트 구성
        prompt = self._build_analysis_prompt(character_data)
        
        try:
            # Anthropic 클라이언트 생성
            client = get_anthropic_client()
            
            # Claude API 호출
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # 응답 추출
            analysis = message.content[0].text
            return analysis
            
        except Exception as e:
            raise Exception(f"AI 분석 실패: {str(e)}")
    
    def _build_analysis_prompt(self, data):
        """분석 프롬프트 생성"""
        
        equipment_info = f"""무기: {data['equipment']['weapon']['name']} (+{data['equipment']['weapon']['level']})
갑옷: {data['equipment']['armor']['name']} (+{data['equipment']['armor']['level']})
악세서리: {', '.join([f"{a['slot']}: {a['name']} (+{a['level']})" for a in data['equipment']['accessories']])}"""

        stats_info = f"""공격력: {data['stats']['attack']}
방어력: {data['stats']['defense']}
체력: {data['stats']['hp']:,}
치명타 확률: {data['stats']['criticalRate']}%
치명타 피해: {data['stats']['criticalDamage']}%
명중: {data['stats']['accuracy']}
회피: {data['stats']['evasion']}"""

        prompt = f"""아이온2 게임의 {data['class']} 캐릭터에 대한 전투력 향상 분석을 해주세요.

# 캐릭터 기본 정보
- 이름: {data['name']}
- 서버: {data['server']}
- 레벨: {data['level']}
- 직업: {data['class']}
- 현재 전투력: {data['combatPower']:,}

# 장비 정보
{equipment_info}

# 스탯 정보
{stats_info}

# 스티그마 정보
- 완성도: {data['skills']['completionRate']}%
- 보유 스킬: {', '.join(data['skills']['stigma'])}

# 펫 컬렉션
- 야성: {data['petCollection']['wild']}%
- 지성: {data['petCollection']['intelligence']}%
- 자연: {data['petCollection']['nature']}%
- 변형: {data['petCollection']['transformation']}%

# 영혼 각인
- 무기: {', '.join(data['soulEngraving']['weapon'])}
- 방어구: {', '.join(data['soulEngraving']['armor'])}

다음 형식으로 상세 분석을 제공해주세요:

## 1. 현재 상태 평가
- 강점 3가지
- 약점 3가지
- 전반적인 평가

## 2. 전투력 향상 우선순위 (Top 5)

### 1순위: [항목명]
- 이유: [왜 이게 최우선인지]
- 실행 방법: [구체적인 방법 3-5가지]
- 예상 전투력 증가: [+XXX ~ +XXX]
- 필요 시간/비용: [예상치]

### 2순위: [항목명]
...

(3~5순위도 동일한 형식)

## 3. 단기/중기/장기 로드맵
- 1주일 목표: 
- 1개월 목표:
- 3개월 목표:

## 4. 효율적인 플레이 팁
- 일일 필수 콘텐츠
- 주간 필수 콘텐츠
- 재화 사용 우선순위

## 5. 예상 전투력
- 1개월 후 예상: {data['combatPower'] + 1500:,} (+1,500)
- 3개월 후 예상: {data['combatPower'] + 4000:,} (+4,000)

명확하고 실용적으로 작성해주세요. 게임 용어는 정확하게 사용하고, 숫자는 구체적으로 제시해주세요."""

        return prompt
    
    def answer_question(self, character_data, question, conversation_history=None):
        """
        캐릭터 관련 추가 질문에 답변
        
        Args:
            character_data: 캐릭터 정보
            question: 사용자 질문
            conversation_history: 이전 대화 내역
            
        Returns:
            str: 답변
        """
        
        # 컨텍스트 구성
        context = f"""현재 분석 중인 캐릭터:
- 이름: {character_data['name']}
- 직업: {character_data['class']}
- 전투력: {character_data['combatPower']:,}
- 레벨: {character_data['level']}"""

        messages = []
        
        # 대화 히스토리가 있으면 추가
        if conversation_history:
            messages.extend(conversation_history)
        
        # 새 질문 추가
        messages.append({
            "role": "user",
            "content": f"{context}\n\n질문: {question}\n\n위 캐릭터를 기준으로 구체적이고 실용적인 답변을 해주세요."
        })
        
        try:
            # Anthropic 클라이언트 생성
            client = get_anthropic_client()
            
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=messages
            )
            
            return message.content[0].text
            
        except Exception as e:
            raise Exception(f"질문 답변 실패: {str(e)}")


# API 엔드포인트
crawler = Aion2CharacterCrawler()
analyzer = Aion2PowerAnalyzer()


@app.route('/')
def index():
    """메인 페이지 - HTML 파일 서빙"""
    try:
        from flask import send_file
        import os
        
        # HTML 파일 경로 확인
        html_files = [
            'index.html',                      # 우선순위 1
            'aion2-power-guide.html',         # 우선순위 2
            'aion2-power-guide-production.html' # 우선순위 3
        ]
        
        for html_file in html_files:
            if os.path.exists(html_file):
                return send_file(html_file)
        
        # HTML 파일이 없으면 간단한 안내 페이지
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>아이온2 AI 가이드 API</title>
            <meta charset="utf-8">
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: #0f172a;
                    color: #e2e8f0;
                }
                h1 { color: #a78bfa; }
                .endpoint {
                    background: #1e293b;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 8px;
                    border-left: 4px solid #a78bfa;
                }
                code {
                    background: #334155;
                    padding: 2px 6px;
                    border-radius: 4px;
                    color: #fbbf24;
                }
                a { color: #60a5fa; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>🎮 아이온2 전투력 향상 AI 가이드 API</h1>
            <p>백엔드 서버가 정상적으로 실행 중입니다!</p>
            
            <h2>📡 사용 가능한 API 엔드포인트:</h2>
            
            <div class="endpoint">
                <strong>GET /health</strong>
                <p>서버 상태 확인</p>
                <code>curl https://your-app.up.railway.app/health</code>
            </div>
            
            <div class="endpoint">
                <strong>POST /api/character/search</strong>
                <p>캐릭터 정보 검색</p>
            </div>
            
            <div class="endpoint">
                <strong>POST /api/character/analyze</strong>
                <p>AI 캐릭터 분석</p>
            </div>
            
            <div class="endpoint">
                <strong>POST /api/character/question</strong>
                <p>추가 질문 답변</p>
            </div>
            
            <h2>🎨 프론트엔드 배포 필요</h2>
            <p>
                현재는 백엔드 API만 실행 중입니다.<br>
                프론트엔드를 사용하려면:
            </p>
            <ol>
                <li><code>aion2-power-guide.html</code> 파일을 GitHub 저장소에 추가하세요</li>
                <li>또는 <a href="https://vercel.com" target="_blank">Vercel</a>에 프론트엔드를 별도로 배포하세요</li>
            </ol>
            
            <p style="margin-top: 40px; color: #64748b;">
                Railway에서 실행 중 • 
                <a href="/health">헬스체크</a>
            </p>
        </body>
        </html>
        """
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route('/api')
def api_info():
    """API 정보"""
    return jsonify({
        'name': 'Aion2 Power Guide API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'character_search': '/api/character/search',
            'character_analyze': '/api/character/analyze',
            'character_question': '/api/character/question'
        }
    })


@app.route('/api/character/search', methods=['POST'])
def search_character():
    """캐릭터 검색 API"""
    try:
        data = request.json
        character_name = data.get('characterName')
        server = data.get('server')
        
        if not character_name:
            return jsonify({'error': '캐릭터 이름을 입력해주세요'}), 400
        
        # 캐릭터 정보 조회
        character_data = crawler.search_character(character_name, server)
        
        return jsonify(character_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/character/analyze', methods=['POST'])
def analyze_character():
    """캐릭터 AI 분석 API"""
    try:
        character_data = request.json
        
        # AI 분석 수행
        analysis = analyzer.analyze_character(character_data)
        
        return jsonify({'analysis': analysis})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/character/question', methods=['POST'])
def answer_question():
    """추가 질문 답변 API"""
    try:
        data = request.json
        character_data = data.get('characterData')
        question = data.get('question')
        conversation_history = data.get('conversationHistory', [])
        
        if not question:
            return jsonify({'error': '질문을 입력해주세요'}), 400
        
        # 답변 생성
        answer = analyzer.answer_question(character_data, question, conversation_history)
        
        return jsonify({'answer': answer})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """헬스체크"""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    print("=" * 60)
    print("아이온2 전투력 향상 AI 가이드 서버")
    print("=" * 60)
    print("\n서버가 http://localhost:5000 에서 시작됩니다.")
    print("\nAPI 엔드포인트:")
    print("  POST /api/character/search - 캐릭터 검색")
    print("  POST /api/character/analyze - AI 분석")
    print("  POST /api/character/question - 추가 질문")
    print("  GET  /health - 헬스체크")
    print("\n주의: ANTHROPIC_API_KEY 환경변수 설정 필요")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
