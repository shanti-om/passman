from rich.console import Console
from rich.panel import Panel
from rich.style import Style

console = Console()

def show_menu() -> int:
    """Отображает главное меню и возвращает выбор пользователя."""
    menu_title = "🔐 [bold #ff79c6]Менеджер паролей[/]"
    menu_options = [
        "1. Добавить запись",
        "2. Просмотреть записи",
        "3. Редактировать запись",
        "4. Удалить запись",
        "5. Изменить мастер-пароль",
        "6. Выход"
    ]
    menu_panel = Panel(
        "\n".join(menu_options),
        title=menu_title,
        border_style=Style(color="#bd93f9"),
        width=50
    )
    console.print(menu_panel)
    return int(console.input("Введите номер: "))

def run_cli():
    """Запускает CLI-интерфейс."""
    while True:
        try:
            choice = show_menu()
            if choice == 6:
                break
            # TODO: Добавить вызовы функций
        except ValueError:
            console.print("[red]Ошибка: введите число от 1 до 6![/]")