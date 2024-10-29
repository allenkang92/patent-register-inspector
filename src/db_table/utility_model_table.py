import sqlite3

# SQLite DB 연결
conn = sqlite3.connect('patent_register.db')
cursor = conn.cursor()

# 실용신안(Utility Model) 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS utility_model_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rgstNo TEXT,
    rgstDate TEXT,
    opnDate TEXT,
    applNo TEXT,
    applDate TEXT,
    title TEXT
)
''')

# DB 연결 종료
conn.close()
