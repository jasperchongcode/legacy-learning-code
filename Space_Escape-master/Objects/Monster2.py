from GameFrame import RoomObject
from GameFrame import Globals

class Monster2(RoomObject):
    def __init__(self, room, x, y):
        RoomObject.__init__(self, room, x, y)

        image = self.load_image('monster.png')
        self.set_image(image, 32, 32)

        self.x_speed = -1*int(Globals.monster_speed)

        self.register_collision_object('Block')

    def handle_collision(self, other):
        if type(other).__name__ == 'Block':
            self.x_speed *= -1
