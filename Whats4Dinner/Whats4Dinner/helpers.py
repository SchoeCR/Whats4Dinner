import sqlite3

def duplicate_user(email):
    # Check if a user profile with argument email, already exists
    # Query table users

def db_execute():
    
    conn = get_db_connection()
    cursor = conn.cursor()

def get_db_connection():
    conn = sqlite3.connect('dinner.db')
    conn.row_factory = sqlite3.Row
    return conn