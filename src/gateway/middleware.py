# src/gateway/middleware.py
from fastapi import Request
from fastapi.responses import JSONResponse
import time
import logging
from .queue_manager import QueueManager
from typing import Callable

logger = logging.getLogger(__name__)

class ApiGatewayMiddleware:
    def __init__(self):
        self.queue_manager = QueueManager()
        self.logger = logging.getLogger(__name__)
    
    async def __call__(
        self, 
        request: Request, 
        call_next: Callable
    ):
        try:
            start_time = time.time()
            
            # API 요청만 처리
            if request.url.path.startswith("/api/"):
                response = await self._handle_api_request(request, call_next)
            else:
                response = await call_next(request)
                
            # 처리 시간 측정
            process_time = time.time() - start_time
            if isinstance(response, JSONResponse):
                response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Middleware error: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": str(e),
                    "path": request.url.path
                }
            )
    
    async def _handle_api_request(
        self,
        request: Request,
        call_next: Callable
    ):
        """API 요청 처리"""
        try:
            # 작업 큐에 추가
            job_id = await self.queue_manager.enqueue_job(
                request.url.path,
                request.path_params
            )
            
            # 실제 API 호출
            response = await call_next(request)
            
            # 작업 상태 추가
            if isinstance(response, JSONResponse):
                response_data = response.body.decode()
                await self.queue_manager.update_job_status(
                    job_id,
                    "completed",
                    response_data
                )
            
            return response
            
        except Exception as e:
            self.logger.error(f"API request error: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": str(e),
                    "path": request.url.path
                }
            )