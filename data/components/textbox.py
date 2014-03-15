__author__ = 'justinarmstrong'
import pygame as pg
from .. import setup
from .. import constants as c

class DialogueBox(object):
    """Text box used for dialogue"""
    def __init__(self, x, dialogue):
        self.bground = setup.GFX['dialoguebox']
        self.rect = self.bground.get_rect(centerx=x)
        self.image = pg.Surface(self.rect.size)
        self.image.set_colorkey(c.BLACK)
        self.image.blit(self.bground, (0, 0))
        self.timer = 0.0
        self.font = pg.font.Font(setup.FONTS['Fixedsys500c'], 22)
        self.dialogue_image = self.font.render(dialogue, False,  c.NEAR_BLACK)
        self.dialogue_rect = self.dialogue_image.get_rect(left=50, top=50)
        self.image.blit(self.dialogue_image, self.dialogue_rect)
        self.done = False
        self.arrow_image = setup.GFX['rightarrow']
        self.arrow_rect = self.arrow_image.get_rect(right=self.rect.right - 20,
                                                    bottom=self.rect.bottom - 10)
        self.image.blit(self.arrow_image, self.arrow_rect)

    def update(self, current_time, keys):
        """Updates scrolling text"""
        self.current_time = current_time
        self.animate_dialogue()
        self.terminate_check(keys)


    def animate_dialogue(self):
        """Reveal dialogue on textbox"""
        text_image = self.dialogue_image
        text_rect = self.dialogue_rect

        self.image.blit(text_image, text_rect)


    def terminate_check(self, keys):
        """Remove textbox from sprite group after 2 seconds"""

        if self.timer == 0.0:
            self.timer = self.current_time
        elif (self.current_time - self.timer) > 300:
            if keys[pg.K_SPACE]:
                self.done = True


class DialogueHandler(object):
    """Handles interaction between sprites to create dialogue boxes"""

    def __init__(self, player, sprites, level_object):
        self.player = player
        self.sprites = sprites
        self.textbox = None
        self.level = level_object
        self.last_textbox_timer = 0.0


    def update(self, keys, current_time):
        """Checks for the creation of Dialogue boxes"""
        if keys[pg.K_SPACE] and not self.textbox:
            for sprite in self.sprites:
                if (current_time - self.last_textbox_timer) > 300:
                    self.check_for_dialogue(sprite)

        if self.textbox:
            self.level.state = 'dialogue'
            self.textbox.update(current_time, keys)

            if self.textbox.done:
                self.level.state = 'normal'
                self.textbox = None
                self.last_textbox_timer = current_time


    def check_for_dialogue(self, sprite):
        """Checks if a sprite is in the correct location to give dialogue"""
        player = self.player
        tile_x, tile_y = player.location

        if player.direction == 'up':
            if sprite.location == (tile_x, tile_y - 1):
                self.textbox = DialogueBox(400, sprite.dialogue)
        elif player.direction == 'down':
            if sprite.location == (tile_x, tile_y + 1):
                self.textbox = DialogueBox(400, sprite.dialogue)
        elif player.direction == 'left':
            if sprite.location == (tile_x - 1, tile_y):
                self.textbox = DialogueBox(400, sprite.dialogue)
        elif player.direction == 'right':
            if sprite.location == (tile_x + 1, tile_y):
                self.textbox = DialogueBox(400, sprite.dialogue)


    def draw(self, surface):
        """Draws textbox to surface"""
        if self.textbox:
            surface.blit(self.textbox.image, self.textbox.rect)







