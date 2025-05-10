from dataclasses import dataclass
from typing import Optional

@dataclass
class PasswordEntry:
    """Модель данных для хранения записи пароля."""
    id: Optional[int] = None
    name: str = ""
    login: str = ""
    password: str = ""
    etc: str = ""
    description: str = ""