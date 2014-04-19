"""This is the state that handles battles against
monsters"""

import random
import pygame as pg
from .. import tools, setup
from .. components import person
from .. import constants as c

#STATES

SELECT_ACTION = 'select action'
SELECT_ENEMY = 'select enemy'
ENEMY_ATTACK = 'enemy attack'
PLAYER_ATTACK = 'player attack'
SELECT_ITEM = 'select item'
SELECT_MAGIC = 'select magic'
RUN_AWAY = 'run away'

#EVENTS

END_BATTLE = 'end battle'


class Battle(tools._State):
    def __init__(self):
        super(Battle, self).__init__()

    def startup(self, current_time, game_data):
        """Initialize state attributes"""
        self.current_time = current_time
        self.game_data = game_data
        self.background = self.make_background()
        self.enemy_group, self.enemy_pos_list = self.make_enemies()
        self.player_group = self.make_player()
        self.info_box = InfoBox(game_data)
        self.arrow = SelectArrow(self.enemy_pos_list)
        self.select_box = SelectBox()
        self.state = SELECT_ACTION
        self.select_action_state_dict = self.make_selection_state_dict()
        self.name = 'battle'
        self.next = game_data['last state']
        self.observer = Observer(self)

    def make_background(self):
        """Make the blue/black background"""
        background = pg.sprite.Sprite()
        surface = pg.Surface(c.SCREEN_SIZE).convert()
        surface.fill(c.BLACK_BLUE)
        background.image = surface
        background.rect = background.image.get_rect()
        background_group = pg.sprite.Group(background)

        return background_group

    def make_enemies(self):
        """Make the enemies for the battle. Return sprite group"""
        pos_list  = []

        for column in range(3):
            for row in range(3):
                x = (column * 100) + 100
                y = (row * 100) + 100
                pos_list.append([x,y])

        enemy_group = pg.sprite.Group()

        for enemy in range(random.randint(1, 6)):
            enemy_group.add(person.Person('devil', 0, 0,
                                          'down', 'battle resting'))

        for i, enemy in enumerate(enemy_group):
            enemy.rect.topleft = pos_list[i]
            enemy.image = pg.transform.scale2x(enemy.image)

        return enemy_group, pos_list[0:len(enemy_group)]

    def make_player(self):
        """Make the sprite for the player's character"""
        player = person.Player('left', 630, 220, 'battle resting', 1)
        player.image = pg.transform.scale2x(player.image)
        player_group = pg.sprite.Group(player)

        return player_group

    def make_selection_state_dict(self):
        """
        Make a dictionary of states with arrow coordinates as keys.
        """
        pos_list = self.arrow.make_select_action_pos_list()
        state_list = [SELECT_ENEMY, SELECT_ITEM, SELECT_MAGIC, RUN_AWAY]
        return dict(zip(pos_list, state_list))

    def update(self, surface, keys, current_time):
        """Update the battle state"""
        self.check_input(keys)
        self.enemy_group.update(current_time)
        self.player_group.update(keys, current_time)
        self.arrow.update(keys)

        self.draw_battle(surface)

    def check_input(self, keys):
        """
        Check user input to navigate GUI.
        """
        if keys[pg.K_RETURN]:
            self.notify(END_BATTLE)

        elif keys[pg.K_SPACE] and self.state == SELECT_ACTION:
            self.state = self.select_action_state_dict[self.arrow.rect.topleft]
            self.notify(self.state)

    def notify(self, event):
        """
        Notify observer of event.
        """
        self.observer.on_notify(event)

    def end_battle(self):
        """
        End battle and flip back to previous state.
        """
        self.game_data['last state'] = self.name
        self.done = True

    def draw_battle(self, surface):
        """Draw all elements of battle state"""
        self.background.draw(surface)
        self.enemy_group.draw(surface)
        self.player_group.draw(surface)
        surface.blit(self.info_box.image, self.info_box.rect)
        surface.blit(self.select_box.image, self.select_box.rect)
        surface.blit(self.arrow.image, self.arrow.rect)


class Observer(object):
    """
    Observes events of battle and passes info to components.
    """
    def __init__(self, level):
        self.level = level
        self.info_box = level.info_box
        self.select_box = level.info_box
        self.arrow = level.arrow
        self.player = level.player_group
        self.enemies = level.enemy_group
        self.event_dict = self.make_event_dict()

    def make_event_dict(self):
        """
        Make a dictionary of events the Observer can
        receive.
        """
        event_dict = {END_BATTLE: self.end_battle,
                      SELECT_ACTION: self.select_action,
                      SELECT_ITEM: self.select_item,
                      SELECT_ENEMY: self.select_enemy,
                      ENEMY_ATTACK: self.enemy_attack,
                      PLAYER_ATTACK: self.player_attack,
                      RUN_AWAY: self.run_away}

        return event_dict

    def on_notify(self, event):
        """
        Notify Observer of event.
        """
        if event in self.event_dict:
            self.event_dict[event]()

    def end_battle(self):
        """
        End Battle and flip to previous state.
        """
        self.level.end_battle()

    def select_action(self):
        """
        Set components to select action.
        """
        self.level.state = SELECT_ACTION
        self.arrow.index = 0

    def select_enemy(self):
        self.level.state = SELECT_ENEMY
        self.arrow.state = SELECT_ENEMY

    def select_item(self):
        self.level.state = SELECT_ITEM
        self.info_box.image = self.info_box.make_image(SELECT_ITEM)

    def enemy_attack(self):
        pass

    def player_attack(self):
        pass

    def run_away(self):
        pass


class InfoBox(object):
    """
    Info box that describes attack damage and other battle
    related information.
    """
    def __init__(self, game_data):
        self.game_data = game_data
        self.state = SELECT_ACTION
        self.title_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.title_font.set_underline(True)
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 18)
        self.message_dict = self.make_message_dict()
        self.image = self.make_image(SELECT_ACTION)
        self.rect = self.image.get_rect(bottom=608)

    def make_message_dict(self):
        """
        Make dictionary of states Battle info can be in.
        """
        message_dict = {SELECT_ACTION: 'Select an action.',
                        SELECT_MAGIC: 'Select a magic spell.',
                        SELECT_ITEM: 'Select an item.',
                        SELECT_ENEMY: 'Select an enemy.',
                        ENEMY_ATTACK: 'The enemy attacks player!',
                        PLAYER_ATTACK: 'Player attacks enemy.',
                        RUN_AWAY: 'Run away'}

        return message_dict

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

    def make_image(self, state):
        """
        Make image out of box and message.
        """
        image = setup.GFX['shopbox']
        rect = image.get_rect(bottom=608)
        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        if state == SELECT_ITEM:
            text_sprites = self.make_text_sprites(self.make_item_text())
            text_sprites.draw(surface)
        else:
            text_surface = self.font.render(self.message_dict[state], True, c.NEAR_BLACK)
            text_rect = text_surface.get_rect(x=50, y=50)
            surface.blit(text_surface, text_rect)

        return surface


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

