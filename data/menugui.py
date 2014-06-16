# -*- coding: utf-8 -*-

"""
This class controls all the GUI for the player
menu screen.
"""
import sys
import pygame as pg
from . import setup, observer
from . import constants as c
from . import tools

#Python 2/3 compatibility.
if sys.version_info[0] == 2:
    range = xrange


class SmallArrow(pg.sprite.Sprite):
    """
    Small arrow for menu.
    """
    def __init__(self, info_box):
        super(SmallArrow, self).__init__()
        self.image = setup.GFX['smallarrow']
        self.rect = self.image.get_rect()
        self.state = 'selectmenu'
        self.state_dict = self.make_state_dict()
        self.slots = info_box.slots
        self.pos_list = []

    def make_state_dict(self):
        """
        Make state dictionary.
        """
        state_dict = {'selectmenu': self.navigate_select_menu,
                      'itemsubmenu': self.navigate_item_submenu,
                      'magicsubmenu': self.navigate_magic_submenu}

        return state_dict

    def navigate_select_menu(self, pos_index):
        """
        Nav the select menu.
        """
        self.pos_list = self.make_select_menu_pos_list()
        self.rect.topleft = self.pos_list[pos_index]

    def navigate_item_submenu(self, pos_index):
        """Nav the item submenu"""
        self.pos_list = self.make_item_menu_pos_list()
        self.rect.topleft = self.pos_list[pos_index]

    def navigate_magic_submenu(self, pos_index):
        """
        Nav the magic submenu.
        """
        self.pos_list = self.make_magic_menu_pos_list()
        self.rect.topleft = self.pos_list[pos_index]

    def make_magic_menu_pos_list(self):
        """
        Make the list of possible arrow positions for magic submenu.
        """
        pos_list = [(310, 119),
                    (310, 169)]

        return pos_list

    def make_select_menu_pos_list(self):
        """
        Make the list of possible arrow positions.
        """
        pos_list = []

        for i in range(3):
            pos = (35, 443 + (i * 45))
            pos_list.append(pos)

        return pos_list

    def make_item_menu_pos_list(self):
        """
        Make the list of arrow positions in the item submenu.
        """
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
        """
        Update arrow position.
        """
        state_function = self.state_dict[self.state]
        state_function(pos_index)

    def draw(self, surface):
        """
        Draw to surface"""
        surface.blit(self.image, self.rect)


class QuickStats(pg.sprite.Sprite):
    def __init__(self, game_data):
        self.inventory = game_data['player inventory']
        self.game_data = game_data
        self.health = game_data['player stats']['health']
        self.stats = self.game_data['player stats']
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.small_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 18)
        self.image, self.rect = self.make_image()

    def make_image(self):
        """
        Make the surface for the gold box.
        """
        stat_list = ['GOLD', 'health', 'magic'] 
        magic_health_list  = ['health', 'magic']
        image = setup.GFX['goldbox']
        rect = image.get_rect(left=10, top=244)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        for i, stat in enumerate(stat_list):
            first_letter = stat[0].upper()
            rest_of_letters = stat[1:]
            if stat in magic_health_list:
                current = self.stats[stat]['current']
                max = self.stats[stat]['maximum']
                text = "{}{}: {}/{}".format(first_letter, rest_of_letters, current, max)
            elif stat == 'GOLD':
                text = "Gold: {}".format(self.inventory[stat]['quantity'])
            render = self.small_font.render(text, True, c.NEAR_BLACK)
            x = 26
            y = 45 + (i*30)
            text_rect = render.get_rect(x=x,
                                        centery=y)
            surface.blit(render, text_rect)

        if self.game_data['crown quest']:
            crown = setup.GFX['crown']
            crown_rect = crown.get_rect(x=178, y=40)
            surface.blit(crown, crown_rect)
        
        return surface, rect

    def update(self):
        """
        Update gold.
        """
        self.image, self.rect = self.make_image()

    def draw(self, surface):
        """
        Draw to surface.
        """
        surface.blit(self.image, self.rect)


