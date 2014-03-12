__author__ = 'justinarmstrong'
import pygame as pg
from .. import setup

class Dialogue(pg.sprite.Sprite):
    """Text box used for dialogue"""
    def __init__(self, x):
        super(Dialogue, self).__init__()
        self.image = setup.GFX['dialoguebox']
        self.rect = self.image.get_rect(centerx=x)
        self.timer = 0.0

    def update(self, current_time):
        """Updates scrolling text"""
        if self.timer == 0.0:
            self.timer = current_time
        elif (current_time - self.timer) > 2000:
            self.kill()



