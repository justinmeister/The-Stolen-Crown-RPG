"""
Attack equipment for battles.
"""
import copy
import pygame as pg
from .. import tools, setup


class Sword(object):
    """
    Sword that appears during regular attacks.
    """
    def __init__(self, player):
        self.player = player
        self.sprite_sheet = setup.GFX['shopsigns']
        self.image = tools.get_image(48, 0, 16, 16, self.sprite_sheet)
        self.image = pg.transform.scale2x(self.image)

    @property
    def rect(self):
        new_rect = copy.copy(self.player.rect)
        new_rect.right -= 10
        new_rect.top += 15
        return new_rect

    def draw(self, surface):
        """
        Draw sprite to surface.
        """
        if self.player.state == 'attack':
            if self.player.x_vel % 5 == 0:
                 surface.blit(self.image, self.rect)

