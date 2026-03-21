import sqlite3

def populate_db():
    connection = sqlite3.connect("dev.sqlite3", autocommit=True)
    cursor = connection.cursor()

    songs = [
        (1, "Red Wine Supernova", 2023),
        (2, "Mamma Mia", 1975),
    ]

    albums = [
        (1, "The Rise and Fall of a Midwest Princess", 1),
        (2, "Abba", 2),
    ]

    artists = [
        ("Chappell Roan"),
        ("ABBA"),
    ]

    cursor.execute("DELETE FROM song")
    cursor.executemany("INSERT INTO song(id, title, pub_year) VALUES(?, ?, ?)", songs)
    cursor.executemany("INSERT INTO album(id, title, artist_id) VALUES(?, ?, ?)", albums)
    

    books = [
        ("The Hitchhiker's Guide to the Galaxy", 1979),
        ("Blackshirts and Reds", 1997),
    ]

    authors = [
        ("Douglas Adams"),
        ("Michael Parenti"),
    ]

    movies = [
        ("The Nightmare Before Christmas", 1993),
        ("One Battle After Another", 2025),
    ]

    tv_series = [
        ("Andor", 2022),
        ("Community", 2009),
    ]

    seasons = [
        (1, 2022),
        (1, 2009),
    ]

    episodes = [
        (1, "2022-12-10"),
        (1, "2009-09-23"),
    ]

if __name__ == "__main__":
    populate_db()
