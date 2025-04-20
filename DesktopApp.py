# Импортируем модули
import tkinter as tk                        # Основной модуль для создания графического интерфейса
from tkinter import filedialog              # Модуль для диалогов, например, выбора папки
import subprocess                           # Для запуска внешних приложений (например, калькулятора)
import os                                   # Для работы с файловой системой (например, получить список файлов)

# Основной класс приложения
class DesktopApp:
    def __init__(self, root):
        # Сохраняем ссылку на главное окно
        self.root = root

        # Настройка главного окна
        self.root.title("Рабочий стол")                 # Заголовок окна
        self.root.geometry("800x600")                   # Размер окна
        self.root.configure(bg="#1e1e1e")                # Цвет фона (тёмный серый)

        # === КНОПКА "ПУСК" ===
        self.start_button = tk.Button(
            root,
            text="Пуск",                                 # Текст на кнопке
            command=self.toggle_menu,                    # Функция, которая вызывается при нажатии
            bg="#2e2e2e",                                # Цвет фона кнопки
            fg="white",                                  # Цвет текста
            font=("Arial", 12, "bold"),                  # Шрифт текста
            activebackground="#555",                     # Цвет кнопки при наведении
            relief="flat"                                # Плоский стиль кнопки
        )
        # Размещаем кнопку "Пуск" в левом нижнем углу
        self.start_button.place(x=10, y=560, width=80, height=30)

        # === МЕНЮ "ПУСК" ===
        self.start_menu = tk.Frame(
            root,
            bg="#333333",                                # Цвет фона меню
            bd=1,                                        # Толщина рамки
            relief="raised"                              # Рельеф рамки — приподнятая
        )
        # Меню изначально скрыто (высота = 0)
        self.start_menu.place(x=10, y=400, width=200, height=0)

        # === ДОБАВЛЯЕМ КНОПКИ В МЕНЮ "ПУСК" ===
        self.create_menu_button("Калькулятор", self.launch_calculator)  # Кнопка запуска калькулятора
        self.create_menu_button("Заметки", self.launch_notepad)         # Кнопка запуска блокнота
        self.create_menu_button("Проводник", self.open_explorer)       # Кнопка запуска проводника
        self.create_menu_button("Выход", root.quit)                     # Кнопка выхода из приложения

        # Флаг для отслеживания видимости меню
        self.menu_visible = False

    # === ФУНКЦИЯ СОЗДАНИЯ КНОПКИ В МЕНЮ "ПУСК" ===
    def create_menu_button(self, text, command):
        btn = tk.Button(
            self.start_menu,              # Родитель — меню "Пуск"
            text=text,                    # Надпись на кнопке
            command=command,              # Функция, которая вызывается при нажатии
            bg="#444",                    # Цвет кнопки
            fg="white",                   # Цвет текста
            anchor="w",                   # Выравнивание текста по левому краю
            relief="flat",                # Без рельефа
            font=("Arial", 11),           # Шрифт текста
            activebackground="#666"       # Цвет при наведении
        )
        btn.pack(fill="x", padx=5, pady=3)  # Заполнение по ширине + отступы

    # === ФУНКЦИЯ ПОКАЗА/СКРЫТИЯ МЕНЮ "ПУСК" ===
    def toggle_menu(self):
        if self.menu_visible:
            # Если меню видно — скрываем его (высота 0)
            self.start_menu.place_configure(height=0)
            self.menu_visible = False
        else:
            # Если меню скрыто — показываем (высота 160)
            self.start_menu.place_configure(height=160)
            self.menu_visible = True

    # === ЗАПУСК КАЛЬКУЛЯТОРА (внешнее приложение) ===
    def launch_calculator(self):
        try:
            subprocess.Popen("calc")                # Для Windows
        except FileNotFoundError:
            subprocess.Popen(["gnome-calculator"])  # Для Linux (если Windows-калькулятора нет)

    # === ЗАПУСК БЛОКНОТА (внешнее приложение) ===
    def launch_notepad(self):
        try:
            subprocess.Popen("notepad")             # Для Windows
        except FileNotFoundError:
            subprocess.Popen(["gedit"])             # Для Linux

    # === ПРОСТОЙ ПРОВОДНИК — показать список файлов в папке ===
    def open_explorer(self):
        folder = filedialog.askdirectory()  # Открываем диалог выбора папки
        if not folder:
            return  # Если пользователь отменил выбор — ничего не делаем

        # Создаём новое окно для отображения содержимого папки
        win = tk.Toplevel(self.root)
        win.title(f"Папка: {folder}")
        win.geometry("400x300")

        # Список файлов
        listbox = tk.Listbox(win, font=("Arial", 12))
        listbox.pack(expand=True, fill="both")

        try:
            files = os.listdir(folder)  # Получаем список файлов
            for f in files:
                listbox.insert(tk.END, f)  # Добавляем каждый файл в список
        except Exception as e:
            listbox.insert(tk.END, f"Ошибка: {e}")  # Показываем ошибку, если что-то пошло не так

# === ЗАПУСК ПРИЛОЖЕНИЯ ===
if __name__ == "__main__":
    root = tk.Tk()           # Создаём главное окно
    app = DesktopApp(root)   # Создаём экземпляр приложения
    root.mainloop()          # Запускаем главный цикл интерфейса
