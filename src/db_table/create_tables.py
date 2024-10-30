import sqlite3
import os

def init_database():
    # DB 파일 경로 설정
    db_path = 'patent_register.db'
    
    # DB 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 테이블 생성 SQL 문
    tables_sql = """
    -- 1. 공통 정보 테이블
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
    );

    -- 2. 특허/실용신안 추가 정보 테이블
    CREATE TABLE IF NOT EXISTS patent_utility_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_right_id INTEGER NOT NULL,
        claim_count INTEGER,                   -- 청구항수
        ipc_cd TEXT,                           -- IPC 코드
        cpc_cd TEXT,                           -- CPC 코드
        rfoex_yn TEXT,                         -- 심사청구여부
        rfoex_date TEXT,                       -- 심사청구일
        FOREIGN KEY (ip_right_id) REFERENCES ip_rights(id)
    );

    -- 3. 디자인 추가 정보 테이블
    CREATE TABLE IF NOT EXISTS design_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_right_id INTEGER NOT NULL,
        ds_tgt_nm TEXT,                        -- 물품명
        ptdsn_yn TEXT,                         -- 부분디자인여부
        ds_cls_nm TEXT,                        -- 디자인분류명
        ds_main_cs_cd TEXT,                    -- 국내분류코드
        ds_lc_cs_cd TEXT,                      -- 국제분류코드
        rtact_date TEXT,                       -- 소급일자
        FOREIGN KEY (ip_right_id) REFERENCES ip_rights(id)
    );

    -- 4. 상표 추가 정보 테이블
    CREATE TABLE IF NOT EXISTS trademark_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_right_id INTEGER NOT NULL,
        mark_type TEXT,                        -- 상표유형
        tm_type TEXT,                          -- 상표분류
        org_appl_rgst_no TEXT,                -- 원출원번호
        org_appl_rgst_date TEXT,              -- 원출원일자
        rtact_date TEXT,                       -- 소급일자
        FOREIGN KEY (ip_right_id) REFERENCES ip_rights(id)
    );

    -- 5. 출원인 정보 테이블
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
    );

    -- 6. 발명자/창작자 정보 테이블
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
    );

    -- 7. 권리자 정보 테이블
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
    );

    -- 8. 연차료 납부 정보 테이블
    CREATE TABLE IF NOT EXISTS annual_fees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_right_id INTEGER NOT NULL,
        start_year INTEGER,                    -- 시작연차
        end_year INTEGER,                      -- 종료연차
        payment_date TEXT,                     -- 납부일
        amount INTEGER,                        -- 납부금액
        FOREIGN KEY (ip_right_id) REFERENCES ip_rights(id)
    );

    -- 9. 상품분류 정보 테이블 (상표 전용)
    CREATE TABLE IF NOT EXISTS trademark_products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trademark_id INTEGER NOT NULL,
        product_cls_cd TEXT,                   -- 상품분류코드
        designated_goods TEXT,                 -- 지정상품
        FOREIGN KEY (trademark_id) REFERENCES ip_rights(id)
    );
    """

    # 인덱스 생성 SQL 문
    indexes_sql = """
    CREATE INDEX IF NOT EXISTS idx_ip_rights_rgst_no ON ip_rights(rgst_no);
    CREATE INDEX IF NOT EXISTS idx_ip_rights_appl_no ON ip_rights(appl_no);
    CREATE INDEX IF NOT EXISTS idx_ip_rights_type ON ip_rights(right_type);
    CREATE INDEX IF NOT EXISTS idx_right_holders_name ON right_holders(name);
    CREATE INDEX IF NOT EXISTS idx_applicants_name ON applicants(name);
    CREATE INDEX IF NOT EXISTS idx_creators_name ON creators(name);
    """

    try:
        # 테이블 생성
        cursor.executescript(tables_sql)
        
        # 인덱스 생성
        cursor.executescript(indexes_sql)
        
        # 변경사항 저장
        conn.commit()
        print("Database tables and indexes created successfully!")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        
    finally:
        # 연결 종료
        conn.close()

if __name__ == "__main__":
    init_database()