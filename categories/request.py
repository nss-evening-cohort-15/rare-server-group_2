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
        """)

        categories = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            category = Category(row['id'], row['label'])  
                        
            categories.append(category.__dict__)  

    # Use `json` package to properly serialize list as JSON
    return json.dumps(categories)  #⭕️⭕️⭕️ convert Python data type to a string.


def create_catergory(new_category):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO Catergory
            ( label )
        VALUES
            ( ? );
        """,( new_category['label'], ))
        
        id = db_cursor.lastrowid
        
        new_animal['id'] = id
        
    return json.dumps(new_category)


def delete_category(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        DELETE FROM Category
        WHERE id = ?
        """, (id, ))