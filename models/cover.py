import sqlite3

DATABASE = "db/dev.sqlite3"
ALLOWED_TYPES = ["image/png", "image/jpg", "image/jpeg"]

def addCover(type, content):
    if type not in ALLOWED_TYPES:
        raise ValueError(f"type {type} is not an allowed image type!")
    db = sqlite3.connect(DATABASE, autocommit=True).cursor()
    db.execute("INSERT INTO cover (type, content) VALUES (?, ?)", (type, content))
    return db.lastrowid

def getCoverById(id):
    db = sqlite3.connect(DATABASE, autocommit=True).cursor()
    db.execute("SELECT * FROM cover WHERE id=?", (id,))
    result = db.fetchone()
    if not result:
        raise ValueError("Cover with given ID does not exist")
    return {"id": result[0], "type": result[1], "content": result[2]}

def updateCover(id, type, content):
    if type not in ALLOWED_TYPES:
        raise ValueError(f"type {type} is not an allowed image type!")
    db = sqlite3.connect(DATABASE, autocommit=True).cursor()

    db.execute("SELECT * FROM cover WHERE id=?", (id,))
    result = db.fetchone()
    if not result:
        raise ValueError("Cover with given ID does not exist")
    
    db.execute("UPDATE cover SET type=?, content=? WHERE id=?", (type, content, id))
    if db.rowcount < 1:
        raise RuntimeError("Unknown error updating cover")
    
def removeCover(id, cursor = None):
    should_close = True
    if not cursor:
        db = sqlite3.connect(DATABASE, autocommit=True).cursor()
    else:
        db = cursor
        should_close = False

    db.execute("SELECT * FROM cover WHERE id=?", (id,))
    result = db.fetchone()
    if not result:
        raise ValueError("Cover with given ID does not exist")
    
    db.execute("DELETE FROM cover WHERE id=?", (id,))
    if db.rowcount < 1:
        raise RuntimeError("Unknown error deleting cover")
    
    if should_close:
        db.close()
    
