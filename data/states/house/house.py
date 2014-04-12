"""This is the house on the lower left hand
corner of the town.  Most of its functionality is inherited
from the level_state.py module.  Most of the level data is contained
in the tilemap .txt files in this state's directory.  Essentially the
only purpose of house.py is to assign dialogue to each sprite.
"""


from .. import level_state
from ... import constants as c
from ... import setup

class House(level_state.LevelState):
    def __init__(self):
        super(House, self).__init__()
        self.name = c.HOUSE
        self.tmx_map = setup.TMX['house']

    def set_sprite_dialogue(self):
        """Sets unique dialogue for each sprite"""
        for sprite in self.sprites:
            if sprite.location == [14, 6]:
                sprite.dialogue = ["I am very sick.   cough... cough...",
                                   "Only an ELIXIR can help me.",
                                   "Please go to my brother and obtain one for me.",
                                   "He lives in a house on the NorthEast shores.",
                                   "I will be forever in your debt."]
