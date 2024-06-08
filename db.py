import sqlite3

#creating a database connection
def get_db_connection():
    conn  = sqlite3.connect('pim.db')
    return conn

#create a table that has the users
def create_user_table():
    conn = get_db_connection() #connect to database
    cursor = conn.cursor() #creates a cursor, look more into this
    #SQL command to create users table if it doesnt already exist
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users (
                   username TEXT PRIMARY KEY,
                   password TEXT NOT NULL
                   )
                   ''')
    conn.commit() #commit the transaction
    conn.close() #close the connection
#table is created, this will create a new user, and check for errors if username already exists
def add_user(username, password):
    conn = get_db_connection()
    cursor =  conn.cursor()

    try:
        #execute a SQL command to insert a new user
        cursor.execute('INSERT INTO users (username,password) VALUES (?,?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

#authentication to make sure the username and password exist
def authenticate(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username,password))
    result = cursor.fetchone() #fetch one result(none if no match)
    conn.close()
    return result is not None #wierd way to say return true if a match was found, otherwise return false








    # get_db_connection: Connects to the SQLite database.
    # create_users_table: Creates a table for storing users if it doesn't already exist.
    # add_user: Adds a new user to the database and handles duplicate usernames.
    # authenticate: Verifies if the provided username and password match an entry in the database.