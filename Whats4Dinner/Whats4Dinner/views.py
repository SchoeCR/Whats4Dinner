"""
Routes and views for the flask application.
"""

import sqlite3
import tkinter.messagebox
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask import render_template, request, flash, redirect
from Whats4Dinner import app
from .utils import *

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
        added_date = datetime.now().date

        # TODO: Add more validation (null checks etc)
        
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

        # Check if profile with received email already exists
        profile = db_select("SELECT * FROM users WHERE email = ?",email)
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

        # TODO: Add more validation (null checks etc)
        
        # Check form variables for null values

        # Check if email is null
        if not email:
            return render_template

