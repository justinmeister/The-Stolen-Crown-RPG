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
    def __init__(self, dialogue, index=0, image_key='dialoguebox', item=None):
        self.item = item
        self.bground = setup.GFX[image_key]
        self.rect = self.bground.get_rect(centerx=400)
        self.timer = 0.0
        self.arrow_timer = 0.0
        self.font = pg.font.Font(setup.FONTS['Fixedsys500c'], 22)
        self.dialogue_list = dialogue
        self.index = index
        self.image = self.make_dialogue_box_image()
        self.arrow = NextArrow()
        self.check_to_draw_arrow()
        self.done = False
        self.name = image_key


    def make_dialogue_box_image(self):
        """Make the image of the dialogue box"""
        image = pg.Surface(self.rect.size)
        image.set_colorkey(c.BLACK)
        image.blit(self.bground, (0, 0))

        dialogue_image = self.font.render(self.dialogue_list[self.index],
                                          False,
                                          c.NEAR_BLACK)
        dialogue_rect = dialogue_image.get_rect(left=50, top=50)
        image.blit(dialogue_image, dialogue_rect)

        return image



    def update(self, keys, current_time):
        """Updates scrolling text"""
        self.current_time = current_time
        self.draw_box(current_time)
        self.terminate_check(keys)


    def draw_box(self, current_time, x=400):
        """Reveal dialogue on textbox"""
        self.image = self.make_dialogue_box_image()
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


class ItemBox(DialogueBox):
    """Text box for information like obtaining new items"""
    def __init__(self, dialogue, item=None):
        super(ItemBox, self).__init__(None, 0, 'infobox', item)


    def make_dialogue_box_image(self):
        """Make the image of the dialogue box"""
        image = pg.Surface(self.rect.size)
        image.set_colorkey(c.BLACK)
        image.blit(self.bground, (0, 0))

        if self.item:
            total = str(self.item['total'])
            type = self.item['type']
            dialogue = 'You received ' + total + ' ' + type + '.'
            self.dialogue_list = [dialogue]
            self.item = None

        dialogue_image = self.font.render(self.dialogue_list[self.index],
                                          False,
                                          c.NEAR_BLACK)
        dialogue_rect = dialogue_image.get_rect(left=50, top=50)
        image.blit(dialogue_image, dialogue_rect)

        return image



class TextHandler(object):
    """Handles interaction between sprites to create dialogue boxes"""

    def __init__(self, level):
        self.player = level.player
        self.sprites = level.sprites
        self.talking_sprite = None
        self.textbox = None
        self.level = level
        self.last_textbox_timer = 0.0
        self.game_data = level.persist


    def update(self, keys, current_time):
        """Checks for the creation of Dialogue boxes"""
        if keys[pg.K_SPACE] and not self.textbox:
            for sprite in self.sprites:
                if (current_time - self.last_textbox_timer) > 300:
                    self.check_for_dialogue(sprite)

        if self.textbox:
            self.textbox.update(keys, current_time)

            if self.textbox.done:

                if self.textbox.index < (len(self.textbox.dialogue_list) - 1):
                    index = self.textbox.index + 1
                    dialogue = self.textbox.dialogue_list
                    if self.textbox.name == 'dialoguebox':
                        self.textbox = DialogueBox(dialogue, index)
                    elif self.textbox.name == 'infobox':
                        self.textbox = ItemBox(dialogue, index)
                elif self.talking_sprite.item:
                    item = self.check_for_item()
                    self.textbox = ItemBox(None, item)
                else:
                    self.level.state = 'normal'
                    self.textbox = None
                    self.last_textbox_timer = current_time
                    self.reset_sprite_direction()


    def check_for_dialogue(self, sprite):
        """Checks if a sprite is in the correct location to give dialogue"""
        player = self.player
        tile_x, tile_y = player.location

        if player.direction == 'up':
            if sprite.location == [tile_x, tile_y - 1]:
                self.textbox = DialogueBox(sprite.dialogue)
                sprite.direction = 'down'
                self.talking_sprite = sprite
        elif player.direction == 'down':
            if sprite.location == [tile_x, tile_y + 1]:
                self.textbox = DialogueBox(sprite.dialogue)
                sprite.direction = 'up'
                self.talking_sprite = sprite
        elif player.direction == 'left':
            if sprite.location == [tile_x - 1, tile_y]:
                self.textbox = DialogueBox(sprite.dialogue)
                sprite.direction = 'right'
                self.talking_sprite = sprite
        elif player.direction == 'right':
            if sprite.location == [tile_x + 1, tile_y]:
                self.textbox = DialogueBox(sprite.dialogue)
                sprite.direction = 'left'
                self.talking_sprite = sprite


    def check_for_item(self):
        """Checks if sprite has an item to give to the player"""
        item = self.talking_sprite.item
        if item:
            self.player.item_list.append(item)
            self.talking_sprite.item = None
            if self.talking_sprite.name == 'king':
                self.game_data['king item'] = None

        return item



    def reset_sprite_direction(self):
        """Reset sprite to default direction"""
        for sprite in self.sprites:
            if sprite.state == 'resting':
                sprite.direction = sprite.default_direction


    def draw(self, surface):
        """Draws textbox to surface"""
        if self.textbox:
            surface.blit(self.textbox.image, self.textbox.rect)


    def make_textbox(self, name, dialogue, item=None):
        """Make textbox on demand"""
        if name == 'itembox':
            textbox = ItemBox(dialogue, item)
        elif name == 'dialoguebox':
            textbox = DialogueBox(dialogue)
        else:
            textbox = None

        return textbox


    def update_for_shops(self, keys, current_time):
        """Update text handler when player is in a shop"""
        self.textbox.update(keys, current_time)
        last_index = len(self.textbox.dialogue_list) - 1

        if self.textbox.done and (self.textbox.index < last_index):
            index = self.textbox.index + 1
            dialogue = self.textbox.dialogue_list
            self.textbox = DialogueBox(dialogue, index)








