"""
This class is the parent class of all shop states.
This includes weapon, armour, magic and potion shops.
It also includes the inn.  These states are scaled
twice as big as a level state.
"""

import pygame as pg
from .. import tools
from .. import tilemap as tm
from .. components import person, textbox


class Shop(tools._State):
    """Basic shop state"""
    def __init__(self, name):
        super(Shop, self).__init__(name)
        self.map_width = 13
        self.map_height = 10

    def startup(self, current_time, persist):
        """Startup state"""
        self.persist = persist
        self.current_time = current_time
        self.state = 'normal'
        self.level_map = tm.make_level_map(self.name,
                                           self.map_width,
                                           self.map_height)
        self.level_surface = tm.make_level_surface(self.level_map)
        self.level_rect = self.level_surface.get_rect()
        self.player = person.Player('right')
        self.shop_owner = self.make_shop_owner()


        self.dialogue_handler = textbox.DialogueHandler(self.player,
                                                        self.shop_owner,
                                                        self)


    def make_shop_owner(self):
        """Make the shop owner sprite"""
        return None


    def update(self, surface, keys, current_time):
        """Update level state"""
        pass
