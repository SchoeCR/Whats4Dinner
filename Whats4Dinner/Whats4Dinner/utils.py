import sqlite3
import requests
import random
from .config import API_KEY
from datetime import datetime

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