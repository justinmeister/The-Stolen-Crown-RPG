__author__ = 'justinarmstrong'

import pygame as pg
from ... import setup, tools
from ... import constants as c


class Menu(tools._State):
    def __init__(self, name):
        super(Menu, self).__init__(name)
        self.next = c.TOWN
        self.surface = setup.SCREEN
        self.rect = self.surface.get_rect()
        text = 'Main Menu placeholder'
        self.font = pg.font.Font(setup.FONTS['Fixedsys500c'], 15)
        self.rendered_text = self.font.render(text, 1, c.BLACK)
        self.text_rect = self.rendered_text.get_rect()
        self.text_rect.center = self.rect.center


    def update(self, surface, keys, current_time):
        self.current_time = current_time
        surface.fill(c.WHITE)
        surface.blit(self.rendered_text, self.text_rect)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.done = True