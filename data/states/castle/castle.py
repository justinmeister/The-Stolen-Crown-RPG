"""This is the castle state.  Most of its functionality is inherited
from the level_state.py module.  Most of the level data is contained
in the tilemap .txt files in this state's directory.  Essentially the
only purpose of castle.py is to assign dialogue to each sprite.
"""

from .. import level_state
from ... import constants as c

class Castle(level_state.LevelState):
    def __init__(self, name, width, height):
        super(Castle, self).__init__(name, width, height)
        self.parent_level = c.TOWN

    def set_sprite_dialogue(self):
        """Sets unique dialogue for each sprite"""
        for sprite in self.level_sprites:
            if sprite.location == [12, 6]:
                sprite.dialogue = ["Please!  You must help me!",
                                   "An evil sorceror has stolen my magic crown!",
                                   "Without it, our town will be overun by monsters!",
                                   "Take this money for supplies.",
                                   "Our town's fate is in your hands!"]
                sprite.item = self.persist['king item']
            else:
                sprite.dialogue = ['Hail to the King!']