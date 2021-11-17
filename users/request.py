import json
import sqlite3

from urllib.parse import unquote_plus

from models import User


def get_all_users():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:
    #  keyword with will open a file connection fro you, 
    #  at line 102, the indentation stops, means the file connection is shut down.
    
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor() # ⭕️cursor prepares you to execute a statement, it will scan table for you⭕️

        # Write the SQL query (a multi-line string) to get the information you want
        # alias Animal and Location to a , l 
        # id, first_name, last_name, email, bio, username, password, profile_image_url, created_on, active
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Users u 
        """)
        users = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            
            user = User(row['id'], row['first_name'], row['last_name'], row['email'],
                        row['password'], row['profile_image_url'], row['created_on'],
                        row['active'])              
            
            users.append(user.__dict__)  

    # Use `json` package to properly serialize list as JSON
    return json.dumps(users)  #⭕️convert Python data type to a string.⭕️



# Function with a single parameter
def get_single_user(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            u.id,
            u.username,
            u.first_name,
            u.last_name,
            u.email,
            u.password
        FROM Users u
        WHERE u.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an user instance from the current row
        user = User(data['id'], data['name'], data['breed'],
                            data['status'], data['location_id'],
                            data['customer_id'])

        return json.dumps(user.__dict__)
    

def get_users_by_email(email):

    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select 
            first_name,
            last_name,
            email,
            password,
            bio,
            username,
            profile_image_url,
            created_on,
            active,
            id
        from Users u
        WHERE u.email = ?
        """, ( email, ))

        users = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            user = User(*row)
            serializable_user = user.__dict__
            serializable_user['created_on'] = str(user.created_on)
            users.append(serializable_user)
        
    return json.dumps(users)
    
    
def create_user(new_user):
    
    user = User(first_name=new_user['first_name'],
              last_name=new_user['last_name'], email=new_user['email'],
              password=new_user['password'])
    
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Users
          ( id,
            first_name,
            last_name,
            email,
            bio,
            username,
            password,
            profile_image_url,
            created_on,
            active )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, ( user.id, user.first_name, user.last_name, user.email, user.bio,
              user.username, user.password, user.profile_image_url, user.created_on, user.active))

        # The `lastrowid` property on the cursor will return the primary key of the last thing that got added to the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the user dictionary that was sent by the client so that 
        # the client sees the primary key in the response.
        user.id = id

    serializable_user = user.__dict__
    serializable_user['created_on'] = str(user.created_on)

    return json.dumps(serializable_user)  
    # it's better to just return user, to keep this function single-purpose instead pf handling any web response stuff
