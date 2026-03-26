import sqlite3
from datetime import date

from .owner import addOwner
from .cover import addCover, updateCover, removeCover
from .author import addAuthor

DATABASE = "db/dev.sqlite3"

def addBook(title, owner, pub_year = None, cover = None, authors = None):
    if len(title) == 0:
        raise ValueError("Title cannot be an empty string")
    if not "id" in owner and not "username" in owner or not isinstance(owner, dict):
        raise ValueError("owner must be a dict with keys 'id' and 'username'")
    if pub_year and pub_year not in range(0, date.today().year):
        raise ValueError("pub_year must be between 0 and current year")
    if cover and ((not "type" in cover and not "content" in cover) or not isinstance(cover, dict)):
        raise ValueError("cover must be a dict with keys 'type' and 'content'")
    if authors:
        for author in authors:
            if not isinstance(author, dict) or "last_name" not in author:
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
    
    db.close()
    return book_id

def updateBook(id, title = None, owner = None, pub_year = None, cover = None, authors = None):
    db = sqlite3.connect(DATABASE, autocommit=True).cursor()

    db.execute("SELECT * FROM book WHERE id=?", (id,))
    result = db.fetchone()
    if not result:
        raise ValueError("Book with given ID does not exist")

    db.execute("BEGIN TRANSACTION")
    if title is not None or pub_year is not None:
        changeBookData(id, title, pub_year, db)
    if cover is not None:
        changeBookCover(id, cover, db)
    if owner is not None:
        changeBookOwner(id, owner, db)
    if authors is not None:
        changeBookAuthors(id, authors, db)
    db.execute("COMMIT")
    db.close()

def getBookById(id):
    db = sqlite3.connect(DATABASE, autocommit=True).cursor()

    db.execute("SELECT * FROM book WHERE id=?", (id,))
    result = db.fetchone()
    if not result:
        raise ValueError("Book with given ID does not exist")
    (book_id, title, pub_year, cover_id, owner_id) = result
    book_dict = {"id": book_id, "title": title, "pub_year": pub_year}
    if cover_id:
        db.execute("SELECT * FROM cover WHERE id=?", (cover_id,))
        cover = db.fetchone()
        book_dict["cover"] = {}
        book_dict["cover"]["type"] = cover[1]
        book_dict["cover"]["content"] = cover[2]
    
    db.execute("SELECT * FROM owner WHERE id=?", (owner_id,))
    owner = db.fetchone()
    book_dict["owner"] = {}
    book_dict["owner"]["id"] = owner[0]
    book_dict["owner"]["username"] = owner[1]
    
    db.execute("SELECT author.id, author.last_name, author.first_name FROM book_has_author JOIN author ON book_has_author.author_id=author.id WHERE book_has_author.book_id=?", (id,))
    authors = db.fetchall()
    book_dict["authors"] = []
    for author in authors:
        book_dict["authors"].append({"id": author[0], "last_name": author[1], "first_name": author[2]})

    db.close()
    return book_dict

def getBooks():
    db = sqlite3.connect(DATABASE, autocommit=True).cursor()

    db.execute("SELECT id FROM book")

    while (result := db.fetchone()) is not None:
        (book_id,) = result
        book_dict = getBookById(book_id)
        yield book_dict

    db.close()

def removeBook(id):
    db = sqlite3.connect(DATABASE, autocommit=True).cursor()

    db.execute("SELECT * FROM book WHERE id=?", (id,))
    result = db.fetchone()
    if not result:
        raise ValueError("Book with given ID does not exist")
    
    db.execute("BEGIN TRANSACTION")
    db.execute("SELECT cover_id FROM book WHERE id=?", (id,))
    cover_id = db.fetchone()[0]
    if cover_id is not None:
        removeCover(cover_id, db)
    db.execute("DELETE FROM book_has_author WHERE book_id=?", (id,))
    db.execute("DELETE FROM book WHERE id=?", (id,))
    db.execute("COMMIT")
    db.close()

def changeBookData(id, title, pub_year, cursor = None):
    if not cursor:
        cursor = sqlite3.connect(DATABASE, autocommit=True).cursor()
    if title is not None and len(title) == 0:
        raise ValueError("Title cannot be an empty string")
    if pub_year is not None and pub_year not in range(0, date.today().year + 1):
        raise ValueError("pub_year must be between 0 and current year")
    
    cursor.execute("UPDATE book SET title=?, pub_year=? WHERE id=?", (title, pub_year, id))
    if cursor.rowcount < 1:
        raise RuntimeError("Unknown error changing book data")

def changeBookCover(id, cover, cursor = None):
    if not cursor:
        cursor = sqlite3.connect(DATABASE, autocommit=True).cursor()
    
    if not isinstance(cover, dict) or ("type" not in cover and "content" not in cover):
        raise ValueError("cover must be a dict with keys 'type' and 'content'")

    cursor.execute("SELECT cover_id FROM book WHERE id=?", (id,))
    cover_id = cursor.fetchone()[0]
    updateCover(cover_id, cover["type"], cover["content"])

def changeBookOwner(id, owner, cursor = None):
    if not cursor:
        cursor = sqlite3.connect(DATABASE, autocommit=True).cursor()
    
    if not isinstance(owner, dict) or ("id" not in owner and "username" not in owner):
        raise ValueError("owner must be a dict with keys 'id' and 'username'")
    
    addOwner(owner["id"], owner["username"])
    cursor.execute("UPDATE book SET owner_id=? WHERE id=?", (owner["id"], id))
    if cursor.rowcount < 1:
        raise RuntimeError("Unknown error changing book owner")

def changeBookAuthors(id, authors, cursor = None):
    if not cursor:
        cursor = sqlite3.connect(DATABASE, autocommit=True).cursor()

    if not isinstance(authors, list):
        raise ValueError("authors must be a list")
    
    for author in authors:
        if not isinstance(author, dict) or "last_name" not in author:
            raise ValueError("all authors must be dicts with at least 'last_name' key")
        
    author_ids = []
    for author in authors:
        author_ids.append(addAuthor(author["last_name"], author.get("first_name")))

    cursor.execute("DELETE FROM book_has_author WHERE book_id=?", (id,))

    for author_id in author_ids:
        cursor.execute("INSERT INTO book_has_author (book_id, author_id) VALUES (?, ?)", (id, author_id))

