import sqlite3

def db_insert(table, columns, values):
    placeholders = ", ".join(["?"] * len(values))  # Create placeholders dynamically
    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)  # Pass the values dynamically
    conn.commit()
    conn.close()
    return

def db_select(qryStr):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(qryStr)  # Pass args as a tuple
    result = cursor.fetchall()  # Fetch data before closing
    conn.close()
    return result  # Now returning fetched data


def get_db_connection():
    conn = sqlite3.connect('dinner.db')
    conn.row_factory = sqlite3.Row
    return conn
