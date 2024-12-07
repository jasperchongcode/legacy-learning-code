from turtle import Turtle
FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.level = 1
        self.score_update()

    def level_up(self):
        self.level += 1
        self.score_update()

    def score_update(self):
        self.clear()
        self.goto(0,270)
        self.write(arg=f"Level: {self.level}", align='center', font=FONT)

    def game_over(self):
        self.goto(0,0)
        self.write(arg="GAME OVER", align='center', font=FONT)

