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