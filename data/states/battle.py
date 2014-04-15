"""This is the state that handles battles against
monsters"""

import pygame as pg
from .. import tools
from .. components import person
from .. import constants as c

class Battle(tools._State):
    def __init__(self):
        super(Battle, self).__init__()

    def startup(self, current_time, game_data):
        """Initialize state attributes"""
        self.current_time = current_time
        self.game_data = game_data
        self.background = self.make_background()
        self.enemy_group = self.make_enemies()
        self.player_group = self.make_player()
        self.menu = None
        self.name = 'battle'
        self.next = game_data['last state']

    def make_background(self):
        """Make the blue/black background"""
        background = pg.sprite.Sprite()
        surface = pg.Surface(c.SCREEN_SIZE).convert()
        surface.fill(c.BLACK_BLUE)
        background.image = surface
        background.rect = background.image.get_rect()
        background_group = pg.sprite.Group(background)

        return background_group

    def make_enemies(self):
        """Make the enemies for the battle. Return sprite group"""
        enemy = person.Person('devil', 100, 100, 'down', 'battle resting')
        group = pg.sprite.Group(enemy)

        return group

    def make_player(self):
        """Make the sprite for the player's character"""
        player = person.Player('left', 300, 300, 'battle resting')
        player_group = pg.sprite.Group(player)

        return player_group

    def update(self, surface, keys, current_time):
        """Update the battle state"""
        self.check_input(keys)
        self.enemy_group.update(current_time)
        self.player_group.update(keys, current_time)
        #self.menu.update()
        self.draw_battle(surface)

    def check_input(self, keys):
        """
        Check user input to navigate GUI.
        """
        if keys[pg.K_SPACE]:
            self.game_data['last state'] = self.name
            self.done = True

    def draw_battle(self, surface):
        """Draw all elements of battle state"""
        self.background.draw(surface)
        self.enemy_group.draw(surface)
        self.player_group.draw(surface)
        #self.menu.draw(surface)

