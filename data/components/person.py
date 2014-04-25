import math, random
import pygame as pg
from .. import setup
from .. import constants as c


class Person(pg.sprite.Sprite):
    """Base class for all world characters
    controlled by the computer"""

    def __init__(self, sheet_key, x, y, direction='down', state='resting', index=0):
        super(Person, self).__init__()
        self.name = sheet_key
        self.get_image = setup.tools.get_image
        self.spritesheet_dict = self.create_spritesheet_dict(sheet_key)
        self.animation_dict = self.create_animation_dict()
        self.index = index
        self.direction = direction
        self.image_list = self.animation_dict[self.direction]
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(left=x, top=y)
        self.origin_pos = self.rect.topleft
        self.state_dict = self.create_state_dict()
        self.vector_dict = self.create_vector_dict()
        self.x_vel = 0
        self.y_vel = 0
        self.timer = 0.0
        self.move_timer = 0.0
        self.current_time = 0.0
        self.state = state
        self.blockers = self.set_blockers()
        self.location = self.get_tile_location()
        self.dialogue = ['Location: ' + str(self.location)]
        self.default_direction = direction
        self.item = None
        self.wander_box = self.make_wander_box()
        self.observers = []

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
                    self.get_image(column*32, row*32, 32, 32, sheet))

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
                      'moving': self.moving,
                      'animated resting': self.animated_resting,
                      'autoresting': self.auto_resting,
                      'automoving': self.auto_moving,
                      'battle resting': self.battle_resting,
                      'attack': self.attack,
                      'enemy attack': self.enemy_attack}

        return state_dict

    def create_vector_dict(self):
        """Return a dictionary of x and y velocities set to
        direction keys."""
        vector_dict = {'up': (0, -1),
                       'down': (0, 1),
                       'left': (-1, 0),
                       'right': (1, 0)}

        return vector_dict

    def update(self, current_time, *args):
        """Implemented by inheriting classes"""
        self.blockers = self.set_blockers()
        self.current_time = current_time
        self.image_list = self.animation_dict[self.direction]
        state_function = self.state_dict[self.state]
        state_function()
        self.location = self.get_tile_location()



    def set_blockers(self):
        """Sets blockers to prevent collision with other sprites"""
        blockers = []

        if self.state == 'resting' or self.state == 'autoresting':
            blockers.append(pg.Rect(self.rect.x, self.rect.y, 32, 32))

        elif self.state == 'moving' or self.state == 'automoving':
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

    def get_tile_location(self):
        """
        Convert pygame coordinates into tile coordinates.
        """
        if self.rect.x == 0:
            tile_x = 0
        elif self.rect.x % 32 == 0:
            tile_x = (self.rect.x / 32)
        else:
            tile_x = 0

        if self.rect.y == 0:
            tile_y = 0
        elif self.rect.y % 32 == 0:
            tile_y = (self.rect.y / 32)
        else:
            tile_y = 0

        return [tile_x, tile_y]


    def make_wander_box(self):
        """
        Make a list of rects that surround the initial location
        of a sprite to limit his/her wandering.
        """
        x = int(self.location[0])
        y = int(self.location[1])
        box_list = []
        box_rects = []

        for i in range(x-3, x+4):
            box_list.append([i, y-3])
            box_list.append([i, y+3])

        for i in range(y-2, y+3):
            box_list.append([x-3, i])
            box_list.append([x+3, i])

        for box in box_list:
            left = box[0]*32
            top = box[1]*32
            box_rects.append(pg.Rect(left, top, 32, 32))

        return box_rects


    def resting(self):
        """
        When the Person is not moving between tiles.
        Checks if the player is centered on a tile.
        """
        self.image = self.image_list[self.index]

        assert(self.rect.y % 32 == 0), ('Player not centered on tile: '
                                        + str(self.rect.y) + " : " + str(self.name))
        assert(self.rect.x % 32 == 0), ('Player not centered on tile'
                                        + str(self.rect.x))

    def moving(self):
        """
        Increment index and set self.image for animation.
        """
        self.animation()
        assert(self.rect.x % 32 == 0 or self.rect.y % 32 == 0), \
            'Not centered on tile'

    def animated_resting(self):
        self.animation(500)

    def animation(self, freq=100):
        """
        Adjust sprite image frame based on timer.
        """
        if (self.current_time - self.timer) > freq:
            if self.index < (len(self.image_list) - 1):
                self.index += 1
            else:
                self.index = 0
            self.timer = self.current_time

        self.image = self.image_list[self.index]

    def begin_moving(self, direction):
        """
        Transition the player into the 'moving' state.
        """
        self.direction = direction
        self.image_list = self.animation_dict[direction]
        self.timer = self.current_time
        self.move_timer = self.current_time
        self.state = 'moving'

        if self.rect.x % 32 == 0:
            self.y_vel = self.vector_dict[self.direction][1]
        if self.rect.y % 32 == 0:
            self.x_vel = self.vector_dict[self.direction][0]


    def begin_resting(self):
        """
        Transition the player into the 'resting' state.
        """
        self.state = 'resting'
        self.index = 1
        self.x_vel = self.y_vel = 0

    def begin_auto_moving(self, direction):
        """
        Transition sprite to a automatic moving state.
        """
        self.direction = direction
        self.image_list = self.animation_dict[direction]
        self.state = 'automoving'
        self.x_vel = self.vector_dict[direction][0]
        self.y_vel = self.vector_dict[direction][1]
        self.move_timer = self.current_time

    def begin_auto_resting(self):
        """
        Transition sprite to an automatic resting state.
        """
        self.state = 'autoresting'
        self.index = 1
        self.x_vel = self.y_vel = 0
        self.move_timer = self.current_time


    def auto_resting(self):
        """
        Determine when to move a sprite from resting to moving in a random
        direction.
        """
        #self.image = self.image_list[self.index]
        self.image_list = self.animation_dict[self.direction]
        self.image = self.image_list[self.index]

        assert(self.rect.y % 32 == 0), ('Player not centered on tile: '
                                        + str(self.rect.y))
        assert(self.rect.x % 32 == 0), ('Player not centered on tile'
                                        + str(self.rect.x))

        if (self.current_time - self.move_timer) > 2000:
            direction_list = ['up', 'down', 'left', 'right']
            random.shuffle(direction_list)
            direction = direction_list[0]
            self.begin_auto_moving(direction)
            self.move_timer = self.current_time

    def battle_resting(self):
        """
        Player stays still during battle state unless he attacks.
        """
        pass

    def enter_attack_state(self, enemy):
        """
        Set values for attack state.
        """
        self.attacked_enemy = enemy
        self.x_vel = -5
        self.state = 'attack'

    def attack(self):
        """
        Player does an attack animation.
        """
        SLOW_BACK = 1
        FAST_FORWARD = -5
        FAST_BACK = 5

        self.rect.x += self.x_vel

        if self.x_vel == SLOW_BACK:
            if self.rect.x >= self.origin_pos[0] + 20:
                self.x_vel = FAST_FORWARD
        elif self.x_vel == FAST_FORWARD:
            if self.rect.topleft >= self.origin_pos:
                self.image = self.spritesheet_dict['facing left 1']
                self.image = pg.transform.scale2x(self.image)
            elif self.rect.x <= self.origin_pos[0] - 110:
                self.x_vel = FAST_BACK
                self.notify('attack animation')
        else:
            if self.rect.x >= self.origin_pos[0]:
                self.rect.x = self.origin_pos[0]
                self.x_vel = 0
                self.state = 'battle resting'
                self.image = self.spritesheet_dict['facing left 2']
                self.image = pg.transform.scale2x(self.image)
                self.notify(c.PLAYER_FINISHED_ATTACK)

    def enter_enemy_attack_state(self):
        """
        Set values for enemy attack state.
        """
        self.x_vel = -5
        self.state = 'enemy attack'
        self.origin_pos = self.rect.topleft
        self.move_counter = 0

    def enemy_attack(self):
        """
        Enemy does an attack animation.
        """
        FAST_LEFT = -5
        FAST_RIGHT = 5
        STARTX = self.origin_pos[0]

        self.rect.x += self.x_vel

        if self.move_counter == 3:
            self.x_vel = 0
            self.state = 'battle resting'
            self.rect.x = STARTX
            self.notify(c.SWITCH_ENEMY)

        elif self.x_vel == FAST_LEFT:
            if self.rect.x <= (STARTX - 15):
                self.x_vel = FAST_RIGHT
        elif self.x_vel == FAST_RIGHT:
            if self.rect.x >= (STARTX + 15):
                self.move_counter += 1
                self.x_vel = FAST_LEFT

    def auto_moving(self):
        """
        Animate sprite and check to stop.
        """
        self.animation()

        assert(self.rect.x % 32 == 0 or self.rect.y % 32 == 0), \
            'Not centered on tile'

    def notify(self, event):
        """
        Notify all observers of events.
        """
        for observer in self.observers:
            observer.on_notify(event)


