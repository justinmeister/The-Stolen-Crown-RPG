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
        self.arrow_timer = 0.0
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.dialogue_list = dialogue
        self.index = index
        self.image = self.make_dialogue_box_image()
        self.arrow = NextArrow()
        self.check_to_draw_arrow()
        self.done = False
        self.allow_input = False
        self.name = image_key


    def make_dialogue_box_image(self):
        """Make the image of the dialogue box"""
        image = pg.Surface(self.rect.size)
        image.set_colorkey(c.BLACK)
        image.blit(self.bground, (0, 0))

        dialogue_image = self.font.render(self.dialogue_list[self.index],
                                          True,
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
        if keys[pg.K_SPACE] and self.allow_input:
            self.done = True

        if not keys[pg.K_SPACE]:
            self.allow_input = True

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
            type = 'Healing Potion'
            total = str(1)
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
        self.allow_input = False
        self.level = level
        self.last_textbox_timer = 0.0
        self.game_data = level.game_data


    def update(self, keys, current_time):
        """Checks for the creation of Dialogue boxes"""
        if keys[pg.K_SPACE] and not self.textbox and self.allow_input:
            for sprite in self.sprites:
                if (current_time - self.last_textbox_timer) > 300:
                    if self.player.state == 'resting':
                        self.allow_input = False
                        self.check_for_dialogue(sprite)

        if self.textbox:
            if self.talking_sprite.name == 'treasurechest':
                self.open_chest(self.talking_sprite)

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
                    self.check_for_item()
                elif self.talking_sprite.battle:
                    self.game_data['battle type'] = self.talking_sprite.battle
                    self.dialogue_reset()
                    self.talking_sprite = None
                    self.level.state = 'normal'
                    self.level.switch_to_battle = True
                    self.textbox = None
                    self.last_textbox_timer = current_time
                    self.reset_sprite_direction()
                else:
                    self.dialogue_reset()
                    self.talking_sprite = None
                    self.level.state = 'normal'
                    self.textbox = None
                    self.last_textbox_timer = current_time
                    self.reset_sprite_direction()

        if not keys[pg.K_SPACE]:
            self.allow_input = True


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
            if item in self.game_data['player inventory']:
                if 'quantity' in self.game_data['player inventory'][item]:
                    self.game_data['player inventory'][item]['quantity'] += 1
            else:
                self.add_new_item_to_inventory(item)

            self.update_game_items_info(self.talking_sprite)
            self.talking_sprite.item = None

            if self.talking_sprite.name == 'treasurechest':
                self.talking_sprite.dialogue = ['Empty.']

            if item == 'ELIXIR':
                self.game_data['has brother elixir'] = True
                self.game_data['old man gift'] = 'Fire Blast'
                dialogue = ['Hurry! There is precious little time.']
                self.level.reset_dialogue = self.talking_sprite, dialogue

    def add_new_item_to_inventory(self, item):
        inventory = self.game_data['player inventory']
        potions = ['Healing Potion', 'Ether Potion']
        if item in potions:
            inventory[item] = dict([('quantity',1),
                                    ('value',15)])
        elif item == 'ELIXIR':
            inventory[item] = dict([('quantity',1)])
        elif item == 'Fire Blast':
            inventory[item] = dict([('magic points', 25),
                                    ('power', 10)])
        else:
            pass

    def update_game_items_info(self, sprite):
        if sprite.name == 'treasurechest':
            self.game_data['treasure{}'.format(sprite.id)] = False
        elif sprite.name == 'oldmanbrother':
            self.game_data['brother elixir'] = False

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

    def open_chest(self, sprite):
        if sprite.name == 'treasurechest':
            sprite.index = 1

    def dialogue_reset(self):
        """
        Reset dialogue if necessary.
        """
        if self.level.reset_dialogue:
            sprite = self.level.reset_dialogue[0]
            dialogue = self.level.reset_dialogue[1]
            sprite.dialogue = dialogue
            self.level.reset_dialogue = ()

