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

<b>For example:</b>
The hello() view that was added to the app factory earlier in the tutorial has the name <b>'hello'</b> and can
be linked to with url_for('hello'). If it took an argument, which you will see later, it would be linked to using 
url_for('hello', who='World').

When using a blueprint, the name of the blueprint is prepended to the name of the function, so the endpoint for the 
login function you wrote above is 'auto.login' because you added it to the 'auto' blueprint.
