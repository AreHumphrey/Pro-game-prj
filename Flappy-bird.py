# -*- coding: utf-8 -*-
import pygame  # основная библиотека для создания игр
import sys     # для корректного выхода из игры
import random  # для случайного размещения труб

# Инициализируем все модули Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # создаём окно заданного размера
pygame.display.set_caption("Flappy Bird")  # заголовок окна

# Цвета (RGB)
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)    # фон
GREEN = (0, 255, 0)     # трубы
RED = (255, 0, 0)       # птица

# Частота кадров в секунду
clock = pygame.time.Clock()
fps = 60  # FPS (кадры в секунду)

# === ПАРАМЕТРЫ ПТИЦЫ ===
bird_size = 30
bird_x = 100                # начальная позиция X
bird_y = HEIGHT // 2        # начальная позиция Y (по вертикали — посередине)
bird_velocity = 0           # скорость птицы по Y
gravity = 0.5               # ускорение свободного падения
jump_strength = -8          # сила прыжка при нажатии пробела

# === ПАРАМЕТРЫ ТРУБ ===
pipe_width = 50
pipe_gap = 150              # расстояние между верхней и нижней трубой
pipe_velocity = 3           # скорость движения труб
pipes = []                  # список труб: [x, высота_верхней_трубы, был_ли_пройден]
pipe_timer = 0              # таймер для создания новых труб

# === СЧЁТ ===
score = 0
font = pygame.font.Font(None, 36)  # шрифт для отображения текста

def draw_text(text, x, y, color=WHITE):
    """
    Функция для отрисовки текста на экране.
    
    Аргументы:
    text -- текст для отображения
    x -- координата X текста
    y -- координата Y текста
    color -- цвет текста (по умолчанию белый)
    """
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


# === ОСНОВНОЙ ЦИКЛ ИГРЫ ===
running = True
while running:
    screen.fill(BLUE)  # заливаем экран цветом фона

    # === ОБРАБОТКА СОБЫТИЙ ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Если пользователь закрыл окно — выходим из игры
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # При нажатии пробела — птица делает прыжок
                bird_velocity = jump_strength

    # === ЛОГИКА ПТИЦЫ ===
    bird_velocity += gravity  # применяем гравитацию
    bird_y += bird_velocity   # перемещаем птицу по Y

    # Проверяем выход за границы экрана
    if bird_y > HEIGHT - bird_size or bird_y < 0:
        running = False

    # === ЛОГИКА ТРУБ ===
    pipe_timer += 1
    if pipe_timer > 90:  # каждые 90 кадров создаём новую трубу
        pipe_height = random.randint(100, HEIGHT - pipe_gap - 100)
        pipes.append([WIDTH, pipe_height, False])  # добавляем трубу
        pipe_timer = 0  # сбрасываем таймер

    new_pipes = []  # временный список для труб, которые ещё не ушли за экран

    # Прямоугольник птицы для проверки столкновений
    bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)

    # === ОТРИСОВКА И ЛОГИКА КАЖДОЙ ТРУБЫ ===
    for pipe in pipes:
        pipe[0] -= pipe_velocity  # двигаем трубу влево

        if pipe[0] + pipe_width > 0:
            new_pipes.append(pipe)  # если труба всё ещё видима — оставляем её

        # Координаты прямоугольников труб
        top_rect = pygame.Rect(pipe[0], 0, pipe_width, pipe[1])
        bottom_rect = pygame.Rect(pipe[0], pipe[1] + pipe_gap, pipe_width, HEIGHT - pipe[1] - pipe_gap)

        # Рисуем трубы
        pygame.draw.rect(screen, GREEN, top_rect)
        pygame.draw.rect(screen, GREEN, bottom_rect)

        # === ПРОВЕРКА СТОЛКНОВЕНИЙ ===
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            running = False  # если произошло столкновение — игра окончена

        # === УВЕЛИЧЕНИЕ СЧЁТА ===
        if not pipe[2] and pipe[0] + pipe_width < bird_x:
            score += 1         # увеличиваем счёт
            pipe[2] = True     # помечаем трубу как пройденную

    pipes = new_pipes  # обновляем список труб

    # === ОТРИСОВКА ПТИЦЫ ===
    pygame.draw.rect(screen, RED, (bird_x, bird_y, bird_size, bird_size))

    # === ОТОБРАЖЕНИЕ СЧЁТА ===
    draw_text(f"Очки: {score}", 10, 10)

    # === ОБНОВЛЕНИЕ ЭКРАНА ===
    pygame.display.flip()  # обновляем экран
    clock.tick(fps)        # ограничиваем частоту кадров

# === ИГРА ЗАВЕРШЕНА ===
print(f"Ваш счёт: {score}")
pygame.quit()  # выходим из Pygame
