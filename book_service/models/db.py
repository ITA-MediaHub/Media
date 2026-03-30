def get_database():
    import os
    return os.environ.get("DATABASE") or "db/dev.sqlite3"
