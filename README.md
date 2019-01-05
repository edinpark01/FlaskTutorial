# Flask Tutorial
Here I will be working on the tutorial provided at [Flask Tutorial](http://flask.pocoo.org/docs/1.0/tutorial/)

### Run The Application
Now you can run your application using the flask command. From the terminal, tell Flask where to find your application, 
then run it in development mode.

Development mode shows an interactive debugger whenever a page raises an exception, and restarts the server whenever 
you make changes to the code. You can leave it running and just reload the browser page as you follow the tutorial.

###### For Mac/Linux 
``` 
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

### Define and Access the Database
Python comes with built-in support for SQLite in the sqlite3 module.

SQLite is convenient because it doesn’t require setting up a separate database server and is built-in to Python. 
However, if concurrent requests try to write to the database at the same time, they will slow down as each write 
happens sequentially. Small applications won’t notice this. Once you become big, you may want to switch to a different 
database.

###### Connect to the Database
The first thing to do when working with a SQLite database (and most other Python database libraries) is to create 
a connection to it. Any queries and operations are performed using the connection, which is closed after the work is 
finished.

In web applications this connection is typically tied to the request. It is created at some point when handling a 
request, and closed before the response is sent.

###### CREATE the tables
In SQLite, data is stored in tables and columns. These need to be created before you can store and retrieve data. 
Flaskr will store users in the user table, and posts in the post table. Create a file with the SQL commands needed 
to create empty tables:

###### Register with the Application
The close_db and init_db_command functions need to be registered with the application instance, otherwise they
won’t be used by the application. However, since you’re using a factory function, that instance isn’t available 
when writing the functions. Instead, write a function that takes an application and does the registration.

###### Initialize the Database File
Now that init-db has been registered with the app, it can be called using the flask command, similar to the 
run command from the previous page.

<b>Note</b>
If you’re still running the server from the previous page, you can either stop the server, or run this command 
in a new terminal. If you use a new terminal, remember to change to your project directory and activate the env as 
described in Activate the environment. You’ll also need to set FLASK_APP and FLASK_ENV as shown on the previous page.

Run the init-db command:

```
flask init-db
Initialized the database.
```

There will now be a flaskr.sqlite file in the instance folder in your project.

### Blueprints and Views
A view function is the code you write to respond to requests to your applications.
* Flask uses patterns to match the incoming request URL to the view that should handle it. 
* The view returns data that Flask turns into an outgoing response.
* Flask can also go the other direction and generate a URL to a view based on its name and arguments.

###### Create a blueprint
A <b>Blueprint</b> is a way to organize group of related views and other code. Rather than registering views and other 
code directly with an application, they are registered with a blueprint. Then the blueprint is registered with the 
application when its available in the factory function.

Our app, Flaskr, will have two blueprints:
1. One for authentication functions
2. One for the blog posts functions
The code for each blueprint will go in a separate module. 

Since the blog needs to know about authentication, you will write the authentication one first. 

###### The First View: Register
When the user visits the /auth/register URL, the register view will:
1. Return HTML with a form for them to fill out. 
2. Once submitted it will validate the input and:
* Show the form again with an error message OR
* Create the new user and go to the login page

For now you will just write the view code.

###### Login View
This view follows the same pattern as the register view. 

###### Logout View                                          
To log out, you need to remove the user id from the session. Then load_logged_in_user won't load a user on 
subsequent requests.    

###### Required Authentication in Other Views
Creating, editing, and deleting blog posts will require a user to be logged in. A decorator can be used to ckeck 
this for each view it's applied to.

###### Endpoints and URLs
The url_for() function generates the URL to a view based on a name and arguments. 
The name associated with a view is also called the endpoint, and by default it is the same as the name of the view 
function. 

<b>For example:</b><br/>
The hello() view that was added to the app factory earlier in the tutorial has the name <b>'hello'</b> and can
be linked to with url_for('hello'). If it took an argument, which you will see later, it would be linked to using 
url_for('hello', who='World').

When using a blueprint, the name of the blueprint is prepended to the name of the function, so the endpoint for the 
login function you wrote above is 'auto.login' because you added it to the 'auto' blueprint.

### Templates
You've written the authentication views for your application, but if you are running the server and try to go to any 
of the URLs, you will see a TemplateNotFound Error. 

The reason why you are seeing this error is because the view are calling render_template(), but you haven't written 
the templates yet. The templates files will be stored in the templates directory inside the flaskr package. 

Templates are files that contain static data as well as placeholders for dynamic data. A template is rendered with 
specific data to produce a final document. <b><i>Flask uses the [Jinja](http://jinja.pocoo.org/docs/2.10/templates/) 
template library to render templates.</i></b>

In your application, you will use templates to render HTML, which will display in the user's browser. In Flask,
Jinja is configured to <i>autoescape</i> any data that is rendered in HTML templates. This means that it is safe to
render user input; any characters they've entered that could mess with the HTML, such as < and > will be escaped with 
safe values that look the same in the browser but don't cause unwanted effects. 

Junja looks and behaves mostly like Python. Special delimiters are used to distinguish Jinja syntax from the static
data in the template. 
* Anything between {{ and }} is an expression that will be output to the final document. 
* {% and %} denotes a control flow statement like if and for. 

Unlike Python, blocks are denoted by start and end tags rather than indetentation since static text within a block 
could change indentation. 

###### The Base Layout
Each page in the application will have the same basic layout around a different body. Instead of writing the entire HTML 
structure in each template, each template will extend a base template and override specific sections. 

The base template is directly in the <b>templates</b> directory. To keep the others organized, the templates for
a blueprint will be placed in a directory with the same name as the blueprint.

### Register A User
Now that the authentication templates are written, you can register a user. Make sure the server is still running 
(flask run if it’s not), then go to http://127.0.0.1:5000/auth/register.

Try clicking the “Register” button without filling out the form and see that the browser shows an error message. 
Try removing the required attributes from the register.html template and click “Register” again. Instead of the 
browser showing an error, the page will reload and the error from flash() in the view will be shown.

Fill out a username and password and you’ll be redirected to the login page. Try entering an incorrect username, 
or the correct username and incorrect password. If you log in you’ll get an error because there’s no index view to 
redirect to yet.

### Static Files
The authentication views and templates work, but they look very plain right now. Some CSS can be added to add style 
to the HTML layout you constructed. The style won't change, so it's a static file rather than a template. 

Flask automatically ads a static view that takes a path relative to the flask/static directory and server it. 
The base.html template already has a link to the style.css file:
``` 
{{ url_for('static', filename='style.css') }}
``` 
Besides CSS, other types of static files might be files with JavaScript functions, or a logo image. They are all 
placed under the flask/static directory and referenced with url_for('static', filename=' ... ').

### Blog Blueprint
You will use the same techniques you learned about when writing the authentication blueprint to write the blog
blueprint. The blog should list all posts, allow logged in users to create posts, and allow the author of a post
to edit or delete it. 

As you implement each view, keep the development server running. As you save your changes, try going to the URL 
in your browser and testing them out. 

### Make your project Installable
Making your project installable means that you can build a distribution file and install that in another environment, 
just like you installed Flask in your project’s environment. This makes deploying your project the same as installing 
any other library, so you’re using all the standard Python tools to manage everything.

Installing also comes with other benefits that might not be obvious from the tutorial or as a new Python user, 
including:

* Currently, Python and Flask understand how to use the flaskr package only because you’re running from your project’s 
directory. Installing means you can import it no matter where you run from.
* You can manage your project’s dependencies just like other packages do, so pip install yourproject.whl installs them.
* Test tools can isolate your test environment from your development environment.

<b>Note</b>

This is being introduced late in the tutorial, but in your future projects you should always start with this.

###### Describe the project
The setup.py file describes your file and the files that belong to it.

To include other files, such as the static and templates directories, include_package_data is set. 
Python needs another file named MANIFEST.in to tell what this other data is.

MANIFEST.in
```
include flaskr/schema.sql
graft flaskr/static
graft flaskr/templates
global-exclude *.pyc
```

This tells Python to copy everything in the static and templates directories, and the schema.sql file, but to 
exclude all bytecode files.

###### Install the Project
Use <b>pip</b> to install your project in the virtual environment.

```
pip install -e
```

This tells pip to find setup.py in the current directory and install it in editable or development mode. 
* <b>Editable mode</b> means that as you make changes to your local code, you’ll only need to re-install if you 
change the metadata about the project, such as its dependencies.

Nothing changes from how you’ve been running your project so far. FLASK_APP is still set to flaskr and flask run 
still runs the application.

### Test Coverage
Writing unit tests for your application lets you check that the code you wrote works the way you expect. Flask provides
a test client that simulates requests to the application and returns the response data. 

You should test as much of your code as possible. Code in functions only runs when the function is called, and code in 
branches, such as if blocks, only runs if conditions is met. You want to make sure that each function is tested with 
data that covers each branch. 

You will use <b>pytest</b> and <b>coverage</b> to test and measure your code. Install them both:
```
pip install pytest coverage
``` 

###### Setup and fixtures
The test code is located in the tests directory. This directory is next to the flaskr package, <b>not inside it</b>. 
The tests/conftest.py file contains setup functions called fixtures that each test will used. Tests are in Python modules
that start with test_, and each test function in those modules also starts with test_.

Each test will create a new temporary database file and populate some data that will be used in the tests. Write a SQL
file to insert that data. 

