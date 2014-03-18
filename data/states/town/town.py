"""This is town state.  Most of its functionality is inherited from
the level_state.py module.  Most of the level data is contained in
the tilemap .txt files in this state's directory.  Essentially the
only purpose of town.py is to assign dialogue to each sprite
"""

from .. import level_state

class Town(level_state.LevelState):
    def __init__(self, name):
        super(Town, self).__init__(name)

    def set_sprite_dialogue(self):
        """Sets unique dialogue for each sprite"""
        for sprite in self.town_sprites:
            if sprite.location == (10, 47):
                sprite.dialogue = ['Welcome to our town, Mr. Traveller!',
                                   'The King is loved by all!',
                                   'You should go visit him in his castle.']
            elif sprite.location == (16, 42):
                sprite.dialogue = ['You seem tired, why not rest at our Inn?']
                sprite.begin_auto_resting()
            elif sprite.location == (14, 14):
                sprite.dialogue = ['Be careful. There are monsters surrounding our town.',
                                   'Make sure to equip sufficient armour and weapons.',
                                   'Spells and potions are useful too.']
            elif sprite.location == (11, 14):
                sprite.dialogue = ['I have heard rumours that the King has lost something...',
                                   'Perhaps you should pay him a visit.']
            elif sprite.location == (11, 8):
                sprite.dialogue = ['Welcome to the castle, citizen.']
            elif sprite.location == (14, 8):
                sprite.dialogue = ['Move along.']

