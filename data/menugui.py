# -*- coding: utf-8 -*-
"""
This class controls all the GUI for the player
menu screen.
"""
import pygame as pg
from . import setup
from . import constants as c
from . import tools


class SmallArrow(pg.sprite.Sprite):
    """Small arrow for menu"""
    def __init__(self, info_box):
        super(SmallArrow, self).__init__()
        self.image = setup.GFX['smallarrow']
        self.rect = self.image.get_rect()
        self.state = 'selectmenu'
        self.state_dict = self.make_state_dict()
        self.slots = info_box.slots
        self.pos_list = []


    def make_state_dict(self):
        """Make state dictionary"""
        state_dict = {'selectmenu': self.navigate_select_menu,
                      'itemsubmenu': self.navigate_item_submenu}

        return state_dict


    def navigate_select_menu(self, pos_index):
        """Nav the select menu"""
        self.pos_list = self.make_select_menu_pos_list()
        self.rect.topleft = self.pos_list[pos_index]


    def navigate_item_submenu(self, pos_index):
        """Nav the item submenu"""
        self.pos_list = self.make_item_menu_pos_list()
        self.rect.topleft = self.pos_list[pos_index]


    def make_select_menu_pos_list(self):
        """Make the list of possible arrow positions"""
        pos_list = []

        for i in range(4):
            pos = (35, 356 + (i * 50))
            pos_list.append(pos)

        return pos_list


    def make_item_menu_pos_list(self):
        """Make the list of arrow positions in the item submenu"""
        pos_list = [(300, 173),
                    (300, 223),
                    (300, 323),
                    (300, 373),
                    (300, 478),
                    (300, 528),
                    (535, 478),
                    (535, 528)]

        return pos_list


    def update(self, pos_index):
        """Update arrow position"""
        state_function = self.state_dict[self.state]
        state_function(pos_index)


    def draw(self, surface):
        """Draw to surface"""
        surface.blit(self.image, self.rect)



class GoldBox(pg.sprite.Sprite):
    def __init__(self, inventory):
        self.inventory = inventory
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.image, self.rect = self.make_image()

    def make_image(self):
        """Make the surface for the gold box"""
        image = setup.GFX['goldbox2']
        rect = image.get_rect(left=10, top=234)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        text = "Gold: " + str(self.inventory['GOLD']['quantity'])
        text_render = self.font.render(text, True, c.NEAR_BLACK)
        text_rect = text_render.get_rect(centerx=130,
                                         centery=35)
        surface.blit(text_render, text_rect)

        return surface, rect


    def update(self):
        """Update gold"""
        self.image, self.rect = self.make_image()


    def draw(self, surface):
        """Draw to surface"""
        surface.blit(self.image, self.rect)



class InfoBox(pg.sprite.Sprite):
    def __init__(self, inventory, player_stats):
        super(InfoBox, self).__init__()
        self.inventory = inventory
        self.player_stats = player_stats
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.big_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 24)
        self.title_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 28)
        self.title_font.set_underline(True)
        self.get_tile = tools.get_tile
        self.sword = self.get_tile(48, 0, setup.GFX['shopsigns'], 16, 16, 2)
        self.shield = self.get_tile(32, 0, setup.GFX['shopsigns'], 16, 16, 2)
        self.potion = self.get_tile(16, 0, setup.GFX['shopsigns'], 16, 16, 2)
        self.possible_potions = ['Healing Potion', 'ELIXIR', 'Ether Potion']
        self.possible_armor = ['Wooden Shield', 'Chain Mail']
        self.possible_weapons = ['Long Sword', 'Rapier']
        self.possible_magic = ['Fire Blast', 'Cure']
        self.quantity_items = ['Healing Potion', 'ELIXIR', 'Ether Potion']
        self.slots = {}
        self.state = 'stats'
        self.state_dict = self.make_state_dict()
        self.print_slots = True


    def make_state_dict(self):
        """Make the dictionary of state methods"""
        state_dict = {'stats': self.show_player_stats,
                      'items': self.show_items,
                      'magic': self.show_magic}

        return state_dict


    def show_player_stats(self):
        """Show the player's main stats"""
        title = 'STATS'
        stat_list = ['Level', 'health',
                     'magic points', 'experience to next level']
        surface, rect = self.make_blank_info_box(title)

        for i, stat in enumerate(stat_list):
            if stat == 'health' or stat == 'magic points':
                text = "{}{}: {} / {}".format(stat[0].upper(),
                                              stat[1:],
                                              str(self.player_stats[stat]['current']),
                                              str(self.player_stats[stat]['maximum']))
            elif stat == 'experience to next level':
                text = "{}{}: {}".format(stat[0].upper(),
                                         stat[1:],
                                         self.player_stats[stat])
            else:
                text = "{}: {}".format(stat, str(self.player_stats[stat]))
            text_image = self.font.render(text, True, c.NEAR_BLACK)
            text_rect = text_image.get_rect(x=50, y=80+(i*50))
            surface.blit(text_image, text_rect)

        self.image = surface
        self.rect = rect


    def show_items(self):
        """Show list of items the player has"""
        title = 'ITEMS'
        potions = ['POTIONS']
        weapons = ['WEAPONS']
        armor = ['ARMOR']
        for i, item in enumerate(self.inventory):
            if item in self.possible_weapons:
                weapons.append(item)
            elif item in self.possible_armor:
                armor.append(item)
            elif item in self.possible_potions:
                potions.append(item)

        self.assign_slots(weapons, 85)
        self.assign_slots(armor, 235)
        self.assign_slots(potions, 390)

        surface, rect = self.make_blank_info_box(title)

        self.blit_item_lists(surface)

        self.sword['rect'].topleft = 40, 80
        self.shield['rect'].topleft = 40, 230
        self.potion['rect'].topleft = 40, 385
        surface.blit(self.sword['surface'], self.sword['rect'])
        surface.blit(self.shield['surface'], self.shield['rect'])
        surface.blit(self.potion['surface'], self.potion['rect'])

        self.image = surface
        self.rect = rect


    def assign_slots(self, item_list, starty):
        """Assign each item to a slot in the menu"""
        if len(item_list) > 3:
            for i, item in enumerate(item_list[:3]):
                posx = 80
                posy = starty + (i * 50)
                self.slots[(posx, posy)] = item
            for i, item in enumerate(item_list[3:]):
                posx = 315
                posy = (starty + 50) + (i * 5)
                self.slots[(posx, posy)] = item
        else:
            for i, item in enumerate(item_list):
                posx = 80
                posy = starty + (i * 50)
                self.slots[(posx, posy)] = item


    def blit_item_lists(self, surface):
        """Blit item list to info box surface"""
        for coord in self.slots:
            item = self.slots[coord]
            if item in self.inventory:
                text = "{}: {}".format(self.slots[coord],
                                       self.inventory[item]['quantity'])
            else:
                text = "{}".format(self.slots[coord])
            text_image = self.font.render(text, True, c.NEAR_BLACK)
            text_rect = text_image.get_rect(topleft=coord)
            surface.blit(text_image, text_rect)



    def show_magic(self):
        """Show list of magic spells the player knows"""
        title = 'MAGIC'
        item_list = []
        for item in self.inventory:
            if item in self.possible_magic:
                item_list.append(item)
                item_list = sorted(item_list)

        surface, rect = self.make_blank_info_box(title)

        for i, item in enumerate(item_list):
            text_image = self.font.render(item, True, c.NEAR_BLACK)
            text_rect = text_image.get_rect(x=50, y=80+(i*50))
            surface.blit(text_image, text_rect)

        self.image = surface
        self.rect = rect


    def make_blank_info_box(self, title):
        """Make an info box with title, otherwise blank"""
        image = setup.GFX['playerstatsbox']
        rect = image.get_rect(left=285, top=35)
        centerx = rect.width / 2

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0,0))

        title_image = self.title_font.render(title, True, c.NEAR_BLACK)
        title_rect = title_image.get_rect(centerx=centerx, y=30)
        surface.blit(title_image, title_rect)

        return surface, rect


    def update(self):
        state_function = self.state_dict[self.state]
        state_function()


    def draw(self, surface):
        """Draw to surface"""
        surface.blit(self.image, self.rect)


