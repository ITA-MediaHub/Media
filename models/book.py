import sqlite3
from datetime import date

from .owner import addOwner
from .cover import addCover
from .author import addAuthor

DATABASE = "db/dev.sqlite3"

def addBook(title, owner, pub_year = None, cover = None, authors = None):
    if len(title) == 0:
        raise ValueError("Title cannot be an empty string")
    if not "id" in owner and not "username" in owner or not isinstance(owner, dict):
        raise ValueError("owner must be a dict with keys 'id' and 'username'")
    if pub_year and pub_year not in range(0, date.today().year):
        raise ValueError("pub_year must be between 0 and current year")
    if cover and not "type" in cover and not "content" in cover:
        raise ValueError("cover must be a dict with keys 'type' and 'content'")
    if authors:
        for author in authors:
            if "last_name" not in author:
                raise ValueError("all authors must be dicts with at least 'last_name' key")
            
    db = sqlite3.connect(DATABASE, autocommit=True).cursor()

    owner_id = addOwner(owner["id"], owner["username"])

    author_ids = []
    if authors:
        for author in authors:
            author_ids.append(addAuthor(author["last_name"], author.get("first_name"))) # used get so lack of first_name key doesn't raise an error

    if cover:
        cover_id = addCover(cover["type"], cover["content"])
        db.execute("INSERT INTO book (title, pub_year, cover_id, owner_id) VALUES (?, ?, ?, ?)", (title, pub_year, cover_id, owner_id))
    else:
        db.execute("INSERT INTO book (title, pub_year, owner_id) VALUES (?, ?, ?)", (title, pub_year, owner_id))
    book_id = db.lastrowid

    for author_id in author_ids:
        db.execute("INSERT INTO book_has_author (book_id, author_id) VALUES (?, ?)", (book_id, author_id))
    
    return book_id
