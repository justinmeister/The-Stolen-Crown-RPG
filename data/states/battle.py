"""This is the state that handles battles against
monsters"""

import pygame as pg
from .. import tools, setup
from .. components import person
from .. import constants as c

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
        state_dict = {'select action': self.select_action,
                      'select enemy': self.select_enemy,
                      'enemy attack': self.enemy_attack,
                      'player attack': self.player_attack,
                      'run away': self.run_away}

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
        #self.menu.update()
        self.draw_battle(surface)

    def check_input(self, keys):
        """
        Check user input to navigate GUI.
        """
        if keys[pg.K_SPACE]:
            self.game_data['last state'] = self.name
            self.done = True

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
        self.image = setup.GFX['shopbox']
        self.rect = self.image.get_rect(bottom=608)


class SelectBox(object):
    """
    Box to select whether to attack, use item, use magic or run away.
    """
    def __init__(self):
        self.image = setup.GFX['goldbox']
        self.rect = self.image.get_rect(bottom=608, right=800)


