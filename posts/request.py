from datetime import datetime
import json
import sqlite3

from models import Post
from models import User


def get_all_posts():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
    SELECT
      p.id,
      p.user_id,
      p.category_id,
      p.title,
      p.publication_date,
      p.image_url,
      p.content,
      p.approved,
      u.first_name user_first_name,
      u.last_name user_last_name,
      u.username user_username,
      u.email user_email
    FROM Posts p
    JOIN Users u
      ON u.id = p.user_id
      
    """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['image_url'], row['content'], row['approved'])
            
            user = User(id=row['id'], first_name=row['user_first_name'], last_name=row['user_last_name'], username=row['user_username'], email=row['user_email'])
            
            post.user = user.__dict__
            post.user['created_on'] = str(user.created_on)
            
            posts.append(post.__dict__)
            
    return json.dumps(posts)
