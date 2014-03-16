__author__ = 'justinarmstrong'
import copy
import pygame as pg
from .. import setup
from .. import constants as c



class NextArrow(pg.sprite.Sprite):
    """Flashing arrow indicating more dialogue"""
    def __init__(self):
        super(NextArrow, self).__init__()
        self.image = setup.GFX['fancyarrow']
        self.rect = self.image.get_rect(right=780,
                                        bottom=135)


class DialogueBox(object):
    """Text box used for dialogue"""
    def __init__(self, x, dialogue, dialogue_index=0):
        self.bground = setup.GFX['dialoguebox']
        self.rect = self.bground.get_rect(centerx=x)
        self.image = pg.Surface(self.rect.size)
        self.image.set_colorkey(c.BLACK)
        self.image.blit(self.bground, (0, 0))
        self.timer = 0.0
        self.arrow_timer = 0.0
        self.font = pg.font.Font(setup.FONTS['Fixedsys500c'], 22)
        self.dialogue_list = dialogue
        self.index = dialogue_index
        self.dialogue_image = self.font.render(dialogue[self.index],
                                               False,
                                               c.NEAR_BLACK)
        self.dialogue_rect = self.dialogue_image.get_rect(left=50, top=50)
        self.image.blit(self.dialogue_image, self.dialogue_rect)
        self.arrow = NextArrow()
        self.check_to_draw_arrow()
        self.done = False


    def update(self, current_time, keys):
        """Updates scrolling text"""
        self.current_time = current_time
        self.draw_box(current_time)
        self.terminate_check(keys)


    def draw_box(self, current_time, x=400):
        """Reveal dialogue on textbox"""
        bground = setup.GFX['dialoguebox']
        rect = bground.get_rect(centerx=x)
        text_image = self.dialogue_image
        text_rect = self.dialogue_rect
        self.image = pg.Surface(rect.size)
        self.image.set_colorkey(c.BLACK)

        self.image.blit(bground, (0, 0))
        self.image.blit(text_image, text_rect)
        self.check_to_draw_arrow()


    def terminate_check(self, keys):
        """Remove textbox from sprite group after 2 seconds"""

        if self.timer == 0.0:
            self.timer = self.current_time
        elif (self.current_time - self.timer) > 300:
            if keys[pg.K_SPACE]:
                self.done = True


    def check_to_draw_arrow(self):
        """Blink arrow if more text needs to be read"""
        if self.index < len(self.dialogue_list) - 1:
            self.image.blit(self.arrow.image, self.arrow.rect)
        else:
            pass


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
            self.textbox.update(current_time, keys)

            if self.textbox.done:
                if self.textbox.index < (len(self.textbox.dialogue_list) - 1):
                    index = self.textbox.index + 1
                    dialogue = self.textbox.dialogue_list
                    self.textbox = DialogueBox(400, dialogue, index)
                else:
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
                sprite.direction = 'down'
        elif player.direction == 'down':
            if sprite.location == (tile_x, tile_y + 1):
                self.textbox = DialogueBox(400, sprite.dialogue)
                sprite.direction = 'up'
        elif player.direction == 'left':
            if sprite.location == (tile_x - 1, tile_y):
                self.textbox = DialogueBox(400, sprite.dialogue)
                sprite.direction = 'right'
        elif player.direction == 'right':
            if sprite.location == (tile_x + 1, tile_y):
                self.textbox = DialogueBox(400, sprite.dialogue)
                sprite.direction = 'left'


    def draw(self, surface):
        """Draws textbox to surface"""
        if self.textbox:
            surface.blit(self.textbox.image, self.textbox.rect)







