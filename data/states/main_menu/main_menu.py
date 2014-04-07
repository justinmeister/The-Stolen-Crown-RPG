import pygame as pg
from ... import setup, tools
from ... import constants as c

class Menu(tools._State):
    def __init__(self):
        super(Menu, self).__init__()
        self.next = c.BROTHER_HOUSE
        self.surface = setup.SCREEN
        self.rect = self.surface.get_rect()
        text = 'Arrows for navigation, space for input, Enter/Return for menu'
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.rendered_text = self.font.render(text, 1, c.BLACK)
        self.text_rect = self.rendered_text.get_rect()
        self.text_rect.center = self.rect.center
        self.game_data = tools.create_game_data_dict()
        self.name = c.MAIN_MENU


    def update(self, surface, keys, current_time):
        self.current_time = current_time
        surface.fill(c.WHITE)
        surface.blit(self.rendered_text, self.text_rect)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.game_data['last state'] = self.name
            self.done = True
