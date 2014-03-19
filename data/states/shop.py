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
        self.background = self.make_background()
        self.player = None
        self.sprites = None
        self.text_handler = textbox.TextHandler(self)
        self.make_greeting_text()


    def make_background(self):
        """Make the level surface"""
        background = pg.sprite.Sprite()
        surface = pg.Surface(c.SCREEN_SIZE).convert()
        surface.fill(c.BLACK_BLUE)
        background.image = surface
        background.rect = background.image.get_rect()

        player = self.make_sprite('player', 96, 32, 150)
        shop_owner = self.make_sprite('man1', 32, 32, 600)
        counter = self.make_counter()

        background.image.blit(player.image, player.rect)
        background.image.blit(shop_owner.image, shop_owner.rect)
        background.image.blit(counter.image, counter.rect)

        return background


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


    def make_greeting_text(self):
        """Make the textbox for the shop owner's greeting"""
        dialogue = ["Welcome to the " + self.name + "!",
                    "Would you like to spend 30 gold on a room tonight?"]
        textbox = self.text_handler.make_textbox('dialoguebox', dialogue)

        self.text_handler.textbox = textbox


    def make_counter(self):
        """Make the counter to conduct business"""
        sprite_sheet = copy.copy(setup.GFX['house'])
        sprite = pg.sprite.Sprite()
        sprite.image = self.get_image(102, 64, 26, 82, sprite_sheet)
        sprite.image = pg.transform.scale2x(sprite.image)
        sprite.rect = sprite.image.get_rect(left=550, top=225)

        return sprite


    def update(self, surface, keys, current_time):
        """Update level state"""
        self.text_handler.update_for_shops(keys, current_time)
        self.draw_level(surface)


    def draw_level(self, surface):
        """Blit graphics to game surface"""
        surface.blit(self.background.image, self.background.rect)
        self.text_handler.draw(surface)