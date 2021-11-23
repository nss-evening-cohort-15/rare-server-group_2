import sqlite3
import json
from models import Category


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