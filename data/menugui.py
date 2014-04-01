"""
This class controls all the GUI for the player
menu screen.
"""
import pygame as pg
from . import setup
from . import constants as c


class SmallArrow(pg.sprite.Sprite):
    """Small arrow for menu"""
    def __init__(self):
        super(SmallArrow, self).__init__()
        self.image = setup.GFX['smallarrow']
        self.rect = self.image.get_rect()


class MenuGui(object):
    def __init__(self, level, inventory):
        self.level = level
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.inventory = inventory
        self.allow_input = False
        self.state = 'topmenu'
        self.gold_box = None
        self.stat_box = None
        self.selection_box = None
        self.arrow = SmallArrow()
        self.arrow_index = 0
        self.arrow_pos = self.make_arrow_pos_list()
        self.state_dict = self.make_state_dict()


    def make_arrow_pos_list(self):
        """Make the list of possible arrow positions"""
        pos_list = []

        for i in range(4):
            pos = (35, 356 + (i * 50))
            pos_list.append(pos)

        return pos_list


    def make_gold_box(self):
        """Makes the box that displays gold"""
        image = setup.GFX['goldbox2']
        rect = image.get_rect(left=10, top=234)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        text = "Gold: " + str(self.inventory['gold'])
        text_render = self.font.render(text, True, c.NEAR_BLACK)
        text_rect = text_render.get_rect(centerx=130,
                                         centery=35)
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


    def make_selection_box(self, choices):
        """Make the menu with selection options"""
        image = setup.GFX['selectionbox']
        rect = image.get_rect(left=10, top=330)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        for i, choice in enumerate(choices):
            choice_image = self.font.render(choice, True, c.NEAR_BLACK)
            y_position = 25 + (i * 50)
            choice_rect = choice_image.get_rect(x=100, y=y_position)
            surface.blit(choice_image, choice_rect)

        sprite = pg.sprite.Sprite()
        sprite.image = surface
        sprite.rect = rect

        return sprite


    def make_box_group(self):
        """Make the sprite group for each GUI box"""
        return pg.sprite.Group(self.gold_box,
                               self.stat_box,
                               self.selection_box)


    def make_state_dict(self):
        """Make the dictionary of all menu states"""
        state_dict = {'topmenu': self.select_main_options}

        return state_dict


    def select_main_options(self, keys):
        """Allow player to select items, magic, weapons and armor"""
        choices = ['Equip', 'Items', 'Magic', 'Exit']
        self.selection_box = self.make_selection_box(choices)
        self.gold_box = self.make_gold_box()
        self.stat_box = self.make_stat_box()
        self.arrow.rect.topleft = self.arrow_pos[self.arrow_index]

        if self.allow_input:
            if keys[pg.K_DOWN]:
                if self.arrow_index < len(choices) - 1:
                    self.arrow_index += 1
                    self.allow_input = False
            elif keys[pg.K_UP]:
                if self.arrow_index > 0:
                    self.arrow_index -= 1
                    self.allow_input = False
            elif keys[pg.K_SPACE]:
                if self.arrow_index == len(choices) - 1:
                    self.level.done = True

        if not keys[pg.K_DOWN] and not keys[pg.K_UP]:
            self.allow_input = True



    def update(self, keys):
        state_function = self.state_dict[self.state]
        state_function(keys)


    def draw(self, surface):
        if self.gold_box and self.stat_box and self.selection_box:
            surface.blit(self.gold_box.image, self.gold_box.rect)
            surface.blit(self.stat_box.image, self.stat_box.rect)
            surface.blit(self.selection_box.image, self.selection_box.rect)
            surface.blit(self.arrow.image, self.arrow.rect)