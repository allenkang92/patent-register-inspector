import os
import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), 'data', 'patent_register.db')
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def initialize_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 특허 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    registration_number TEXT UNIQUE,
                    title TEXT,
                    applicant TEXT,
                    registration_date TEXT
                )
            ''')
            
            # 실용신안 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS utility_models (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    registration_number TEXT UNIQUE,
                    title TEXT,
                    applicant TEXT,
                    registration_date TEXT
                )
            ''')
            
            # 디자인 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS designs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    registration_number TEXT UNIQUE,
                    title TEXT,
                    applicant TEXT,
                    registration_date TEXT
                )
            ''')
            
            # 상표 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trademarks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    registration_number TEXT UNIQUE,
                    title TEXT,
                    applicant TEXT,
                    registration_date TEXT
                )
            ''')
            
            conn.commit()

db = Database()