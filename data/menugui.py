"""
This class controls all the GUI for the player
menu screen.
"""
import pygame as pg
from . import setup
from . import constants as c



class MenuGui(object):
    def __init__(self, inventory):
        self.font = pg.font.Font(setup.FONTS['Fixedsys500c'], 22)
        self.inventory = inventory
        self.gold_box = self.make_gold_box()
        self.stat_box = self.make_stat_box()
        self.selection_box = self.make_selection_box()
        self.box_group = self.make_box_group()


    def make_gold_box(self):
        """Makes the box that displays gold"""
        image = setup.GFX['goldbox']
        rect = image.get_rect(left=10, top=234)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        text = "Gold: " + str(self.inventory['gold'])
        text_render = self.font.render(text, True, c.NEAR_BLACK)
        text_rect = text_render.get_rect(x=80, y=60)
        surface.blit(text_render, text_rect)

        sprite = pg.sprite.Sprite()
        sprite.image = surface
        sprite.rect = rect

        return sprite


    def make_stat_box(self):
        """Make the box for displaying stats and items"""
        image = setup.GFX['playerstatsbox']
        rect = image.get_rect(left=285, top=35)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0,0))

        sprite = pg.sprite.Sprite()
        sprite.image = surface
        sprite.rect = rect

        return sprite


    def make_selection_box(self):
        """Make the menu with selection options"""
        image = setup.GFX['goldbox']
        rect = image.get_rect(left=10, top=410)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        sprite = pg.sprite.Sprite()
        sprite.image = surface
        sprite.rect = rect

        return sprite


    def make_box_group(self):
        """Make the sprite group for each GUI box"""
        return pg.sprite.Group(self.gold_box,
                               self.stat_box,
                               self.selection_box)

    def update(self, keys):
        pass

    def draw(self, surface):
        self.box_group.draw(surface)