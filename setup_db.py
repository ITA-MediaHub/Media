import sqlite3

DATABASE = "db/dev.sqlite3"
SETUP_SCRIPT = "db/setup.sql"

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

with open(SETUP_SCRIPT) as file:
    script = file.read()
    cursor.executescript(script)

