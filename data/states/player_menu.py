"""
This is the state where the player can look at
his inventory, equip items and check stats.
"""
import pygame as pg
from .. import tools, setup, menugui
from .. import constants as c


class Player_Menu(tools._State):
    def __init__(self):
        super(Player_Menu, self).__init__()
        self.get_image = tools.get_image



    def startup(self, current_time, game_data):
        """Call when state is switched to"""
        inventory = game_data['player inventory']
        stats = game_data['player stats']
        self.next = game_data['last state']
        self.allow_input = False
        self.game_data = game_data
        self.current_time = current_time
        self.background = self.make_background()
        self.gui = menugui.MenuGui(self, inventory, stats)


    def make_background(self):
        """Makes the generic black/blue background"""
        background = pg.sprite.Sprite()
        surface = pg.Surface(c.SCREEN_SIZE).convert()
        surface.fill(c.BLACK_BLUE)
        background.image = surface
        background.rect = background.image.get_rect()

        player = self.make_sprite('player', 96, 32)

        background.image.blit(player.image, player.rect)

        return background


    def make_sprite(self, key, coordx, coordy, x=40, y=25):
        """Get the image for the player"""
        spritesheet = setup.GFX[key]
        surface = pg.Surface((32, 32))
        surface.set_colorkey(c.BLACK)
        image = self.get_image(coordx, coordy, 32, 32, spritesheet)
        rect = image.get_rect()
        surface.blit(image, rect)

        surface = pg.transform.scale(surface, (192, 192))
        rect = surface.get_rect(left=x, top=y)
        sprite = pg.sprite.Sprite()
        sprite.image = surface
        sprite.rect = rect

        return sprite


    def update(self, surface, keys, current_time):
        self.gui.update(keys)
        self.draw(surface)


    def draw(self, surface):
        surface.blit(self.background.image, self.background.rect)
        self.gui.draw(surface)

