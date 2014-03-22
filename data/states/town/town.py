"""This is town state.  Most of its functionality is inherited from
the level_state.py module.  Most of the level data is contained in
the tilemap .txt files in this state's directory.  Essentially the
only purpose of town.py is to assign dialogue to each sprite
"""

from .. import level_state
from ... import constants as c

class Town(level_state.LevelState):
    def __init__(self):
        super(Town, self).__init__()
        self.name = c.TOWN
        self.map_width = 25
        self.map_height = 50

    def set_sprite_dialogue(self):
        """Sets unique dialogue for each sprite"""
        for sprite in self.sprites:
            if sprite.location == [9, 46]:
                sprite.dialogue = ['Welcome to our town, Mr. Traveller!',
                                   'The King is loved by all!',
                                   'You should go visit him in his castle.']
            elif sprite.location == [15, 41]:
                sprite.dialogue = ['You seem tired, why not rest at our Inn?']
                sprite.begin_auto_resting()
            elif sprite.location == [13, 13]:
                sprite.dialogue = ['Be careful. There are monsters surrounding our town.',
                                   'Make sure to equip sufficient armour and weapons.',
                                   'Spells and potions are useful too.']
            elif sprite.location == [10, 13]:
                sprite.dialogue = ['I have heard rumours that the King has lost something...',
                                   'Perhaps you should pay him a visit.']
            elif sprite.location == [10, 7]:
                sprite.dialogue = ['Welcome to the castle, citizen.']
            elif sprite.location == [13, 7]:
                sprite.dialogue = ['Move along.']

