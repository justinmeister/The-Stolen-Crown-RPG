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
        self.enemy_damage = 0
        self.player_damage = 0
        self.state = c.SELECT_ACTION
        self.title_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.title_font.set_underline(True)
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 18)
        self.state_dict = self.make_state_dict()
        self.image = self.make_image()
        self.rect = self.image.get_rect(bottom=608)

    def make_state_dict(self):
        """
        Make dictionary of states Battle info can be in.
        """
        state_dict   = {c.SELECT_ACTION: 'Select an action.',
                        c.SELECT_MAGIC: 'Select a magic spell.',
                        c.SELECT_ITEM: 'Select an item.',
                        c.SELECT_ENEMY: 'Select an enemy.',
                        c.ENEMY_ATTACK: 'Enemy attacks player!',
                        c.PLAYER_ATTACK: 'Player attacks enemy.',
                        c.RUN_AWAY: 'Run away',
                        c.ENEMY_HIT: self.enemy_hit(),
                        c.ENEMY_DEAD: 'Enemy killed.',
                        c.DISPLAY_ENEMY_ATTACK_DAMAGE: self.player_hit()}

        return state_dict

    def enemy_hit(self):
        """
        Return text of enemy being hit using calculated damage.
        """
        return "Enemy hit with {} damage.".format(self.enemy_damage)

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

    def make_magic_text(self):
        """
        Make the text for when the player selects magic.
        """
        inventory = self.game_data['player inventory']
        allowed_item_list = ['Fire Blast', 'Cure']
        title = 'SELECT MAGIC SPELL'
        magic_text_list = [title]
        spell_list = [item for item in inventory if item in allowed_item_list]
        magic_text_list.extend(spell_list)
        magic_text_list.append('BACK')

        return magic_text_list

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
        elif self.state == c.SELECT_MAGIC:
            text_sprites = self.make_text_sprites(self.make_magic_text())
            text_sprites.draw(surface)
        else:
            text_surface = self.font.render(self.state_dict[self.state], True, c.NEAR_BLACK)
            text_rect = text_surface.get_rect(x=50, y=50)
            surface.blit(text_surface, text_rect)

        return surface

    def set_enemy_damage(self, enemy_damage):
        """
        Set enemy damage in state dictionary.
        """
        self.enemy_damage = enemy_damage
        self.state_dict[c.ENEMY_HIT] = self.enemy_hit()

    def set_player_damage(self, player_damage):
        """
        Set player damage in state dictionary.
        """
        self.player_damage = player_damage
        self.state_dict[c.DISPLAY_ENEMY_ATTACK_DAMAGE] = self.player_hit()

    def player_hit(self):
        return "Player hit with {} damage".format(self.player_damage)

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
    def __init__(self, enemy_pos_list, info_box):
        self.info_box = info_box
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
                      'select enemy': self.select_enemy,
                      'select item': self.select_item,
                      'select magic': self.select_magic}

        return state_dict

    def select_action(self, keys):
        """
        Select what action the player should take.
        """
        self.pos_list = self.make_select_action_pos_list()
        if self.index > (len(self.pos_list) - 1):
            print self.pos_list, self.index
        self.rect.topleft = self.pos_list[self.index]

        self.check_input(keys)

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

        if self.pos_list:
            pos = self.pos_list[self.index]
            self.rect.x = pos[0] - 60
            self.rect.y = pos[1] + 20

        self.check_input(keys)

    def check_input(self, keys):
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

    def select_item(self, keys):
        """
        Select item to use.
        """
        self.pos_list = self.make_select_item_pos_list()

        pos = self.pos_list[self.index]
        self.rect.x = pos[0] - 60
        self.rect.y = pos[1] + 20

        self.check_input(keys)

    def make_select_item_pos_list(self):
        """
        Make the coordinates for the arrow for the item select screen.
        """
        pos_list = []
        text_list = self.info_box.make_item_text()
        text_list = text_list[1:]

        for i in range(len(text_list)):
            left = 90
            top = (i * 29) + 488
            pos_list.append((left, top))

        return pos_list

    def select_magic(self, keys):
        """
        Select magic to use.
        """
        self.pos_list = self.make_select_magic_pos_list()

        pos = self.pos_list[self.index]
        self.rect.x = pos[0] - 60
        self.rect.y = pos[1] + 20

        self.check_input(keys)

    def make_select_magic_pos_list(self):
        """
        Make the coordinates for the arrow for the magic select screen.
        """
        pos_list = []
        text_list = self.info_box.make_magic_text()
        text_list = text_list[1:]

        for i in range(len(text_list)):
            left = 90
            top = (i * 29) + 488
            pos_list.append((left, top))

        return pos_list


    def become_invisible_surface(self):
        """
        Make image attribute an invisible surface.
        """
        self.image = pg.Surface((32, 32))
        self.image.set_colorkey(c.BLACK)

    def become_select_item_state(self):
        self.index = 0
        self.state = c.SELECT_ITEM

    def become_select_magic_state(self):
        self.index = 0
        self.state = c.SELECT_MAGIC

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

    def remove_pos(self, enemy):
        enemy_list = self.enemy_pos_list
        enemy_pos = list(enemy.rect.topleft)

        self.enemy_pos_list = [pos for pos in enemy_list if pos != enemy_pos]


class PlayerHealth(object):
    """
    Basic health meter for player.
    """
    def __init__(self, select_box_rect, game_data):
        self.health_stats = game_data['player stats']['health']
        self.magic_stats = game_data['player stats']['magic points']
        self.title_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.posx = select_box_rect.centerx
        self.posy = select_box_rect.y - 5

    @property
    def image(self):
        """
        Make the image surface for the player
        """
        current_health = str(self.health_stats['current'])
        max_health = str(self.health_stats['maximum'])
        if len(current_health) == 2:
            buffer = '  '
        elif len(current_health) == 1:
            buffer = '    '
        else:
            buffer = ''
        health_string = "Health: " + buffer + current_health + "/" + max_health
        health_surface =  self.title_font.render(health_string, True, c.NEAR_BLACK)
        health_rect = health_surface.get_rect(x=20, y=9)

        current_magic = str(self.magic_stats['current'])
        max_magic = str(self.magic_stats['maximum'])
        magic_string = "Magic:  " + current_magic + "/" + max_magic
        magic_surface = self.title_font.render(magic_string, True, c.NEAR_BLACK)
        magic_rect = magic_surface.get_rect(x=20, top=health_rect.bottom)

        box_surface = setup.GFX['battlestatbox']
        box_rect = box_surface.get_rect()

        parent_surface = pg.Surface(box_rect.size)
        parent_surface.blit(box_surface, box_rect)
        parent_surface.blit(health_surface, health_rect)
        parent_surface.blit(magic_surface, magic_rect)

        return parent_surface

    @property
    def rect(self):
        """
        Make the rect object for image surface.
        """
        return self.image.get_rect(centerx=self.posx, bottom=self.posy)

    def draw(self, surface):
        """
        Draw health to surface.
        """
        surface.blit(self.image, self.rect)
