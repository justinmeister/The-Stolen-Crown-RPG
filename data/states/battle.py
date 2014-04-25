"""This is the state that handles battles against
monsters"""

import random
import pygame as pg
from .. import tools, battlegui, observer
from .. components import person, attack, attackitems
from .. import constants as c



class Battle(tools._State):
    def __init__(self):
        super(Battle, self).__init__()

    def startup(self, current_time, game_data):
        """Initialize state attributes"""
        self.current_time = current_time
        self.allow_input = False
        self.allow_info_box_change = False
        self.game_data = game_data
        self.background = self.make_background()
        self.enemy_group, self.enemy_pos_list, self.enemy_list = self.make_enemies()
        self.enemy_index = 0
        self.player = self.make_player()
        self.attack_animations = pg.sprite.Group()
        self.info_box = battlegui.InfoBox(game_data)
        self.arrow = battlegui.SelectArrow(self.enemy_pos_list,
                                           self.info_box)
        self.select_box = battlegui.SelectBox()
        self.player_health = battlegui.PlayerHealth(self.select_box.rect,
                                                    self.game_data)
        self.sword = attackitems.Sword(self.player)
        self.attacked_enemy = None
        self.attacking_enemy = None
        self.state = c.SELECT_ACTION
        self.select_action_state_dict = self.make_selection_state_dict()
        self.name = 'battle'
        self.next = game_data['last state']
        self.observers = [observer.Battle(self)]
        self.player.observers.extend(self.observers)

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
            enemy.index = i

        enemy_list = [enemy for enemy in enemy_group]

        return enemy_group, pos_list[0:len(enemy_group)], enemy_list

    def make_player(self):
        """Make the sprite for the player's character"""
        player = person.Player('left', 630, 220, 'battle resting', 1)
        player.image = pg.transform.scale2x(player.image)

        return player

    def make_selection_state_dict(self):
        """
        Make a dictionary of states with arrow coordinates as keys.
        """
        pos_list = self.arrow.make_select_action_pos_list()
        state_list = [c.SELECT_ENEMY, c.SELECT_ITEM, c.SELECT_MAGIC, c.RUN_AWAY]
        return dict(zip(pos_list, state_list))

    def update(self, surface, keys, current_time):
        """Update the battle state"""
        self.check_input(keys)
        self.check_if_battle_won()
        self.enemy_group.update(current_time)
        self.player.update(keys, current_time)
        self.attack_animations.update()
        self.info_box.update()
        self.arrow.update(keys)

        self.draw_battle(surface)

    def check_input(self, keys):
        """
        Check user input to navigate GUI.
        """
        if self.allow_input:
            if keys[pg.K_RETURN]:
                self.notify(c.END_BATTLE)

            elif keys[pg.K_SPACE]:
                if self.state == c.SELECT_ACTION:
                    self.state = self.select_action_state_dict[
                        self.arrow.rect.topleft]
                    self.notify(self.state)

                elif self.state == c.SELECT_ENEMY:
                    self.state = c.PLAYER_ATTACK
                    self.notify(self.state)

                elif self.state == c.PLAYER_ATTACK:
                    self.state = c.ENEMY_DEAD
                    self.info_box.state = c.ENEMY_DEAD

                elif self.state == c.ENEMY_DEAD:
                    if len(self.enemy_list):
                        self.state = c.ENEMY_ATTACK
                    else:
                        self.state = c.BATTLE_WON
                    self.notify(self.state)

                elif self.state == c.SELECT_ITEM or self.state == c.SELECT_MAGIC:
                    if self.arrow.index == (len(self.arrow.pos_list) - 1):
                        self.state = c.SELECT_ACTION
                        self.notify(self.state)

            self.allow_input = False

        if keys[pg.K_RETURN] == False and keys[pg.K_SPACE] == False:
            self.allow_input = True

    def check_if_battle_won(self):
        """
        Check if state is SELECT_ACTION and there are no enemies left.
        """
        if self.state == c.SELECT_ACTION:
            if len(self.enemy_group) == 0:
                self.notify(c.BATTLE_WON)

    def notify(self, event):
        """
        Notify observer of event.
        """
        for observer in self.observers:
            observer.on_notify(event)

    def end_battle(self):
        """
        End battle and flip back to previous state.
        """
        self.game_data['last state'] = self.name
        self.done = True

    def attack_enemy(self):
        enemy = self.player.attacked_enemy
        self.set_enemy_indices()

        if enemy:
            enemy.kill()
            self.enemy_list.pop(enemy.index)
            self.enemy_index = 0
            posx = enemy.rect.x - 32
            posy = enemy.rect.y - 64
            fire_sprite = attack.Fire(posx, posy)
            self.attack_animations.add(fire_sprite)
            self.player.attacked_enemy = None

    def set_enemy_indices(self):
        for i, enemy in enumerate(self.enemy_list):
            enemy.index = i


    def draw_battle(self, surface):
        """Draw all elements of battle state"""
        self.background.draw(surface)
        self.enemy_group.draw(surface)
        self.attack_animations.draw(surface)
        surface.blit(self.player.image, self.player.rect)
        surface.blit(self.info_box.image, self.info_box.rect)
        surface.blit(self.select_box.image, self.select_box.rect)
        surface.blit(self.arrow.image, self.arrow.rect)
        self.player_health.draw(surface)
        self.sword.draw(surface)


