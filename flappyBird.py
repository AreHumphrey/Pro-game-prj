import pygame
import sys
import random

pygame.init()
WIDHT, HEIGHT = 600, 600

screen = pygame.display.set_mode((WIDHT, HEIGHT))

pygame.display.set_caption("Flappy Bird")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

clock = pygame.time.Clock()
fps = 60

#Птица

bird_size = 30

bird_x = 100
bird_y = HEIGHT// 2
bird_vel = 0
gravity = 0.5
jump = -8

#Труба
pipe_width = 50
pipe_gap = 150
pipe_vel = 3
pipes = []
pipe_timer = 0


#счёт
score = 0
font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

run = True
while run:
    screen.fill(BLUE)

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                bird_vel = jump
    #ПТИЦА
    bird_vel += gravity
    bird_y += bird_vel  

    if bird_y > HEIGHT - bird_size or bird_y < 0:
        run = False

    pipe_timer += 1
    if pipe_timer          > 90:
        pipe_height = random.randint(100, HEIGHT - pipe_gap - 50)
        pipes.append([WIDHT, pipe_height, False] )
        pipe_timer = 0

    new_pipes = []

    bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)

    for pipe in pipes:
        pipe[0] -= pipe_vel
        if pipe[0] + pipe_width > 0:
            new_pipes.append(pipe)



        top_pipe = pygame.Rect(pipe[0], 0, pipe_width, pipe[1])
        bottom_pipe = pygame.Rect(pipe[0], pipe[1] + pipe_gap, pipe_width, HEIGHT- pipe[1] - pipe_gap)
        pygame.draw.rect(screen, GREEN, top_pipe)
        pygame.draw.rect(screen, GREEN, bottom_pipe)
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            run = False
        if not pipe[2] and pipe[0] + pipe_width < bird_x:
            score += 1
            pipe[2] = True


    pipes = new_pipes

    pygame.draw.rect(screen, RED, (bird_x, bird_y, bird_size, bird_size))

    draw_text(f"Очки: {score}", 10, 10)
    pygame.display.flip()
    clock.tick(fps)
print(f"Очки: {score}")
pygame.quit()