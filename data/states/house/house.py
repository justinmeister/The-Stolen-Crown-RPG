"""This is the house on the lower left hand
corner of the town.  Most of its functionality is inherited
from the level_state.py module.  Most of the level data is contained
in the tilemap .txt files in this state's directory.  Essentially the
only purpose of house.py is to assign dialogue to each sprite.
"""


from .. import level_state
from ... import constants as c

class House(level_state.LevelState):
    def __init__(self):
        super(House, self).__init__()
        self.name = c.HOUSE
        self.map_width = 25
        self.map_height = 19

    def set_sprite_dialogue(self):
        """Sets unique dialogue for each sprite"""
        for sprite in self.sprites:
            if sprite.location == [14, 6]:
                sprite.dialogue = ["There are evil forces encroaching on our town.",
                                   "Trust no one and you may leave these lands alive."]
