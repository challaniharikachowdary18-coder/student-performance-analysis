import mysql.connector
from config import Config

def get_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST, user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD, database=Config.MYSQL_DATABASE,
        port=Config.MYSQL_PORT
    )

def fetch_all(query, params=None):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params or ())
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def fetch_one(query, params=None):
    rows = fetch_all(query, params)
    return rows[0] if rows else None

def execute(query, params=None):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params or ())
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()
        conn.close()