class InfoBox(pg.sprite.Sprite):
    def __init__(self, inventory, player_stats):
        super(InfoBox, self).__init__()
        self.inventory = inventory
        self.player_stats = player_stats
        self.attack_power = self.get_attack_power()
        self.defense_power = self.get_defense_power()
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
        self.state = 'invisible'
        self.state_dict = self.make_state_dict()
        self.print_slots = True

    def get_attack_power(self):
        """
        Calculate the current attack power based on equipped weapons.
        """
        weapon = self.inventory['equipped weapon']
        return self.inventory[weapon]['power']

    def get_defense_power(self):
        """
        Calculate the current defense power based on equipped weapons.
        """
        defense_power = 0
        for armor in self.inventory['equipped armor']:
            defense_power += self.inventory[armor]['power']

        return defense_power

    def make_state_dict(self):
        """Make the dictionary of state methods"""
        state_dict = {'stats': self.show_player_stats,
                      'items': self.show_items,
                      'magic': self.show_magic,
                      'invisible': self.show_nothing}

        return state_dict


    def show_player_stats(self):
        """Show the player's main stats"""
        title = 'STATS'
        stat_list = ['Level', 'experience to next level',
                     'health', 'magic', 'Attack Power', 
                     'Defense Power', 'gold']
        attack_power = 5
        surface, rect = self.make_blank_info_box(title)

        for i, stat in enumerate(stat_list):
            if stat == 'health' or stat == 'magic':
                text = "{}{}: {} / {}".format(stat[0].upper(),
                                              stat[1:],
                                              str(self.player_stats[stat]['current']),
                                              str(self.player_stats[stat]['maximum']))
            elif stat == 'experience to next level':
                text = "{}{}: {}".format(stat[0].upper(),
                                         stat[1:],
                                         self.player_stats[stat])
            elif stat == 'Attack Power':
				text = "{}: {}".format(stat, self.get_attack_power()) 
            elif stat == 'Defense Power':
                text = "{}: {}".format(stat, self.get_defense_power())
            elif stat == 'gold':
                text = "Gold: {}".format(self.inventory['GOLD']['quantity'])
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
                if item == self.inventory['equipped weapon']:
                    item += " (E)"
                weapons.append(item)
            elif item in self.possible_armor:
                if item in self.inventory['equipped armor']:
                    item += " (E)"
                armor.append(item)
            elif item in self.possible_potions:
                potions.append(item)

        self.slots = {}
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


    def assign_slots(self, item_list, starty, weapon_or_armor=False):
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

    def assign_magic_slots(self, magic_list, starty):
        """
        Assign each magic spell to a slot in the menu.
        """
        for i, spell in enumerate(magic_list):
            posx = 120
            posy = starty + (i * 50)
            self.slots[(posx, posy)] = spell

    def blit_item_lists(self, surface):
        """Blit item list to info box surface"""
        for coord in self.slots:
            item = self.slots[coord]

            if item in self.possible_potions:
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

        self.slots = {}
        self.assign_magic_slots(item_list, 80)

        surface, rect = self.make_blank_info_box(title)

        for i, item in enumerate(item_list):
            text_image = self.font.render(item, True, c.NEAR_BLACK)
            text_rect = text_image.get_rect(x=100, y=80+(i*50))
            surface.blit(text_image, text_rect)

        self.image = surface
        self.rect = rect

    def show_nothing(self):
        """
        Show nothing when the menu is opened from a level.
        """
        self.image = pg.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.image.fill(c.BLACK_BLUE)

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
        choices = ['Items', 'Magic', 'Stats']
        image = setup.GFX['goldbox']
        rect = image.get_rect(left=10, top=425)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        for i, choice in enumerate(choices):
            choice_image = self.font.render(choice, True, c.NEAR_BLACK)
            choice_rect = choice_image.get_rect(x=100, y=(15 + (i * 45)))
            surface.blit(choice_image, choice_rect)

        return surface, rect

    def draw(self, surface):
        """Draw to surface"""
        surface.blit(self.image, self.rect)


