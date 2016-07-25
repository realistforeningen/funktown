from pony.orm import *
from functools import wraps

from db import db

class SchemaMigration(db.Entity):
    version = PrimaryKey(int)

db.generate_mapping(create_tables=True)

def migration(version):
    def decorator(func):
        @wraps(func)
        def wrapper():
            if SchemaMigration.get(version=version) is None:
                func()
                SchemaMigration(version=version)
            else:
                pass
        return wrapper
    return decorator

@db_session
@migration(1)
def initial_version():
    db.execute("""
        CREATE TABLE Person (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT
        )
    """)

    db.execute("""
        CREATE TABLE Role (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT UNIQUE NOT NULL
        )
    """)

    db.execute("""
        CREATE TABLE Assignment (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          person INTEGER NOT NULL REFERENCES Person (id),
          role INTEGER NOT NULL REFERENCES Role (id),
          year INTEGER NOT NULL,
          semester INTEGER NOT NULL
        )
    """)

    db.execute("""
        CREATE INDEX idx_assignment__person ON Assignment (person)
    """)

    db.execute("""
        CREATE INDEX idx_assignment__role ON Assignment (role)
    """)

def migrate():
    initial_version()

if __name__ == "__main__":
    migrate()

