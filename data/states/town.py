__author__ = 'justinarmstrong'

import pygame as pg
from .. import tools, collision
from .. import tilemap as tm
from .. components import person, textbox



class Town(tools._State):
    def __init__(self):
        super(Town, self).__init__()


    def startup(self, current_time, persist):
        """Called when the State object is created"""
        self.persist = persist
        self.current_time = current_time
        self.state = 'normal'
        self.town_map = tm.create_town_map()
        self.viewport = tm.create_viewport(self.town_map)
        self.blockers = tm.create_blockers()
        self.level_surface = tm.create_level_surface(self.town_map)
        self.level_rect = self.level_surface.get_rect()
        self.player = person.Player('up')
        self.town_sprites = pg.sprite.Group()
        self.start_positions = tm.set_sprite_positions(self.player,
                                                       self.town_sprites)
        self.set_sprite_dialogue()
        self.collision_handler = collision.CollisionHandler(self.player,
                                                            self.blockers,
                                                            self.town_sprites)
        self.dialogue_handler = textbox.DialogueHandler(self.player,
                                                        self.town_sprites,
                                                        self)
        self.state_dict = self.make_state_dict()


    def set_sprite_dialogue(self):
        """Sets unique dialogue for each sprite"""
        for sprite in self.town_sprites:
            if sprite.location == (10, 47):
                sprite.dialogue = 'Welcome to our town, Mr. Traveller!'
            elif sprite.location == (16, 42):
                sprite.dialogue = 'You seem tired, why not rest at our Inn?'
                sprite.begin_auto_resting()
            elif sprite.location == (14, 14):
                sprite.dialogue = 'Welcome to the castle, citizen.'
            elif sprite.location == (11, 14):
                sprite.dialogue = 'I have heard rumours that the King has lost something...'
            elif sprite.location == (11, 8):
                sprite.dialogue = 'Be careful. There are monsters surrounding our town.'
            elif sprite.location == (14, 8):
                sprite.dialogue = 'Move along, citizen.'


    def make_state_dict(self):
        """Make a dictionary of states the level can be in"""
        state_dict = {'normal': self.running_normally,
                      'dialogue': self.handling_dialogue}

        return state_dict


    def running_normally(self, surface, keys, current_time):
        """Update level normally"""
        self.player.update(keys, current_time)
        self.town_sprites.update(current_time)
        self.collision_handler.update(keys, current_time)
        self.dialogue_handler.update(keys, current_time)
        self.viewport_update()

        self.draw_level(surface)


    def handling_dialogue(self, surface, keys, current_time):
        """Update only dialogue boxes"""
        self.dialogue_handler.update(keys, current_time)
        self.draw_level(surface)


    def update(self, surface, keys, current_time):
        """Updates state"""
        state_function = self.state_dict[self.state]
        state_function(surface, keys, current_time)


    def viewport_update(self):
        """Viewport stays centered on character, unless at edge of map"""
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.level_rect)


    def draw_level(self, surface):
        """Blits all images to screen"""
        self.level_surface.blit(self.town_map['surface'], self.viewport, self.viewport)
        self.level_surface.blit(self.player.image, self.player.rect)
        self.town_sprites.draw(self.level_surface)

        surface.blit(self.level_surface, (0, 0), self.viewport)
        self.dialogue_handler.draw(surface)


    def get_event(self, event):
        """Set event to level attribute"""
        self.event = event