class Player(Person):
    """
    User controlled character.
    """

    def __init__(self, direction, x=0, y=0, state='resting', index=0):
        super(Player, self).__init__('player', x, y, direction, state, index)

    def create_vector_dict(self):
        """Return a dictionary of x and y velocities set to
        direction keys."""
        vector_dict = {'up': (0, -2),
                       'down': (0, 2),
                       'left': (-2, 0),
                       'right': (2, 0)}

        return vector_dict

    def update(self, keys, current_time):
        """Updates player behavior"""
        self.blockers = self.set_blockers()
        self.keys = keys
        self.current_time = current_time
        self.check_for_input()
        state_function = self.state_dict[self.state]
        state_function()
        self.location = self.get_tile_location()

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




class Well(pg.sprite.Sprite):
    """Talking well"""
    def __init__(self, x, y):
        super(Well, self).__init__()
        self.image = pg.Surface((32, 32))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(left=x, top=y)
        self.location = self.get_location()
        self.dialogue = ["I'm a well!"]
        self.blockers = [self.rect]
        self.x_vel = self.y_vel = 0
        self.state = 'resting'
        self.direction = 'down'
        self.default_direction = self.direction
        self.item = None
        self.wander_box = []

    def get_location(self):
        """Get tile location"""
        x = self.rect.x / 32
        y = self.rect.y / 32

        return [x, y]

    def begin_auto_resting(self):
        """Placeholder"""
        pass


