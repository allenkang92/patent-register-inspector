import os
import httpx
import sqlite3

# SQLite 데이터베이스 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, '..', 'data', 'patent_register.db')

# SQLite 데이터베이스 연결
conn = sqlite3.connect(db_path)
c = conn.cursor()

async def fetch_utility_model_data(registration_number: str, service_key: str):
    api_url = "https://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc/getUtilityModelHistory"
    params = {
        'serviceKey': service_key,
        'type': 'json',
        'rgstNo': registration_number
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()

            # 데이터 중복 방지
            c.execute('SELECT * FROM utility_models WHERE registration_number = ?', (registration_number,))
            result = c.fetchone()

            if result is None:
                # 데이터 SQLite에 적재
                c.execute('''
                    INSERT INTO utility_models (registration_number, title, applicant, registration_date)
                    VALUES (?, ?, ?, ?)
                ''', (data['items']['rgstNo'], data['items']['title'], data['items']['applicant'][0]['applicantName'], data['items']['rgstDate']))
                conn.commit()
                return data
            else:
                print(f"실용신안 데이터가 이미 존재합니다: {registration_number}")
                return result
        else:
            print(f"API 요청 실패: {response.status_code}")
            return None
