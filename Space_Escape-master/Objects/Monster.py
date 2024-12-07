from GameFrame import RoomObject
from GameFrame import Globals


class Monster(RoomObject):
    def __init__(self, room, x, y):
        RoomObject.__init__(self, room, x, y)

        image = self.load_image('monster.png')
        self.set_image(image, 32, 32)

        self.y_speed = int(Globals.monster_speed)*-1

        self.register_collision_object('Block')

    def handle_collision(self, other):
        if type(other).__name__ == 'Block':
            self.y_speed *= -1
