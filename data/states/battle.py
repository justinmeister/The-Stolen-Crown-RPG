"""This is the state that handles battles against
monsters"""

import pygame as pg
from .. import tools, setup
from .. components import person
from .. import constants as c


SELECT_ACTION = 'select action'
SELECT_ENEMY = 'select enemy'
ENEMY_ATTACK = 'enemy attack'
PLAYER_ATTACK = 'player attack'
SELECT_ITEM = 'select item'
SELECT_MAGIC = 'select magic'
RUN_AWAY = 'run away'



class Battle(tools._State):
    def __init__(self):
        super(Battle, self).__init__()

    def startup(self, current_time, game_data):
        """Initialize state attributes"""
        self.current_time = current_time
        self.game_data = game_data
        self.background = self.make_background()
        self.enemy_group = self.make_enemies()
        self.player_group = self.make_player()
        self.battle_info = BattleInfo()
        self.select_box = SelectBox()
        self.state_dict = self.make_state_dict()
        self.state = SELECT_ACTION
        self.select_action_state_dict = self.make_selection_state_dict()
        self.name = 'battle'
        self.next = game_data['last state']

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
        enemy = person.Person('devil', 100, 220, 'down', 'battle resting')
        enemy.image = pg.transform.scale2x(enemy.image)
        group = pg.sprite.Group(enemy)

        return group

    def make_player(self):
        """Make the sprite for the player's character"""
        player = person.Player('left', 630, 220, 'battle resting', 1)
        player.image = pg.transform.scale2x(player.image)
        player_group = pg.sprite.Group(player)

        return player_group

    def make_state_dict(self):
        """
        Make the dictionary of states the battle can be in.
        """
        state_dict = {SELECT_ACTION: self.select_action,
                      SELECT_ENEMY: self.select_enemy,
                      ENEMY_ATTACK: self.enemy_attack,
                      PLAYER_ATTACK: self.player_attack,
                      RUN_AWAY: self.run_away}

        return state_dict

    def make_selection_state_dict(self):
        """
        Make a dictionary of states with arrow coordinates as keys.
        """
        pos_list = self.select_box.arrow.make_select_action_pos_list()
        state_list = [SELECT_ENEMY, SELECT_ITEM, SELECT_MAGIC, RUN_AWAY]
        return dict(zip(pos_list, state_list))

    def select_action(self):
        """
        Select player action, of either attack, item, magic, run away.
        """
        pass

    def select_enemy(self):
        """
        Select enemy you wish to attack.
        """
        pass

    def enemy_attack(self):
        """
        Enemies, each in turn, attack the player.
        """
        pass

    def player_attack(self):
        """
        Player attacks enemy
        """
        pass

    def run_away(self):
        """
        Player attempts to run away.
        """
        pass

    def update(self, surface, keys, current_time):
        """Update the battle state"""
        self.check_input(keys)
        self.enemy_group.update(current_time)
        self.player_group.update(keys, current_time)
        self.select_box.update(keys)
        self.battle_info.update(self.state)
        self.draw_battle(surface)

    def check_input(self, keys):
        """
        Check user input to navigate GUI.
        """
        arrow = self.select_box.arrow

        if keys[pg.K_RETURN]:
            self.game_data['last state'] = self.name
            self.done = True

        elif keys[pg.K_SPACE]:
            self.state = self.select_action_state_dict[arrow.rect.topleft]

    def draw_battle(self, surface):
        """Draw all elements of battle state"""
        self.background.draw(surface)
        self.enemy_group.draw(surface)
        self.player_group.draw(surface)
        surface.blit(self.battle_info.image, self.battle_info.rect)
        surface.blit(self.select_box.image, self.select_box.rect)


class BattleInfo(object):
    """
    Info box that describes attack damage and other battle
    related information.
    """
    def __init__(self):
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.message_dict = self.make_message_dict()
        self.image = self.make_image('select action')
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

    def make_image(self, state):
        """
        Make image out of box and message.
        """
        image = setup.GFX['shopbox']
        rect = image.get_rect(bottom=608)
        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        text_surface = self.font.render(self.message_dict[state], True, c.NEAR_BLACK)
        text_rect = text_surface.get_rect(x=50, y=50)
        surface.blit(text_surface, text_rect)

        return surface

    def update(self, state):
        self.image = self.make_image(state)


class SelectBox(object):
    """
    Box to select whether to attack, use item, use magic or run away.
    """
    def __init__(self):
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.slots = self.make_slots()
        self.arrow = SelectArrow()
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

        surface.blit(self.arrow.image, self.arrow.rect)

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

    def update(self, keys):
        """Update components.
        """
        self.arrow.update(keys)
        self.image = self.make_image()


class SelectArrow(object):
    """Small arrow for menu"""
    def __init__(self):
        self.image = setup.GFX['smallarrow']
        self.rect = self.image.get_rect()
        self.state = 'select action'
        self.state_dict = self.make_state_dict()
        self.pos_list = self.make_select_action_pos_list()
        self.index = 0
        self.rect.topleft = self.pos_list[self.index]
        self.allow_input = False

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
            x = 50
            y = (i * 34) + 12
            pos_list.append((x, y))

        return pos_list

    def select_enemy(self):
        """
        Select what enemy you want to take action on.
        """
        pass

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

