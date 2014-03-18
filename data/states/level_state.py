__author__ = 'justinarmstrong'
"""
This is the base class all level states (i.e. states
where the player can move around the screen) inherit
from.  This class inherits from the generic state class
found in the tools.py module.
"""

import copy
import pygame as pg
from .. import tools, collision
from .. import tilemap as tm
from .. components import person, textbox


class LevelState(tools._State):
    def __init__(self, name, width, height):
        super(LevelState, self).__init__(name)
        self.map_width = width
        self.map_height = height


    def startup(self, current_time, persist):
        """Called when the State object is created"""
        self.persist = persist
        self.current_time = current_time
        self.state = 'normal'
        self.town_map = tm.create_town_map(self.name,
                                           self.map_width,
                                           self.map_height)
        self.viewport = tm.create_viewport(self.town_map)
        self.blockers = tm.create_blockers(self.name)
        self.level_surface = tm.create_level_surface(self.town_map)
        self.level_rect = self.level_surface.get_rect()
        self.player = person.Player(persist['last direction'])
        self.level_sprites = pg.sprite.Group()
        self.start_positions = tm.set_sprite_positions(self.player,
                                                       self.level_sprites,
                                                       self.name,
                                                       self.persist)
        self.set_sprite_dialogue()
        self.collision_handler = collision.CollisionHandler(self.player,
                                                            self.blockers,
                                                            self.level_sprites)
        self.dialogue_handler = textbox.DialogueHandler(self.player,
                                                        self.level_sprites,
                                                        self)
        self.state_dict = self.make_state_dict()
        self.portals = tm.make_level_portals(self.name)
        self.parent_level = None


    def set_sprite_dialogue(self):
        """Sets unique dialogue for each sprite"""
        raise NotImplementedError


    def make_state_dict(self):
        """Make a dictionary of states the level can be in"""
        state_dict = {'normal': self.running_normally,
                      'dialogue': self.handling_dialogue}

        return state_dict


    def running_normally(self, surface, keys, current_time):
        """Update level normally"""
        self.check_for_dialogue()
        self.check_for_portals()
        self.player.update(keys, current_time)
        self.level_sprites.update(current_time)
        self.collision_handler.update(keys, current_time)
        self.dialogue_handler.update(keys, current_time)
        self.viewport_update()

        self.draw_level(surface)


    def check_for_portals(self):
        """Check if the player walks into a door, requiring a level change"""
        portal = pg.sprite.spritecollideany(self.player, self.portals)

        if portal and self.player.state == 'resting':
            self.player.location = self.player.get_tile_location()
            self.next = portal.name
            self.update_game_data()
            self.done = True


    def update_game_data(self):
        """Update the persistant game data dictionary"""
        self.persist['last location'] = self.player.location
        self.persist['last direction'] = self.player.direction
        self.persist['last state'] = self.name

        self.set_new_start_pos()


    def set_new_start_pos(self):
        """Set new start position based on previous state"""
        location = copy.deepcopy(self.persist['last location'])
        direction = self.persist['last direction']
        state = self.persist['last state']

        if direction == 'up':
            location[1] += 1
        elif direction == 'down':
            location[1] -= 1
        elif direction == 'left':
            location[0] += 1
        elif direction == 'right':
            location[0] -= 1

        self.persist[state + ' start pos'] = location






    def handling_dialogue(self, surface, keys, current_time):
        """Update only dialogue boxes"""
        self.dialogue_handler.update(keys, current_time)
        self.draw_level(surface)


    def check_for_dialogue(self):
        """Check if the level needs to freeze"""
        if self.dialogue_handler.textbox:
            self.state = 'dialogue'


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
        self.level_sprites.draw(self.level_surface)

        surface.blit(self.level_surface, (0, 0), self.viewport)
        self.dialogue_handler.draw(surface)















