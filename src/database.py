# src/database.py
import os
import sqlite3
from contextlib import contextmanager
import logging

class Database:
    def __init__(self):
        # 데이터베이스 파일 경로 설정
        self.db_path = os.path.join(os.getcwd(), 'patent_register.db')
        
        # 로거 설정
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        if not os.path.exists(self.db_path):
            self.initialize_tables()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def initialize_tables(self):
        """데이터베이스 테이블 초기화"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # ip_rights 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ip_rights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rgst_no TEXT UNIQUE NOT NULL,          -- 등록번호
                    right_type TEXT NOT NULL,              -- 권리구분 (특허/실용신안/디자인/상표)
                    appl_no TEXT,                          -- 출원번호
                    title TEXT,                            -- 명칭/물품명
                    title_eng TEXT,                        -- 영문명칭
                    appl_date TEXT,                        -- 출원일자
                    rgst_date TEXT,                        -- 등록일자
                    pub_no TEXT,                           -- 공고번호
                    pub_date TEXT,                         -- 공고일자
                    opn_no TEXT,                           -- 공개번호
                    opn_date TEXT,                         -- 공개일자
                    last_dspst TEXT,                       -- 최종처분
                    cndrt_exptn_date TEXT,                 -- 존속기간만료일
                    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # patent_utility_details 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patent_utility_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_right_id INTEGER NOT NULL,
                    claim_count INTEGER,                   -- 청구항수
                    ipc_cd TEXT,                          -- IPC 코드
                    cpc_cd TEXT,                          -- CPC 코드
                    rfoex_yn TEXT,                        -- 심사청구여부
                    rfoex_date TEXT,                      -- 심사청구일
                    FOREIGN KEY (ip_right_id) REFERENCES ip_rights(id)
                )
            ''')
            
            # applicants 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS applicants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_right_id INTEGER NOT NULL,
                    name TEXT NOT NULL,                    -- 출원인 이름
                    eng_name TEXT,                         -- 영문 이름
                    nationality TEXT,                      -- 국적
                    address TEXT,                          -- 주소
                    rpstr_yn TEXT,                         -- 대표자 여부
                    applicant_cd TEXT,                     -- 출원인 코드
                    FOREIGN KEY (ip_right_id) REFERENCES ip_rights(id)
                )
            ''')
            
            # creators 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS creators (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_right_id INTEGER NOT NULL,
                    creator_type TEXT NOT NULL,            -- 발명자/창작자 구분
                    name TEXT NOT NULL,                    -- 이름
                    nationality TEXT,                      -- 국적
                    address TEXT,                          -- 주소
                    creator_cd TEXT,                       -- 발명자/창작자 코드
                    seq INTEGER,                           -- 일련번호
                    FOREIGN KEY (ip_right_id) REFERENCES ip_rights(id)
                )
            ''')
            
            # right_holders 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS right_holders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_right_id INTEGER NOT NULL,
                    name TEXT NOT NULL,                    -- 권리자 이름
                    eng_name TEXT,                         -- 영문 이름
                    nationality TEXT,                      -- 국적
                    address TEXT,                          -- 주소
                    rgst_cs_name TEXT,                     -- 권리자등록(변경)이름
                    rgst_cs_date TEXT,                     -- 권리자등록(변경)일
                    rgst_cs_reason TEXT,                   -- 권리자등록(변경)사유
                    is_final_owner BOOLEAN DEFAULT 0,      -- 최종권리자여부
                    FOREIGN KEY (ip_right_id) REFERENCES ip_rights(id)
                )
            ''')
            
            # annual_fees 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS annual_fees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_right_id INTEGER NOT NULL,
                    start_year INTEGER,                    -- 시작연차
                    end_year INTEGER,                      -- 종료연차
                    payment_date TEXT,                     -- 납부일
                    amount INTEGER,                        -- 납부금액
                    FOREIGN KEY (ip_right_id) REFERENCES ip_rights(id)
                )
            ''')
            
            # 인덱스 생성
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_ip_rights_rgst_no ON ip_rights(rgst_no)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_ip_rights_appl_no ON ip_rights(appl_no)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_ip_rights_type ON ip_rights(right_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_right_holders_name ON right_holders(name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_applicants_name ON applicants(name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_creators_name ON creators(name)')
            
            conn.commit()
            self.logger.info("Database tables and indexes created successfully")

db = Database()