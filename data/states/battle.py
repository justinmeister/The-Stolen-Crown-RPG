"""This is the state that handles battles against
monsters"""
import random, sys
from itertools import izip
import pygame as pg
from .. import tools, battlegui, observer, setup
from .. components import person, attack, attackitems
from .. import constants as c


#Python 2/3 compatibility.
if sys.version_info[0] == 2:
    range = xrange


class Battle(tools._State):
    def __init__(self):
        super(Battle, self).__init__()
        self.name = 'battle'
        self.music = setup.MUSIC['high_action']
        self.volume = 0.4

    def startup(self, current_time, game_data):
        """
        Initialize state attributes.
        """
        self.current_time = current_time
        self.timer = current_time
        self.allow_input = False
        self.game_data = game_data
        self.inventory = game_data['player inventory']
        self.state = 'transition in'
        self.next = game_data['last state']
        self.run_away = False

        self.player = self.make_player()
        self.attack_animations = pg.sprite.Group()
        self.sword = attackitems.Sword(self.player)
        self.enemy_group, self.enemy_pos_list, self.enemy_list = self.make_enemies()
        self.experience_points = self.get_experience_points()
        self.new_gold = self.get_new_gold()
        self.background = self.make_background()
        self.info_box = battlegui.InfoBox(game_data, 
                                          self.experience_points, 
                                          self.new_gold)
        self.arrow = battlegui.SelectArrow(self.enemy_pos_list,
                                           self.info_box)
        self.select_box = battlegui.SelectBox()
        self.player_health_box = battlegui.PlayerHealth(self.select_box.rect,
                                                        self.game_data)

        self.select_action_state_dict = self.make_selection_state_dict()
        self.observers = [observer.Battle(self),
                          observer.MusicChange()]
        self.player.observers.extend(self.observers)
        self.observers.append(observer.SoundEffects())
        self.damage_points = pg.sprite.Group()
        self.player_actions = []
        self.player_action_dict = self.make_player_action_dict()
        self.player_level = self.game_data['player stats']['Level']
        self.enemies_to_attack = []
        self.action_selected = False
        self.just_leveled_up = False
        self.transition_rect = setup.SCREEN.get_rect()
        self.transition_alpha = 255
        self.temp_magic = self.game_data['player stats']['magic']['current']

    def make_player_action_dict(self):
        """
        Make the dict to execute player actions.
        """
        action_dict = {c.PLAYER_ATTACK: self.enter_player_attack_state,
                       c.CURE_SPELL: self.cast_cure,
                       c.FIRE_SPELL: self.cast_fire_blast,
                       c.DRINK_HEALING_POTION: self.enter_drink_healing_potion_state,
                       c.DRINK_ETHER_POTION: self.enter_drink_ether_potion_state}

        return action_dict

    def make_enemy_level_dict(self):
        new_dict = {c.OVERWORLD: 1,
                    c.DUNGEON: 2,
                    c.DUNGEON2: 2,
                    c.DUNGEON3: 2,
                    c.DUNGEON4: 2,
                    c.DUNGEON5: 4}

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
            experience_total += (random.randint(5,10))

        return experience_total

    def get_new_gold(self):
        """
        Calculate the gold collected at the end of the battle.
        """
        gold = 0

        for enemy in self.enemy_list:
            max_gold = enemy.level * 20
            gold += (random.randint(1, max_gold))

        return gold

    def make_background(self):
        """
        Make the blue/black background.
        """
        background = pg.sprite.Sprite()
        surface = pg.Surface(c.SCREEN_SIZE).convert()
        surface.fill(c.BLACK_BLUE)
        background.image = surface
        background.rect = background.image.get_rect()
        background_group = pg.sprite.Group(background)

        return background_group

    def make_enemies(self):
        """
        Make the enemies for the battle. Return sprite group.
        """
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
            if self.game_data['start of game']:
                for enemy in range(3):
                    enemy_group.add(person.Enemy('devil', 0, 0,
                                                 'down', 'battle resting'))
                self.game_data['start of game'] = False
            else:
                for enemy in range(random.randint(1, 6)):
                    enemy_group.add(person.Enemy('devil', 0, 0,
                                                  'down', 'battle resting'))

        for i, enemy in enumerate(enemy_group):
            enemy.rect.topleft = pos_list[i]
            enemy.image = pg.transform.scale2x(enemy.image)
            enemy.index = i
            enemy.level = self.make_enemy_level_dict()[self.previous]
            if enemy.name == 'evilwizard':
                enemy.health = 100
            else:
                enemy.health = enemy.level * 4

        enemy_list = [enemy for enemy in enemy_group]

        return enemy_group, pos_list[0:len(enemy_group)], enemy_list

    def make_player(self):
        """
        Make the sprite for the player's character.
        """
        player = person.Player('left', self.game_data, 630, 220, 'battle resting', 1)
        player.image = pg.transform.scale2x(player.image)
        return player

    def make_selection_state_dict(self):
        """
        Make a dictionary of states with arrow coordinates as keys.
        """
        pos_list = self.arrow.make_select_action_pos_list()
        state_list = [self.enter_select_enemy_state, self.enter_select_item_state,
                      self.enter_select_magic_state, self.try_to_run_away]
        return dict(izip(pos_list, state_list))

    def update(self, surface, keys, current_time):
        """
        Update the battle state.
        """
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
        self.execute_player_actions()

        self.draw_battle(surface)

    def check_input(self, keys):
        """
        Check user input to navigate GUI.
        """
        if self.allow_input:
            if keys[pg.K_SPACE]:
                if self.state == c.SELECT_ACTION:
                    self.notify(c.CLICK2)
                    enter_state_function = self.select_action_state_dict[
                        self.arrow.rect.topleft]
                    enter_state_function()

                elif self.state == c.SELECT_ENEMY:
                    self.notify(c.CLICK2)
                    self.player_actions.append(c.PLAYER_ATTACK)
                    self.enemies_to_attack.append(self.get_enemy_to_attack())
                    self.action_selected = True

                elif self.state == c.SELECT_ITEM:
                    self.notify(c.CLICK2)
                    if self.arrow.index == (len(self.arrow.pos_list) - 1):
                        self.enter_select_action_state()
                    elif self.info_box.item_text_list[self.arrow.index][:14] == 'Healing Potion':
                        if 'Healing Potion' in self.game_data['player inventory']:
                            self.player_actions.append(c.DRINK_HEALING_POTION)
                            self.action_selected = True
                    elif self.info_box.item_text_list[self.arrow.index][:5] == 'Ether':
                        if 'Ether Potion' in self.game_data['player inventory']:
                            self.player_actions.append(c.DRINK_ETHER_POTION)
                            self.action_selected = True
                elif self.state == c.SELECT_MAGIC:
                    self.notify(c.CLICK2)
                    if self.arrow.index == (len(self.arrow.pos_list) - 1):
                        self.enter_select_action_state()
                    elif self.info_box.magic_text_list[self.arrow.index] == 'Cure':
                        magic_points = self.game_data['player inventory']['Cure']['magic points']
                        if self.temp_magic >= magic_points:
                            self.temp_magic -= magic_points
                            self.player_actions.append(c.CURE_SPELL)
                            self.action_selected = True
                    elif self.info_box.magic_text_list[self.arrow.index] == 'Fire Blast':
                        magic_points = self.game_data['player inventory']['Fire Blast']['magic points']
                        if self.temp_magic >= magic_points:
                            self.temp_magic -= magic_points
                            self.player_actions.append(c.FIRE_SPELL)
                            self.action_selected = True

            self.allow_input = False

        if keys[pg.K_RETURN] == False and keys[pg.K_SPACE] == False:
            self.allow_input = True

    def check_timed_events(self):
        """
        Check if amount of time has passed for timed events.
        """
        timed_states = [c.PLAYER_DAMAGED,
                        c.ENEMY_DAMAGED,
                        c.ENEMY_DEAD,
                        c.DRINK_HEALING_POTION,
                        c.DRINK_ETHER_POTION]
        long_delay = timed_states[1:]

        if self.state in long_delay:
            if (self.current_time - self.timer) > 1000:
                if self.state == c.ENEMY_DAMAGED:
                    if self.player_actions:
                        self.player_action_dict[self.player_actions[0]]()
                        self.player_actions.pop(0)
                    else:
                        if len(self.enemy_list):
                            self.enter_enemy_attack_state()
                        else:
                            self.enter_battle_won_state()
                elif (self.state == c.DRINK_HEALING_POTION or
                      self.state == c.CURE_SPELL or
                      self.state == c.DRINK_ETHER_POTION):
                    if self.player_actions:
                        self.player_action_dict[self.player_actions[0]]()
                        self.player_actions.pop(0)
                    else:
                        if len(self.enemy_list):
                            self.enter_enemy_attack_state()
                        else:
                            self.enter_battle_won_state()
                self.timer = self.current_time

        elif self.state == c.FIRE_SPELL or self.state == c.CURE_SPELL:
            if (self.current_time - self.timer) > 1500:
                if self.player_actions:
                    if not len(self.enemy_list):
                        self.enter_battle_won_state()
                    else:
                        self.player_action_dict[self.player_actions[0]]()
                        self.player_actions.pop(0)
                else:
                    if len(self.enemy_list):
                        self.enter_enemy_attack_state()
                    else:
                        self.enter_battle_won_state()
                self.timer = self.current_time

        elif self.state == c.RUN_AWAY:
            if (self.current_time - self.timer) > 1500:
                self.end_battle()

        elif self.state == c.BATTLE_WON:
            if (self.current_time - self.timer) > 1800:
                self.enter_show_gold_state()

        elif self.state == c.SHOW_GOLD:
            if (self.current_time - self.timer) > 1800:
                self.enter_show_experience_state()

        elif self.state == c.LEVEL_UP:
            if (self.current_time - self.timer) > 2200:
                if self.game_data['player stats']['Level'] == 3:
                    self.enter_two_actions_per_turn_state()
                else:
                    self.end_battle()

        elif self.state == c.TWO_ACTIONS:
            if (self.current_time - self.timer) > 3000:
                self.end_battle()

        elif self.state == c.SHOW_EXPERIENCE:
            if (self.current_time - self.timer) > 2200:
                player_stats = self.game_data['player stats']
                player_stats['experience to next level'] -= self.experience_points
                if player_stats['experience to next level'] <= 0:
                    extra_experience = player_stats['experience to next level'] * -1
                    player_stats['Level'] += 1
                    player_stats['health']['maximum'] += int(player_stats['health']['maximum']*.25)
                    player_stats['magic']['maximum'] += int(player_stats['magic']['maximum']*.20)
                    new_experience = int((player_stats['Level'] * 50) * .75)
                    player_stats['experience to next level'] = new_experience - extra_experience
                    self.enter_level_up_state()
                    self.just_leveled_up = True
                else:
                    self.end_battle()

        elif self.state == c.PLAYER_DAMAGED:
            if (self.current_time - self.timer) > 600:
                if self.enemy_index == (len(self.enemy_list) - 1):
                    if self.run_away:
                        self.enter_run_away_state()
                    else:
                        self.enter_select_action_state()
                else:
                    self.switch_enemy()
                self.timer = self.current_time

    def check_if_battle_won(self):
        """
        Check if state is SELECT_ACTION and there are no enemies left.
        """
        if self.state == c.SELECT_ACTION:
            if len(self.enemy_group) == 0:
                self.enter_battle_won_state()

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
            self.game_data['talked to king'] = True
        self.game_data['last state'] = self.name
        self.game_data['battle counter'] = random.randint(50, 255)
        self.game_data['battle type'] = None
        self.state = 'transition out'

    def attack_enemy(self, enemy_damage):
        enemy = self.player.attacked_enemy
        enemy.health -= enemy_damage
        self.set_enemy_indices()

        if enemy:
            enemy.enter_knock_back_state()
            if enemy.health <= 0:
                self.enemy_list.pop(enemy.index)
                enemy.state = c.FADE_DEATH
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
        self.draw_transition(surface)

    def draw_transition(self, surface):
        """
        Fade in and out of state.
        """
        if self.state == 'transition in':

            transition_image = pg.Surface(self.transition_rect.size)
            transition_image.fill(c.TRANSITION_COLOR)
            transition_image.set_alpha(self.transition_alpha)
            surface.blit(transition_image, self.transition_rect)
            self.transition_alpha -= c.TRANSITION_SPEED 
            if self.transition_alpha <= 0:
                self.state = c.SELECT_ACTION
                self.transition_alpha = 0

        elif self.state == 'transition out':
            transition_image = pg.Surface(self.transition_rect.size)
            transition_image.fill(c.TRANSITION_COLOR)
            transition_image.set_alpha(self.transition_alpha)
            surface.blit(transition_image, self.transition_rect)
            self.transition_alpha += c.TRANSITION_SPEED 
            if self.transition_alpha >= 255:
                self.done = True

        elif self.state == c.DEATH_FADE:
            transition_image = pg.Surface(self.transition_rect.size)
            transition_image.fill(c.TRANSITION_COLOR)
            transition_image.set_alpha(self.transition_alpha)
            surface.blit(transition_image, self.transition_rect)
            self.transition_alpha += c.DEATH_TRANSITION_SPEED
            if self.transition_alpha >= 255:
                self.done = True
                self.next = c.DEATH_SCENE

    def player_damaged(self, damage):
        self.game_data['player stats']['health']['current'] -= damage
        if self.game_data['player stats']['health']['current'] <= 0:
            self.game_data['player stats']['health']['current'] = 0
            self.state = c.DEATH_FADE

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
            self.game_data['player stats']['magic']['current'] -= magic_points

    def magic_boost(self, magic_points):
        """
        Add magic from ether to game data.
        """
        magic = self.game_data['player stats']['magic']
        magic['current'] += magic_points
        self.temp_magic += magic_points
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
        self.notify(c.FIRE)
        self.state = self.info_box.state = c.FIRE_SPELL
        POWER = self.inventory['Fire Blast']['power']
        MAGIC_POINTS = self.inventory['Fire Blast']['magic points']
        self.game_data['player stats']['magic']['current'] -= MAGIC_POINTS
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
        self.arrow.state = 'invisible'
        self.set_timer_to_current_time()

    def cast_cure(self):
        """
        Cast cure spell on player.
        """
        self.state = c.CURE_SPELL
        HEAL_AMOUNT = self.inventory['Cure']['power']
        MAGIC_POINTS = self.inventory['Cure']['magic points']
        self.player.healing = True
        self.set_timer_to_current_time()
        self.arrow.state = 'invisible'
        self.enemy_index = 0
        self.damage_points.add(
            attackitems.HealthPoints(HEAL_AMOUNT, self.player.rect.topright, False))
        self.player_healed(HEAL_AMOUNT, MAGIC_POINTS)
        self.info_box.state = c.DRINK_HEALING_POTION
        self.notify(c.POWERUP)

    def enter_select_enemy_state(self):
        """
        Transition battle into the select enemy state.
        """
        self.state = self.arrow.state = c.SELECT_ENEMY
        self.arrow.index = 0

    def enter_select_item_state(self):
        """
        Transition battle into the select item state.
        """
        self.state = self.info_box.state = c.SELECT_ITEM
        self.arrow.become_select_item_state()

    def enter_select_magic_state(self):
        """
        Transition battle into the select magic state.
        """
        self.state = self.info_box.state = c.SELECT_MAGIC
        self.arrow.become_select_magic_state()

    def try_to_run_away(self):
        """
        Transition battle into the run away state.
        """
        self.run_away = True
        self.arrow.state = 'invisible'
        self.enemy_index = 0
        self.enter_enemy_attack_state()

    def enter_enemy_attack_state(self):
        """
        Transition battle into the Enemy attack state.
        """
        self.state = self.info_box.state = c.ENEMY_ATTACK
        enemy = self.enemy_list[self.enemy_index]
        enemy.enter_enemy_attack_state()

    def enter_player_attack_state(self):
        """
        Transition battle into the Player attack state.
        """
        self.state = self.info_box.state = c.PLAYER_ATTACK
        enemy_to_attack = self.enemies_to_attack.pop(0)
        if enemy_to_attack in self.enemy_list:
            self.player.enter_attack_state(enemy_to_attack)
        else:
            if self.enemy_list:
                self.player.enter_attack_state(self.enemy_list[0])
            else:
                self.enter_battle_won_state()
        self.arrow.state = 'invisible'

    def get_enemy_to_attack(self):
        """
        Get enemy for player to attack by arrow position.
        """
        enemy_posx = self.arrow.rect.x + 60
        enemy_posy = self.arrow.rect.y - 20
        enemy_pos = (enemy_posx, enemy_posy)
        enemy_to_attack = None

        for enemy in self.enemy_list:
            if enemy.rect.topleft == enemy_pos:
                enemy_to_attack = enemy

        return enemy_to_attack


    def enter_drink_healing_potion_state(self):
        """
        Transition battle into the Drink Healing Potion state.
        """
        self.state = self.info_box.state = c.DRINK_HEALING_POTION
        self.player.healing = True
        self.set_timer_to_current_time()
        self.arrow.state = 'invisible'
        self.enemy_index = 0
        self.damage_points.add(
            attackitems.HealthPoints(30,
                                     self.player.rect.topright,
                                     False))
        self.player_healed(30)
        self.notify(c.POWERUP)

    def enter_drink_ether_potion_state(self):
        """
        Transition battle into the Drink Ether Potion state.
        """
        self.state = self.info_box.state = c.DRINK_ETHER_POTION
        self.player.healing = True
        self.arrow.state = 'invisible'
        self.enemy_index = 0
        self.damage_points.add(
            attackitems.HealthPoints(30,
                                     self.player.rect.topright,
                                     False,
                                     True))
        self.magic_boost(30)
        self.set_timer_to_current_time()
        self.notify(c.POWERUP)

    def enter_select_action_state(self):
        """
        Transition battle into the select action state
        """
        self.state = self.info_box.state = c.SELECT_ACTION
        self.arrow.index = 0
        self.arrow.state = self.state

    def enter_player_damaged_state(self):
        """
        Transition battle into the player damaged state.
        """
        self.state = self.info_box.state = c.PLAYER_DAMAGED
        if self.enemy_index > len(self.enemy_list) - 1:
            self.enemy_index = 0
        enemy = self.enemy_list[self.enemy_index]
        player_damage = enemy.calculate_hit(self.inventory['equipped armor'],
                                            self.inventory)
        self.damage_points.add(
            attackitems.HealthPoints(player_damage,
                                     self.player.rect.topright))
        self.info_box.set_player_damage(player_damage)
        self.set_timer_to_current_time()
        self.player_damaged(player_damage)
        if player_damage:
            sfx_num = random.randint(1,3)
            self.notify('punch{}'.format(sfx_num))
            self.player.damaged = True
            self.player.enter_knock_back_state()
        else:
            self.notify(c.MISS)

    def enter_enemy_damaged_state(self):
        """
        Transition battle into the enemy damaged state.
        """
        self.state = self.info_box.state = c.ENEMY_DAMAGED
        enemy_damage = self.player.calculate_hit()
        self.damage_points.add(
            attackitems.HealthPoints(enemy_damage,
                                     self.player.attacked_enemy.rect.topright))

        self.info_box.set_enemy_damage(enemy_damage)

        self.arrow.index = 0
        self.attack_enemy(enemy_damage)
        self.set_timer_to_current_time()

    def switch_enemy(self):
        """
        Switch which enemy the player is attacking.
        """
        if self.enemy_index < len(self.enemy_list) - 1:
            self.enemy_index += 1
            self.enter_enemy_attack_state()

    def enter_run_away_state(self):
        """
        Transition battle into the run away state.
        """
        self.state = self.info_box.state = c.RUN_AWAY
        self.arrow.state = 'invisible'
        self.player.state = c.RUN_AWAY
        self.set_timer_to_current_time()
        self.notify(c.RUN_AWAY)

    def enter_battle_won_state(self):
        """
        Transition battle into the battle won state.
        """
        self.notify(c.BATTLE_WON)
        self.state = self.info_box.state = c.BATTLE_WON
        self.player.state = c.VICTORY_DANCE
        self.set_timer_to_current_time()

    def enter_show_gold_state(self):
        """
        Transition battle into the show gold state.
        """
        self.inventory['GOLD']['quantity'] += self.new_gold
        self.state = self.info_box.state = c.SHOW_GOLD
        self.set_timer_to_current_time()

    def enter_show_experience_state(self):
        """
        Transition battle into the show experience state.
        """
        self.state = self.info_box.state = c.SHOW_EXPERIENCE
        self.set_timer_to_current_time()

    def enter_level_up_state(self):
        """
        Transition battle into the LEVEL UP state.
        """
        self.state = self.info_box.state = c.LEVEL_UP
        self.info_box.reset_level_up_message()
        self.set_timer_to_current_time()

    def enter_two_actions_per_turn_state(self):
        self.state = self.info_box.state = c.TWO_ACTIONS
        self.set_timer_to_current_time()

    def execute_player_actions(self):
        """
        Execute the player actions.
        """
        if self.player_level < 3:
            if self.player_actions:
                enter_state = self.player_action_dict[self.player_actions[0]]
                enter_state()
                self.player_actions.pop(0)
        else:
            if len(self.player_actions) == 2:
                enter_state = self.player_action_dict[self.player_actions[0]]
                enter_state()
                self.player_actions.pop(0)
                self.action_selected = False
            else:
                if self.action_selected:
                    self.enter_select_action_state()
                    self.action_selected = False









