"""This is the castle state.  Most of its functionality is inherited
from the level_state.py module.  Most of the level data is contained
in the tilemap .txt files in this state's directory.  Essentially the
only purpose of castle.py is to assign dialogue to each sprite.
"""

from .. import level_state

class Castle(level_state.LevelState):
    def __init__(self, name):
        super(Castle, self).__init__(name)

    def set_sprite_dialogue(self):
        """Sets unique dialogue for each sprite"""
        return None