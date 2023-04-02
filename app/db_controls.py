import sqlite3
from app import app
from flask import g


def add_new_book(title=None, author=None, genre=None, language=None, topic=None, topic_to_insert=None):
    if topic is not None:
        request = f"CREATE TABLE {topic} (title TEXT, author TEXT, genre TEXT, language TEXT)"
    else:
        request = f"""INSERT INTO {topic_to_insert}
            (title, author, genre, language) VALUES 
            {title, author, genre, language}"""
    msg = ""
    try:
        with sqlite3.connect("../app.db") as connection:
            cursor = connection.cursor()
            cursor.execute(request)
            connection.commit()
            msg = "Successfully added"
    except Exception as e:
        connection.rollback()
        msg = str(e)
    finally:
        connection.close()
        return msg


def get_db(name=None):
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("../app.db")
        cursor = db.cursor()
        if name is None:
            all_data = cursor.execute("SELECT name FROM sqlite_schema WHERE type = 'table'").fetchall()
        else:
            cursor.execute(f"select * from {name}")
            all_data = cursor.fetchall()
            all_data = [list(tu) for tu in all_data]
        return all_data


def remove_table(name):
    with sqlite3.connect("../app.db") as connection:
        cursor = connection.cursor()
        cursor.execute(f"""DROP TABLE {name}""")
        connection.commit()


@app.teardown_appcontext
def close_connection(ex):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()