import sqlite3
from typing import List, Optional
from pathlib import Path
from rich.console import Console
from .models import PasswordEntry


class DatabaseManager:
    """Управление базой данных SQLite."""

    def __init__(self, db_path: str = "passwords.db", console: Optional[Console] = None):
        self.db_path = Path(db_path)
        self.console = console or Console()

    def _get_connection(self):
        """Возвращает соединение с БД."""
        return sqlite3.connect(self.db_path)

    def initialize(self):
        """Инициализирует таблицы в БД."""
        with self._get_connection() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                login TEXT,
                password TEXT,
                etc TEXT,
                description TEXT
            )
            """)

    def add_entry(self, entry: PasswordEntry) -> int:
        """Добавляет новую запись в БД."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO entries (name, login, password, etc, description) VALUES (?, ?, ?, ?, ?)",
                (entry.name, entry.login, entry.password, entry.etc, entry.description)
            )
            return cursor.lastrowid

    def get_entry(self, entry_id: int) -> Optional[PasswordEntry]:
        """Возвращает запись по ID."""
        try:
            with self._get_connection() as conn:
                row = conn.execute(
                    "SELECT id, name, login, password, etc, description FROM entries WHERE id = ?",
                    (entry_id,)
                ).fetchone()

                return PasswordEntry(*row) if row else None
        except sqlite3.Error as e:
            self.console.print(f"[red]Ошибка при получении записи: {e}[/]")
            return None

    def delete_entry(self, entry_id: int) -> bool:
        """Удаляет запись по ID."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            self.console.print(f"[red]Ошибка при удалении: {e}[/]")
            return False

    def get_all_entries(self) -> List[tuple[int, str]]:
        """Возвращает список всех записей (id и name)."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM entries")
            return cursor.fetchall()

    def update_entry(self, entry: PasswordEntry) -> bool:
        """Обновляет существующую запись."""
        if not entry.id:
            self.console.print("[red]Ошибка: запись не имеет ID![/]")
            return False

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """UPDATE entries 
                    SET name = ?, login = ?, password = ?, etc = ?, description = ?
                    WHERE id = ?""",
                    (entry.name, entry.login, entry.password, entry.etc, entry.description, entry.id)
                )
                conn.commit()
                return cursor.rowcount > 0  # Возвращает True если запись была обновлена
        except sqlite3.Error as e:
            self.console.print(f"[red]Ошибка БД: {e}[/]")
            return False