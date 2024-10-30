# test_api_key.py
import asyncio
import httpx
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

async def test_api():
    # API 키 가져오기
    api_key = os.getenv('API_SERVICE_KEY')
    print(f"Using API Key: {api_key}")
    
    # 테스트할 등록번호들
    test_cases = [
        {
            "type": "특허",
            "url": "https://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc/getPatentRegisterHistory",
            "number": "1016699340000"
        },
        {
            "type": "실용신안",
            "url": "https://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc/getUtilityModelHistory",
            "number": "2000040570000"
        },
        {
            "type": "디자인",
            "url": "https://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc/getDesignHistory",
            "number": "3009184930000"
        },
        {
            "type": "상표",
            "url": "https://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc/getMarkHistory",
            "number": "4004557770000"
        }
    ]
    
    async with httpx.AsyncClient() as client:
        for case in test_cases:
            print(f"\n{case['type']} API 테스트:")
            params = {
                'serviceKey': api_key,
                'type': 'json',
                'rgstNo': case['number']
            }
            
            try:
                response = await client.get(
                    case['url'],
                    params=params,
                    timeout=30.0
                )
                
                print(f"Status Code: {response.status_code}")
                print(f"Response Headers: {response.headers}")
                print(f"Raw Response: {response.text}")
                
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_api())