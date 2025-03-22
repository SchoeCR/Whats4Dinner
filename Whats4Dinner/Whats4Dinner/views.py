"""
Routes and views for the flask application.
"""

import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask import render_template, request
from Whats4Dinner import app

def get_db_connection():
    conn = sqlite3.connect('dinner.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
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

        # TODO: Add more validation (null checks etc)
        
        # Check form variables for null values

        # Validate psw entry matches
        if password != confirmation:
            return render_template(
            'register.html',
            title='Register',
            year=datetime.now().year,
            message='Your application description page.',
            validation_error='Passwords do not match. Please fix.'
        )

        # Hash password
        hash = generate_password_hash(password)

        # Post new user to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute ("INSERT INTO users (first_name, last_name, email, hash) VALUES (?, ?, ?, ?)", (first_name, last_name, email, hash))

        conn.commit()
        conn.close()

        return render_template(
            'register.html',
            title='Register',
            year=datetime.now().year,
            message='Your user has been created.'
            )

@app.route('/login', methods=["GET", "POST"])
def login():
    """Renders the login page."""
    
    if request.method == "GET":
        return render_template(
            'login.html',
            title='Login',
            year=datetime.now().year,
            message='Please enter your account details to login.'
        )

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # TODO: Add more validation (null checks etc)
        
        # Check form variables for null values


        # Validate psw entry matches
        if password != confirmation:
            return render_template(
            'register.html',
            title='Register',
            year=datetime.now().year,
            message='Your application description page.',
            validation_error='Passwords do not match. Please fix.'
        )

        # Post new user to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute ("INSERT INTO users (first_name, last_name, email, hash) VALUES (?, ?, ?, ?)", (first_name, last_name, email, hash))

        conn.commit()
        conn.close()

        return render_template(
            'register.html',
            title='Register',
            year=datetime.now().year,
            message='Your user has been created.'
            )
