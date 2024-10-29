import sqlite3

# SQLite DB 연결
conn = sqlite3.connect('patent_register.db')
cursor = conn.cursor()

# 특허(Patent) 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS patent_data (
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
