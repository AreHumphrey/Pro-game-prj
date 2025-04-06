# Импортируем модуль tkinter для создания графического интерфейса (GUI)
import tkinter as tk

# Импортируем стандартные диалоги из tkinter:
# - colorchooser — для выбора цвета
# - filedialog — для открытия и сохранения файлов
from tkinter import colorchooser, filedialog

# Импортируем классы из библиотеки Pillow (работа с изображениями):
# - Image — для создания/открытия изображений
# - ImageDraw — позволяет рисовать на изображении (аналог холста)
from PIL import Image, ImageDraw


# Создаём основной класс приложения — расширенный Paint
class AdvancedPaint:
    def __init__(self, root):
        # Сохраняем главное окно
        self.root = root
        self.root.title("Расширенный Paint")  # Устанавливаем заголовок окна
        self.root.geometry("900x700")  # Размер окна: ширина 900px, высота 700px

        # Начальные настройки кисти и инструментов
        self.color = "black"         # Цвет кисти по умолчанию — чёрный
        self.eraser_on = False       # Ластик выключен (если True — рисуем белым)
        self.brush_size = 5          # Толщина линии по умолчанию — 5 пикселей
        self.tool = "brush"          # Активный инструмент — кисть
        self.start_x = None          # Начальная X координата при рисовании (будет установлена при клике)
        self.start_y = None          # Начальная Y координата

        # Создаём графический холст (виджет Canvas) внутри главного окна
        # bg="white" — белый фон
        # width, height — размеры холста
        self.canvas = tk.Canvas(root, bg="white", width=900, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Автоматически расширяется по размеру окна

        # Создаём "внутреннее" изображение с помощью Pillow — аналог холста, но в памяти
        # Позволяет сохранять изображение в файл
        self.image = Image.new("RGB", (900, 600), "white")  # Создаём белое изображение
        self.draw = ImageDraw.Draw(self.image)  # Создаём инструмент рисования по изображению

        # Привязываем события мыши к функциям:
        self.canvas.bind("<Button-1>", self.start_draw)        # Нажатие левой кнопки мыши — начало рисования
        self.canvas.bind("<B1-Motion>", self.draw_motion)      # Движение мыши с зажатой кнопкой — рисование
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)  # Отпускание кнопки — конец рисования

        # Создаём панель с кнопками и ползунком (UI-интерфейс)
        self.create_ui()


    # Метод создания интерфейса (панель инструментов сверху)
    def create_ui(self):
        frame = tk.Frame(self.root)  # Панель для кнопок
        frame.pack(pady=5)  # Отступ сверху

        # Кнопки для разных действий (каждая вызывает свой метод)
        tk.Button(frame, text="Цвет", command=self.choose_color).pack(side=tk.LEFT)
        tk.Button(frame, text="Ластик", command=self.use_eraser).pack(side=tk.LEFT)
        tk.Button(frame, text="Кисть", command=self.use_brush).pack(side=tk.LEFT)
        tk.Button(frame, text="Линия", command=lambda: self.set_tool("line")).pack(side=tk.LEFT)
        tk.Button(frame, text="Прямоугольник", command=lambda: self.set_tool("rect")).pack(side=tk.LEFT)
        tk.Button(frame, text="Овал", command=lambda: self.set_tool("oval")).pack(side=tk.LEFT)
        tk.Button(frame, text="Очистить", command=self.clear_canvas).pack(side=tk.LEFT)
        tk.Button(frame, text="Сохранить", command=self.save_image).pack(side=tk.LEFT)

        # Подпись "Толщина"
        tk.Label(frame, text="Толщина:").pack(side=tk.LEFT, padx=5)

        # Ползунок для выбора толщины линии (от 1 до 50)
        self.size_scale = tk.Scale(frame, from_=1, to=50, orient=tk.HORIZONTAL,
                                   command=self.set_brush_size)
        self.size_scale.set(self.brush_size)  # Устанавливаем начальное значение = 5
        self.size_scale.pack(side=tk.LEFT)


    # Открываем диалог выбора цвета и сохраняем выбранный цвет
    def choose_color(self):
        color = colorchooser.askcolor()[1]  # Возвращает кортеж (RGB, HEX), берём HEX-строку
        if color:
            self.color = color             # Применяем новый цвет
            self.eraser_on = False         # Если был включён ластик — выключаем

    # Метод изменения толщины кисти
    def set_brush_size(self, value):
        self.brush_size = int(value)  # Переводим значение из строки в целое число

    # Метод включения ластика (по сути — рисуем белым цветом)
    def use_eraser(self):
        self.color = "white"          # Цвет — белый
        self.eraser_on = True         # Включаем флаг ластика
        self.tool = "brush"           # Инструмент — кисть (но цвет — белый)

    # Метод возврата к обычной кисти
    def use_brush(self):
        self.eraser_on = False        # Выключаем ластик
        self.tool = "brush"           # Инструмент — кисть

    # Устанавливаем активный инструмент (кисть, линия, прямоугольник, овал)
    def set_tool(self, tool):
        self.tool = tool              # Устанавливаем текущий инструмент
        self.eraser_on = False        # При переключении — выключаем ластик

    # Сохраняем координаты начала рисования
    def start_draw(self, event):
        self.start_x = event.x        # Сохраняем начальную X координату
        self.start_y = event.y        # Сохраняем начальную Y координату
        if self.tool == "brush":
            self.draw_point(event.x, event.y)  # Рисуем точку сразу, если клик без движения

    # Метод рисования во время движения мыши
    def draw_motion(self, event):
        if self.tool == "brush":
            # Рисуем линию от предыдущей точки к новой
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                    fill=self.color, width=self.brush_size,
                                    capstyle=tk.ROUND, smooth=True)
            self.draw.line([self.start_x, self.start_y, event.x, event.y],
                           fill=self.color, width=self.brush_size)
            # Обновляем координаты
            self.start_x, self.start_y = event.x, event.y

    # Завершение рисования (для линий, прямоугольников и овалов)
    def stop_draw(self, event):
        if self.tool in ["line", "rect", "oval"]:
            if self.tool == "line":
                # Рисуем линию
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                        fill=self.color, width=self.brush_size)
                self.draw.line([self.start_x, self.start_y, event.x, event.y],
                               fill=self.color, width=self.brush_size)
            elif self.tool == "rect":
                # Рисуем прямоугольник
                self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y,
                                             outline=self.color, width=self.brush_size)
                self.draw.rectangle([self.start_x, self.start_y, event.x, event.y],
                                    outline=self.color, width=self.brush_size)
            elif self.tool == "oval":
                # Рисуем овал (эллипс)
                self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y,
                                        outline=self.color, width=self.brush_size)
                self.draw.ellipse([self.start_x, self.start_y, event.x, event.y],
                                  outline=self.color, width=self.brush_size)

    # Метод для одиночного клика (рисуем маленькую точку)
    def draw_point(self, x, y):
        self.canvas.create_oval(x, y, x+1, y+1, fill=self.color, outline=self.color)
        self.draw.ellipse([x, y, x+1, y+1], fill=self.color, outline=self.color)

    # Полная очистка холста и внутреннего изображения
    def clear_canvas(self):
        self.canvas.delete("all")  # Удаляем всё с canvas
        self.image = Image.new("RGB", (900, 600), "white")  # Создаём новое белое изображение
        self.draw = ImageDraw.Draw(self.image)  # Обновляем объект рисования

    # Сохранение изображения в файл
    def save_image(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG Files", "*.png")])
        if filepath:
            self.image.save(filepath)  # Сохраняем текущее Pillow-изображение в PNG
            

# Точка входа в программу (если скрипт запущен напрямую)
if __name__ == "__main__":
    root = tk.Tk()             # Создаём главное окно
    app = AdvancedPaint(root)  # Создаём экземпляр класса Paint
    root.mainloop()            # Запускаем главный цикл tkinter — окно остаётся открытым
