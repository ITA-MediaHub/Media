def get_database():
    import os
    from pathlib import Path
    return os.environ.get("DATABASE") or Path(__file__).resolve().parent.parent / "db/dev.sqlite3"

