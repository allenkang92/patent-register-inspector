import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, make_asgi_app

# Local imports
from src.config import settings
from src.database import Database
from src.api.patent_api import fetch_patent_data
from src.api.utility_model_api import fetch_utility_model_data
from src.api.design_api import fetch_design_data
from src.api.trademark_api import fetch_trademark_data

# FastAPI 앱 초기화
app = FastAPI(
    title="특허 등록원부 조회 API",
    description="특허, 실용신안, 디자인, 상표 등록원부 조회 API Gateway",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 초기화
database = Database()
database.initialize_tables()

# Prometheus 메트릭 설정
REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'endpoint', 'http_status'])

# Prometheus 미들웨어
@app.middleware("http")
async def add_prometheus_metrics(request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
    return response

# 루트 경로 -> Swagger 문서
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# 상태 확인 엔드포인트
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "api_status": "operational"
    }

# API 엔드포인트 목록
@app.get("/api")
async def api_routes():
    return {
        "endpoints": {
            "patents": "/api/patents/{rgstNo}",
            "utility_models": "/api/utility_models/{rgstNo}",
            "designs": "/api/designs/{rgstNo}",
            "trademarks": "/api/trademarks/{rgstNo}"
        }
    }

# 특허 API 엔드포인트
@app.get("/api/patents/{rgstNo}")
async def get_patents(rgstNo: str):
    try:
        patent_data = await fetch_patent_data(rgstNo, settings.API_SERVICE_KEY)
        if patent_data:
            return {
                "status": "success",
                "data": patent_data
            }
        raise HTTPException(status_code=404, detail="특허 데이터를 찾을 수 없습니다")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 실용신안 API 엔드포인트
@app.get("/api/utility_models/{rgstNo}")
async def get_utility_models(rgstNo: str):
    try:
        utility_model_data = await fetch_utility_model_data(rgstNo, settings.API_SERVICE_KEY)
        if utility_model_data:
            return {
                "status": "success",
                "data": utility_model_data
            }
        raise HTTPException(status_code=404, detail="실용신안 데이터를 찾을 수 없습니다")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 디자인 API 엔드포인트
@app.get("/api/designs/{rgstNo}")
async def get_designs(rgstNo: str):
    try:
        design_data = await fetch_design_data(rgstNo, settings.API_SERVICE_KEY)
        if design_data:
            return {
                "status": "success",
                "data": design_data
            }
        raise HTTPException(status_code=404, detail="디자인 데이터를 찾을 수 없습니다")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 상표 API 엔드포인트
@app.get("/api/trademarks/{rgstNo}")
async def get_trademarks(rgstNo: str):
    try:
        trademark_data = await fetch_trademark_data(rgstNo, settings.API_SERVICE_KEY)
        if trademark_data:
            return {
                "status": "success",
                "data": trademark_data
            }
        raise HTTPException(status_code=404, detail="상표 데이터를 찾을 수 없습니다")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Prometheus 메트릭 엔드포인트
app.mount("/metrics", make_asgi_app())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)