from turtle import Turtle
SCORE = 0

class Scoreboard(Turtle):
    def __init__(self):
       super().__init__()
       self.color('white')
       self.high_score = 0
       self.penup()
       self.goto(0,270)
       self.hideturtle()
       self.refresh(0)

    def refresh(self, score):
        self.clear()
        self.write(arg=f'Score: {score}', align='center', font=('Ms serif', '25', 'normal'))



    def game_over(self):
         self.home()
         self.write(arg='GAME OVER', align='center', font=('ms serif', '30', 'normal'))

