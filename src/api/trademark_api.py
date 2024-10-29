async def fetch_trademark_data(registration_number):
    api_url = "https://apis.data.go.kr/1430000/PttRgstRtInfoInqSvc/getMarkHistory"
    params = {
        'serviceKey': 'your_service_key',
        'type': 'json',
        'rgstNo': registration_number
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"API 응답 데이터: {data}")  # API 응답 확인
            # 데이터 SQLite에 적재
            c.execute('''
                INSERT INTO trademarks (registration_number, title, applicant, registration_date)
                VALUES (?, ?, ?, ?)
            ''', (data['items']['rgstNo'], data['items']['title'], data['items']['applicant'][0]['applicantName'], data['items']['rgstDate']))
            conn.commit()
            print(f"데이터 적재 완료: {data['items']['rgstNo']}, {data['items']['title']}")
        else:
            print(f"API 요청 실패: {response.status_code}")
