import sqlite3
import json
from models import Tag


def get_all_tags():
    with sqlite3.connect("./rare.db") as conn:

        # It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        ORDER BY label;
        """)

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            tag = Tag(row['id'], row['label'])  
                        
            tags.append(tag.__dict__)  

    # Use `json` package to properly serialize list as JSON
    return json.dumps(tags)  #⭕️⭕️⭕️ convert Python data type to a string.


def get_single_tag(id):
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        where id = ?;
        """)

        dataset = db_cursor.fetchone()

        tag = Tag(dataset['id'], dataset['label'])  

    return json.dumps(tag.__dict__)  #⭕️⭕️⭕️ convert Python data type to a string.



def create_tag(new_tag):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO Tags
            ( label )
        VALUES
            ( ? );
        """,( new_tag['label'], ))
        
        id = db_cursor.lastrowid
        
        new_tag['id'] = id
        
    return json.dumps(new_tag)


def delete_tag(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        DELETE FROM Tags
        WHERE id = ?
        """, (id, ))
        
        
def edit_tag(id, new_tag): 
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Tags
        SET
          label = ?
        WHERE id = ?
        """, (new_tag['label'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # 🚫🚫🚫 Forces 404 response by main module
        return False
    else:
        # ⭕️⭕️⭕️ Forces 204 response (No) by main module
        return True