class SelectionBox(pg.sprite.Sprite):
    def __init__(self):
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.image, self.rect = self.make_image()


    def make_image(self):
        choices = ['Stats', 'Items', 'Magic', 'Exit']
        image = setup.GFX['selectionbox']
        rect = image.get_rect(left=10, top=330)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        for i, choice in enumerate(choices):
            choice_image = self.font.render(choice, True, c.NEAR_BLACK)
            choice_rect = choice_image.get_rect(x=100, y=(25 + (i * 50)))
            surface.blit(choice_image, choice_rect)

        return surface, rect


    def draw(self, surface):
        """Draw to surface"""
        surface.blit(self.image, self.rect)




class MenuGui(object):
    def __init__(self, level, inventory, stats):
        self.level = level
        self.inventory = inventory
        self.stats = stats
        self.info_box = InfoBox(inventory, stats)
        self.gold_box = GoldBox(inventory)
        self.selection_box = SelectionBox()
        self.arrow = SmallArrow(self.info_box)
        self.arrow_index = 0
        self.allow_input = False
        self.state = 'stats'


    def check_for_input(self, keys):
        """Check for input"""
        if self.allow_input:
            if keys[pg.K_DOWN]:
                if self.arrow_index < len(self.arrow.pos_list) - 1:
                    self.arrow_index += 1
                    self.allow_input = False
            elif keys[pg.K_UP]:
                if self.arrow_index > 0:
                    self.arrow_index -= 1
                    self.allow_input = False
            elif keys[pg.K_RIGHT]:
                if self.info_box.state == 'items':
                    if not self.arrow.state == 'itemsubmenu':
                        self.arrow_index = 0
                    self.arrow.state = 'itemsubmenu'

            elif keys[pg.K_LEFT]:
                self.arrow.state = 'selectmenu'
                self.arrow_index = 0
            elif keys[pg.K_SPACE]:
                if self.arrow.state == 'selectmenu':
                    if self.arrow_index == 0:
                        self.info_box.state = 'stats'

                    elif self.arrow_index == 1:
                        self.info_box.state = 'items'

                    elif self.arrow_index == 2:
                        self.info_box.state = 'magic'

                    elif self.arrow_index == 3:
                        self.level.state = 'normal'
                        self.arrow_index = 0
                        self.info_box.state = 'stats'


                self.allow_input = False
            elif keys[pg.K_RETURN]:
                self.level.state = 'normal'
                self.info_box.state = 'stats'
                self.allow_input = False
                self.arrow_index = 0

        if (not keys[pg.K_DOWN]
                and not keys[pg.K_UP]
                and not keys[pg.K_RETURN]
                and not keys[pg.K_SPACE]):
            self.allow_input = True


    def update(self, keys):
        self.info_box.update()
        self.gold_box.update()
        self.arrow.update(self.arrow_index)
        self.check_for_input(keys)


    def draw(self, surface):
        self.gold_box.draw(surface)
        self.info_box.draw(surface)
        self.selection_box.draw(surface)
        self.arrow.draw(surface)
