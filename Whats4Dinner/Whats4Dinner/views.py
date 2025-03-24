"""
Routes and views for the flask application.
"""

import sqlite3
import tkinter.messagebox
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask import render_template, request
from Whats4Dinner import app
from supplementary import get_db_connection, db_select, db_insert

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
        if not first_name:
            tkinter.messagebox.showwarning("Missing value","Please enter a first name.")
            return
        if not last_name:
            tkinter.messagebox.showwarning("Missing value","Please enter a last name.")
            return
        if not email:
            tkinter.messagebox.showwarning("Missing value","Please enter an email.")
            return
        if not password:
            tkinter.messagebox.showwarning("Missing value","Please enter a password.")
            return
        if not confirmation:
            tkinter.messagebox.showwarning("Missing value","Please enter password confirmation.")
            return

        # Validate psw entry matches
        if password != confirmation:
            return render_template(
            'register.html',
            title='Register',
            year=datetime.now().year,
            message='Your application description page.',
            validation_error='Passwords do not match. Please fix.'
        )

        # Check if profile with received email already exists
        profile = db_select("SELECT * FROM users WHERE email = ?",email)
        if profile:
            tkinter.messagebox.showwarning("Existing profile","A user profile with the entered email already exists.")
            return

        # Hash password
        hash = generate_password_hash(password)

        # Post new user to database
        db_execute("INSERT INTO users (first_name, last_name, email, hash) VALUES (?, ?, ?, ?)", (first_name, last_name, email, hash))

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
