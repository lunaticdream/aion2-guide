"""
아이온2 캐릭터 정보 크롤링 상세 구현
실제 공식 홈페이지 또는 비공식 API를 활용한 데이터 수집

주의: 실제 사용 전 NC소프트 이용약관 및 robots.txt 확인 필수!
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from typing import Dict, Optional, List
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Aion2OfficialCrawler:
    """
    아이온2 공식 홈페이지 크롤러
    
    주의: 
    1. robots.txt 확인 필수
    2. 요청 간격 준수 (최소 1초)
    3. User-Agent 설정
    """
    
    BASE_URL = "https://aion2.plaync.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        })
    
    def search_character(self, character_name: str, server: Optional[str] = None) -> Dict:
        """
        공식 홈페이지에서 캐릭터 검색
        
        실제 구현 시 페이지 구조 분석 필요:
        1. 개발자 도구로 네트워크 요청 분석
        2. API 엔드포인트 확인
        3. 필요한 파라미터 파악
        """
        
        try:
            # 방법 1: 검색 페이지 크롤링
            search_url = f"{self.BASE_URL}/ko-kr/characters/index"
            
            # 검색 파라미터 (실제 페이지 분석 필요)
            params = {
                'characterName': character_name,
            }
            if server:
                params['server'] = server
            
            logger.info(f"Searching character: {character_name} on server: {server}")
            
            # 요청 전 대기 (서버 부담 방지)
            time.sleep(1)
            
            response = self.session.get(search_url, params=params)
            response.raise_for_status()
            
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 캐릭터 정보 추출 (실제 HTML 구조에 맞게 수정)
            character_data = self._parse_character_page(soup, character_name)
            
            return character_data
            
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Parsing failed: {e}")
            raise
    
    def _parse_character_page(self, soup: BeautifulSoup, character_name: str) -> Dict:
        """
        HTML에서 캐릭터 정보 파싱
        
        실제 구현 시 페이지 구조에 맞게 셀렉터 수정 필요
        예시 구조:
        - 기본 정보: .character-info
        - 장비: .equipment-list
        - 스탯: .stats-table
        """
        
        # 예시 파싱 로직 (실제 HTML 구조에 맞게 수정)
        character_data = {
            'name': character_name,
            'server': self._extract_text(soup, '.server-name'),
            'level': self._extract_number(soup, '.character-level'),
            'class': self._extract_text(soup, '.character-class'),
            'combatPower': self._extract_number(soup, '.combat-power'),
            'equipment': self._parse_equipment(soup),
            'stats': self._parse_stats(soup),
            'skills': self._parse_skills(soup),
            'petCollection': self._parse_pet_collection(soup),
            'soulEngraving': self._parse_soul_engraving(soup),
        }
        
        return character_data
    
    def _extract_text(self, soup: BeautifulSoup, selector: str) -> str:
        """CSS 셀렉터로 텍스트 추출"""
        element = soup.select_one(selector)
        return element.text.strip() if element else ""
    
    def _extract_number(self, soup: BeautifulSoup, selector: str) -> int:
        """CSS 셀렉터로 숫자 추출"""
        text = self._extract_text(soup, selector)
        # 숫자만 추출 (쉼표 제거)
        return int(''.join(filter(str.isdigit, text))) if text else 0
    
    def _parse_equipment(self, soup: BeautifulSoup) -> Dict:
        """장비 정보 파싱"""
        return {
            'weapon': {
                'name': self._extract_text(soup, '.weapon-name'),
                'level': self._extract_number(soup, '.weapon-level'),
                'grade': self._extract_text(soup, '.weapon-grade'),
            },
            'armor': {
                'name': self._extract_text(soup, '.armor-name'),
                'level': self._extract_number(soup, '.armor-level'),
                'grade': self._extract_text(soup, '.armor-grade'),
            },
            'accessories': self._parse_accessories(soup),
        }
    
    def _parse_accessories(self, soup: BeautifulSoup) -> List[Dict]:
        """악세서리 정보 파싱"""
        accessories = []
        # 실제 구조에 맞게 수정
        accessory_elements = soup.select('.accessory-item')
        
        for elem in accessory_elements:
            accessories.append({
                'slot': self._extract_text(elem, '.slot-name'),
                'name': self._extract_text(elem, '.item-name'),
                'level': self._extract_number(elem, '.item-level'),
            })
        
        return accessories
    
    def _parse_stats(self, soup: BeautifulSoup) -> Dict:
        """스탯 정보 파싱"""
        return {
            'attack': self._extract_number(soup, '.stat-attack'),
            'defense': self._extract_number(soup, '.stat-defense'),
            'hp': self._extract_number(soup, '.stat-hp'),
            'criticalRate': float(self._extract_text(soup, '.stat-crit-rate').replace('%', '')),
            'criticalDamage': float(self._extract_text(soup, '.stat-crit-dmg').replace('%', '')),
            'accuracy': self._extract_number(soup, '.stat-accuracy'),
            'evasion': self._extract_number(soup, '.stat-evasion'),
        }
    
    def _parse_skills(self, soup: BeautifulSoup) -> Dict:
        """스킬/스티그마 정보 파싱"""
        stigma_list = []
        stigma_elements = soup.select('.stigma-skill')
        
        for elem in stigma_elements:
            stigma_list.append(self._extract_text(elem, '.skill-name'))
        
        return {
            'stigma': stigma_list,
            'completionRate': self._extract_number(soup, '.stigma-completion'),
        }
    
    def _parse_pet_collection(self, soup: BeautifulSoup) -> Dict:
        """펫 컬렉션 정보 파싱"""
        return {
            'wild': self._extract_number(soup, '.pet-wild-percent'),
            'intelligence': self._extract_number(soup, '.pet-intel-percent'),
            'nature': self._extract_number(soup, '.pet-nature-percent'),
            'transformation': self._extract_number(soup, '.pet-trans-percent'),
        }
    
    def _parse_soul_engraving(self, soup: BeautifulSoup) -> Dict:
        """영혼 각인 정보 파싱"""
        weapon_engravings = []
        armor_engravings = []
        
        # 무기 각인
        weapon_elems = soup.select('.weapon-engraving')
        for elem in weapon_elems:
            weapon_engravings.append(self._extract_text(elem, '.engraving-text'))
        
        # 방어구 각인
        armor_elems = soup.select('.armor-engraving')
        for elem in armor_elems:
            armor_engravings.append(self._extract_text(elem, '.engraving-text'))
        
        return {
            'weapon': weapon_engravings,
            'armor': armor_engravings,
        }


class Aion2UnofficialAPIClient:
    """
    비공식 API 클라이언트 (예: aion2tool.com, aon2.info)
    
    주의: 
    1. 비공식 API는 언제든 변경/중단될 수 있음
    2. API 제공자의 이용 정책 확인 필수
    3. Rate Limiting 준수
    """
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or "https://api.example.com"  # 실제 API URL로 변경
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Aion2PowerGuide/1.0',
            'Accept': 'application/json',
        })
    
    def search_character(self, character_name: str, server: Optional[str] = None) -> Dict:
        """
        비공식 API로 캐릭터 검색
        
        API 문서가 있다면 그에 맞게 구현
        """
        
        try:
            # API 엔드포인트 (예시)
            endpoint = f"{self.base_url}/character/search"
            
            params = {
                'name': character_name,
            }
            if server:
                params['server'] = server
            
            logger.info(f"Calling API: {endpoint}")
            
            # Rate limiting
            time.sleep(0.5)
            
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            
            # JSON 응답 파싱
            data = response.json()
            
            # 표준 형식으로 변환
            return self._normalize_data(data)
            
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def _normalize_data(self, raw_data: Dict) -> Dict:
        """
        API 응답을 표준 형식으로 변환
        각 API의 응답 형식에 맞게 수정
        """
        
        # 예시: API 응답 구조가 다를 수 있으므로 매핑
        normalized = {
            'name': raw_data.get('characterName', ''),
            'server': raw_data.get('serverName', ''),
            'level': raw_data.get('level', 0),
            'class': raw_data.get('className', ''),
            'combatPower': raw_data.get('power', 0),
            # ... 나머지 필드 매핑
        }
        
        return normalized


class Aion2HybridCrawler:
    """
    여러 소스를 결합한 하이브리드 크롤러
    - 공식 API (출시 시)
    - 공식 홈페이지 크롤링
    - 비공식 API
    
    우선순위에 따라 데이터 소스 선택
    """
    
    def __init__(self):
        self.official_crawler = Aion2OfficialCrawler()
        self.unofficial_client = Aion2UnofficialAPIClient()
    
    def search_character(self, character_name: str, server: Optional[str] = None) -> Dict:
        """
        우선순위에 따라 캐릭터 검색
        1. 공식 API (출시 시)
        2. 비공식 API (빠르고 안정적)
        3. 공식 홈페이지 크롤링 (최후 수단)
        """
        
        errors = []
        
        # 1. 공식 API 시도 (현재 미출시)
        # try:
        #     return self.official_api_client.search(character_name, server)
        # except Exception as e:
        #     errors.append(f"Official API: {e}")
        
        # 2. 비공식 API 시도
        try:
            logger.info("Trying unofficial API...")
            return self.unofficial_client.search_character(character_name, server)
        except Exception as e:
            errors.append(f"Unofficial API: {e}")
            logger.warning(f"Unofficial API failed: {e}")
        
        # 3. 공식 홈페이지 크롤링 시도
        try:
            logger.info("Trying official website crawling...")
            return self.official_crawler.search_character(character_name, server)
        except Exception as e:
            errors.append(f"Official crawling: {e}")
            logger.error(f"Official crawling failed: {e}")
        
        # 모든 방법 실패
        raise Exception(f"Failed to fetch character data. Errors: {'; '.join(errors)}")


# 사용 예제
if __name__ == "__main__":
    print("=" * 60)
    print("아이온2 캐릭터 정보 크롤러 테스트")
    print("=" * 60)
    
    # 하이브리드 크롤러 생성
    crawler = Aion2HybridCrawler()
    
    # 테스트 캐릭터 검색
    try:
        character_data = crawler.search_character(
            character_name="테스트캐릭터",
            server="서버1"
        )
        
        print("\n[검색 결과]")
        print(json.dumps(character_data, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"\n[오류] {e}")
        print("\n참고:")
        print("1. 실제 캐릭터 이름과 서버를 입력하세요")
        print("2. 공식 홈페이지 HTML 구조에 맞게 파서를 수정하세요")
        print("3. 또는 비공식 API의 실제 엔드포인트를 설정하세요")
    
    print("\n" + "=" * 60)
