import turtle
import time
import random

window = turtle.Screen()
window.title("Dino Runner")
window.bgcolor("white")
window.setup(width=800, height=400)
window.tracer(0)

dino = turtle.Turtle()
dino.shape("square")
dino.color("black")
dino.penup()
dino.goto(-200, -100)
dino.speed(0)
dino.dy = 0
gravity = -0.6

obstacles = []

def create_obstacle():
    obstacle = turtle.Turtle()
    obstacle.shape("square")
    obstacle.color("gray")
    obstacle.shapesize(stretch_wid=1, stretch_len=2)
    obstacle.penup()
    obstacle.speed(0)
    obstacle.goto(300, -100)
    obstacles.append(obstacle)

def jump():
    if dino.ycor() == -100:
        dino.dy = 12

window.listen()
window.onkey(jump, "space")

create_obstacle()

while True:
    window.update()

    dino.dy += gravity
    y = dino.ycor() + dino.dy
    if y < -100:
        y = -100
    dino.sety(y)

    for obstacle in obstacles:
        x = obstacle.xcor()
        x -= 5
        obstacle.setx(x)

        if obstacle.distance(dino) < 20:
            time.sleep(1)
            dino.goto(-200, -100)
            dino.dy = 0
            for obs in obstacles:
                obs.goto(1000, 1000)
            obstacles.clear()
            create_obstacle()

        if obstacle.xcor() < -400:
            obstacle.goto(1000, 1000)
            obstacles.remove(obstacle)
            create_obstacle()

    if len(obstacles) < 3 and random.randint(1, 100) == 1:
        create_obstacle()

    time.sleep(0.02)
