# Импортируем необходимые модули
import pygame  # библиотека для создания игр
import sys     # для выхода из программы
import random  # для генерации случайных чисел

# Инициализация всех модулей Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # создаём окно игры
pygame.display.set_caption("Flappy Bird")  # устанавливаем заголовок окна

# Цвета в формате RGB
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)    # фон неба
GREEN = (0, 255, 0)     # трубы
RED = (255, 0, 0)       # птичка

# Создаём объект clock для ограничения FPS
clock = pygame.time.Clock()
fps = 60  # количество кадров в секунду

# Параметры птички
bird_size = 30
bird_x = 100                # начальная координата X
bird_y = HEIGHT // 2        # начальная координата Y — по центру экрана
bird_velocity = 0           # скорость птички по оси Y
gravity = 0.5               # сила гравитации
jump_strength = -8          # сила прыжка при нажатии клавиши

# Параметры труб
pipe_width = 50
pipe_gap = 150              # расстояние между верхней и нижней трубой
pipe_velocity = 3           # скорость движения труб
pipes = []                  # список труб (каждая труба — [x, высота, был_ли_пройден])

pipe_timer = 0              # таймер для появления труб

# Счёт и шрифт
score = 0
font = pygame.font.Font(None, 36)  # стандартный шрифт

# Функция для отображения текста на экране
def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Основной цикл игры
running = True
while running:
    screen.fill(BLUE)  # заливаем фон синим цветом

    # Обрабатываем события (нажатия клавиш, выход)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # если нажата кнопка "Закрыть"
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # если нажата клавиша
            if event.key == pygame.K_SPACE:  # если это пробел — птичка прыгает
                bird_velocity = jump_strength

    # Применяем гравитацию и перемещаем птичку
    bird_velocity += gravity
    bird_y += bird_velocity

    # Если птичка вышла за границы экрана — конец игры
    if bird_y > HEIGHT - bird_size or bird_y < 0:
        running = False

    # Создаём новую трубу каждые 90 кадров
    pipe_timer += 1
    if pipe_timer > 90:
        pipe_height = random.randint(100, HEIGHT - pipe_gap - 100)  # случайная высота трубы
        pipes.append([WIDTH, pipe_height, False])  # [x, высота, флаг_счёта]
        pipe_timer = 0

    # Новый список для активных труб
    new_pipes = []

    # Прямоугольник птички для столкновений
    bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)

    # Отрисовываем и двигаем трубы
    for pipe in pipes:
        pipe[0] -= pipe_velocity  # труба движется влево
        if pipe[0] + pipe_width > 0:
            new_pipes.append(pipe)  # если труба всё ещё на экране — сохраняем

        # Создаём прямоугольники верхней и нижней трубы
        top_rect = pygame.Rect(pipe[0], 0, pipe_width, pipe[1])
        bottom_rect = pygame.Rect(pipe[0], pipe[1] + pipe_gap, pipe_width, HEIGHT - pipe[1] - pipe_gap)

        # Рисуем трубы
        pygame.draw.rect(screen, GREEN, top_rect)
        pygame.draw.rect(screen, GREEN, bottom_rect)

        # Проверка на столкновение птички с трубой
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            running = False

        # Увеличиваем счёт, если птичка пролетела трубу
        if not pipe[2] and pipe[0] + pipe_width < bird_x:
            score += 1
            pipe[2] = True  # отмечаем, что труба уже пройдена

    # Обновляем список труб
    pipes = new_pipes

    # Рисуем птичку
    pygame.draw.rect(screen, RED, (bird_x, bird_y, bird_size, bird_size))

    # Показываем счёт
    draw_text(f"Очки: {score}", 10, 10)

    # Обновляем экран
    pygame.display.flip()
    clock.tick(fps)  # задержка для соблюдения fps

# Игра окончена — выводим финальный счёт
print(f"Ваш счёт: {score}")
pygame.quit()
