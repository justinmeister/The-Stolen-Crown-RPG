__author__ = 'justinarmstrong'

import pygame as pg
from .. import tools, collision
from .. import tilemap as tm
from ..components import person, textbox


class Town(tools._State):
    def __init__(self):
        super(Town, self).__init__()


    def startup(self, current_time, persist):
        """Called when the State object is created"""
        self.persist = persist
        self.current_time = current_time
        self.town_map = tm.create_town_map()
        self.viewport = tm.create_viewport(self.town_map)
        self.blockers = tm.create_blockers()
        self.level_surface = tm.create_level_surface(self.town_map)
        self.level_rect = self.level_surface.get_rect()
        self.player = person.Player('up')
        self.town_sprites = pg.sprite.Group()
        self.start_positions = tm.set_sprite_positions(self.player,
                                                       self.town_sprites)
        self.collision_handler = collision.CollisionHandler(self.player,
                                                            self.blockers,
                                                            self.town_sprites)
        self.textbox_group = pg.sprite.Group()
        self.dialogue_handler = textbox.DialogueHandler(self.player,
                                                        self.town_sprites,
                                                        self.textbox_group)


    def update(self, surface, keys, current_time):
        """Updates state"""
        self.keys = keys
        self.current_time = current_time
        self.player.update(keys, current_time)
        self.collision_handler.update()
        self.update_viewport()
        self.dialogue_handler.update(keys, current_time)

        self.draw_level(surface)


    def draw_level(self, surface):
        """Blits all images to screen"""
        self.level_surface.blit(self.town_map['surface'], self.viewport, self.viewport)
        self.level_surface.blit(self.player.image, self.player.rect)
        self.town_sprites.draw(self.level_surface)

        surface.blit(self.level_surface, (0, 0), self.viewport)
        self.textbox_group.draw(surface)


    def update_viewport(self):
        """Viewport stays centered on character, unless at edge of map"""
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.level_rect)










