"""This is the house on the lower left hand
corner of the town.  Most of its functionality is inherited
from the level_state.py module.  Most of the level data is contained
in the tilemap .txt files in this state's directory.  Essentially the
only purpose of house.py is to assign dialogue to each sprite.
"""


from .. import levels
from ... import constants as c

class House(levels.LevelState):
    def __init__(self):
        super(House, self).__init__()
        self.name = c.BROTHER_HOUSE
        self.map_width = 25
        self.map_height = 19

    def set_sprite_dialogue(self):
        """Sets unique dialogue for each sprite"""
        for sprite in self.sprites:
            if sprite.location == [9, 6]:
                sprite.dialogue = ["My brother is sick?!?",
                                   "I haven't seen him in years.  I had no idea he was not well.",
                                   "Quick, take this ELIXIR to him immediately."]
                sprite.item = self.game_data['old man item']
