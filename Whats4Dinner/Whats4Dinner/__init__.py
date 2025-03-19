"""
The flask application package.
"""

from flask import Flask, flash, redirect, render_template
from flask_session import Session
from cs50 import SQL
app = Flask(__name__)

import Whats4Dinner.views

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

