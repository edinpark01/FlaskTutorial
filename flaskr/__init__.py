# coding: utf-8
#   The __init__.py serves double duty:
#
#   1.  It will contain the application factory, AND
#   2.  It tells Python that the flaskr directory should be treated as a package.
#
#   --------------------------------------------------------------------------------------------------------------------
#   The project directory will contain:
#
#   flaskr/     a Python package containing your application code and files.
#   tests/      a directory containing test modules
#

import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    # create_app is also known as "the application factory function."

    app = Flask(__name__, instance_relative_config=True)
    print(" * ( Current Module Name ) __name__ [ ", __name__," ]")
    """
    app = Flask(__name__, instance_relative_config=True) creates the Flask instance.
        *   __name__ is the name of the current Python module. The app needs to know where it’s located to set up 
            some paths, and __name__ is a convenient way to tell it that.
        *   instance_relative_config=True tells the app that configuration files are relative to the instance folder. 
            The instance folder is located outside the flaskr package and can hold local data that shouldn’t be 
            committed to version control, such as configuration secrets and the database file.
    """

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    print(" * app.instance_path ==>> [ ", app.instance_path, " ]")

    """
    app.config.from_mapping() sets some default configuration that the app will use:
        *   SECRET_KEY is used by Flask and extensions to keep data safe. It’s set to 'dev' to provide a 
            convenient value during development, but it should be overridden with a random value when deploying.
        *   DATABASE is the path where the SQLite database file will be saved. It’s under app.instance_path, which 
            is the path that Flask has chosen for the instance folder. You’ll learn more about the database in the 
            next section.
    """

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        """
        app.config.from_pyfile():
            *   overrides the default configuration with values taken from the config.py file in the instance folder 
                if it exists. For example, when deploying, this can be used to set a real SECRET_KEY.
            *   test_config can also be passed to the factory, and will be used instead of the instance configuration. 
                This is so the tests you’ll write later in the tutorial can be configured independently of any 
                development values you have configured.
        """
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        """
        os.makedirs():
            *   ensures that app.instance_path exists. Flask doesn’t create the instance folder automatically, 
                but it needs to be created because your project will create the SQLite database file there.
        """
    except OSError:
        pass

    # a simple page that says hello
    """
        @app.route():
            *   creates a simple route so you can see the application working before getting into the rest of 
                the tutorial. It creates a connection between the URL /hello and a function that returns a response, 
                the string 'Hello, World!' in this case.
    """
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    print(" * Registering with application - calling init_app(app)")
    from . import db
    db.init_app(app)

    print(" * Registering with application - auth Blueprint")
    from . import auth
    app.register_blueprint(auth.bp)

    print(" * Registering with application - blog Blueprint")
    from . import blog
    app.register_blueprint(blog.bp)
    """
    Unlike the auth blueprint, the blog blueprint does not have a url_prefix ( for auth it is /auth ). 
    So the index view will be at /, the create view at /create, and so on. The blog is the main feature of Flask, so it 
    makes sense that the blog index will be the main index. 
    
    However, the endpoint for the index view defined below will be blog.index. Some of the authentication views referred 
    to a plain index endpoint. 
    
    app.add_url_rule(): 
        *   Associates the endpoint name 'index' with the '/' url so that url_for('index') or url_for('blog.index') will 
            both work, generating the same '/' URL either way. 
    
    In another application you might give the blog blueprint a url_prefix and define a separate index view in the 
    application factory, similar to the hello view. Then the index and blog.index endpoints and URLs would be different. 
    """
    app.add_url_rule('/', endpoint='index')
    print(" * Returning App")
    return app
