from GameFrame import Level, TextObject, Globals
from Objects import Goal, Block, Player, Banner, Monster, Monster2, start_button, end_button



class end_splash(Level):

    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)

        # - Set Background image - #
        self.set_background_image("congradulations.png")
        #self.add_room_object(start_button(self,350,350))
        self.add_room_object(end_button(self, 350, 350))
        self.bonus_sound = self.load_sound('bonus.wav')
        self.bonus_sound.play()

        placeholder = int(Globals.score)

        text = placeholder - (5*(Globals.total_lives - Globals.LIVES))
        if text < 0:
            text = 0
        text = str(text)
        self.title_text = TextObject(self, 280, 150, 'Score:' + text)
        self.title_text.depth = 200
        self.title_text.colour = (255, 255, 255)
        self.title_text.update_text()
        self.add_room_object(self.title_text)





        # - Add Banner for game info (lives) 800x56 - #
        self.add_room_object(Banner(self, 0, 544))

        # - Add Text - #
        self.score_text = TextObject(self, 20, 560, 'Lives: %i' % Globals.LIVES)
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

