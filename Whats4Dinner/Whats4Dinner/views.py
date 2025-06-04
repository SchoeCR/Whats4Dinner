"""
Routes and views for the flask application.
"""

from asyncio.windows_events import NULL
from importlib import reload
import sqlite3
import tkinter.messagebox
from urllib import response
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import render_template, request, flash, redirect, session, json, Flask, jsonify
from Whats4Dinner import app
from .utils import *
import requests
from .config import API_KEY

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/profile')
def profile():
    """Renders the profile page."""
    return render_template(
        'profile.html',
        title='User Profile',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/register', methods=["GET", "POST"])
def register():
    """Renders the register page."""
    
    if request.method == "GET":
        return render_template(
            'register.html',
            title='Register',
            year=datetime.now().year,
            message='Your application description page.'
        )

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        added_date = datetime.now().date
        
        # Check form variables for null values
        if not first_name:
            return render_template(
            'register.html', title='Register',
            year=datetime.now().year,
            validation_error='Please enter a first name.')

        if not last_name:
            return render_template(
            'register.html', title='Register',
            year=datetime.now().year,
            validation_error='Please enter a last name.')

        if not email:
            return render_template(
            'register.html', title='Register',
            year=datetime.now().year,
            validation_error='Please enter an email.')

        if not password:
            return render_template(
            'register.html', title='Register',
            year=datetime.now().year,
            validation_error='Please enter a password.')

        if not confirmation:
            return render_template(
            'register.html', title='Register',
            year=datetime.now().year,
            validation_error='Please confirm your password.')

        # Validate psw entry matches
        if password != confirmation:
            return render_template(
            'register.html',
            title='Register',
            year=datetime.now().year,
            validation_error='Passwords do not match. Please fix.')

        # TODO: Improve security by changing to parameterised query
        # Check if profile with received email already exists
        profile = db_select("SELECT * FROM users WHERE email = ?",(email,))
        if len(profile) >= 1:
            return render_template(
            'register.html', title='Register',
            year=datetime.now().year,
            validation_error='Sorry, a user profile with the entered email already exists.')

        # Hash password
        psw_hash = generate_password_hash(password)

        # Get current date
        date_now = datetime.now()

        # Post new user to database
        db_insert("users",["first_name","last_name","email","hash","added_date"],[first_name,last_name,email,psw_hash,date_now])

        return render_template(
        'login.html', title='Login',
        year=datetime.now().year,
        new_user='A new user has been created!')

@app.route('/login', methods=["GET", "POST"])
def login():
    """Renders the login page."""
    
    if request.method == "GET":
        return render_template(
            'login.html',
            title='Login',
            year=datetime.now().year,
            login_prompt='Please enter your account details to login.'
        )

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check form variables for null values
        # Check if email is null
        if not email:
            return render_template(
            'login.html', title='Login',
            year=datetime.now().year,
            validation_error='Please enter an email.')

        # Check if password is null
        if not password:
            return render_template(
            'login.html', title='Login',
            year=datetime.now().year,
            validation_error='Please enter a password.')

        # Query database for existing account with matching credentials
        profile = db_select(f"SELECT * FROM users WHERE email='{email}'")

        # Retrieve stored password hash
        pswhash = profile[0]["hash"]

        # Check if profile is null or passwords do not match
        if len(profile) != 1 or not check_password_hash(pswhash,password):
            return render_template(
            'login.html', title='Login',
            year=datetime.now().year,
            validation_error='The email or password is incorrect.\nPlease try again.')

        # TODO: Create new session for user_id
        session['user_id'] = profile[0]['user_id']
        session['first_name'] = profile[0]['first_name']

        # Redirect user to home page
        return redirect("/")

@app.route('/logout', methods=["GET"])
def logout():
    """Logs user out of web app (Clears session)."""

    # Forget any user_id
    session.clear()

    # Redirect user to login
    return redirect("/")

@app.route('/search', methods=["GET","POST"])
def search_recipe():
    """Route for user to search for recipe on root page"""
    if request.method == "GET":       
        render_template(
            'index.html',
            title='Home page',
            year=datetime.now().year)

    elif request.method == "POST":

        # Assign form values to variables
        query_input = request.form.get("keyword")
        
        # Loop through list items and return item name if it's checked
        #intolerance_input = request.form.get("intolerances_id")

        # Combine list into CSV string
        intolerance_list = request.form.getlist("intolerances");
        intolerance_csv_string = ",".join(intolerance_list)

        # Validate form input
        if not query_input:
            return render_template(
            'index.html',
            title='Home page',
            year=datetime.now().year,
            missing_input='Please enter a meal or ingredient to search')
    
        base_url = "https://api.spoonacular.com/recipes/complexSearch"
        query = query_input 
        number = 5
        offset = get_random_Int(0,150)
       
        # TODO: Improve URL ecoding and string building
        URL = f"{base_url}?query={query}&intolerances={intolerance_csv_string}&number={number}&offset={offset}&apiKey={API_KEY}"

        # API call via requests library
        response = requests.get(URL)

        # Verify response is valid
        if response.status_code == 200:
            # Assign API call results to data
            parsed_json = response.json()
            print(f'json: {parsed_json}')
            
            # Extract title and image
            extracted_data = {}
            for recipe in parsed_json['results']:
                extracted_data[recipe['id']] = {
                    'id': recipe['id'],
                    'title': recipe['title'],
                    'image': recipe['image']
                }
            print(extracted_data)
            # Redirect/render index.html template. Pass results dictionary to index.html to be rendered.
            return render_template(
                'index.html',
                title='Home page',
                year=datetime.now().year,
                recipes=extracted_data)
        # API call has returned a response code other than 200
        else:
            # Render index.html page with message code alerting no results.
            return render_template(
            'index.html',
            title='Home page',
            year=datetime.now().year,
            invalid_response='No results found.')

        # TODO: Parameterise the query 
        # Figure out how to process the JSON. I think we can render it directly in the view template. 
        # Otherwise, we need to process the JSON and return an array of data.
        # Review ... https://medium.com/@modimuskan397/how-to-parse-json-file-and-show-output-json-using-flask-c0b415f3f0a0

@app.route('/recipe/view/<recipe_id>', methods=["GET"])
def recipe_view(recipe_id):
    # Route for user to view recipe in detail.
    # User reached page via GET method.
        
    # Validate form input
    if not recipe_id:
        return render_template(
        'recipe.html',
        title='Recipe - Detail',
        year=datetime.now().year,
        recipe_missing='Error - recipe ID cannot be found.')
    
    base_url = "https://api.spoonacular.com/recipes/"
        
    URL = f"{base_url}{recipe_id}/information?addWinePairing=true&apiKey={API_KEY}"

    # API call via requests library
    response = requests.get(URL)

    # Verify response is valid
    if response.status_code == 200:
        # Assign API call results to data
        parsed_json = response.json()
        #print(f'json: {parsed_json}')
            
        # Extract form content fields
        extracted_data = {}
        instructions = {}
        nutrition = {}
        recipe_summary = {}
        extracted_data = parsed_json
        dairyFree = extracted_data["dairyFree"]
        glutenFree = extracted_data["glutenFree"]
        vegan = extracted_data["vegan"]
        vegetarian = extracted_data["vegetarian"]
        instructions = {} #get_Recipe_Instructions(recipe_id)
        nutrition = {} #get_Nutrition(recipe_id)
        recipe_summary = {} #get_Recipe_Summary(recipe_id)
        similar = {} #get_Recipe_Similar(recipe_id)
        wine_pair = extracted_data["winePairing"]

        # Redirect/render index.html template. Pass results dictionary to index.html to be rendered.
        return render_template(
            'recipe.html',
            title='Recipe - Detail',
            year=datetime.now().year,
            recipes=extracted_data, 
            dairyFree=dairyFree, 
            glutenFree=glutenFree, 
            vegan=vegan, 
            vegetarian=vegetarian, 
            instructions=instructions, 
            nutrition=nutrition,
            similar=similar,
            wine_pair=wine_pair)
        
    # API call has returned a response code other than 200
    else:
        # Render index.html page with message code alerting no results.
        return render_template(
        'index.html',
        title='Home page',
        year=datetime.now().year,
        invalid_response='No results found.')

@app.route('/recipe/instructions/<recipe_id>', methods=["GET"])
def get_recipe_instructions(recipe_id):

    instructions_json = get_Recipe_Instructions(recipe_id)
    return instructions_json

@app.route('/recipe/nutrition/<recipe_id>', methods=["GET"])
def get_recipe_nutrition(recipe_id):

    nutrition_json = get_Nutrition(recipe_id)
    return nutrition_json

@app.route('/recipe/similar/<recipe_id>', methods=["GET"])
def get_recipe_similar(recipe_id):

    similar_json = get_Recipe_Similar(recipe_id)
    return similar_json

@app.route('/favourite-recipe', methods=["POST"])
def add_favourite():
    """Adds a favourite for a user."""
    user_id = request.form.get("user_id")
    recipe_id = request.form.get("recipe_id")
    recipe_name = request.form.get("recipe_name")
    recipe_summary = request.form.get("recipe_summary")
    recipe_image = request.form.get("recipe_image")

    # Validate inputs
    if not user_id:
        return jsonify({'success': False, 'message': "Invalid user"}), 400
    if not recipe_id or not recipe_name:
        return jsonify({'success': False, 'message': "Invalid recipe"}), 400

    # Save to Database
    try:

        # Check to see if it's already favourited. 
        existing_favourite_id = db_select(f"SELECT favourite_id FROM favourite_Recipes WHERE user_id = {user_id} AND recipe_id = {recipe_id}")

        if not existing_favourite_id:
            db_insert("favourite_Recipes", ["user_id", "recipe_id", "recipe_name", "recipe_summary", "recipe_image"],
                      [user_id, recipe_id, recipe_name, recipe_summary, recipe_image])
            return jsonify({'success': True, 'message': "Recipe added to favourites"}), 200
        else:
            return jsonify({'success': True, 'message': "You've already favourited this recipe. ;)"}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/favourite-recipe/<recipe_id>/user/<user_id>/check', methods=["GET"])
def check_favourite_recipe(recipe_id, user_id):
       
    # Validate inputs
    if not user_id:
        return jsonify({'success': False, 'message': "Invalid user"}), 400
    if not recipe_id:
        return jsonify({'success': False, 'message': "Invalid recipe"}), 400

    # TODO: Improve security
    # Check to see if it's already favourited. 
    existing_favourite_id = db_select(f"SELECT favourite_id FROM favourite_Recipes WHERE user_id = {user_id} AND recipe_id = {recipe_id}")
        
    if existing_favourite_id:
        return jsonify({'success': True, 'message': "Recipe already favourited. :)"}), 200
    else:
        return jsonify({'success': False, 'message': "Recipe not favourited :("}), 400

@app.route('/login/modal/user/<email>/password/<password>', methods=["POST"])
def favourite_loginReq(email, password):
    # User attempted to favourite a recipe without being logged in.
        
    # Validate input
    if not email:
        return jsonify({'success': False, 'message': "Email invalid"}), 400

    # Check if password is null
    if not password:
        return jsonify({'success': False, 'message': "Password invalid"}), 400

    # Query database for existing account with matching credentials
    profile = db_select(f"SELECT * FROM users WHERE email='{email}'")

    # Retrieve stored password hash
    pswhash = profile[0]["hash"]

    # Check if profile is null or passwords do not match
    if len(profile) != 1 or not check_password_hash(pswhash,password):
        return 

    # Create new session for user_id
    session['user_id'] = profile[0]['user_id']
    session['first_name'] = profile[0]['first_name']

    return jsonify({'success': True, 'message': "Logged in."})

@app.route('/profile/user/favourites', methods=["GET"])
def user_favourites():
    
    if "user_id" not in session:
        return redirect("/login")
    else:
        user_id = session["user_id"]

    response = get_user_favourites(user_id)
    # Convert to list of dictionaries
    favourites = [dict(row) for row in response]

    print(favourites)

    return render_template(
        "favourites.html",
        title='My favourites',
        year=datetime.now().year,
        favourites=favourites)

@app.route('/favourite-recipe/<recipe_id>/user/<user_id>/delete/<favourite_id>', methods=["POST"])
def delete_favourite(recipe_id, user_id, favourite_id):
    # TODO
    # Validate arguments
    if not favourite_id:
        return
    # Call util function: Db_Delete
    if db_delete("favourite_Recipes","favourite_id",favourite_id) == 200:
        return user_favourites()
    else:
        return render_template(
            "favourites.html",
            title="My favourites",
            year=datetime.now().year,
            validation_error="An error has occurred")

