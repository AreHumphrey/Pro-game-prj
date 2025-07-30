import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# 🖥️ Большой экран
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Змейка — Крупная версия")

# 🎨 Цвета
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# 🔲 Размер блока (уже крупный — 20x20)
block = 20

# ⏱️ Скорость игры
clock = pygame.time.Clock()
speed = 10  # Можно увеличить, если хочется быстрее

# 🍎 Функция для генерации новой еды
def new_food():
    return (
        random.randint(0, (width - block) // block) * block,
        random.randint(0, (height - block) // block) * block
    )

# 🐍 Главная функция игры
def game():
    # Начальная позиция — центр экрана
    x = width // 2
    y = height // 2

    # Направление движения (начинаем вправо)
    dx, dy = block, 0

    # Тело змейки — список координат [x, y]
    snake = [[x, y]]
    length = 1  # Длина змейки

    # Еда
    food_x, food_y = new_food()

    # Главный игровой цикл
    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Управление стрелками
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:  # Нельзя развернуться на 180
                    dx, dy = -block, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = block, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -block
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, block

        # Двигаем голову
        x += dx
        y += dy

        # 🚧 Проверка столкновения со стенами
        if x < 0 or x >= width or y < 0 or y >= height:
            break  # Проигрыш — выходим, будет перезапуск

        # 🐍 Проверка столкновения с собой (кроме хвоста, который уйдёт)
        if [x, y] in snake:
            break

        # Добавляем новую голову
        snake.append([x, y])

        # 🍽️ Если съели еду — не удаляем хвост, иначе удаляем
        if x == food_x and y == food_y:
            length += 1
            food_x, food_y = new_food()  # Новая еда
        else:
            snake.pop(0)  # Удаляем хвост

        # 🎨 Отрисовка
        screen.fill(black)  # Фон

        # Рисуем еду (красный квадрат 20x20)
        pygame.draw.rect(screen, red, [food_x, food_y, block, block])

        # Рисуем змейку (каждый сегмент — зелёный квадрат 20x20)
        for part in snake:
            pygame.draw.rect(screen, green, [part[0], part[1], block, block])

        # Обновляем экран
        pygame.display.update()

        # Контролируем скорость
        clock.tick(speed)

    # ⏳ Задержка перед перезапуском
    time.sleep(1)
    game()  # Автоматический перезапуск

# ▶️ Запуск игры
game()
