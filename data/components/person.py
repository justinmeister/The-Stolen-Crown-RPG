__author__ = 'justinarmstrong'
import math
import pygame as pg
from .. import setup


class Person(pg.sprite.Sprite):
    """Base class for all world characters
    controlled by the computer"""

    def __init__(self, sheet_key, x, y, direction='down'):
        super(Person, self).__init__()
        self.get_image = setup.tools.get_image
        self.spritesheet_dict = self.create_spritesheet_dict(sheet_key)
        self.animation_dict = self.create_animation_dict()
        self.index = 0
        self.direction = direction
        self.image_list = self.animation_dict[self.direction]
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(left=x, top=y)
        self.old_rect = self.rect
        self.state_dict = self.create_state_dict()
        self.vector_dict = self.create_vector_dict()
        self.x_vel = 0
        self.y_vel = 0
        self.timer = 0.0
        self.current_time = 0.0
        self.state = 'resting'
        self.blockers = self.set_blockers()


    def create_spritesheet_dict(self, sheet_key):
        """Implemented by inheriting classes"""
        image_list = []
        image_dict = {}
        sheet = setup.GFX[sheet_key]

        image_keys = ['facing up 1', 'facing up 2',
                      'facing down 1', 'facing down 2',
                      'facing left 1', 'facing left 2',
                      'facing right 1', 'facing right 2']

        for row in range(2):
            for column in range(4):
                image_list.append(
                    self.get_image(self, column*32, row*32, 32, 32, sheet))

        for key, image in zip(image_keys, image_list):
            image_dict[key] = image

        return image_dict


    def create_animation_dict(self):
        """Return a dictionary of image lists for animation"""
        image_dict = self.spritesheet_dict

        left_list = [image_dict['facing left 1'], image_dict['facing left 2']]
        right_list = [image_dict['facing right 1'], image_dict['facing right 2']]
        up_list = [image_dict['facing up 1'], image_dict['facing up 2']]
        down_list = [image_dict['facing down 1'], image_dict['facing down 2']]

        direction_dict = {'left': left_list,
                          'right': right_list,
                          'up': up_list,
                          'down': down_list}

        return direction_dict


    def create_state_dict(self):
        """Return a dictionary of all state methods"""
        state_dict = {'resting': self.resting,
                      'moving': self.moving}

        return state_dict


    def create_vector_dict(self):
        """Return a dictionary of x and y velocities set to
        direction keys."""
        vector_dict = {'up': (0, -2),
                       'down': (0, 2),
                       'left': (-2, 0),
                       'right': (2, 0)}

        return vector_dict


    def update(self, keys, current_time):
        """Implemented by inheriting classes"""
        self.blockers = self.set_blockers()
        self.current_time = current_time
        self.check_for_input()
        state_function = self.state_dict[self.state]
        state_function()


    def set_blockers(self):
        """Sets blockers to prevent collision with other sprites"""
        blockers = []

        if self.state == 'resting':
            blockers.append(pg.Rect(self.rect.x, self.rect.y, 32, 32))

        elif self.state == 'moving':
            if self.rect.x % 32 == 0:
                tile_float = self.rect.y / float(32)
                tile1 = (self.rect.x, math.ceil(tile_float)*32)
                tile2 = (self.rect.x, math.floor(tile_float)*32)
                tile_rect1 = pg.Rect(tile1[0], tile1[1], 32, 32)
                tile_rect2 = pg.Rect(tile2[0], tile2[1], 32, 32)
                blockers.extend([tile_rect1, tile_rect2])

            elif self.rect.y % 32 == 0:
                tile_float = self.rect.x / float(32)
                tile1 = (math.ceil(tile_float)*32, self.rect.y)
                tile2 = (math.floor(tile_float)*32, self.rect.y)
                tile_rect1 = pg.Rect(tile1[0], tile1[1], 32, 32)
                tile_rect2 = pg.Rect(tile2[0], tile2[1], 32, 32)
                blockers.extend([tile_rect1, tile_rect2])

        return blockers


    def resting(self):
        """
        When the Person is not moving between tiles.
        Checks if the player is centered on a tile.
        """
        self.image = self.image_list[self.index]

        assert(self.rect.y % 32 == 0), ('Player not centered on tile: '
                                        + str(self.rect.y))
        assert(self.rect.x % 32 == 0), ('Player not centered on tile'
                                        + str(self.rect.x))


    def moving(self):
        """Increment index and set self.image for animation."""
        self.animation()

        assert(self.rect.x % 32 == 0 or self.rect.y % 32 == 0), \
            'Not centered on tile'


    def animation(self):
        """Adjust sprite image frame based on timer"""
        if (self.current_time - self.timer) > 100:
            if self.index < (len(self.image_list) - 1):
                self.index += 1
            else:
                self.index = 0
            self.timer = self.current_time

        self.image = self.image_list[self.index]



    def begin_moving(self, direction):
        """Transition the player into the 'moving' state."""
        self.direction = direction
        self.image_list = self.animation_dict[direction]
        self.timer = self.current_time
        self.state = 'moving'
        self.old_rect = self.rect

        if self.rect.x % 32 == 0:
            self.y_vel = self.vector_dict[self.direction][1]
        if self.rect.y % 32 == 0:
            self.x_vel = self.vector_dict[self.direction][0]


    def begin_resting(self):
        """Transition the player into the 'resting' state."""
        self.state = 'resting'
        self.index = 1
        self.x_vel = self.y_vel = 0


class Player(Person):
    """User controlled character"""

    def __init__(self, direction):
        super(Player, self).__init__('player', 0, 0, direction)


    def update(self, keys, current_time):
        """Updates player behavior"""
        self.blockers = self.set_blockers()
        self.keys = keys
        self.current_time = current_time
        self.check_for_input()
        state_function = self.state_dict[self.state]
        state_function()


    def check_for_input(self):
        """Checks for player input"""
        if self.state == 'resting':
            if self.keys[pg.K_UP]:
                self.begin_moving('up')
            elif self.keys[pg.K_DOWN]:
                self.begin_moving('down')
            elif self.keys[pg.K_LEFT]:
                self.begin_moving('left')
            elif self.keys[pg.K_RIGHT]:
                self.begin_moving('right')



class Soldier(Person):
    """Soldier for the castle"""

    def __init__(self):
        super(Soldier, self).__init__('soldier', x, y)


class FemaleVillager(Person):
    """Female Person for town"""

    def __init__(self, x, y):
        super(FemaleVillager, self).__init__('femalevillager', x, y)


class MaleVillager(Person):
    """Male Person for town"""

    def __init__(self):
        super(MaleVillager, self).__init__('male villager', x, y)

