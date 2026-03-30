import sqlite3
import os

def setup(database_url, setup_script):
    connection = sqlite3.connect(database_url)
    cursor = connection.cursor()

    with open(setup_script) as file:
        script = file.read()
        cursor.executescript(script)

if __name__ == "__main__":
    setup(os.environ.get("DATABASE") or "db/dev.sqlite3", os.environ.get("DB_SETUP_SCRIPT") or "db/setup.sql")