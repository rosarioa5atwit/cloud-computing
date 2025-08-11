from contextlib import contextmanager
import mysql.connector
from fastapi import HTTPException
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "C@t23321",
    "database": "cd_database",
    "use_pure": True,  # Use pure Python implementation
    "autocommit": True,
    "charset": "utf8mb4"
}

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn
    except mysql.connector.Error as e:
        print(f"MySQL Connection Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")
    finally:
        if conn and conn.is_connected():
            conn.close()

# Database Cursor Manager
@contextmanager
def get_db_cursor(dictionary=True):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=dictionary)
        try:
            yield cursor
            conn.commit()
        except mysql.connector.Error as e:
            conn.rollback()
            print(f"MySQL Error: {e}")
            raise HTTPException(status_code=500, detail="Database operation failed")
        finally:
            cursor.close()

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_db_connection)
# Base = declarative_base()

