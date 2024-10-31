# src/gateway/queue_manager.py
import redis
from rq import Queue
import logging
import json
from typing import Dict, Any, Optional
import time

class QueueManager:
   def __init__(self):
       # Redis 연결
       self.redis_conn = redis.Redis(
           host='localhost',
           port=6379,
           db=0,
           decode_responses=True  # 문자열 자동 디코딩
       )
       
       # 큐 설정
       self.main_queue = Queue('main', connection=self.redis_conn)
       self.backup_queue = Queue('backup', connection=self.redis_conn)
       
       # 로거 설정
       self.logger = logging.getLogger(__name__)
   
   async def enqueue_job(
       self,
       path: str,
       params: Dict[str, Any]
   ) -> str:
       """
       작업을 큐에 추가
       
       Args:
           path: API 엔드포인트 경로
           params: 요청 파라미터
           
       Returns:
           str: 작업 ID
       """
       try:
           # API 타입 결정
           api_type = self._get_api_type(path)
           if not api_type:
               raise ValueError(f"Invalid API path: {path}")
           
           # 메인 큐에 작업 추가
           job = self.main_queue.enqueue(
               f'src.api.{api_type}_api.fetch_{api_type}_data',
               args=(params.get('rgstNo'),),
               kwargs={'retry': 3},
               timeout=60
           )
           
           # Redis에 작업 상태 저장
           job_key = f"job:{job.id}"
           self.redis_conn.hmset(job_key, {
               'status': 'queued',
               'api_type': api_type,
               'registration_number': params.get('rgstNo'),
               'created_at': time.time(),
               'updated_at': time.time()
           })
           
           # 작업 만료시간 설정 (24시간)
           self.redis_conn.expire(job_key, 86400)
           
           self.logger.info(f"Job enqueued: {job.id} ({api_type})")
           return job.id
           
       except Exception as e:
           self.logger.error(f"Failed to enqueue job: {str(e)}")
           
           # 메인 큐 실패시 백업 큐 사용
           try:
               job = self.backup_queue.enqueue(
                   f'src.api.{api_type}_api.fetch_{api_type}_data',
                   args=(params.get('rgstNo'),),
                   timeout=60
               )
               
               self.logger.info(f"Job enqueued to backup queue: {job.id}")
               return job.id
               
           except Exception as backup_error:
               self.logger.error(f"Backup queue also failed: {str(backup_error)}")
               raise
   
   async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
       """작업 상태 조회"""
       try:
           job_key = f"job:{job_id}"
           status = self.redis_conn.hgetall(job_key)
           
           if not status:
               return None
               
           return {
               'id': job_id,
               **status
           }
           
       except Exception as e:
           self.logger.error(f"Failed to get job status: {str(e)}")
           return None
   
   async def update_job_status(
       self,
       job_id: str,
       status: str,
       result: Optional[str] = None
   ):
       """작업 상태 업데이트"""
       try:
           job_key = f"job:{job_id}"
           update_data = {
               'status': status,
               'updated_at': time.time()
           }
           
           if result:
               update_data['result'] = result
               
           self.redis_conn.hmset(job_key, update_data)
           self.logger.info(f"Job status updated: {job_id} -> {status}")
           
       except Exception as e:
           self.logger.error(f"Failed to update job status: {str(e)}")
   
   def _get_api_type(self, path: str) -> Optional[str]:
       """API 경로에서 타입 추출"""
       if '/patents/' in path:
           return 'patent'
       elif '/utility_models/' in path:
           return 'utility_model'
       elif '/designs/' in path:
           return 'design'
       elif '/trademarks/' in path:
           return 'trademark'
       return None

   def cleanup_old_jobs(self, max_age: int = 86400):
       """오래된 작업 정리 (기본 24시간)"""
       try:
           current_time = time.time()
           pattern = 'job:*'
           
           for key in self.redis_conn.scan_iter(match=pattern):
               job_data = self.redis_conn.hgetall(key)
               created_at = float(job_data.get('created_at', 0))
               
               if current_time - created_at > max_age:
                   self.redis_conn.delete(key)
                   self.logger.info(f"Cleaned up old job: {key}")
                   
       except Exception as e:
           self.logger.error(f"Failed to cleanup old jobs: {str(e)}")