import turtle as t
import random

tim = t.Turtle()
t.colormode(255)

def random_colour():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    return (r,g,b)


tim.pensize(1)
moves = [0,90, 180, 270]
tim.speed(0)

for i in range(100):
    tim.circle(50)
    tim.color(random_colour())
    tim.right(5)












screen = t.Screen()
screen.exitonclick()