class MenuGui(object):
    def __init__(self, level, inventory, stats):
        self.level = level
        self.game_data = self.level.game_data
        self.sfx_observer = observer.SoundEffects()
        self.observers = [self.sfx_observer]
        self.inventory = inventory
        self.stats = stats
        self.info_box = InfoBox(inventory, stats)
        self.gold_box = QuickStats(self.game_data)
        self.selection_box = SelectionBox()
        self.arrow = SmallArrow(self.info_box)
        self.arrow_index = 0
        self.allow_input = False

    def check_for_input(self, keys):
        """Check for input"""
        if self.allow_input:
            if keys[pg.K_DOWN]:
                if self.arrow_index < len(self.arrow.pos_list) - 1:
                    self.notify(c.CLICK)
                    self.arrow_index += 1
                    self.allow_input = False
            elif keys[pg.K_UP]:
                if self.arrow_index > 0:
                    self.notify(c.CLICK)
                    self.arrow_index -= 1
                    self.allow_input = False
            elif keys[pg.K_RIGHT]:
                if self.info_box.state == 'items':
                    if not self.arrow.state == 'itemsubmenu':
                        self.notify(c.CLICK)
                        self.arrow_index = 0
                    self.arrow.state = 'itemsubmenu'
                elif self.info_box.state == 'magic':
                    if not self.arrow.state == 'magicsubmenu':
                        self.notify(c.CLICK)
                        self.arrow_index = 0
                    self.arrow.state = 'magicsubmenu'
                self.allow_input = False

            elif keys[pg.K_LEFT]:
                self.notify(c.CLICK)
                self.arrow.state = 'selectmenu'
                self.arrow_index = 0
                self.allow_input = False
            elif keys[pg.K_SPACE]:
                self.notify(c.CLICK2)
                if self.arrow.state == 'selectmenu':
                    if self.arrow_index == 0:
                        self.info_box.state = 'items'
                        self.arrow.state = 'itemsubmenu'
                        self.arrow_index = 0
                    elif self.arrow_index == 1:
                        self.info_box.state = 'magic'
                        self.arrow.state = 'magicsubmenu'
                        self.arrow_index = 0
                    elif self.arrow_index == 2:
                        self.info_box.state = 'stats'
                elif self.arrow.state == 'itemsubmenu':
                    self.select_item()
                elif self.arrow.state == 'magicsubmenu':
                    self.select_magic()

                self.allow_input = False
            elif keys[pg.K_RETURN]:
                self.level.state = 'normal'
                self.info_box.state = 'invisible'
                self.allow_input = False
                self.arrow_index = 0
                self.arrow.state = 'selectmenu'

        if (not keys[pg.K_DOWN]
                and not keys[pg.K_UP]
                and not keys[pg.K_RETURN]
                and not keys[pg.K_SPACE]
                and not keys[pg.K_RIGHT]
                and not keys[pg.K_LEFT]):
            self.allow_input = True

    def notify(self, event):
        """
        Notify all observers of event.
        """
        for observer in self.observers:
            observer.on_notify(event)

    def select_item(self):
        """
        Select item from item menu.
        """
        health = self.game_data['player stats']['health']
        posx = self.arrow.rect.x - 220
        posy = self.arrow.rect.y - 38

        if (posx, posy) in self.info_box.slots:
            if self.info_box.slots[(posx, posy)][:7] == 'Healing':
                potion = 'Healing Potion'
                value = 30
                self.drink_potion(potion, health, value)
            elif self.info_box.slots[(posx, posy)][:5] == 'Ether':
                potion = 'Ether Potion'
                stat = self.game_data['player stats']['magic']
                value = 30
                self.drink_potion(potion, stat, value)
            elif self.info_box.slots[(posx, posy)][:10] == 'Long Sword':
                self.inventory['equipped weapon'] = 'Long Sword'
            elif self.info_box.slots[(posx, posy)][:6] == 'Rapier':
                self.inventory['equipped weapon'] = 'Rapier'
            elif self.info_box.slots[(posx, posy)][:13] == 'Wooden Shield':
                if 'Wooden Shield' in self.inventory['equipped armor']:
                    self.inventory['equipped armor'].remove('Wooden Shield')
                else:
                    self.inventory['equipped armor'].append('Wooden Shield')
            elif self.info_box.slots[(posx, posy)][:10] == 'Chain Mail':
                if 'Chain Mail' in self.inventory['equipped armor']:
                    self.inventory['equipped armor'].remove('Chain Mail')
                else:
                    self.inventory['equipped armor'].append('Chain Mail')

    def select_magic(self):
        """
        Select spell from magic menu.
        """
        health = self.game_data['player stats']['health']
        magic = self.game_data['player stats']['magic']
        posx = self.arrow.rect.x - 190
        posy = self.arrow.rect.y - 39

        if (posx, posy) in self.info_box.slots:
            if self.info_box.slots[(posx, posy)][:4] == 'Cure':
               self.use_cure_spell()

    def use_cure_spell(self):
        """
        Use cure spell to heal player.
        """
        health = self.game_data['player stats']['health']
        magic = self.game_data['player stats']['magic']
        inventory = self.game_data['player inventory']

        if health['current'] != health['maximum']:
            if magic['current'] >= inventory['Cure']['magic points']:
                self.notify(c.POWERUP)
                magic['current'] -= inventory['Cure']['magic points']
                health['current'] += inventory['Cure']['power']
                if health['current'] > health['maximum']:
                    health['current'] = health['maximum']

    def drink_potion(self, potion, stat, value):
        """
        Drink potion and change player stats.
        """
        if stat['current'] != stat['maximum']:
            self.notify(c.POWERUP)
            self.inventory[potion]['quantity'] -= 1
            stat['current'] += value
            if stat['current'] > stat['maximum']:
                stat['current'] = stat['maximum']
            if not self.inventory[potion]['quantity']:
                del self.inventory[potion]

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
