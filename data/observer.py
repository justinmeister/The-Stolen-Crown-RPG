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
        self.player = level.player
        self.set_observer_for_enemies()
        self.event_dict = self.make_event_dict()

    def set_observer_for_enemies(self):
        for enemy in self.level.enemy_list:
            enemy.observers.append(self)

    def make_event_dict(self):
        """
        Make a dictionary of events the Observer can
        receive.
        """
        event_dict = {c.ENEMY_DEAD: self.enemy_dead,
                      c.ENEMY_DAMAGED: self.enemy_damaged,
                      c.PLAYER_DAMAGED: self.player_damaged}

        return event_dict

    def on_notify(self, event):
        """
        Notify Observer of event.
        """
        if event in self.event_dict:
            self.event_dict[event]()

    def player_damaged(self):
        self.level.enter_player_damaged_state()

    def enemy_damaged(self):
        """
        Make an attack animation over attacked enemy.
        """
        self.level.enter_enemy_damaged_state()

    def enemy_dead(self):
        """
        Eliminate all traces of enemy.
        """
        self.level.player.attacked_enemy = None











