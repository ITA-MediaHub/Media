import sqlite3

DATABASE = "db/dev.sqlite3"

def addAuthor(last_name, first_name = None):
    db = sqlite3.connect(DATABASE, autocommit=True).cursor()
    
    if len(last_name) == 0 or (first_name is not None and len(first_name) == 0):
        raise ValueError("Names cannot be empty strings")

    if first_name:
        db.execute("SELECT id FROM author WHERE last_name=? AND first_name=?", (last_name, first_name))
    else:
        db.execute("SELECT id FROM author WHERE last_name=?", (last_name,))
    result = db.fetchone()
    if result:
        return result[0]
    
    db.execute("INSERT INTO author (last_name, first_name) VALUES (?, ?)", (last_name, first_name))
    return db.lastrowid

def removeAuthor(id):
    db = sqlite3.connect(DATABASE, autocommit=True).cursor()

    db.execute("SELECT * FROM author WHERE id=?", (id,))
    result = db.fetchone()
    if not result:
        raise ValueError("Author with given ID does not exist")

    db.execute("DELETE FROM author WHERE id=?", (id,))
    if db.rowcount < 1:
        raise RuntimeError("Unknown error deleting author")
    
def updateAuthor(id, last_name, first_name = None):
    db = sqlite3.connect(DATABASE, autocommit=True).cursor()
    
    if len(last_name) == 0 or (first_name is not None and len(first_name) == 0):
        raise ValueError("Names cannot be empty strings")
    
    db.execute("SELECT * FROM author WHERE id=?", (id,))
    result = db.fetchone()
    if not result:
        raise ValueError("Author with given ID does not exist")

    db.execute("UPDATE author SET last_name=?, first_name=? WHERE id=?", (last_name, first_name, id))
    if db.rowcount < 1:
        raise RuntimeError("Unknown error updating author")
    
def getAuthorById(id):
    db = sqlite3.connect(DATABASE, autocommit=True).cursor()
    db.execute("SELECT * FROM author WHERE id=?", (id,))
    result = db.fetchone()
    if not result:
        raise ValueError("Author with given ID does not exist")
    author_dict = {"id": result[0], "last_name": result[2]}
    if result[1]:
        author_dict["first_name"] = result[1]
    return author_dict
