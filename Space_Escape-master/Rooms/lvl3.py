from GameFrame import Level, TextObject, Globals
from Objects import Goal, Block, Player, Banner, Monster, Monster2


class lvl3(Level):

    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)
        Globals.score += 50
        Globals.monster_speed = 4
        self.portal_sound = self.load_sound('portal.wav')
        self.portal_sound.play()

        # - Set Background image - #
        self.set_background_image("800px-Astronaut-in-space.jpeg")

        # - Preload images from disk - #
        img_grnd_flat = self.load_image('Grass_Tile_Flat.png')
        img_grnd_left = self.load_image('Grass_Tile_Corner_Edge_l.png')
        img_grnd_right = self.load_image('Grass_Tile_Corner_Edge_r.png')
        img_grnd_under = self.load_image('Grass_Tile_lower.png')

        # - Set up maze, objects 32x32 25x17 - #
        room_objects = [
            'uuuuuuuuuuuuuuuuuuuuuuuuu',
            'u___M_M_____Muu__M______u',
            'u____________uu_________u',
            'ug___________uu_________u',
            'ummm_________uu____l____u',
            'u____________uu____um___u',
            'u____________lu____u____u',
            'u____m________u____u___mu',
            'u___________M_l____u____u',
            'u_______mmm________um___u',
            'u__________________u____u',
            'u____________mm____u___mu',
            'u__________________u____u',
            'u__________________um___u',
            'u_______________________u',
            'up__M_M_____M___M_______u',
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
