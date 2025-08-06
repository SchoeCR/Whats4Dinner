from ast import Return
from doctest import debug
from math import e
from multiprocessing import Value
from optparse import Values
import sqlite3
from turtle import update
from flask import redirect, jsonify, session
import requests
import random
from .config import API_KEY
from datetime import datetime

tables_approved = ['users', 'favourite_Recipes', 'shopping_List', 'meal_plan']
columns_approved = {
    'db_update': {
        'users': ['user_id', 'first_name', 'last_name', 'email', 'hash', 'added_date'],
        'meal_plan': ['user_id', 'meal_id', 'meal_name','meal_image','planned_date','made_bool','flavour_rating','cooking_rating']},
    'db_select': {
        'users': ['user_id', 'first_name','last_name','email','hash','added_date'],
        'favourite_Recipes':['favourite_id','user_id','recipe_id','recipe_name','recipe_summary','recipe_image'],
        'shopping_List':['shopping_id','user_id','ingredient_id','ingredient_name','ingredient_image','quantity','unit','date_added'],
        'meal_plan': ['user_id', 'meal_id', 'meal_name','meal_image','planned_date','made_bool','flavour_rating','cooking_rating']},
    'db_insert': {
        'users':['user_id','first_name','last_name','email','hash','added_date'],
        'favourite_Recipes':['favourite_id','user_id','recipe_id','recipe_name','recipe_summary','recipe_image'],
        'shopping_List':['shopping_id','user_id','ingredient_id','ingredient_name','ingredient_image','quantity','unit','date_added'],
        'meal_plan': ['user_id', 'meal_id', 'meal_name','meal_image','planned_date','made_bool','flavour_rating','cooking_rating']}
    }

# TODO: Upgrade to paramaterized query (refer db_update)
def db_insert(table, insertvalues=None):
    try:
        # Check table against whitelist
        if table not in tables_approved:
            return 400
        
        # Check insert_values against whitelist
        function_name = "db_insert"
        if function_name not in columns_approved or table not in columns_approved[function_name]:
            return 400
        if not insertvalues:
            return 400
                
        columns_list = []
        values_list = []
        
        for key, value in insertvalues.items():
            if key in columns_approved[function_name][table]:
                columns_list.append(key)
                values_list.append(value)
        
        if not columns_list:
            return 400 # No valid columns to insert
                
        # Build query
        columns = ", ".join(columns_list)
        placeholders = ", ".join(["?"] * len(columns_list))        
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values_list)  # Pass the values dynamically
        conn.commit()
        conn.close()
        return 200

    except Exception as e:
        print("Error in db_insert:", e)
        return 500
    
def db_delete(table, where=None):
    try:
        # Check table against whitelist
        if table not in tables_approved:
            return 400 #Bad Request

        if not where:
            return 400 #Prevent full table deletion

        # Build WHERE clause
        where_values = []
        where_clauses = [f"{key} = ?" for key in where]
        where_values = list(where.values())
        where_clause = " AND ".join(where_clauses)

        sql = f"DELETE FROM {table} WHERE {where_clause}"

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, where_values)
        conn.commit()
        deleted = cursor.rowcount
        conn.close()
        
        return 200 if deleted else 204 # No Content
    except Exception as e:
        print(f"Error in db_delete: {e}")
        return 500

def db_select(table, *column_select, where=None, orderby=None): #qryStr, args=()
    
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

def db_update(table, where=None, orderby=None, updateValues=None):
    function_name = "db_update"
    try:
        # Validate table arg against tables_approved
        if table not in tables_approved:
            return 400
        if function_name in columns_approved and table in columns_approved[function_name]:
            if updateValues:
                for key, value in updateValues.items():
                    if key not in columns_approved[function_name][table]:
                        return 400

        # Build SET clause
        set_clauses = []
        values = []
        if updateValues:
            for key, value in updateValues.items():
                set_clauses.append(f"{key} = ?")
                values.append(value)
            set_clause = ", ".join(set_clauses)

        # Build WHERE clause
        where_clauses = []
        if where:
            for key, value in where.items():
                where_clauses.append(f"{key} = ?")
                values.append(value)
            where_clause = " AND ".join(where_clauses)

        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

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
    # Call db_Select
    returned_data = db_select("favourite_Recipes",where={"user_id": user_id})

    # Check if any data has been returned, then return to calling function
    return returned_data or []

def get_user_shopping(user_id):
    # Get items user has added to their shopping list
    returned_data = db_select("shopping_List",where={"user_id": user_id})
    # Check if any data has been returned, then return to calling function
    return returned_data or []

def deleteShoppingListItem(shopping_id):
    if not shopping_id:
        return 400
    try:
        if db_delete("shopping_List","shopping_id",shopping_id) == 200:
            return 200
    except:
        return 500

def checkIfUserIsLoggedIn(user_id):
    if "user_id" not in session or str(session["user_id"]) != str(user_id):
        return redirect("/")
    return;

def get_user_mealplan(user_id):
    returned_data = db_select("meal_plan",where={"user_id": user_id})
    
    if isinstance(returned_data,(list,tuple)):
        return returned_data

    if returned_data is None:
        return []

    return [returned_data]


