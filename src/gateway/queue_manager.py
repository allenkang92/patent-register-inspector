from redis import Redis
from rq import Queue
import logging
import json
import httpx
from typing import Dict, Any, Optional

class QueueManager:
    """
    KIPRIS API 요청을 관리하는 큐 시스템
    
    주요 기능:
    - 메인/백업 큐 관리
    - 작업 상태 추적
    - 재시도 메커니즘
    """
    
    def __init__(self):
        """큐 매니저 초기화"""
        self.redis = Redis(host='localhost', port=6379, db=0)
        self.main_queue = Queue('kipris_main', connection=self.redis)
        self.backup_queue = Queue('kipris_backup', connection=self.redis)
        
        # 로거 설정
        self.logger = logging.getLogger(__name__)
        
    async def enqueue_job(
        self,
        endpoint: str,
        params: Dict[str, Any]
    ) -> str:
        """
        작업을 큐에 추가
        
        Args:
            endpoint (str): API 엔드포인트 URL
            params (dict): 요청 파라미터
            
        Returns:
            str: 작업 ID
            
        Raises:
            Exception: 큐 처리 중 발생한 에러
        """
        try:
            # 메인 큐에 작업 추가
            job = self.main_queue.enqueue(
                func='src.api.patent_api.fetch_patent_data',
                args=(params.get('rgstNo'),),
                timeout=30,
                retry=3  # 최대 3번 재시도
            )
            
            # Redis에 작업 상태 저장
            self.redis.hset(
                f"job:{job.id}",
                mapping={
                    "status": "queued",
                    "endpoint": endpoint,
                    "params": json.dumps(params),
                    "retry_count": 0
                }
            )
            
            self.logger.info(f"Job {job.id} enqueued successfully")
            return job.id
            
        except Exception as e:
            self.logger.error(f"Main queue error: {str(e)}")
            
            # 백업 큐로 전환
            try:
                job = self.backup_queue.enqueue(
                    func='src.api.patent_api.fetch_patent_data',
                    args=(params.get('rgstNo'),),
                    timeout=30
                )
                return job.id
                
            except Exception as backup_error:
                self.logger.error(f"Backup queue error: {str(backup_error)}")
                raise
                
    async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        작업 상태 조회
        
        Args:
            job_id (str): 작업 ID
            
        Returns:
            dict: 작업 상태 정보
        """
        return self.redis.hgetall(f"job:{job_id}")