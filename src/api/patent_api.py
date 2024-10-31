# src/api/patent_api.py
import httpx
from ..config import settings
from ..database import Database
from fastapi import HTTPException
import json
import logging
from typing import Dict, Any, Optional

# 로거 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

db = Database()

async def fetch_patent_data(registration_number: str, service_key: str):
   """특허 등록원부 데이터를 조회하고 저장하는 함수"""
   try:
       params = {
           'serviceKey': service_key,
           'type': 'json',
           'rgstNo': registration_number
       }

       async with httpx.AsyncClient() as client:
           response = await client.get(
               settings.PATENT_API_URL,
               params=params,
               timeout=30.0
           )

           response.raise_for_status()
           
           try:
               data = response.json()
               if not data.get('response', {}).get('body', {}).get('items'):
                   raise HTTPException(
                       status_code=404,
                       detail=f"등록번호 {registration_number}에 대한 특허 데이터가 없습니다."
                   )
               
               items = data['response']['body']['items']
               
           except json.JSONDecodeError:
               raise HTTPException(
                   status_code=500,
                   detail="응답 데이터 파싱 실패"
               )

           # DB 저장
           with db.get_connection() as conn:
               cursor = conn.cursor()
               try:
                   # 1. ip_rights 테이블에 기본 정보 저장
                   cursor.execute('''
                       INSERT OR REPLACE INTO ip_rights (
                           rgst_no, right_type, appl_no, title, title_eng,
                           appl_date, rgst_date, pub_no, pub_date, opn_no,
                           opn_date, last_dspst, cndrt_exptn_date
                       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ''', (
                       items['rgstNo'],
                       'patent',
                       items.get('applNo'),
                       items.get('title'),
                       items.get('engTitle'),
                       items.get('applDate'),
                       items.get('rgstDate'),
                       items.get('pubNo'),
                       items.get('pubDate'),
                       items.get('opnNo'),
                       items.get('opnDate'),
                       items.get('lastDspst'),
                       items.get('cndrtExptnDate')
                   ))
                   ip_right_id = cursor.lastrowid
                   
                   # 2. patent_utility_details 저장
                   cursor.execute('''
                       INSERT INTO patent_utility_details (
                           ip_right_id, claim_count, ipc_cd, cpc_cd,
                           rfoex_yn, rfoex_date
                       ) VALUES (?, ?, ?, ?, ?, ?)
                   ''', (
                       ip_right_id,
                       items.get('claimCount'),
                       items.get('ipcCd'),
                       items.get('cpcCd'),
                       items.get('rfoexYn'),
                       items.get('rfoexDate')
                   ))
                   
                   # 3. 출원인 정보 저장
                   applicants = items.get('applicant', [])
                   for applicant in applicants:
                       cursor.execute('''
                           INSERT INTO applicants (
                               ip_right_id, name, eng_name, nationality,
                               address, rpstr_yn, applicant_cd
                           ) VALUES (?, ?, ?, ?, ?, ?, ?)
                       ''', (
                           ip_right_id,
                           applicant.get('applicantName'),
                           applicant.get('applicantEngName'),
                           applicant.get('applicantNatl'),
                           applicant.get('applicantAddr'),
                           applicant.get('rpstrYn'),
                           applicant.get('applicantCd')
                       ))
                   
                   # 4. 발명자 정보 저장
                   inventors = items.get('inventor', [])
                   for inventor in inventors:
                       cursor.execute('''
                           INSERT INTO creators (
                               ip_right_id, creator_type, name, nationality,
                               address, creator_cd, seq
                           ) VALUES (?, ?, ?, ?, ?, ?, ?)
                       ''', (
                           ip_right_id,
                           'inventor',
                           inventor.get('inventorName'),
                           inventor.get('inventorNatl'),
                           inventor.get('inventorAddr'),
                           inventor.get('inventorCd'),
                           inventor.get('inventorSeq')
                       ))
                   
                   # 5. 권리자 정보 저장
                   owners = items.get('owner', [])
                   for owner in owners:
                       cursor.execute('''
                           INSERT INTO right_holders (
                               ip_right_id, name, eng_name, nationality,
                               address, rgst_cs_name, rgst_cs_date,
                               rgst_cs_reason, is_final_owner
                           ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                       ''', (
                           ip_right_id,
                           owner.get('ownerName'),
                           owner.get('ownerEngName'),
                           owner.get('ownerNatl'),
                           owner.get('ownerAddr'),
                           owner.get('ownerRgstCsName'),
                           owner.get('ownerRgstCsDate'),
                           owner.get('ownerRgstCsReason'),
                           1 if owner.get('finalOwnerYn') == 'Y' else 0
                       ))
                   
                   # 6. 연차료 정보 저장
                   payments = items.get('pay', [])
                   for payment in payments:
                       cursor.execute('''
                           INSERT INTO annual_fees (
                               ip_right_id, start_year, end_year,
                               payment_date, amount
                           ) VALUES (?, ?, ?, ?, ?)
                       ''', (
                           ip_right_id,
                           payment.get('statAnnl'),
                           payment.get('lastAnnl'),
                           payment.get('payDate'),
                           payment.get('payAmount')
                       ))
                   
                   conn.commit()
                   logger.info(f"특허 데이터 저장 완료: {registration_number}")
                   
               except Exception as e:
                   conn.rollback()
                   logger.error(f"데이터 저장 실패: {str(e)}")
                   raise

           return {
               "status": "success",
               "message": "데이터 저장 완료",
               "data": items
           }

   except httpx.TimeoutException:
       raise HTTPException(
           status_code=504,
           detail="API 서버 응답 시간 초과"
       )
   except httpx.HTTPStatusError as exc:
       raise HTTPException(
           status_code=exc.response.status_code,
           detail=f"공공데이터포털 API 오류: {exc.response.text}"
       )
   except Exception as e:
       logger.error(f"처리 중 오류 발생: {str(e)}")
       raise HTTPException(
           status_code=500,
           detail=f"데이터 처리 중 오류 발생: {str(e)}"
       )