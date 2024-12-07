from GameFrame import Level, TextObject, Globals
from Objects import Goal, Block, Player, Banner, Monster, Monster2


class lvl2(Level):

    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)
        Globals.score += 50
        Globals.monster_speed = 3
        self.portal_sound = self.load_sound('portal.wav')
        self.portal_sound.play()

        # - Set Background image - #
        self.set_background_image("800x600_space-stars-universe-outer-space.jpeg")

        # - Preload images from disk - #
        img_grnd_flat = self.load_image('Grass_Tile_Flat.png')
        img_grnd_left = self.load_image('Grass_Tile_Corner_Edge_l.png')
        img_grnd_right = self.load_image('Grass_Tile_Corner_Edge_r.png')
        img_grnd_under = self.load_image('Grass_Tile_lower.png')

        # - Set up maze, objects 32x32 25x17 - #
        room_objects = [
            'uuuuuuuuuuuuuuuuuuuuuuuuu',
            'u____u____u_____________u',
            'u____l____u_____________u',
            'u_________u_____________u',
            'u_________u_____________u',
            'u____l____u_____________u',
            'u____u____u_____________u',
            'u___mu____u_____________u',
            'u____u____u_____________u',
            'um___u____u_____________u',
            'u____u____u_____________u',
            'u___mu____l_____________u',
            'u____u__________________u',
            'um___u__________________u',
            'u____u________l________gu',
            'up__muG___l__GuG___lG__lu',
            'uuuuuuuuuuuuuuuuuuuuuuuuu'
        ]

        for i, row in enumerate(room_objects):
            for j, obj in enumerate(row):
                if obj == 'm':
                    self.add_room_object(Block(self, j*32, i*32, img_grnd_flat))
                elif obj == 'l':
                    self.add_room_object(Block(self, j * 32, i * 32, img_grnd_left))
                elif obj == 'r':
                    self.add_room_object(Block(self, j * 32, i * 32, img_grnd_right))
                elif obj == 'u':
                    self.add_room_object(Block(self, j * 32, i * 32, img_grnd_under))
                elif obj == 'p':
                    self.add_room_object(Player(self, j*32, i*32))
                elif obj == 'g':
                    self.add_room_object(Goal(self, j*32, i*32))
                elif obj == 'G':
                    self.add_room_object(Monster2(self, j*32, i*32))
                elif obj == 'M':
                    self.add_room_object(Monster(self, j * 32, i * 32))

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
