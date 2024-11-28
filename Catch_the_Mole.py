import turtle
import time
import random

initial_lives = 5
score = 0
lives = initial_lives

window = turtle.Screen()
window.title("Catch the Mole!")
window.bgcolor("white")
window.setup(width=600, height=600)
window.tracer(0)

mole = turtle.Turtle()
mole.shape("square")
mole.color("gray")
mole.penup()
mole.speed(0)
mole.shapesize(stretch_wid=2, stretch_len=2)
mole.goto(1000, 1000)

score_display = turtle.Turtle()
score_display.hideturtle()
score_display.penup()
score_display.goto(0, 260)

def update_score():
    score_display.clear()
    score_display.write(f"Жизни: {lives}  Очки: {score}", align="center", font=("Arial", 16, "normal"))

def hit_mole(x, y):
    global score
    score += 1
    mole.hideturtle()
    update_score()

def show_mole():
    global lives
    if lives > 0:
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        mole.goto(x, y)
        mole.showturtle()
        window.ontimer(hide_mole, 800)
    else:
        reset_game()

def hide_mole():
    global lives
    if mole.isvisible():
        lives -= 1
        update_score()
    mole.hideturtle()
    if lives > 0:
        window.ontimer(show_mole, 1000)

def reset_game():
    global lives, score
    lives = initial_lives
    score = 0
    update_score()
    show_mole()

mole.onclick(hit_mole)

reset_game()

while True:
    window.update()
    time.sleep(0.02)
