__author__ = 'justinarmstrong'
import pygame as pg
from .. import constants as c


class Portal(pg.sprite.Sprite):
    """Used to change level state"""
    def __init__(self, x, y, name):
        super(Portal, self).__init__()
        self.image = pg.Surface((32, 32))
        self.image.fill(c.BLACK)
        self.rect = pg.Rect(x, y, 32, 32)
        self.name = name
