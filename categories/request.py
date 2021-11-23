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