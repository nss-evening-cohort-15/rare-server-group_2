import sqlite3
import json

from models import Category

def get_all_categories():
    with sqlite3.connect("./rare.db") as conn:

        # It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM categories c
        ORDER BY label;
        """)

        categories = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            category = Category(row['id'], row['label'])  
                        
            categories.append(category.__dict__)  

    # Use `json` package to properly serialize list as JSON
    return json.dumps(categories)  #⭕️⭕️⭕️ convert Python data type to a string.


def get_single_category(id):
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM categories c
        where id = ?;
        """)

        dataset = db_cursor.fetchone()

        category = Category(dataset['id'], dataset['label'])  

    return json.dumps(category.__dict__)  #⭕️⭕️⭕️ convert Python data type to a string.


def edit_category(id, new_category): 
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Categories
        SET
          label = ?
        WHERE id = ?
        """, (new_category['label'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # 🚫🚫🚫 Forces 404 response by main module
        return False
    else:
        # ⭕️⭕️⭕️ Forces 204 response (No) by main module
        return True

