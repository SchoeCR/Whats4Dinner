"""
Helper functions for application
"""

import requests
from flask import render_template, redirect, session

def exception(message):
    #TODO - exception handler function