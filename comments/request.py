import sqlite3
import json
import comments
from models import Comment
from models import User
from models import Post



    # Function with a single parameter
def get_single_comment(id):
    # Variable to hold the found comment, if it exists
    requested_comment = None

    # Iterate the comments list above. Very similar to the
    # for..of loops you used in JavaScript.
    for comment in comments:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if comment["id"] == id:
            requested_comment = comment

    return requested_comment

def create_comment(new_comment):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Comment
            ( id, post_id, author_id, content, created_on )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_comment['id'], new_comment['post_id'],
              new_comment['author_id'], new_comment['content'], 
              new_comment['created_on']
             ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the comment dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_comment['id'] = id


    return json.dumps(new_comment)

def get_all_comments():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.post_id,
            c.author_id,
            c.content,
            c.created_on,
            u.username,
            u.email,
            u.first_name,
            u.last_name,
            p.title post_title,
            p.publication_date
        FROM Comments c
        JOIN Users u
            ON u.id = c.author_id
        JOIN Posts p 
            ON p.id = c.post_id
        """)

        # Initialize an empty list to hold all comment representations
        comments = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

     # Create a comment instance from the current row
            comment = Comment(row['id'], row['post_id'], row['author_id'], row['content'],
                              row['created_on'])
            

    # Create a user instance from the current row
            user = User(id=row['id'], username=row['username'],
                        first_name=row['first_name'], 
                        last_name=row['last_name'], 
                        email=row['email'])
            post = Post( title=row['post_title'],
                        id='', 
                        user_id='',
                        category_id='',
                        publication_date=row['publication_date'], 
                        image_url='', 
                        content='', 
                        approved=True
                        )

    # Add the dictionary representation of the user to the comment
            comment.user = user.__dict__
            comment.post = post.__dict__
            comment.user['created_on'] = str(user.created_on)
            comment.post['publication_date'] = str(post.publication_date)
            comment.created_on = str(comment.created_on)


    # Add the dictionary representation of the comment to the list
            comments.append(comment.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(comments)