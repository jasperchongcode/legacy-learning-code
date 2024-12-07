from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:

    def __init__(self):
        self.cars = []
        self.move_distance = STARTING_MOVE_DISTANCE

    def create_car(self):
        random_chance = random.randint(1,6)
        if random_chance == 1:
            new_car = Turtle('square')
            new_car.penup()
            new_car.shape('square')
            new_car.setheading(180)
            new_car.shapesize(stretch_wid=1,stretch_len=2)
            new_car.color(random.choice(COLORS))
            new_car.goto(300, (random.randint(-250, 250)))
            self.cars.append(new_car)

    def move_car(self):
        for car in self.cars:
            car.forward(self.move_distance)

    def speed_up(self):
        self.move_distance += MOVE_INCREMENT
