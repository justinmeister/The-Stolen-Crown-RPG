__author__ = 'justinarmstrong'
import random
import pygame as pg
from .. import setup
from .. import constants as c

class Dialogue(pg.sprite.Sprite):
    """Text box used for dialogue"""
    def __init__(self, x, dialogue):
        super(Dialogue, self).__init__()
        self.image = setup.GFX['dialoguebox']
        self.rect = self.image.get_rect(centerx=x)
        self.timer = 0.0
        self.font = pg.font.Font(setup.FONTS['Fixedsys500c'], 20)
        self.dialogue_image = self.font.render(dialogue, True,  c.BLACK)
        self.dialogue_rect = self.dialogue_image.get_rect(left=50, top=50)
        self.image.blit(self.dialogue_image, self.dialogue_rect)

    def update(self, current_time):
        """Updates scrolling text"""
        self.current_time = current_time
        self.animate_dialogue()
        self.terminate_check()


    def animate_dialogue(self):
        """Reveal dialogue on textbox"""
        text_image = self.dialogue_image
        text_rect = self.dialogue_rect

        self.image.blit(text_image, text_rect)


    def terminate_check(self):
        """Remove textbox from sprite group after 2 seconds"""

        if self.timer == 0.0:
            self.timer = self.current_time
        elif (self.current_time - self.timer) > 2000:
            self.kill()


class DialogueHandler(object):
    """Handles interaction between sprites to create dialogue boxes"""

    def __init__(self, player, sprites, textbox_group):
        self.player = player
        self.sprites = sprites
        self.textbox_group = textbox_group
        self.textbox_onscreen = False
        self.image_list = []


    def update(self, keys, current_time):
        """Checks for the creation of Dialogue boxes"""
        if keys[pg.K_SPACE] and not self.textbox_onscreen:
            for sprite in self.sprites:
                self.check_for_dialogue(sprite)

        self.textbox_group.update(current_time)

        if len(self.textbox_group) < 1:
            self.textbox_onscreen = False

        assert(len(self.textbox_group) < 2)



    def check_for_dialogue(self, sprite):
        """Checks if a sprite is in the correct location to give dialogue"""
        player = self.player
        tile_x, tile_y = player.location

        if player.direction == 'up':
            if sprite.location == (tile_x, tile_y - 1):
                self.textbox_group.add(Dialogue(400, sprite.dialogue))
                self.textbox_onscreen = True
        elif player.direction == 'down':
            if sprite.location == (tile_x, tile_y + 1):
                self.textbox_group.add(Dialogue(400, sprite.dialogue))
                self.textbox_onscreen = True
        elif player.direction == 'left':
            if sprite.location == (tile_x - 1, tile_y):
                self.textbox_group.add(Dialogue(400, sprite.dialogue))
                self.textbox_onscreen = True
        elif player.direction == 'right':
            if sprite.location == (tile_x + 1, tile_y):
                self.textbox_group.add(Dialogue(400, sprite.dialogue))
                self.textbox_onscreen = True







