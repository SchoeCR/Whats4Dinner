import sqlite3

def db_insert(qryStr, *args):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(qryStr, args)  # Pass args correctly
    conn.commit()  # Commit the transaction
    result = cursor.lastrowid  # Get the last inserted row's ID
    conn.close()  # Close connection after fetching the result
    return result  # Return last inserted ID


def db_select(qryStr, *args):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(qryStr, args)  # Pass args as a tuple
    result = cursor.fetchall()  # Fetch data before closing
    conn.close()
    return result  # Now returning fetched data


def get_db_connection():
    conn = sqlite3.connect('dinner.db')
    conn.row_factory = sqlite3.Row
    return conn
