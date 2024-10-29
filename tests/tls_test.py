import httpx
import asyncio

# TLS 확인
async def check_tls_connection(api_url):
    async with httpx.AsyncClient(verify=True) as client:
        try:
            # API 엔드포인트에 대한 요청
            response = await client.get(api_url)
            
            # TLS 버전 및 HTTP 버전 확인
            tls_version = response.http_version
            print(f"TLS 버전 확인: {tls_version}")
            
            # HTTP 버전이 1.1인지 확인
            assert tls_version == "HTTP/1.1", f"서버가 HTTP/1.1 대신 {tls_version} 사용 중"
            print("TLS 및 HTTP/1.1 지원 확인됨")
            
        except Exception as e:
            print(f"TLS 연결 확인 중 오류 발생: {e}")

# 비동기 함수 실행
async def main():
    api_url = 'https://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc/getPatentRegisterHistory'
    await check_tls_connection(api_url)

# 실행
asyncio.run(main())
