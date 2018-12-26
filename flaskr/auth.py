import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

"""
This creates a Blueprint named 'auth'. Like the application object, the blueprint needs to know where it’s defined, 
so __name__ is passed as the second argument. The url_prefix will be will be added to the beggining of all the URLs 
associated with the blueprint.

Import and register the blueprint from the factory using app.register_blueprint(). Place the new code at the end 
of the factory function before returning the app.
"""