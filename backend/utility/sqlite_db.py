import sqlite3
import os

db_path = os.getenv("DB_PATH", "./db.sqlite")


def connection():
    return sqlite3.connect(db_path)
