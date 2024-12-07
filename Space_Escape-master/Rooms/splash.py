from GameFrame import Level, TextObject, Globals
from Objects import Goal, Block, Player, Banner, Monster, Monster2, start_button, easy, medium, hard



class splash(Level):

    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)
        Globals.LIVES = Globals.total_lives
        Globals.score = 0

        # - Set Background image - #
        self.set_background_image("title.png")
        self.add_room_object(start_button(self,350,450))
        self.add_room_object(hard(self,350,390))
        self.add_room_object(medium(self, 350, 330))
        self.add_room_object(easy(self, 350, 270))
        Globals.score = 0






        # - Add Banner for game info (lives) 800x56 - #
        self.add_room_object(Banner(self, 0, 544))

        # - Add Text - #
        self.score_text = TextObject(self, 15, 560, 'Easy:50 Medium:30 Hard:10')
        self.score_text.depth = 1000
        self.score_text.colour = (255, 255, 255)
        self.score_text.update_text()
        self.add_room_object(self.score_text)

    def update_lives(self, value):
        Globals.LIVES += value
        if Globals.LIVES == 0:
            self.running = False
            self.quitting = True
        self.score_text.text = 'Lives: %i' % Globals.LIVES
        self.score_text.update_text()

