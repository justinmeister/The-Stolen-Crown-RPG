"""
This is the state where the player can look at
his inventory, equip items and check stats.
Most of the logic is in menugui.MenuGUI()
"""
import pygame as pg
from .. import tools, setup, menugui
from .. import constants as c


class Player_Menu(object):
    def __init__(self, game_data, level):
        inventory = game_data['player inventory']
        stats = game_data['player stats']
        self.get_image = tools.get_image
        self.allow_input = False
        self.background = self.make_background()
        self.gui = menugui.MenuGui(level, inventory, stats)

    def make_background(self):
        """
        Makes the generic black/blue background.
        """
        background = pg.sprite.Sprite()
        surface = pg.Surface(c.SCREEN_SIZE).convert()
        surface.fill(c.BLACK_BLUE)
        background.image = surface
        background.rect = background.image.get_rect()

        player = self.make_sprite('player', 96, 32)

        background.image.blit(player.image, player.rect)

        return background

    def make_sprite(self, key, coordx, coordy, x=40, y=25):
        """
        Get the image for the player.
        """
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

    def update(self, surface, keys):
        self.gui.update(keys)
        self.draw(surface)

    def draw(self, surface):
        surface.blit(self.background.image, self.background.rect)
        self.gui.draw(surface)

