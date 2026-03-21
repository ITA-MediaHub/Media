import sqlite3

DB_PATH = "dev.sqlite3"

def validateNotEmptyString(**kwargs):
    for k, v in kwargs.items():
        if len(v) <= 0:
            raise ValueError(f"{k} must not be an empty string!")
        
def validateYear(year, var_name):
    if year < 0 or year > 2100:
        raise ValueError(f"{var_name} must be a valid year (between 0 and 2100)")

db_conn = sqlite3.connect(DB_PATH, autocommit=True)
cursor = db_conn.cursor()

def createPersonOrGetId(name):
    cursor.execute("SELECT id FROM person WHERE name=?;", (name,))
    id = cursor.fetchone()
    if id is None:
        cursor.execute("INSERT INTO person (name) VALUES (?)", (name,))
        id = cursor.lastrowid
    else:
        id = id[0]
    return id

def createAlbumOrGetId(title, artist):
    artist_id = createPersonOrGetId(artist)
    cursor.execute("SELECT id FROM album WHERE title=? AND artist_id=?;", (title, artist_id))
    id = cursor.fetchone()
    if id is None:
        cursor.execute("INSERT INTO album (title, artist_id) VALUES (?, ?);", (title, artist_id))
        id = cursor.lastrowid
    else:
        id = id[0]
    return id    

def createSong(title, pub_year, album_title, artist):
    validateNotEmptyString(title=title, album_title=album_title, artist=artist)
    validateYear(pub_year, "pub_year")
    cursor.execute("SELECT * FROM song WHERE title=? AND pub_year=?", (title, pub_year))
    if cursor.fetchone():
        raise ValueError("Song already exists!")
    artist_id = createPersonOrGetId(artist)
    album_id = createAlbumOrGetId(album_title, artist)
    cursor.execute("INSERT INTO song (title, pub_year, artist_id, album_id) VALUES (?,?,?,?);", (title, pub_year, artist_id, album_id))
    return cursor.lastrowid


createSong("Pink Pony Club", 2023, "The Rise and Fall of a Midwest Princess", "Chappell Roan")
