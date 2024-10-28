import asyncio
import os
from dotenv import load_dotenv
import httpx

# 환경 변수 로드
load_dotenv()

# 엔드포인트 URL
api_url = os.getenv('API_ENDPOINT', 'http://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc')

# Keep-Alive 및 TLS 최적화 확인 코드
async def check_keep_alive_tls():
    async with httpx.AsyncClient(http2=True, verify=True) as client:
        try:
            # API 엔드포인트에서 Keep-Alive 및 TLS 확인
            headers = {
                'User-Agent': 'MyAPI/1.0',
                'Connection': 'keep-alive',
                'Accept': 'application/json'
            }
            response = await client.get(api_url, headers=headers)
            
            # Keep-Alive 확인
            if response.headers.get('Connection') == 'keep-alive':
                print("Keep-Alive 설정 확인됨")
            else:
                print("Keep-Alive 설정되지 않음")

            # TLS 확인
            tls_version = response.http_version
            print(f"TLS 버전 확인: {tls_version}")
        except Exception as e:
            print(f"오류 발생: {str(e)}")

# 비동기 함수 실행
async def main():
    await check_keep_alive_tls()

# main 함수 호출
asyncio.run(main())
