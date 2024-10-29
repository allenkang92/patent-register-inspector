import os
import sqlite3

# SQLite 데이터베이스 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, '..', 'data', 'patent_register.db')

# SQLite 데이터베이스 확인
def check_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 테이블 조회
    c.execute('SELECT * FROM trademarks')
    rows = c.fetchall()

    if rows:
        print(f"적재된 데이터: {rows}")
    else:
        print("테이블에 데이터가 없습니다.")

    conn.close()

if __name__ == "__main__":
    check_db()
