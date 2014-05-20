"""This is the state that handles battles against
monsters"""
import random, copy
import pygame as pg
from .. import tools, battlegui, observer
from .. components import person, attack, attackitems
from .. import constants as c


class Battle(tools._State):
    def __init__(self):
        super(Battle, self).__init__()
        self.game_data = {}
        self.current_time = 0.0
        self.timer = 0.0
        self.allow_input = False
        self.allow_info_box_change = False
        self.name = 'battle'
        self.state = None

        self.player = None
        self.attack_animations = None
        self.sword = None
        self.enemy_index = 0
        self.attacked_enemy = None
        self.attacking_enemy = None
        self.enemy_group = None
        self.enemy_pos_list = []
        self.enemy_list = []
        self.experience_points = 0

        self.background = None
        self.info_box = None
        self.arrow = None
        self.select_box = None
        self.player_health_box = None
        self.select_action_state_dict = {}
        self.next = None
        self.observers = []
        self.damage_points = pg.sprite.Group()

    def startup(self, current_time, game_data):
        """Initialize state attributes"""
        self.current_time = current_time
        self.timer = current_time
        self.allow_input = False
        self.game_data = game_data
        self.inventory = game_data['player inventory']
        self.state = c.SELECT_ACTION
        self.next = game_data['last state']
        self.run_away = False

        self.player = self.make_player()
        self.attack_animations = pg.sprite.Group()
        self.sword = attackitems.Sword(self.player)
        self.enemy_group, self.enemy_pos_list, self.enemy_list = self.make_enemies()
        self.experience_points = self.get_experience_points()
        self.background = self.make_background()
        self.info_box = battlegui.InfoBox(game_data, self.experience_points)
        self.arrow = battlegui.SelectArrow(self.enemy_pos_list,
                                           self.info_box)
        self.select_box = battlegui.SelectBox()
        self.player_health_box = battlegui.PlayerHealth(self.select_box.rect,
                                                        self.game_data)

        self.select_action_state_dict = self.make_selection_state_dict()
        self.observers = [observer.Battle(self)]
        self.player.observers.extend(self.observers)
        self.damage_points = pg.sprite.Group()

    def make_enemy_level_dict(self):
        new_dict = {c.OVERWORLD: 1,
                    c.DUNGEON: 2,
                    c.DUNGEON2: 2,
                    c.DUNGEON3: 3,
                    c.DUNGEON4: 2}

        return new_dict

    def set_enemy_level(self, enemy_list):
        dungeon_level_dict = self.make_enemy_level_dict()

        for enemy in enemy_list:
            enemy.level = dungeon_level_dict[self.previous]

    def get_experience_points(self):
        """
        Calculate experience points based on number of enemies
        and their levels.
        """
        experience_total = 0

        for enemy in self.enemy_list:
            experience_total += (random.randint(5,10)*enemy.level)

        return experience_total

    @staticmethod
    def make_background():
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
        pos_list = []

        for column in range(3):
            for row in range(3):
                x = (column * 100) + 100
                y = (row * 100) + 100
                pos_list.append([x, y])

        enemy_group = pg.sprite.Group()

        if self.game_data['battle type']:
            enemy = person.Enemy('evilwizard', 0, 0,
                                  'down', 'battle resting')
            enemy_group.add(enemy)
        else:
            for enemy in range(random.randint(1, 6)):
                enemy_group.add(person.Enemy('devil', 0, 0,
                                              'down', 'battle resting'))

        for i, enemy in enumerate(enemy_group):
            enemy.rect.topleft = pos_list[i]
            enemy.image = pg.transform.scale2x(enemy.image)
            enemy.index = i
            enemy.level = self.make_enemy_level_dict()[self.previous]
            enemy.health = enemy.level * 7

        enemy_list = [enemy for enemy in enemy_group]

        return enemy_group, pos_list[0:len(enemy_group)], enemy_list

    def make_player(self):
        """Make the sprite for the player's character"""
        player = person.Player('left', self.game_data, 630, 220, 'battle resting', 1)
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
        self.current_time = current_time
        self.check_input(keys)
        self.check_timed_events()
        self.check_if_battle_won()
        self.enemy_group.update(current_time)
        self.player.update(keys, current_time)
        self.attack_animations.update()
        self.info_box.update()
        self.arrow.update(keys)
        self.sword.update(current_time)
        self.damage_points.update()

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

                elif self.state == c.SELECT_ITEM:
                    if self.arrow.index == (len(self.arrow.pos_list) - 1):
                        self.state = c.SELECT_ACTION
                        self.notify(self.state)
                    elif self.info_box.item_text_list[self.arrow.index][:14] == 'Healing Potion':
                        self.state = c.DRINK_HEALING_POTION
                        self.notify(self.state)
                    elif self.info_box.item_text_list[self.arrow.index][:5] == 'Ether':
                        self.state = c.DRINK_ETHER_POTION
                        self.notify(self.state)
                elif self.state == c.SELECT_MAGIC:
                    if self.arrow.index == (len(self.arrow.pos_list) - 1):
                        self.state = c.SELECT_ACTION
                        self.notify(self.state)
                    elif self.info_box.magic_text_list[self.arrow.index] == 'Cure':
                        if self.game_data['player stats']['magic points']['current'] >= 25:
                            self.state = c.CURE_SPELL
                            self.notify(self.state)
                    elif self.info_box.magic_text_list[self.arrow.index] == 'Fire Blast':
                        if self.game_data['player stats']['magic points']['current'] >= 25:
                            self.state = c.FIRE_SPELL
                            self.notify(self.state)

            self.allow_input = False

        if keys[pg.K_RETURN] == False and keys[pg.K_SPACE] == False:
            self.allow_input = True

    def check_timed_events(self):
        """
        Check if amount of time has passed for timed events.
        """
        timed_states = [c.DISPLAY_ENEMY_ATTACK_DAMAGE,
                        c.ENEMY_HIT,
                        c.ENEMY_DEAD,
                        c.DRINK_HEALING_POTION,
                        c.DRINK_ETHER_POTION]
        long_delay = timed_states[1:]

        if self.state in long_delay:
            if (self.current_time - self.timer) > 1000:
                if self.state == c.ENEMY_HIT:
                    if len(self.enemy_list):
                        self.state = c.ENEMY_ATTACK
                    else:
                        self.state = c.BATTLE_WON
                elif (self.state == c.DRINK_HEALING_POTION or
                      self.state == c.CURE_SPELL or
                      self.state == c.DRINK_ETHER_POTION):
                    if len(self.enemy_list):
                        self.state = c.ENEMY_ATTACK
                    else:
                        self.state = c.BATTLE_WON
                self.timer = self.current_time
                self.notify(self.state)

        elif self.state == c.FIRE_SPELL or self.state == c.CURE_SPELL:
            if (self.current_time - self.timer) > 1500:
                if len(self.enemy_list):
                    self.state = c.ENEMY_ATTACK
                else:
                    self.state = c.BATTLE_WON
                self.timer = self.current_time
                self.notify(self.state)

        elif self.state == c.FLEE:
            if (self.current_time - self.timer) > 1500:
                self.end_battle()

        elif self.state == c.BATTLE_WON:
            if (self.current_time - self.timer) > 1800:
                self.state = c.SHOW_EXPERIENCE
                self.notify(self.state)

        elif self.state == c.SHOW_EXPERIENCE:
            if (self.current_time - self.timer) > 2200:
                player_stats = self.game_data['player stats']
                player_stats['experience to next level'] -= self.experience_points
                if player_stats['experience to next level'] <= 0:
                    player_stats['Level'] += 1
                    player_stats['health']['maximum'] += int(player_stats['health']['maximum']*.25)
                    player_stats['magic points']['maximum'] += int(player_stats['magic points']['maximum']*.20)
                    new_experience = int((player_stats['Level'] * 100) * .75)
                    player_stats['experience to next level'] = new_experience
                    self.notify(c.LEVEL_UP)
                else:
                    self.end_battle()

        elif self.state == c.DISPLAY_ENEMY_ATTACK_DAMAGE:
            if (self.current_time - self.timer) > 600:
                if self.enemy_index == (len(self.enemy_list) - 1):
                    if self.run_away:
                        self.state = c.FLEE
                    else:
                        self.state = c.SELECT_ACTION
                else:
                    self.state = c.SWITCH_ENEMY
                self.timer = self.current_time
                self.notify(self.state)

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
        for new_observer in self.observers:
            new_observer.on_notify(event)

    def end_battle(self):
        """
        End battle and flip back to previous state.
        """
        if self.game_data['battle type'] == 'evilwizard':
            self.game_data['crown quest'] = True
        self.game_data['last state'] = self.name
        self.game_data['battle counter'] = random.randint(50, 255)
        self.game_data['battle type'] = None
        self.done = True

    def attack_enemy(self, enemy_damage):
        enemy = self.player.attacked_enemy
        enemy.health -= enemy_damage
        self.set_enemy_indices()

        if enemy:
            enemy.enter_knock_back_state()
            if enemy.health <= 0:
                self.enemy_list.pop(enemy.index)
                enemy.state = c.FADE_DEATH
                self.notify(c.FADE_DEATH)
                self.arrow.remove_pos(self.player.attacked_enemy)
            self.enemy_index = 0

    def set_enemy_indices(self):
        for i, enemy in enumerate(self.enemy_list):
            enemy.index = i

    def draw_battle(self, surface):
        """Draw all elements of battle state"""
        self.background.draw(surface)
        self.enemy_group.draw(surface)
        self.attack_animations.draw(surface)
        self.sword.draw(surface)
        surface.blit(self.player.image, self.player.rect)
        surface.blit(self.info_box.image, self.info_box.rect)
        surface.blit(self.select_box.image, self.select_box.rect)
        surface.blit(self.arrow.image, self.arrow.rect)
        self.player_health_box.draw(surface)
        self.damage_points.draw(surface)


    def player_damaged(self, damage):
        self.game_data['player stats']['health']['current'] -= damage

    def player_healed(self, heal, magic_points=0):
        """
        Add health from potion to game data.
        """
        health = self.game_data['player stats']['health']

        health['current'] += heal
        if health['current'] > health['maximum']:
            health['current'] = health['maximum']

        if self.state == c.DRINK_HEALING_POTION:
            self.game_data['player inventory']['Healing Potion']['quantity'] -= 1
            if self.game_data['player inventory']['Healing Potion']['quantity'] == 0:
                del self.game_data['player inventory']['Healing Potion']
        elif self.state == c.CURE_SPELL:
            self.game_data['player stats']['magic points']['current'] -= magic_points

    def magic_boost(self, magic_points):
        """
        Add magic from ether to game data.
        """
        magic = self.game_data['player stats']['magic points']
        magic['current'] += magic_points
        if magic['current'] > magic['maximum']:
            magic['current'] = magic['maximum']

        self.game_data['player inventory']['Ether Potion']['quantity'] -= 1
        if not self.game_data['player inventory']['Ether Potion']['quantity']:
            del self.game_data['player inventory']['Ether Potion']

    def set_timer_to_current_time(self):
        """Set the timer to the current time."""
        self.timer = self.current_time

    def cast_fire_blast(self):
        """
        Cast fire blast on all enemies.
        """
        POWER = self.inventory['Fire Blast']['power']
        MAGIC_POINTS = self.inventory['Fire Blast']['magic points']
        self.game_data['player stats']['magic points']['current'] -= MAGIC_POINTS
        for enemy in self.enemy_list:
            DAMAGE = random.randint(POWER//2, POWER)
            self.damage_points.add(
                attackitems.HealthPoints(DAMAGE, enemy.rect.topright))
            enemy.health -= DAMAGE
            posx = enemy.rect.x - 32
            posy = enemy.rect.y - 64
            fire_sprite = attack.Fire(posx, posy)
            self.attack_animations.add(fire_sprite)
            if enemy.health <= 0:
                enemy.kill()
                self.arrow.remove_pos(enemy)
            else:
                enemy.enter_knock_back_state()
        self.enemy_list = [enemy for enemy in self.enemy_list if enemy.health > 0]
        self.enemy_index = 0
        self.arrow.index = 0
        self.arrow.become_invisible_surface()
        self.arrow.state = c.SELECT_ACTION
        self.state = c.FIRE_SPELL
        self.set_timer_to_current_time()
        self.info_box.state = c.FIRE_SPELL

    def cast_cure(self):
        """
        Cast cure spell on player.
        """
        HEAL_AMOUNT = self.inventory['Cure']['power']
        MAGIC_POINTS = self.inventory['Cure']['magic points']
        self.player.healing = True
        self.set_timer_to_current_time()
        self.state = c.CURE_SPELL
        self.arrow.become_invisible_surface()
        self.enemy_index = 0
        self.damage_points.add(
            attackitems.HealthPoints(HEAL_AMOUNT, self.player.rect.topright, False))
        self.player_healed(HEAL_AMOUNT, MAGIC_POINTS)
        self.info_box.state = c.DRINK_HEALING_POTION

    def drink_ether(self):
        """
        Drink ether potion.
        """
        self.player.healing = True
        self.set_timer_to_current_time()
        self.state = c.DRINK_ETHER_POTION
        self.arrow.become_invisible_surface()
        self.enemy_index = 0
        self.damage_points.add(
            attackitems.HealthPoints(30,
                                     self.player.rect.topright,
                                     False,
                                     True))
        self.magic_boost(30)
        self.info_box.state = c.DRINK_ETHER_POTION

    def drink_healing_potion(self):
        """
        Drink Healing Potion.
        """
        self.player.healing = True
        self.set_timer_to_current_time()
        self.state = c.DRINK_HEALING_POTION
        self.arrow.become_invisible_surface()
        self.enemy_index = 0
        self.damage_points.add(
            attackitems.HealthPoints(30,
                                     self.player.rect.topright,
                                     False))
        self.player_healed(30)
        self.info_box.state = c.DRINK_HEALING_POTION





