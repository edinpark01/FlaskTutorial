import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username '
        'FROM post p JOIN user u ON p.author_id = u.id ' 
        'ORDER BY created DESC'
    ).fetchall()

    return render_template('blog/index.html', posts=posts)


# The create VIEW works the same as the auth register view.
# Either the form is displayed, or the posted data is validated and the post is added to the database or an error
# is shown
#
# The login_required DECORATOR you wrote earlier is used on the blog views. A user must be logged in to visit these
# views, otherwise they will be redirected to the login page.
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id) '
                'VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

        return render_template('blog/create.html')


# Both the Update and Delete views will need to fetch a post by id and check if the author matched the logged in user.
# To avoid duplicating code, you can write a function to get the post and call it from each view.
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username '
        'FROM post p JOIN user u ON p.author_id = u.id'
        'WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, 'Post id {0} does not exist.'.format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

