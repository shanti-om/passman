import sqlite3
from typing import List, Dict

def init_db():
    """Инициализирует БД (вызывается при первом запуске)."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        login TEXT,
        password TEXT,
        etc TEXT,
        description TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_entry(entry: Dict[str, str]):
    """Добавляет запись в БД (пока без шифрования)."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO entries (name, login, password, etc, description) VALUES (?, ?, ?, ?, ?)",
        (entry["name"], entry["login"], entry["password"], entry["etc"], entry["description"])
    )
    conn.commit()
    conn.close()