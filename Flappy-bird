import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

clock = pygame.time.Clock()
fps = 60

bird_size = 30
bird_x = 100
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -8

pipe_width = 50
pipe_gap = 150
pipe_velocity = 3
pipes = []

pipe_timer = 0

score = 0
font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

running = True
while running:
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength

    bird_velocity += gravity
    bird_y += bird_velocity

    if bird_y > HEIGHT - bird_size or bird_y < 0:
        running = False

    pipe_timer += 1
    if pipe_timer > 90:
        pipe_height = random.randint(100, HEIGHT - pipe_gap - 100)
        pipes.append([WIDTH, pipe_height, False])
        pipe_timer = 0

    new_pipes = []
    bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)
    for pipe in pipes:
        pipe[0] -= pipe_velocity
        if pipe[0] + pipe_width > 0:
            new_pipes.append(pipe)

        top_rect = pygame.Rect(pipe[0], 0, pipe_width, pipe[1])
        bottom_rect = pygame.Rect(pipe[0], pipe[1] + pipe_gap, pipe_width, HEIGHT - pipe[1] - pipe_gap)
        pygame.draw.rect(screen, GREEN, top_rect)
        pygame.draw.rect(screen, GREEN, bottom_rect)

        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            running = False

        if not pipe[2] and pipe[0] + pipe_width < bird_x:
            score += 1
            pipe[2] = True

    pipes = new_pipes

    pygame.draw.rect(screen, RED, (bird_x, bird_y, bird_size, bird_size))

    draw_text(f"Очки: {score}", 10, 10)

    pygame.display.flip()
    clock.tick(fps)

print(f"Ваш счёт: {score}")
pygame.quit()
  
