"""This is town state.  Most of its functionality is inherited from
the level_state.py module.  Most of the level data is contained in
the tilemap .txt files in this state's directory.  Essentially the
only purpose of town.py is to assign dialogue to each sprite
"""

from .. import level_state
from ... import constants as c
from ... import setup

class Town(level_state.LevelState):
    def __init__(self):
        super(Town, self).__init__()
        self.name = c.TOWN
        self.tmx_map = setup.TMX['town']


    def set_sprite_dialogue(self):
        """Sets unique dialogue for each sprite"""
        for sprite in self.sprites:
            if sprite.location == [9, 46]:
                sprite.dialogue = ['Welcome to our town, traveller!',
                                   'Our King protects us against the evil forces of the outside world.',
                                   'As long as we never leave, we have nothing to fear!']
            elif sprite.location == [15, 41]:
                sprite.dialogue = ['You seem tired from your travels.',
                                   'Why not rest at our Inn and stay awhile?']
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
                sprite.dialogue = ['Only those given special permission by the King can leave this town.',
                                   'It is for our own good, as few could survive in the outside world.']
            elif sprite.location == [18, 27]:
                sprite.dialogue = ["Don't be frightened. I'm a friendly Demon.",
                                   "My brothers and sisters, however, are not so nice.",
                                   "Be careful not to run into them."]

