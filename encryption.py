def encrypt(data: str, key: bytes) -> bytes:
    """Заглушка для шифрования (пока возвращает данные как есть)."""
    return data.encode("utf-8")

def decrypt(data: bytes, key: bytes) -> str:
    """Заглушка для дешифрования."""
    return data.decode("utf-8")