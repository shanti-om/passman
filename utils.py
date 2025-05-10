from rich.console import Console

console = Console()


def validate_edit_data(data: dict, console) -> bool:
    """Проверяет данные перед редактированием записи.

    Args:
        data: Словарь с данными для проверки
        console: Объект для вывода ошибок

    Returns:
        bool: True если данные валидны
    """
    if not data.get("name", "").strip():
        console.print("[red]Ошибка: название не может быть пустым![/]")
        return False
    if len(data.get("password", "")) < 5:
        console.print("[red]Ошибка: пароль должен содержать минимум 5 символов![/]")
        return False
    return True

def validate_password(password: str) -> bool:
    """Проверяет, что пароль не короче 5 символов."""
    return len(password) >= 5

def validate_edit_data(data: dict) -> bool:
    """Проверяет данные перед редактированием."""
    if not data.get("name", "").strip():
        console.print("[red]Ошибка: название не может быть пустым![/]")
        return False
    if len(data.get("password", "")) < 5:
        console.print("[red]Ошибка: пароль должен содержать минимум 5 символов![/]")
        return False
    return True

def validate_password_entry(entry: PasswordEntry) -> bool:
    """Проверяет корректность данных записи."""
    if not entry.name.strip():
        return False
    if len(entry.password) < 5:
        return False
    return True