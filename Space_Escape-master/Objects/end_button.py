from GameFrame import RoomObject
#from Sounds import button_press


class end_button(RoomObject):
    def __init__(self, room, x, y):
        super().__init__(room, x, y)

        image = self.load_image('exit.png')
        self.set_image(image, 100, 50)

        self.depth = 100

        self.handle_mouse_events = True

    def clicked(self, button_number):
        if button_number == 1:
            #button_press.play()
            #wait(10)
            Globals.exiting = True
