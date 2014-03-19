"""
This class is the parent class of all shop states.
This includes weapon, armour, magic and potion shops.
It also includes the inn.  These states are scaled
twice as big as a level state.
"""
import copy
import pygame as pg
from .. import tools, setup
from .. import constants as c
from .. components import person, textbox


class Shop(tools._State):
    """Basic shop state"""
    def __init__(self, name):
        super(Shop, self).__init__(name)
        self.map_width = 13
        self.map_height = 10

    def startup(self, current_time, persist):
        """Startup state"""
        self.persist = persist
        self.current_time = current_time
        self.state = 'normal'
        self.get_image = tools.get_image
        self.level_surface = pg.Surface(c.SCREEN_SIZE).convert()
        self.level_surface.fill(c.BLACK_BLUE)
        self.level_rect = self.level_surface.get_rect()
        self.player = self.make_sprite('player', 96, 32, 100)
        self.shop_owner = self.make_sprite('man1', 32, 32, 600)


        self.dialogue_handler = textbox.DialogueHandler(self.player,
                                                        self.shop_owner,
                                                        self)


    def make_sprite(self, key, coordx, coordy, x, y=304):
        """Get the image for the player"""
        spritesheet = setup.GFX[key]
        surface = pg.Surface((32, 32))
        surface.set_colorkey(c.BLACK)
        image = self.get_image(coordx, coordy, 32, 32, spritesheet)
        rect = image.get_rect()
        surface.blit(image, rect)

        surface = pg.transform.scale(surface, (96, 96))
        rect = surface.get_rect(left=x, centery=y)
        sprite = pg.sprite.Sprite()
        sprite.image = surface
        sprite.rect = rect

        return sprite


    def make_shop_owner(self):
        """Make the shop owner sprite"""
        return None


    def update(self, surface, keys, current_time):
        """Update level state"""
        self.draw_level(surface)


    def draw_level(self, surface):
        """Blit graphics to game surface"""
        surface.blit(self.level_surface, self.level_rect)
        surface.blit(self.player.image, self.player.rect)
        surface.blit(self.shop_owner.image, self.shop_owner.rect)
