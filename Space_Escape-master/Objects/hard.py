from GameFrame import RoomObject
from GameFrame import Globals
#from Sounds import button_press


class hard(RoomObject):
    def __init__(self, room, x, y):
        super().__init__(room, x, y)

        image = self.load_image('hard.png')
        self.set_image(image, 100, 50)

        self.depth = 100

        self.handle_mouse_events = True

    def clicked(self, button_number):
        if button_number == 1:
            Globals.total_lives = 10
            Globals.LIVES = 10

