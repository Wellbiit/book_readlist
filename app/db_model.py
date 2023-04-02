import sqlite3

connection = sqlite3.connect("../app.db")
print("db successfully added")

connection.execute("CREATE TABLE book_test (title TEXT, author TEXT, genre TEXT, language TEXT)")
print("book_test successfully added")

connection.close()