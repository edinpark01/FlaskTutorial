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

