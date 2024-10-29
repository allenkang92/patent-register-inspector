import os
import sqlite3
from fastapi import FastAPI
from api.patent_api import fetch_patent_data
from api.utility_model_api import fetch_utility_model_data
from api.design_api import fetch_design_data
from api.trademark_api import fetch_trademark_data
from prometheus_client import Counter, make_asgi_app

app = FastAPI()

# Prometheus 메트릭 설정
REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'endpoint', 'http_status'])

# SQLite 데이터베이스 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # src 폴더 상위 디렉터리로 이동
db_path = os.path.join(BASE_DIR, 'data', 'patent_register.db')

# SQLite 데이터베이스 연결 설정
conn = sqlite3.connect(db_path)
c = conn.cursor()

# 테이블 생성 함수
def create_tables():
    c.execute('''
        CREATE TABLE IF NOT EXISTS patents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT,
            title TEXT,
            applicant TEXT,
            registration_date TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS utility_models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT,
            title TEXT,
            applicant TEXT,
            registration_date TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS designs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT,
            title TEXT,
            applicant TEXT,
            registration_date TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS trademarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT,
            title TEXT,
            applicant TEXT,
            registration_date TEXT
        )
    ''')
    conn.commit()

# 테이블 생성 실행
create_tables()

# Prometheus 미들웨어
@app.middleware("http")
async def add_prometheus_metrics(request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
    return response

# 특허 등록원부 API 엔드포인트
@app.get("/api/patents/{rgstNo}")
async def get_patents(rgstNo: str):
    service_key = 'your_service_key'  # 발급받은 API 인증키 입력
    patent_data = await fetch_patent_data(rgstNo, service_key)
    if patent_data:
        return {"특허 등록원부 데이터": patent_data}
    else:
        return {"message": "특허 데이터 조회 실패"}

# 실용신안 등록원부 API 엔드포인트
@app.get("/api/utility_model/{rgstNo}")
async def get_utility_model(rgstNo: str):
    service_key = 'your_service_key'  # 발급받은 API 인증키 입력
    utility_model_data = await fetch_utility_model_data(rgstNo, service_key)
    if utility_model_data:
        return {"실용신안 등록원부 데이터": utility_model_data}
    else:
        return {"message": "실용신안 데이터 조회 실패"}

# 디자인 등록원부 API 엔드포인트
@app.get("/api/design/{rgstNo}")
async def get_design(rgstNo: str):
    service_key = 'your_service_key'  # 발급받은 API 인증키 입력
    design_data = await fetch_design_data(rgstNo, service_key)
    if design_data:
        return {"디자인 등록원부 데이터": design_data}
    else:
        return {"message": "디자인 데이터 조회 실패"}

# 상표 등록원부 API 엔드포인트
@app.get("/api/mark/{rgstNo}")
async def get_mark(rgstNo: str):
    service_key = 'your_service_key'  # 발급받은 API 인증키 입력
    trademark_data = await fetch_trademark_data(rgstNo, service_key)
    if trademark_data:
        return {"상표 등록원부 데이터": trademark_data}
    else:
        return {"message": "상표 데이터 조회 실패"}

# Prometheus 메트릭 엔드포인트
app.mount("/metrics", make_asgi_app())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, debug=True)
