from ast import Return
from multiprocessing import Value
import sqlite3
from flask import redirect, jsonify
import requests
import random
from .config import API_KEY
from datetime import datetime

tables_approved = ['users', 'favourite_Recipes']
columns_approved = {
    'db_update': {
        'users': ['user_id', 'first_name', 'last_name', 'email', 'hash', 'added_date']},
    'db_select': {
        'users': ['user_id', 'first_name','last_name','email','hash','added_date'],
        'favourite_Recipes':['favourite_id','user_id','recipe_id','recipe_name','recipe_summary','recipe_image']},
    }

# TODO: Upgrade to paramaterized query (refer db_update)
def db_insert(table, columns, values):
    placeholders = ", ".join(["?"] * len(values))  # Create placeholders dynamically
    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)  # Pass the values dynamically
    conn.commit()
    conn.close()
    return

# TODO: Upgrade to paramaterized query (refer db_update)
def db_delete(table, column_reference, row_reference):
    try:
        # Validate inputs
        if row_reference is None or table is None or column_reference is None:
            return 400

        sql = f"DELETE FROM {table} WHERE {column_reference}= ?"
        args = (row_reference,)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, args)
        conn.commit()
        conn.close()
        return 200
    except:
        return 500

def db_select(table, where=None, orderby=None, *column_select): #qryStr, args=()
    
    # Check table against whitelist
    if table not in tables_approved:
        return 400
    # Check column_select against whitelist
    function_name = "db_select"
    if column_select:
        if function_name in columns_approved:
            for arg in column_select:
                for table_name, columns in columns_approved[function_name].items():
                    if arg in columns:
                        break
                else:
                    return 400
        else:
            return 400
    else: column_select = ['*']

    # Parse column select into comma separated string
    column_str = ', '.join(column_select)

    sql = f"SELECT {column_str} FROM {table}"

    values = []
    if where:
        conditions=[]
        if function_name in columns_approved and table in columns_approved[function_name]:
            for key, val in where.items():
                if key not in columns_approved[function_name][table]:
                    return 400
                conditions.append(f"{key} = ?")
                values.append(val)
            sql += " WHERE " + " AND ".join(conditions)
        else: return 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)  # Pass args as a tuple
    result = cursor.fetchall()  # Fetch data before closing
    conn.close()
    return result  # Now returning fetched data

def db_update(table, where_column=None, where_value=None, **column_value):
    function_name = "db_update"
    try:
        # Validate table arg against tables_approved
        if table not in tables_approved:
            return 400
        if function_name in columns_approved and table in columns_approved[function_name]:
           if where_column not in columns_approved[function_name][table]:
               return 400

        # Build SET clause with placeholders
        set_clauses = []
        values = []

        for key, value in column_value.items():
            if key not in columns_approved[function_name][table]:
                return 400
            set_clauses.append(f"{key} = ?")
            values.append(value)

        set_clause = ", ".join(set_clauses)

        sql = f"UPDATE {table} SET {set_clause} WHERE {where_column} = ?"
        values.append(where_value)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        return 200

    except Exception as e:
        print(f"Error: {e}")
        return 500

def get_db_connection():
    conn = sqlite3.connect('dinner.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_Recipe_Instructions(recipe_id):
    # Get detailed recipe instructions and return as JSON
    
    base_url = "https://api.spoonacular.com/recipes/"
    URL = f"{base_url}{recipe_id}/analyzedInstructions?apiKey={API_KEY}"

    # API call via requests library
    response = requests.get(URL)

    # Verify response is valid
    if response.status_code == 200:
        # Assign API call results to data
        parsed_json = response.json()
        print(f'json: {parsed_json}')
            
        # Extract form content fields
        extracted_data = {}

        # Loop over each instruction set (main recipe, sub-recipes like sauces, etc.)
        for instruction_set in parsed_json:
            for instruction in instruction_set['steps']:
                extracted_data[instruction['number']] = {
                    'number': instruction['number'],
                    'step': instruction['step']
                }

        return extracted_data
    else:
        return {}

def get_Nutrition(recipe_id):
    # Get recipe nutrition information and return as JSON
    
    base_url = "https://api.spoonacular.com/recipes/"
    URL = f"{base_url}{recipe_id}/nutritionWidget.json?apiKey={API_KEY}"

    # API call via requests library
    response = requests.get(URL)

    # Verify response is valid
    if response.status_code == 200:
        # Assign API call results to data
        parsed_json = response.json()
        print(f'json: {parsed_json}')
            
        # Extract form content fields
        extracted_data = {}
        extracted_data = parsed_json["nutrients"]

        return extracted_data
    
    else:
        return

def get_Recipe_Summary(recipe_id):
    # Get recipe summary and return

    base_url = "https://api.spoonacular.com/recipes/"
    URL = f"{base_url}{recipe_id}/summary?apiKey={API_KEY}"

    # API call via requests library
    response = requests.get(URL)

    # Verify response is valid
    if response.status_code == 200:
        # Assign API call results to data
        parsed_json = response.json()
            
        # Extract form content fields
        extracted_data = {}
        extracted_data = parsed_json

        return extracted_data
    
    else:
        return

def get_Recipe_Similar(recipe_id):
    # Get recipes that are similar to the argument recipe_id and return

    base_url = "https://api.spoonacular.com/recipes/"
    results_number = 5 # Return max 5 results
    URL = f"{base_url}{recipe_id}/similar?number={results_number}&apiKey={API_KEY}"

    # API call via requests library
    response = requests.get(URL)

    # Verify response is valid
    if response.status_code == 200:
        # Assign API call results to data
        parsed_json = response.json()

        # Extract form content fields
        extracted_data = {}
        extracted_data = parsed_json

        return extracted_data

    else:
        return

def get_random_Int(min_val, max_val):
    return random.randint(min_val,max_val)

def get_user_favourites(user_id):
    # Get recipes that user has favourited

    #TODO: Upgrade to paramterized query to increase security
    # Construct query string for db_select
    qry_string = f"SELECT * FROM favourite_Recipes WHERE user_id = {user_id}"

    # Call db_Select and pass in query string as argument
    returned_data = db_select(qry_string)

    # Check if any data has been returned, then return to calling function
    return returned_data or []

