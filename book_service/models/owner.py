import sqlite3
import os

from book_service.models.db import get_database

def addOwner(id, username):
    db = sqlite3.connect(get_database(), autocommit=True).cursor()

    if len(username) == 0:
        raise ValueError("Username cannot be empty string")

    db.execute("SELECT * FROM owner WHERE id=?", (id,))
    result = db.fetchone()
    if result and result[1] != username:
        raise ValueError("User with given ID already exists, but with different username")
    elif result:
        return result[0]
    
    db.execute("INSERT INTO owner (id, username) VALUES (?, ?)", (id, username))
    return db.lastrowid

def updateOwner(id, username):
    db = sqlite3.connect(get_database(), autocommit=True).cursor()

    db.execute("SELECT * FROM owner WHERE id=?", (id,))
    result = db.fetchone()
    if not result:
        raise ValueError("Owner with given ID does not exist")
    
    db.execute("UPDATE owner SET username=? WHERE id=?", (username, id))
    if db.rowcount < 1:
        raise RuntimeError("Unknown error deleting owner")

def removeOwner(id):
    db = sqlite3.connect(get_database(), autocommit=True).cursor()

    db.execute("SELECT * FROM owner WHERE id=?", (id,))
    result = db.fetchone()
    if not result:
        raise ValueError("Owner with given ID does not exist")
    
    db.execute("DELETE FROM owner WHERE id=?", (id,))
    if db.rowcount < 1:
        raise RuntimeError("Unknown error deleting owner")
    
def getOwnerById(id):
    db = sqlite3.connect(get_database(), autocommit=True).cursor()

    db.execute("SELECT * FROM owner WHERE id=?", (id,))
    result = db.fetchone()
    if not result:
        raise ValueError("Owner with given ID does not exist")
    return {"id": result[0], "username": result[1]}
