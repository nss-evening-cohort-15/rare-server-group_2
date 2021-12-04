from datetime import datetime
import json
import sqlite3

from models import Post
from models import User

def get_single_post(id):
    with sqlite3.connect("./rare.db") as conn:
        
        conn.row_factory =  sqlite3.Row
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
            p.approved
        FROM Posts p
        WHERE p.id = ?;
            """, (id, ))
        dataset = db_cursor.fetchone()
        post = Post(dataset["id"], dataset["user_id"], dataset["category_id"], dataset["title"], dataset["publication_date"], dataset["image_url"], dataset["content"], dataset["approved"])
        
    return json.dumps(post.__dict__)
    
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
  
def delete_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """,(id,))

def edit_post(id, post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Posts
            SET
                user_id =?,
                category_id =?,
                title =?,
                publication_date = ?,
                content = ?
        WHERE id = ?
        """, (post["user_id"], post["category_id"], post["title"], post["publication_date"], post["content"], id,))

        rows_affected = db_cursor.rowcount
        if rows_affected == 0:
            return False
        else:
            return True

def create_post(new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            INSERT INTO Posts (
                user_id, category_id, title, publication_date, image_url, content, approved
            ) VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (
            new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'], new_post['image_url'], new_post['content'], new_post['approved'],
        ))
        
        id = db_cursor.lastrowid
        
        new_post['id'] = id
        
    return json.dumps(new_post)