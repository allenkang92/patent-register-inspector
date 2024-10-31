# tests/test_gateway.py를 만들어서 테스트
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_patent_api():
    # 1. API 호출 테스트
    rgst_no = "1016699340000"  # 테스트용 등록번호
    response = client.get(f"/api/patents/{rgst_no}")
    assert response.status_code == 200
    
    # 2. 작업 큐 상태 확인
    job_id = response.headers.get("X-Job-ID")
    assert job_id is not None
    
    # 3. 작업 상태 확인
    job_status = client.get(f"/api/jobs/{job_id}")
    assert job_status.status_code == 200
    
    # 4. DB 저장 확인
    # TODO: DB 연결 및 데이터 확인

def test_error_handling():
    # 1. 잘못된 등록번호 테스트
    response = client.get("/api/patents/invalid")
    assert response.status_code == 404
    
    # 2. Rate limit 테스트
    responses = [
        client.get("/api/patents/1016699340000")
        for _ in range(60)  # 초당 50회 제한 테스트
    ]
    assert any(r.status_code == 429 for r in responses)

def test_queue_system():
    # 1. 메인 큐 테스트
    response = client.get("/api/patents/1016699340000")
    job_id = response.headers.get("X-Job-ID")
    
    # 2. 작업 상태 모니터링
    for _ in range(5):  # 최대 5초 대기
        status = client.get(f"/api/jobs/{job_id}")
        if status.json()["status"] == "completed":
            break
        time.sleep(1)
    
    assert status.json()["status"] == "completed"

    # 3. 백업 큐 테스트 (메인 큐 실패 시나리오)
    # TODO: 메인 큐 실패 상황 시뮬레이션