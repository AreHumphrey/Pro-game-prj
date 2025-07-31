# Импортируем необходимые библиотеки
import pygame
import random

# Инициализация Pygame - обязательный шаг для работы с библиотекой
pygame.init()

# Определяем константы для игры
SCREEN_WIDTH = 400        # Ширина игрового окна в пикселях
SCREEN_HEIGHT = 600       # Высота игрового окна в пикселях
FPS = 30                  # Количество кадров в секунду (частота обновления экрана)

# Определяем цвета в формате RGB (красный, зеленый, синий)
WHITE = (255, 255, 255)   # Белый цвет
BLACK = (0, 0, 0)         # Черный цвет
GREEN = (0, 200, 0)       # Зеленый цвет для платформ
BLUE = (0, 100, 255)      # Синий цвет для игрока
RED = (255, 0, 0)         # Красный цвет для надписей

# Создаем игровое окно с заданными размерами
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Устанавливаем заголовок окна
pygame.display.set_caption("Super Simple Doodle Jump")
# Создаем объект для управления частотой кадров
clock = pygame.time.Clock()

# Инициализируем переменные игрока
player_x = SCREEN_WIDTH // 2    # Начальная позиция игрока по горизонтали (по центру экрана)
player_y = SCREEN_HEIGHT - 100  # Начальная позиция игрока по вертикали (внизу экрана)
player_vel_y = 0                # Вертикальная скорость игрока (для прыжков и падения)
player_vel_x = 0                # Горизонтальная скорость игрока

# Создаем список платформ
# Каждая платформа представлена как список [x, y], где x,y - координаты левого верхнего угла
platforms = []
# Создаем начальные платформы (10 штук) с разными координатами
for i in range(10):
    # Случайная позиция по горизонтали
    x = random.randint(0, SCREEN_WIDTH - 70)
    # Позиция по вертикали с шагом 60 пикселей
    y = SCREEN_HEIGHT - 50 - i * 60
    # Добавляем платформу в список
    platforms.append([x, y])

# Инициализируем игровые параметры
camera_y = 0      # Вертикальное смещение камеры (для следования за игроком)
score = 0         # Текущий счет (зависит от высоты)
game_over = False # Флаг окончания игры

# Основной игровой цикл - выполняется пока игра запущена
running = True
while running:
    # Обработка событий (нажатия клавиш, закрытие окна и т.д.)
    for event in pygame.event.get():
        # Если пользователь закрыл окно, завершаем игру
        if event.type == pygame.QUIT:
            running = False
        # Если нажата клавиша
        if event.type == pygame.KEYDOWN:
            # Если нажат пробел и игра окончена, перезапускаем игру
            if event.key == pygame.K_SPACE and game_over:
                # Сбрасываем параметры игрока
                player_x = SCREEN_WIDTH // 2
                player_y = SCREEN_HEIGHT - 100
                player_vel_y = 0
                player_vel_x = 0
                # Пересоздаем платформы
                platforms = []
                for i in range(10):
                    x = random.randint(0, SCREEN_WIDTH - 70)
                    y = SCREEN_HEIGHT - 50 - i * 60
                    platforms.append([x, y])
                # Сбрасываем другие параметры
                camera_y = 0
                score = 0
                game_over = False
                
    # Если игра не окончена, продолжаем игровой процесс
    if not game_over:
        # Обработка управления игроком
        keys = pygame.key.get_pressed()  # Получаем состояние всех клавиш
        player_vel_x = 0  # Сбрасываем горизонтальную скорость
        # Если нажата стрелка влево, задаем скорость влево
        if keys[pygame.K_LEFT]:
            player_vel_x = -5
        # Если нажата стрелка вправо, задаем скорость вправо
        if keys[pygame.K_RIGHT]:
            player_vel_x = 5
            
        # Применяем гравитацию (увеличиваем вертикальную скорость вниз)
        player_vel_y += 0.5
        
        # Обновляем позицию игрока на основе скорости
        player_y += player_vel_y  # Изменяем вертикальную позицию
        player_x += player_vel_x  # Изменяем горизонтальную позицию
        
        # Проверяем столкновения игрока с платформами
        # Проходим по всем платформам
        for platform in platforms:
            x, y = platform  # Получаем координаты платформы
            # Проверяем условие столкновения:
            # 1. Игрок падает (player_vel_y > 0)
            # 2. Низ игрока находится на уровне платформы
            # 3. Игрок находится над платформой
            # 4. Игрок пересекается с платформой по горизонтали
            if (player_vel_y > 0 and 
                player_y + 20 >= y and 
                player_y + 20 <= y + 10 and
                player_x + 20 > x and 
                player_x < x + 70):
                # При столкновении с платформой игрок отпрыгивает вверх
                player_vel_y = -12
                
        # Обработка выхода игрока за границы экрана по горизонтали
        # Если игрок ушел за левую границу, перемещаем его вправо
        if player_x < -20:
            player_x = SCREEN_WIDTH
        # Если игрок ушел за правую границу, перемещаем его влево
        elif player_x > SCREEN_WIDTH:
            player_x = -20
            
        # Камера следует за игроком по вертикали
        # Если игрок поднимается выше определенного уровня, двигаем камеру
        if player_y < camera_y + 200:
            camera_y = player_y - 200
            
        # Генерация новых платформ при необходимости
        # Если платформ стало меньше 20, добавляем новые
        while len(platforms) < 20:
            # Новая платформа появляется над самой высокой существующей
            x = random.randint(0, SCREEN_WIDTH - 70)
            y = platforms[-1][1] - random.randint(40, 80)
            platforms.append([x, y])
            
        # Удаляем платформы, которые ушли далеко вниз (за пределы экрана)
        platforms = [p for p in platforms if p[1] < camera_y + SCREEN_HEIGHT + 100]
        
        # Обновляем счет в зависимости от высоты подъема игрока
        score = max(score, int(-camera_y / 10))
        
        # Проверяем условие проигрыша (игрок упал ниже экрана)
        if player_y > camera_y + SCREEN_HEIGHT:
            game_over = True
            
    # Отрисовка всех элементов игры
    # Заполняем экран белым цветом (очищаем предыдущий кадр)
    screen.fill(WHITE)
    
    # Рисуем все платформы
    for platform in platforms:
        x, y = platform
        # Рисуем прямоугольник зеленого цвета для каждой платформы
        # Учитываем смещение камеры по вертикали
        pygame.draw.rect(screen, GREEN, (x, y - camera_y, 70, 15))
        
    # Рисуем игрока (синий квадрат)
    # Учитываем смещение камеры по вертикали
    pygame.draw.rect(screen, BLUE, (player_x, player_y - camera_y, 20, 20))
    
    # Отображаем счет на экране
    font = pygame.font.SysFont(None, 36)  # Создаем шрифт
    score_text = font.render(f"Score: {score}", True, BLACK)  # Создаем текст
    screen.blit(score_text, (10, 10))  # Отображаем текст в левом верхнем углу
    
    # Если игра окончена, отображаем сообщение
    if game_over:
        # Создаем и отображаем надпись "GAME OVER"
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 30))
        # Создаем и отображаем надпись с инструкцией перезапуска
        restart_text = font.render("Press SPACE to restart", True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 10))
    
    # Обновляем содержимое экрана (отображаем новый кадр)
    pygame.display.flip()
    # Ограничиваем частоту кадров до заданного значения FPS
    clock.tick(FPS)

# Завершаем работу Pygame при выходе из игрового цикла
pygame.quit()
