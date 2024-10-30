# test_direct_api.py
import requests
from urllib.parse import unquote, quote
import os
from dotenv import load_dotenv
import json

load_dotenv()

def test_patent_api():
    api_key = os.getenv('API_SERVICE_KEY')
    if '%' not in api_key:
        api_key = quote(api_key)
    
    base_url = "http://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc/getPatentRegisterHistory"
    
    params = {
        'serviceKey': unquote(api_key),
        'type': 'json',
        'rgstNo': '1016699340000'
    }
    
    try:
        response = requests.get(
            base_url,
            params=params,
            timeout=30
        )
        
        print("\n=== API 응답 상태 ===")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n=== 특허 기본 정보 ===")
            print(f"등록번호: {data['items']['rgstNo']}")
            print(f"출원번호: {data['items']['applNo']}")
            print(f"발명의 명칭: {data['items']['title']}")
            print(f"영문 명칭: {data['items']['engTitle']}")
            print(f"출원일자: {data['items']['applDate']}")
            print(f"등록일자: {data['items']['rgstDate']}")
            
            print("\n=== 출원인 정보 ===")
            for applicant in data['items']['applicant']:
                print(f"이름: {applicant['applicantName']}")
                print(f"국적: {applicant['applicantNatl']}")
            
            print("\n=== 발명자 정보 ===")
            for inventor in data['items']['inventor']:
                print(f"이름: {inventor['inventorName']}")
                print(f"국적: {inventor['inventorNatl']}")
            
            print("\n=== 권리자 정보 ===")
            for owner in data['items']['owner']:
                print(f"이름: {owner['ownerName']}")
                print(f"최종권리자여부: {'예' if owner['finalOwnerYn'] == 'Y' else '아니오'}")
            
            print("\n=== 연차료 납부 정보 ===")
            for pay in data['items']['pay']:
                print(f"연차: {pay['statAnnl']}~{pay['lastAnnl']}")
                print(f"납부일: {pay['payDate']}")
                print(f"납부금액: {pay['payAmount']}원")
                
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_patent_api()