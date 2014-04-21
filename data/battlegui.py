"""
GUI components for battle states.
"""
import pygame as pg
from . import setup
from . import constants as c
from .components import textbox


class InfoBox(object):
    """
    Info box that describes attack damage and other battle
    related information.
    """
    def __init__(self, game_data):
        self.game_data = game_data
        self.state = c.SELECT_ACTION
        self.title_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.title_font.set_underline(True)
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 18)
        self.state_dict = self.make_state_dict()
        self.image = self.make_image()
        self.rect = self.image.get_rect(bottom=608)
        self.arrow = textbox.NextArrow()
        self.arrow.rect.topleft = (380, 110)


    def make_state_dict(self):
        """
        Make dictionary of states Battle info can be in.
        """
        state_dict   = {c.SELECT_ACTION: 'Select an action.',
                        c.SELECT_MAGIC: 'Select a magic spell.',
                        c.SELECT_ITEM: 'Select an item.',
                        c.SELECT_ENEMY: 'Select an enemy.',
                        c.ENEMY_ATTACK: 'The enemy attacks player!',
                        c.PLAYER_ATTACK: 'Player attacks enemy.',
                        c.RUN_AWAY: 'Run away',
                        c.ENEMY_HIT: 'Enemy hit with 20 damage.',
                        c.ENEMY_DEAD: 'Enemy killed.'}

        return state_dict


    def make_item_text(self):
        """
        Make the text for when the player selects items.
        """
        inventory = self.game_data['player inventory']
        allowed_item_list = ['Healing Potion']
        title = 'SELECT ITEM'
        item_text_list = [title]

        for item in inventory:
            if item in allowed_item_list:
                text = item + ": " + str(inventory[item]['quantity'])
                item_text_list.append(text)

        item_text_list.append('BACK')

        return item_text_list

    def make_text_sprites(self, text_list):
        """
        Make sprites out of text.
        """
        sprite_group = pg.sprite.Group()

        for i, text in enumerate(text_list):
            sprite = pg.sprite.Sprite()

            if i == 0:
                x = 195
                y = 10
                surface = self.title_font.render(text, True, c.NEAR_BLACK)
                rect = surface.get_rect(x=x, y=y)
            else:
                x = 100
                y = (i * 30) + 20
                surface = self.font.render(text, True, c.NEAR_BLACK)
                rect = surface.get_rect(x=x, y=y)
            sprite.image = surface
            sprite.rect = rect
            sprite_group.add(sprite)

        return sprite_group

    def make_image(self):
        """
        Make image out of box and message.
        """
        image = setup.GFX['shopbox']
        rect = image.get_rect(bottom=608)
        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        if self.state == c.SELECT_ITEM:
            text_sprites = self.make_text_sprites(self.make_item_text())
            text_sprites.draw(surface)
        else:
            text_surface = self.font.render(self.state_dict[self.state], True, c.NEAR_BLACK)
            text_rect = text_surface.get_rect(x=50, y=50)
            surface.blit(text_surface, text_rect)
            if self.state == c.ENEMY_HIT or self.state == c.ENEMY_DEAD:
                surface.blit(self.arrow.image, self.arrow.rect)

        return surface

    def update(self):
        """Updates info box"""
        self.image = self.make_image()


class SelectBox(object):
    """
    Box to select whether to attack, use item, use magic or run away.
    """
    def __init__(self):
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.slots = self.make_slots()
        self.image = self.make_image()
        self.rect = self.image.get_rect(bottom=608,
                                        right=800)

    def make_image(self):
        """
        Make the box image for
        """
        image = setup.GFX['goldbox']
        rect = image.get_rect(bottom=608)
        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        for text in self.slots:
            text_surface = self.font.render(text, True, c.NEAR_BLACK)
            text_rect = text_surface.get_rect(x=self.slots[text]['x'],
                                              y=self.slots[text]['y'])
            surface.blit(text_surface, text_rect)

        return surface

    def make_slots(self):
        """
        Make the slots that hold the text selections, and locations.
        """
        slot_dict = {}
        selections = ['Attack', 'Items', 'Magic', 'Run']

        for i, text in enumerate(selections):
            slot_dict[text] = {'x': 150,
                               'y': (i*34)+10}

        return slot_dict


class SelectArrow(object):
    """Small arrow for menu"""
    def __init__(self, enemy_pos_list):
        self.image = setup.GFX['smallarrow']
        self.rect = self.image.get_rect()
        self.state = 'select action'
        self.state_dict = self.make_state_dict()
        self.pos_list = self.make_select_action_pos_list()
        self.index = 0
        self.rect.topleft = self.pos_list[self.index]
        self.allow_input = False
        self.enemy_pos_list = enemy_pos_list

    def make_state_dict(self):
        """Make state dictionary"""
        state_dict = {'select action': self.select_action,
                      'select enemy': self.select_enemy}

        return state_dict

    def select_action(self, keys):
        """
        Select what action the player should take.
        """
        self.pos_list = self.make_select_action_pos_list()
        self.rect.topleft = self.pos_list[self.index]

        if self.allow_input:
            if keys[pg.K_DOWN] and self.index < (len(self.pos_list) - 1):
                self.index += 1
                self.allow_input = False
            elif keys[pg.K_UP] and self.index > 0:
                self.index -= 1
                self.allow_input = False

        if keys[pg.K_DOWN] == False and keys[pg.K_UP] == False:
            self.allow_input = True


    def make_select_action_pos_list(self):
        """
        Make the list of positions the arrow can be in.
        """
        pos_list = []

        for i in range(4):
            x = 590
            y = (i * 34) + 472
            pos_list.append((x, y))

        return pos_list

    def select_enemy(self, keys):
        """
        Select what enemy you want to take action on.
        """
        self.pos_list = self.enemy_pos_list
        pos = self.pos_list[self.index]
        self.rect.x = pos[0] - 60
        self.rect.y = pos[1] + 20

        if self.allow_input:
            if keys[pg.K_DOWN] and self.index < (len(self.pos_list) - 1):
                self.index += 1
                self.allow_input = False
            elif keys[pg.K_UP] and self.index > 0:
                self.index -= 1
                self.allow_input = False


        if keys[pg.K_DOWN] == False and keys[pg.K_UP] == False \
                and keys[pg.K_RIGHT] == False and keys[pg.K_LEFT] == False:
            self.allow_input = True

    def become_invisible_surface(self):
        """
        Make image attribute an invisible surface.
        """
        self.image = pg.Surface((32, 32))
        self.image.set_colorkey(c.BLACK)


    def enter_select_action(self):
        """
        Assign values for the select action state.
        """
        pass

    def enter_select_enemy(self):
        """
        Assign values for the select enemy state.
        """
        pass

    def update(self, keys):
        """
        Update arrow position.
        """
        state_function = self.state_dict[self.state]
        state_function(keys)

    def draw(self, surface):
        """
        Draw to surface.
        """
        surface.blit(self.image, self.rect)

