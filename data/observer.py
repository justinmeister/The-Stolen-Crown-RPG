"""
Module for all game observers.
"""
from . import constants as c
from .components import attackitems
from . import setup

class Battle(object):
    """
    Observes events of battle and passes info to components.
    """
    def __init__(self, level):
        self.level = level
        self.info_box = level.info_box
        self.select_box = level.info_box
        self.arrow = level.arrow
        self.player = level.player
        self.enemies = level.enemy_group
        self.enemy_list = level.enemy_list
        self.enemy_index = level.enemy_index
        self.set_observer_for_enemies()
        self.event_dict = self.make_event_dict()

    def set_observer_for_enemies(self):
        for enemy in self.enemies:
            enemy.observers.append(self)

    def make_event_dict(self):
        """
        Make a dictionary of events the Observer can
        receive.
        """
        event_dict = {c.END_BATTLE: self.end_battle,
                      c.SELECT_ACTION: self.select_action,
                      c.SELECT_ITEM: self.select_item,
                      c.SELECT_ENEMY: self.select_enemy,
                      c.SELECT_MAGIC: self.select_magic,
                      c.ENEMY_ATTACK: self.enemy_attack,
                      c.ENEMY_DEAD: self.enemy_dead,
                      c.SWITCH_ENEMY: self.switch_enemy,
                      c.PLAYER_ATTACK: self.player_attack,
                      c.ATTACK_ANIMATION: self.enemy_damaged,
                      c.RUN_AWAY: self.try_to_run_away,
                      c.FLEE: self.flee,
                      c.BATTLE_WON: self.battle_won,
                      c.ENEMY_ATTACK_DAMAGE: self.player_damaged,
                      c.DRINK_HEALING_POTION: self.drink_healing_potion,
                      c.DRINK_ETHER_POTION: self.drink_ether_potion,
                      c.CURE_SPELL: self.cure_spell,
                      c.FIRE_SPELL: self.fire_spell,
                      c.SHOW_EXPERIENCE: self.show_experience,
                      c.LEVEL_UP: self.level_up}

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
        self.level.state = c.SELECT_ACTION
        self.arrow.index = 0
        self.arrow.state = c.SELECT_ACTION
        self.arrow.image = setup.GFX['smallarrow']
        self.info_box.state = c.SELECT_ACTION

    def select_enemy(self):
        self.level.state = c.SELECT_ENEMY
        self.arrow.index = 0
        self.arrow.state = c.SELECT_ENEMY

    def select_item(self):
        self.level.state = c.SELECT_ITEM
        self.info_box.state = c.SELECT_ITEM
        self.arrow.become_select_item_state()

    def select_magic(self):
        self.level.state = c.SELECT_MAGIC
        self.info_box.state = c.SELECT_MAGIC
        self.arrow.become_select_magic_state()

    def enemy_attack(self):
        enemy = self.level.enemy_list[self.level.enemy_index]
        enemy.enter_enemy_attack_state()
        self.info_box.state = c.ENEMY_ATTACK

    def switch_enemy(self):
        """Switch which enemy is attacking player."""
        if self.level.enemy_index < len(self.level.enemy_list) - 1:
            self.level.enemy_index += 1
            self.on_notify(c.ENEMY_ATTACK)

    def player_damaged(self):
        if self.enemy_index > len(self.enemy_list) - 1:
            self.enemy_index = 0
        enemy = self.enemy_list[self.enemy_index]
        player_damage = enemy.calculate_hit()
        self.level.damage_points.add(
            attackitems.HealthPoints(player_damage,
                                     self.player.rect.topright))
        self.info_box.set_player_damage(player_damage)
        self.info_box.state = c.DISPLAY_ENEMY_ATTACK_DAMAGE
        self.level.state = c.DISPLAY_ENEMY_ATTACK_DAMAGE
        self.level.set_timer_to_current_time()
        self.level.player_damaged(player_damage)
        if player_damage:
            self.player.damaged = True
            self.player.enter_knock_back_state()

    def player_attack(self):
        enemy_posx = self.arrow.rect.x + 60
        enemy_posy = self.arrow.rect.y - 20
        enemy_pos = (enemy_posx, enemy_posy)
        enemy_to_attack = None

        for enemy in self.enemies:
            if enemy.rect.topleft == enemy_pos:
                enemy_to_attack = enemy

        self.player.enter_attack_state(enemy_to_attack)
        self.arrow.become_invisible_surface()

    def enemy_damaged(self):
        """
        Make an attack animation over attacked enemy.
        """
        enemy_damage = self.player.calculate_hit()
        self.level.damage_points.add(
            attackitems.HealthPoints(enemy_damage,
                                     self.player.attacked_enemy.rect.topright))

        self.info_box.set_enemy_damage(enemy_damage)
        self.info_box.state = c.ENEMY_HIT

        self.arrow.state = c.SELECT_ACTION
        self.arrow.index = 0
        self.level.attack_enemy(enemy_damage)
        self.level.set_timer_to_current_time()
        self.level.state = c.ENEMY_HIT


    def try_to_run_away(self):
        """
        Sets a flag in the battle state indicating a desire to run.
        Allows enemies to get one last hit in.
        """
        self.level.run_away = True
        self.level.state = c.ENEMY_ATTACK
        self.arrow.become_invisible_surface()
        self.level.enemy_index = 0
        self.on_notify(c.ENEMY_ATTACK)

    def flee(self):
        """
        Actually run away after enemies get there chance to attack.
        """
        self.info_box.state = c.RUN_AWAY
        self.level.set_timer_to_current_time()
        self.arrow.become_invisible_surface()
        self.player.state = c.RUN_AWAY


    def battle_won(self):
        self.info_box.state = c.BATTLE_WON
        self.level.set_timer_to_current_time()
        self.player.state = c.VICTORY_DANCE


    def drink_healing_potion(self):
        """
        Give player a healing potion.
        """
        self.level.drink_healing_potion()

    def drink_ether_potion(self):
        """
        Give player a ether potion.
        """
        self.level.drink_ether()

    def cure_spell(self):
        """
        Cast cure spell on player.
        """
        self.level.cast_cure()

    def fire_spell(self):
        """
        Cast fire spell on all enemies.
        """
        self.level.cast_fire_blast()

    def enemy_dead(self):
        """
        Eliminate all traces of enemy.
        """
        self.player.attacked_enemy = None

    def show_experience(self):
        """
        Show the experience the player gained that battle.
        """
        self.info_box.state = c.SHOW_EXPERIENCE
        self.level.set_timer_to_current_time()

    def level_up(self):
        """
        Display message that the player leveled up.
        """
        self.info_box.reset_level_up_message()
        self.info_box.state = c.LEVEL_UP
        self.level.set_timer_to_current_time()









