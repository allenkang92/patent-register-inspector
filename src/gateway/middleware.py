from fastapi import Request
from fastapi.responses import JSONResponse
import time
import httpx
from typing import Callable
from .queue_manager import QueueManager

# 큐 매니저 인스턴스 생성
queue_manager = QueueManager()

async def kipris_middleware(
    request: Request,
    call_next: Callable
):
    """
    KIPRIS API 요청을 처리하는 미들웨어
    
    주요 기능:
    1. 요청 처리 시간 측정
    2. API 요청 검증
    3. 큐 시스템 연동
    4. 에러 처리
    
    Args:
        request (Request): FastAPI 요청 객체
        call_next (Callable): 다음 미들웨어 또는 엔드포인트 핸들러
        
    Returns:
        Response: FastAPI 응답 객체
    """
    try:
        # 요청 시작 시간 기록
        start_time = time.time()
        
        # API 요청인 경우에만 특별 처리
        if request.url.path.startswith("/api/"):
            try:
                # 큐에 작업 추가
                job_id = await queue_manager.enqueue_job(
                    endpoint=str(request.url),
                    params=request.path_params
                )
                
                # 작업 상태 확인
                job_status = await queue_manager.get_job_status(job_id)
                
                # 작업 실패 시 에러 응답
                if job_status.get("status") == "error":
                    return JSONResponse(
                        status_code=500,
                        content={
                            "error": job_status.get("error"),
                            "job_id": job_id
                        }
                    )
                
                # API 요청 처리
                response = await call_next(request)
                
                # 처리 시간 헤더 추가
                process_time = time.time() - start_time
                response.headers["X-Process-Time"] = str(process_time)
                
                return response
                
            except httpx.TimeoutException:
                return JSONResponse(
                    status_code=504,
                    content={"error": "Request timeout"}
                )
                
            except httpx.HTTPStatusError as e:
                return JSONResponse(
                    status_code=e.response.status_code,
                    content={"error": str(e)}
                )
                
        # API 요청이 아닌 경우 일반 처리
        return await call_next(request)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "path": request.url.path
            }
        )