import sqlite3

def db_insert(qryStr):
    conn = get_db_connection()
    cursor = conn.cursor()
    result = cursor.execute(qryStr)
    conn.commit()
    conn.close()
    return result

def db_select(qryStr):
    conn = get_db_connection()
    cursor = conn.cursor()
    result = cursor.execute(qryStr)
    conn.close()
    return result

def get_db_connection():
    conn = sqlite3.connect('dinner.db')
    conn.row_factory = sqlite3.Row
    return conn
