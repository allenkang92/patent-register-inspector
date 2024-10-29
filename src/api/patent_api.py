import httpx
import sqlite3
from fastapi import FastAPI

app = FastAPI()

# SQLite 데이터베이스 연결
conn = sqlite3.connect('data/patent_register.db')
c = conn.cursor()

# 특허 테이블 생성 함수 (처음에만 실행)
def create_patents_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS patents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT UNIQUE,
            title TEXT,
            applicant TEXT,
            registration_date TEXT
        )
    ''')
    conn.commit()

# 테이블 생성 실행
create_patents_table()

# 특허 API 호출 및 데이터 적재 함수
async def fetch_patent_data(registration_number: str, service_key: str):
    api_url = "https://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc/getPatentRegisterHistory"
    params = {
        'serviceKey': service_key,
        'type': 'json',
        'rgstNo': registration_number
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            
            # 데이터 중복 방지 (동일한 등록번호가 있는지 확인)
            c.execute('SELECT * FROM patents WHERE registration_number = ?', (registration_number,))
            result = c.fetchone()

            if result is None:
                # 데이터 SQLite에 적재
                c.execute('''
                    INSERT INTO patents (registration_number, title, applicant, registration_date)
                    VALUES (?, ?, ?, ?)
                ''', (data['items']['rgstNo'], data['items']['title'], data['items']['applicant'][0]['applicantName'], data['items']['rgstDate']))
                conn.commit()
                print(f"특허 데이터 적재 성공: {registration_number}")
            else:
                print(f"특허 데이터가 이미 존재합니다: {registration_number}")
        else:
            print(f"API 요청 실패: {response.status_code}")

# 데이터 적재 후 API 엔드포인트에서 확인
@app.get("/api/patents")
async def get_patents_from_db():
    c.execute('SELECT * FROM patents')
    rows = c.fetchall()
    return {"data": rows}
