__author__ = 'justinarmstrong'

import os
import pygame as pg
from .. import setup, tools, tmx
from .. import constants as c

class Town(tools._State):
    def __init__(self):
        super(Town, self).__init__()

    def startup(self, current_time, persist):
        """Called when the State object is created"""
        self.persist = persist
        self.current_time = current_time
        self.tilemap = tmx.load(('map.tmx'),
            (800, 600))
        self.background = setup.GFX['town_background']


    def update(self, surface, keys, current_time):
        """Updates state"""
        self.keys = keys
        self.current_time = current_time
        self.tilemap.update(60)
        surface.blit(self.background, (0, 0))
        self.tilemap.draw(surface)