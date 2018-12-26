import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

"""
This creates a Blueprint named 'auth'. Like the application object, the blueprint needs to know where it’s defined, 
so __name__ is passed as the second argument. The url_prefix will be will be added to the beginning of all the URLs 
associated with the blueprint.

Further Instructions:
1.  Import and register the blueprint from the factory using app.register_blueprint(). Place the new code at the end 
    of the factory function before returning the app.

Note: 
The authentication blueprint will have views to register new users and to log in and log out.

"""


# @bp.route associates the URL /register with the register view function.
# When Flask receives a request to /auth/register, it will call the register view and use the return value
# as the response.
@bp.route('/register', methods=('GET', 'POST'))
def register():

    # If the user submitted the form, request.method will be 'POST'.
    # In this case validating the input.
    if request.method == 'POST':

        # request.form is a special type of dict mapping submitted form keys and values
        # The user will input their username and password
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        if not username:                                                # Validates that username is not empty
            error = 'Username is required.'
        elif not password:                                              # Validates that password is not empty
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            # Validate that username is not already registered by querying the database and checking if a result is
            # returned.
            # db.execute() takes a SQL query with ? placeholders for any user input, and a tuple of values to
            # replace the placeholders with.
            # The database library will take care of escaping the values so you are not vulnerable to a
            # SQL injection attack
            # fetchone() - returns one row from the query. If the query returned no results, it returns None.
            # fetchall() - us used, which returns a list of all results.

            error = 'User {} is already registered.'.format(username)

        if error is None:
            # If validation succeeds, insert the new user data into the database. For security, passwords should
            # never be stored in the database directly. Instead, generate_password_hash() is used to securely hash
            # the password, and that hash is stored. Since this query modifies data, db.commit() needs to be called
            # afterwards to save the changes.
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()

            # After storing the user, they are redirected to the login page.
            # url_for() generates the URL for the login view based on its name.
            # This is preferable to writing the URL directly as it allows you to change the URL later without changing
            # all code that links to it.
            # redirect() generates a redirect response to the generated URL.
            return redirect(url_for('auth.login'))

        # If validation fails, the error is shown to the user.
        # flash() stores messages that can be retrieved when rendering the template.
        flash(error)

    # When the user initially navigates to auth/register, or there was an validation error, an HTML page with the
    # registration form should be shown. render_template() will render (provide) a template containing the HTML,
    # which you’ll write in the next step of the tutorial.
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        # The user is queried first and stored in a variable for later use.
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            # check_password_hash() hashes the submitted password in the same way as the stored hash and
            # securely compares them. If they match, the password is valid.
            error = 'Incorrect password'

        if error is None:
            # session is a dict that stores data across requests. When validation succeeds:
            #   *   the user’s id is stored
            #
            # In a new session:
            #   *   The data is stored in a cookie that is sent to the browser AND
            #   *   The browser then sends it back with subsequent requests.
            #
            # Flask securely signs the data so that it can’t be tampered with.
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# Now that the user's id is stored in the session, it will be available on subsequent requests.
# At the beginning of each request, if a user is logged in their information should be loaded and made
# available to other views
#
# bp.before_app_first_request() - registers a function that runs before the view function, no matter what URL is
# requested.
@bp.before_app_first_request()
def load_logged_in_user():
    """
    Checks if a user id is stored in the session and gets that user's data from the database, storing it on g.user,
    which lasts for the length of the request.

    If there is no user id, or if the id does not exist, g.user will be None.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """ This decorator returns a new view function that wraps the original view it's applied to. """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        """ This new function checks if a user is loaded and redirects to the login page otherwise. """
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    # If a user is loaded the original view is called and continues normally.
    return wrapped_view
