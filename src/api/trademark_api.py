import httpx
from ..config import settings
from ..database import Database
from fastapi import HTTPException
import json

db = Database()

async def fetch_trademark_data(registration_number: str, service_key: str):
    """상표 등록원부 데이터를 조회하는 함수"""
    try:
        params = {
            'serviceKey': service_key,
            'type': 'json',
            'rgstNo': registration_number
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.TRADEMARK_API_URL,
                params=params,
                timeout=30.0
            )

            response.raise_for_status()
            
            try:
                data = response.json()
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=500,
                    detail="응답 데이터 파싱 실패"
                )

            if not data:
                raise HTTPException(
                    status_code=404,
                    detail=f"등록번호 {registration_number}에 대한 상표 데이터가 없습니다."
                )

            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM trademarks WHERE registration_number = ?', 
                             (registration_number,))
                result = cursor.fetchone()

                if result is None:
                    cursor.execute('''
                        INSERT INTO trademarks (registration_number, title, applicant, registration_date)
                        VALUES (?, ?, ?, ?)
                    ''', (data['items']['rgstNo'], 
                         data['items']['title'],
                         data['items']['applicant'][0]['applicantName'],
                         data['items']['rgstDate']))
                    conn.commit()

            return data

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="API 서버 응답 시간 초과"
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"특허청 API 오류: {exc.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"데이터 조회 중 오류 발생: {str(e)}"
        )