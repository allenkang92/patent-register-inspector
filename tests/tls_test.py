import httpx
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API 서비스 키 가져오기
service_key = os.getenv("SERVICE_KEY")

# 특허 등록원부 실시간 이력조회 API URL
api_url = 'https://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc/getPatentRegisterHistory'

# 요청 파라미터 설정
params = {
    'serviceKey': service_key,  # 서비스 키
    'type': 'json',  # 응답 형식 (json 또는 xml)
    'rgstNo': 'your_registration_number'  # 특허 등록번호
}

# API 호출 함수
def get_patent_register_history():
    try:
        # GET 요청 보내기
        response = httpx.get(api_url, params=params)

        # 응답 상태 코드가 200이면 성공
        if response.status_code == 200:
            data = response.json()  # JSON 형식으로 응답을 파싱
            print(f"응답 데이터: {data}")
        else:
            print(f"API 요청 실패: 상태 코드 {response.status_code}")
            print(f"응답 본문: {response.text}")

    except Exception as e:
        print(f"API 요청 중 오류 발생: {e}")

# 함수 호출
get_patent_register_history()
