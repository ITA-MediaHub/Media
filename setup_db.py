import sqlite3

connection = sqlite3.connect("dev.sqlite3")
cursor = connection.cursor()

with open("setup_db.sql") as file:
    script = file.read()
    cursor.executescript(script)

