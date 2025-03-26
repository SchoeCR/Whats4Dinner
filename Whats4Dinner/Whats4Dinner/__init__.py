"""
The flask application package.
"""

from flask import Flask, flash, redirect, render_template, session
from cs50 import SQL
app = Flask(__name__)

import Whats4Dinner.views

app.secret_key = b'49a05b0a2838342efe5dcbbacaae129afb817bc15deaf3b51ec815db696e3012'
