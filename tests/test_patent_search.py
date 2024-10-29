# test_patent_search.py
import asyncio
import httpx
import json

async def search_patent():
    registration_numbers = [
        "1016699340000",  # 특허
        "2000040570000",  # 실용신안
        "3009184930000",  # 디자인
        "4004557770000"   # 상표
    ]
    
    async with httpx.AsyncClient() as client:
        # 특허 검색 및 응답 상세 출력
        print("\n특허 API 응답:")
        response = await client.get(f"http://localhost:8000/api/patents/{registration_numbers[0]}")
        print("Status Code:", response.status_code)
        print("Response Headers:", response.headers)
        print("Raw Response:", response.text)
        try:
            print("Parsed Response:", json.loads(response.text))
        except json.JSONDecodeError as e:
            print("JSON Parse Error:", e)

        # 원본 API 응답 구조 확인을 위한 직접 호출
        print("\n특허청 API 직접 호출:")
        direct_response = await client.get(
            "https://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc/getPatentRegisterHistory",
            params={
                'serviceKey': 'Ut1Rh63x',  # API 키
                'type': 'json',
                'rgstNo': registration_numbers[0]
            }
        )
        print("Direct API Status Code:", direct_response.status_code)
        print("Direct API Headers:", direct_response.headers)
        print("Direct API Raw Response:", direct_response.text)
        try:
            print("Direct API Parsed Response:", json.loads(direct_response.text))
        except json.JSONDecodeError as e:
            print("Direct API JSON Parse Error:", e)

def check_database():
    import sqlite3
    import os
    
    # 데이터베이스 파일 경로 확인
    db_path = os.path.join(os.getcwd(), 'data', 'patent_register.db')
    print(f"\n데이터베이스 경로: {db_path}")
    print(f"데이터베이스 존재 여부: {os.path.exists(db_path)}")
    
    # 데이터베이스 연결 및 내용 확인
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 테이블 존재 여부 확인
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("\n존재하는 테이블:", tables)
        
        if ('patents',) in tables:
            print("\n특허 테이블:")
            cursor.execute("SELECT * FROM patents")
            print(cursor.fetchall())
            
            # 테이블 스키마 확인
            cursor.execute("PRAGMA table_info(patents);")
            print("\n특허 테이블 스키마:", cursor.fetchall())
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"데이터베이스 에러: {e}")

if __name__ == "__main__":
    # 실행 전 data 디렉토리 확인/생성
    import os
    os.makedirs('data', exist_ok=True)
    
    asyncio.run(search_patent())
    check_database()