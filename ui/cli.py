from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.style import Style
from typing import Optional
from core.models import PasswordEntry
from core.database import DatabaseManager


class CLIInterface:
    """Реализация консольного интерфейса."""

    def __init__(self):
        self.console = Console()
        self.db = DatabaseManager(console=self.console)
        self.db.initialize()

    def show_menu(self) -> int:
        """Отображает главное меню."""
        menu = Panel(
            "1. Добавить запись\n2. Просмотреть записи\n3. Редактировать\n4. Удалить\n5. Выход",
            title="🔐 [bold]Менеджер паролей[/]",
            border_style=Style(color="blue")
        )
        self.console.print(menu)
        return int(Prompt.ask("Выберите действие", choices=["1", "2", "3", "4", "5"]))

    def run(self):
        """Запускает основной цикл приложения."""
        while True:
            try:
                choice = self.show_menu()

                if choice == 1:
                    self._handle_add_entry()
                elif choice == 2:
                    self._handle_view_entries()  # Теперь метод существует
                elif choice == 3:
                    self._handle_edit_menu()
                elif choice == 5:
                    if Confirm.ask("Выйти из программы?"):
                        break

            except ValueError:
                self.console.print("[red]Ошибка: введите число от 1 до 5![/]")
            except Exception as e:
                self.console.print(f"[red]Неожиданная ошибка: {e}[/]")

    def _handle_add_entry(self):
        """Обрабатывает добавление новой записи."""
        entry = PasswordEntry()
        entry.name = Prompt.ask("Название ресурса")
        entry.login = Prompt.ask("Логин")
        entry.password = Prompt.ask("Пароль", password=True)
        entry.description = Prompt.ask("Описание", default="")

        if Confirm.ask("Сохранить запись?"):
            entry_id = self.db.add_entry(entry)
            self.console.print(f"[green]Запись #{entry_id} сохранена![/]")

    def _handle_delete_entry(self, entry_id: int) -> bool:
        """Обрабатывает удаление записи."""
        if Confirm.ask("[red]Вы уверены что хотите удалить запись?[/]"):
            if self.db.delete_entry(entry_id):
                self.console.print("[green]Запись удалена![/]")
                return True
            else:
                self.console.print("[red]Ошибка при удалении![/]")
        return False

    def _handle_view_entries(self):
        """Отображает список записей и детали выбранной."""
        # Получаем все записи из БД
        with self.db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM entries")
            entries = cursor.fetchall()

        if not entries:
            self.console.print("[yellow]Нет сохранённых записей.[/]")
            return

        # Выводим список
        self.console.print("[bold]Список записей:[/]")
        for entry_id, name in entries:
            self.console.print(f"[cyan]{entry_id}.[/] {name}")

        # Запрашиваем выбор записи
        selected_id = Prompt.ask("\nВведите ID записи для просмотра", default="", show_default=False)

        if not selected_id.isdigit():
            self.console.print("[red]Ошибка: введите числовой ID![/]")
            return

        # Получаем и отображаем полные данные
        entry = self.db.get_entry(int(selected_id))
        if entry:
            self._display_entry_details(entry)
        else:
            self.console.print("[red]Запись не найдена![/]")

    def _display_entry_details(self, entry: PasswordEntry):
        """Отображает детали записи и обрабатывает действия."""
        while True:  # Добавляем цикл для повторного отображения
            self.console.print(f"\n[bold]Детали записи #{entry.id}:[/]")
            self.console.print(f"Название: [green]{entry.name}[/]")
            self.console.print(f"Логин: [green]{entry.login}[/]")
            self.console.print(f"Пароль: [green]{entry.password}[/]")
            if entry.description:
                self.console.print(f"Описание: [green]{entry.description}[/]")

            action = Prompt.ask(
                "\n(e) Редактировать | (d) Удалить | (b) Назад",
                choices=["e", "d", "b"],
                default="b"
            )

            if action == "e":
                self._handle_edit_entry(entry.id)
                entry = self.db.get_entry(entry.id)  # Обновляем данные после редактирования
            elif action == "d":
                if self._handle_delete_entry(entry.id):
                    break  # Выходим если запись удалена
            elif action == "b":
                break

    def _handle_edit_menu(self):
        """Меню редактирования."""
        entry_id = Prompt.ask("Введите ID записи для редактирования")
        if entry_id.isdigit():
            self._handle_edit_entry(int(entry_id))
        else:
            self.console.print("[red]Неверный ID![/]")

    def _handle_edit_entry(self, entry_id: int):
        """Редактирует существующую запись с проверкой изменений."""
        entry = self.db.get_entry(entry_id)
        if not entry:
            self.console.print("[red]Запись не найдена![/]")
            return

        self.console.print("\n[bold]Редактирование записи:[/]")

        # Сохраняем оригинальные значения для сравнения
        original_values = {
            'name': entry.name,
            'login': entry.login,
            'password': entry.password,
            'description': entry.description
        }

        # Получаем новые значения
        new_values = {
            'name': Prompt.ask("Название", default=entry.name),
            'login': Prompt.ask("Логин", default=entry.login),
            'password': Prompt.ask("Пароль", password=True, default=entry.password),
            'description': Prompt.ask("Описание", default=entry.description)
        }

        # Проверяем, были ли изменения
        if all(new_values[key] == original_values[key] for key in new_values):
            self.console.print("[yellow]Нет изменений для сохранения[/]")
            return

        # Показываем различия
        self.console.print("\n[bold]Изменения:[/]")
        for key in new_values:
            if new_values[key] != original_values[key]:
                self.console.print(
                    f"{key}: [red]{original_values[key]}[/] → [green]{new_values[key]}[/]"
                )

        # Подтверждение сохранения
        if Confirm.ask("\nСохранить изменения?"):
            # Обновляем объект записи
            entry.name = new_values['name']
            entry.login = new_values['login']
            entry.password = new_values['password']
            entry.description = new_values['description']

            if self.db.update_entry(entry):
                self.console.print("[green]Запись успешно обновлена![/]")
            else:
                self.console.print("[red]Ошибка при обновлении записи![/]")