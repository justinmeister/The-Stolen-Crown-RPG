__author__ = 'justinarmstrong'

import pygame as pg
from .. import setup

class Player(pg.sprite.Sprite):
    """User controllable character"""
    def __init__(self):
        super(Player, self).__init__()
        self.get_image = setup.tools.get_image
        self.spritesheet_dict = self.create_spritesheet()
        self.image = self.spritesheet_dict['facing down 1']
        self.rect = self.image.get_rect()
        self.state_dict = self.create_state_dict()
        self.direction_dict = self.create_direction_dict()
        self.state = 'resting'
        self.x_vel = 0
        self.y_vel = 0
        self.direction = 'up'


    def create_spritesheet(self):
        """Creates the sprite sheet dictionary for player"""
        sheet = setup.GFX['player']
        image_list = []
        for row in range(2):
            for column in range(4):
                image_list.append(self.get_image(
                    self, column*32, row*32, 32, 32, sheet))

        dict = {'facing up 1': image_list[0],
                'facing up 2': image_list[1],
                'facing down 1': image_list[2],
                'facing down 2': image_list[3],
                'facing left 1': image_list[4],
                'facing left 2': image_list[5],
                'facing right 1': image_list[6],
                'facing right 2': image_list[7]}

        return dict


    def create_state_dict(self):
        """Creates a dictionary of all the states the player
        can be in"""
        dict = {'resting': self.resting,
                'moving': self.moving}

        return dict


    def create_direction_dict(self):
        """Creates a dictionary of directions with truth values
        corresponding to the player's direction"""
        dict = {'up': (0, -2),
                'down': (0, 2),
                'left': (-2, 0),
                'right': (2, 0)}

        return dict


    def update(self):
        """Updates player behavior"""
        state = self.state_dict[self.state]
        state()


    def resting(self):
        """When the player is not moving between tiles.
        Checks if the player is centered on a tile"""
        assert(self.rect.y % 32 == 0), ('Player not centered on tile: '
                                        + str(self.rect.y))
        assert(self.rect.x % 32 == 0), ('Player not centered on tile'
                                        + str(self.rect.x))


    def moving(self):
        """When the player is moving between tiles"""
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel


    def begin_moving(self, direction):
        """Transitions the player into the moving state"""
        self.state = 'moving'
        self.direction = direction
        self.x_vel, self.y_vel = self.direction_dict[self.direction]


    def begin_resting(self):
        """Transitions the player into the resting state"""
        self.state = 'resting'
        self.x_vel, self.y_vel = 0



